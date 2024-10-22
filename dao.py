import datetime
import math
import re
import time
import ystockquote

from datetime import date
from decimal import Decimal

from connection import db

class Base:
  def __init__(self, dict_):
    self.__dict__ = dict_
 
  def __str__(self):
    s = self.__class__.__name__ + '['
    for k,v in self.__dict__.items():
      s += " %s:%s" % (k,v)
    return s + ' ]'

  def save(self):
    Query.save(self)
 
class Query:
  def __init__(self, query, params):
    self.query = query
    self.params = params

  @staticmethod
  def get_cols(cols):
    return ", ".join(cols)

  def execute(self):
    self.cursor = db.cursor()
    self.cursor.execute(self.query, self.params)
    #print "######## DEBUG ########\n"
    #print self.query % self.params
    #print "\n######## DEBUG ########"
    return self

  def keys_(self):
    keys = re.split(' *, *', re.search('SELECT (.*?) FROM', self.query, flags=re.IGNORECASE).group(1))
    for i, key in enumerate(keys):
      key = re.split(' as ', key)[-1]
      keys[i] = key.strip()
    return keys

  def fetchone_(self):
    return self.cursor.fetchone()

  def fillall(self, aclass):
    self.execute()
    all = []
    while(True):
      values = self.fetchone_()
      if values == None:
        break
      all.append(self.fillone_(aclass, values))
    return all

  def fillone(self, aclass):
    self.execute()
    values = self.fetchone_()
    return self.fillone_(aclass, values)

  def fillone_(self, aclass, values):
    if not values:
      return None
    d = dict()
    for i, k in enumerate(self.keys_()):
      d[k] = values[i]
    return aclass(d)
 
  @staticmethod 
  def save(object):
    table = object.__class__.__name__
    keys = object.__cols__
    cols = ", ".join(keys)
    values = []
    value_places = []
    for k in keys:
      value_places.append("%s")
      values.append(object.__dict__.get(k))
    insert = "INSERT INTO %s (%s) values (%s)" % (table, cols, ", ".join(value_places))
    cursor = db.cursor()
    cursor.execute(insert, values)

  @staticmethod 
  def findall(claz, where, where_args):
    table = claz.__name__
    cols = ", ".join(claz.__cols__)
    select = "SELECT %s FROM %s where %s" % (cols, table, where)
    return Query(select, where_args).fillall(claz)

  @staticmethod 
  def find(claz, where, where_args):
    table = claz.__name__
    cols = ", ".join(claz.__cols__)
    select = "SELECT %s FROM %s where %s" % (cols, table, where)
    return Query(select, where_args).fillone(claz)

class Position(Base):
  __cols__ = ["symbol", "currency", "currency_rate", "enter_date", "exit_date",
      "enter_price", "exit_price", "enter_commission", "exit_commission",
      "shares", "portfolio_id"]

  def __init__(self, args): 
    self.current_quote = None
    Base.__init__(self, args)
  
  def should_sell(self):
    return self.current_quote.close <= self.get_trailing_stop()
 
  def get_trailing_stop(self):
    """ 
        Returns the lowest low of the past 10 days.
        If the value is lower than the initial stop,
        it returns the stop as that is the maximum
        acceptable loss in any case
    """
    indicator = self.current_quote.get_indicator()
    return "" if indicator is None else max(indicator.ll_10, self.get_stop())

  def get_atr_trailing_stop(self):
    """
        Returns the max close value minus
        twice the atr value
    """
    indicator = self.current_quote.get_indicator()
    return "" if indicator is None else indicator.calculate_stop(self.get_max())

 
  def get_stop(self):
    if(self.current_quote.is_cash()):
      return ""
    return self.get_enter_indicator().calculate_stop(self.enter_price)

  def get_enter_indicator(self):
    indicator = Indicator.get_indicator(self.symbol, self.enter_date)
    return indicator
  
  def get_max(self):
    (max,) = Query('SELECT MAX(close) from quote where symbol = %s and date >= %s',
       (self.symbol, self.enter_date)).execute().fetchone_()
    return max
 
  @staticmethod
  def get_position(symbol, date):
    return Query.find(Position, 'symbol = %s and enter_date = %s', (symbol, date))

  @staticmethod
  def get_open_positions(portfolio_id):
    return Query.findall(Position, 'exit_date IS NULL and portfolio_id = %s', (portfolio_id))
  
  @staticmethod
  def open(symbol, currency, currency_rate, enter_date, enter_price,
       enter_commission, shares):
    position = Position({'symbol': symbol, 'currency': currency, 
        'currency_rate': currency_rate, 'enter_date': enter_date, 
        'enter_price': enter_price, 'enter_commission': enter_commission,
        'shares': shares, 'portfolio_id': 1})
    return position

  def get_net_gain(self, exit_price=None, exit_commission=None):
    """
      Returns the gain that you would get if the position would be sold with
      the given price, net of the enter and exit commission.
      If the exit_commission is not given, the enter_commission is used.
    """
    exit_price = exit_price or self.exit_price
    exit_commission = exit_commission or self.enter_commission
    return (exit_price - self.enter_price) * self.shares - self.enter_commission - exit_commission
  
  def get_risk(self):
    """ 
        Returns the risk in money associated to this position.
        The risk is the amount of money you would loose if you
        sold the position at the stop value
    """
    return self.shares * (self.enter_price - self.get_stop()) + self.enter_commission
  
  def get_rtr(self):
    """ 
        Returns the reward to risk ratio for this position.
        The rts is the number of times the money you risked
        yielded by this position
        
    """
    
    risk = self.get_risk()
    return self.get_gain() / risk
  
  def get_value(self, currency):
    """
        Returns the value of the position, i.e. what you would get
        if you sold the position now.
    """
    return self.shares * self.current_quote.close * Currency.get_rate(self.currency + currency)
    
  def get_gain(self):
    return self.shares * (self.current_quote.close - self.enter_price) - self.enter_commission

  @staticmethod
  def get_shares(quote, admissible_risk):
    """
      Returns the number of stocks that a position
      should hold so that it does not exceed the
      admissible risk
    """
    indicator = quote.get_indicator()
    stop = indicator.calculate_stop(quote.close)
    return Decimal(str(math.floor(admissible_risk/(quote.close - stop))))

  def get_next_unit_enter_price(self):
    return self.enter_price + self.current_quote.get_indicator().atr_exp20/2

class Quote(Base):
  __skip_first__ = 20
  __cols__ = ["symbol", "date", "open", "high", "low", "close", "tr"]
  
  class NotFound(Exception):
    def __init__(self, message):
      self.message = message

    def __str__(self):
      return repr(self.message)

  def has_met_stop(self, position):
    if position.is_long:
      return self.close <= position.get_stop()
    else:
      return self.close >= position.get_stop()

  def is_above_sma50_7(self):
    indicators = self.get_trailing_indicators(7)
    for i in indicators:
      if self.close < i.sma_50:
        return False
    return True

  def is_above_sma50(self):
    i = self.get_indicator()
    return self.close > i.sma_50
  
  def is_above_sma20(self):
    i = self.get_indicator()
    return self.close > i.sma_20
 
  def is_cash(self):
    return self.symbol == 'CASH' or self.symbol == 'FUNDS'

  @staticmethod
  def set_tr(symbol, date, value):
    c = Query("UPDATE quote SET tr = %s WHERE symbol = %s and date = %s", (value, symbol, date)).execute()
  
  @staticmethod
  def get_quotes(symbol):
    c = Query("SELECT symbol, date, open, high, low, close, tr from quote where symbol = %s order by date asc", (symbol))
    return c.fillall(Quote)[Quote.__skip_first__:]
  
  @staticmethod
  def get_latest_quotes(match='%%'):
    """ 
        Returns the latest quote for each
        symbol stored in the database.
    """
    c = Query("SELECT"
      " quote.symbol as symbol, quote.date as date, open, high, low, close, tr"
      " FROM quote, (SELECT symbol, max(date) as date from quote " 
      " group by symbol order by date asc) as maxs where "
      " quote.symbol = maxs.symbol and quote.date = maxs.date and quote.symbol like %s", (match))
    return c.fillall(Quote)

  @staticmethod
  def get_latest_quote(symbol):
    if symbol == 'CASH' or symbol == 'FUNDS':
      return Quote({'symbol': symbol, 
        'date': "", 
        'open': Decimal(1), 
        'high': Decimal(1), 
        'low': Decimal(1), 
        'close': Decimal(1)})
    quote = Query.find(Quote, "symbol = %s order by date desc limit 1", (symbol))
    if quote:
      return quote 
    else:
      raise Quote.NotFound("Could not find latest quote for %s" % symbol)

  @staticmethod
  def get_quote(symbol, date):
    c = Query("SELECT symbol, date, open, high, low, close, tr from quote where symbol = %s and date = %s", (symbol, date))
    return c.fillone(Quote)

  def previous(self):
    c = Query("SELECT symbol, date, open, high, low, close from quote where symbol = %s and date < %s order by date desc limit 1", (self.symbol, self.date))
    return c.fillone(Quote)
  
  def next(self):
    c = Query("SELECT symbol, date, open, high, low, close from quote where symbol = %s and date > %s order by date asc limit 1", (self.symbol, self.date))
    return c.fillone(Quote)
  
  def get_trailing_indicators(self, days):
    return Indicator.get_trailing_indicators(self.symbol, self.date, days)

  def get_indicator(self):
    if self.symbol == 'CASH' or self.symbol == 'FUNDS':
      return None
    return Indicator.get_indicator(self.symbol, self.date)
    
  def is_above_50_day_high(self):
    return self.close > self.get_indicator().hh_50

  def is_above_20_day_high(self):
    return self.close > self.get_indicator().hh_20

  def is_below_10_day_low(self):
    return self.close < self.get_indicator().ll_10

class Indicator(Base):
  __cols__ = ['symbol',' date', 'sma_20', 'sma_50', 'atr_exp20', 'atr_14', 'll_10', 'hh_20', 'hh_50']
  atr_stop = Decimal('2')

  def calculate_stop(self, price):
    return price - self.atr_exp20 * self.atr_stop

  @staticmethod
  def get_indicator(symbol, date):
    return Query.find(Indicator, 'symbol = %s and date = %s', (symbol, date))

  @staticmethod
  def get_trailing_indicators(symbol, date, days):
    """
      Returns the indicators for the last x days.
    """
    return Query.findall(Indicator, 'symbol = %s AND date <=%s ORDER BY date desc LIMIT %s', (symbol, date, days))

class Currency(Base):

  @staticmethod
  def get_rate(type):
    if type == 'USDSEK':
      return Decimal('6.70654106')
    if type == 'SEKSEK':
      return Decimal('1')
    if type == 'USDUSD':
      return Decimal('1')
    if type == 'GBPGBP':
      return Decimal('1')
    if type == 'GBPSEK':
      return Decimal('10.6558203')

class Portfolio(Base):
  __cols__ = ['id', 'name', 'currency']
  
  @staticmethod
  def get_portfolio(id):
    positions = Position.get_open_positions(id)
    for position in positions:
      position.current_quote = Quote.get_latest_quote(position.symbol)
    portfolio = Portfolio.load(id)
    portfolio.positions = positions
    return portfolio

  def get_value(self):
    return sum(map(lambda p: p.get_value(self.currency), self.positions))

  @staticmethod
  def load(id):
    return Query.find(Portfolio, 'id= %s', (id))
