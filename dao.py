import ystockquote
import time
import datetime
from datetime import date
import MySQLdb

class Query:
  def __init__(self, query, params):
    self.query = query
    self.params = params
    self.db=MySQLdb.connect(host="localhost", user="robcos",
                      passwd="robcos", db="stocks")

  def execute(self):
    c = self.db.cursor()
    #print "######## DEBUG ########\n" if debug
    #print self.query % self.params
    c.execute(self.query, self.params)
    #print "\n######## DEBUG ########" if debug
    return c
    
class Position:
  def __init__(self, tuple):
    (self.symbol,
    self.stop) = tuple
    self.is_long = True
    self.value = 0

class Quote:
  def __init__(self, tuple):
    (self.symbol,
    self.date,
    self.open,
    self.high,
    self.low,
    self.close) = tuple

  def has_met_stop(self, position):
    print position.is_long
    print self.close
    print position.stop
    return (self.close <= position.stop if position.is_long else self.close >= position.stop)

  def is_over_sma50_7(self):
    indicators = self.get_trailing_indicators(7)
    for i in indicators:
      if self.close < i.sma_50:
        return False
    return True
 
  @staticmethod
  def set_tr(symbol, date, value):
    c = Query("UPDATE quote SET tr = %s WHERE symbol = %s and date = %s", (value, symbol, date)).execute()
  
  @staticmethod
  def get_quotes(symbol):
    start_date = "2009-01-01"
    c = Query("SELECT symbol, date, open, high, low, close from quote where symbol = %s and date > %s order by date asc", (symbol, start_date)).execute()
    quotes = []
    for tuple in c.fetchall():
      quotes.append(Quote(tuple))
    return quotes

  @staticmethod
  def get_quote(symbol, date):
    c = Query("SELECT symbol, date, open, high, low, close from quote where symbol = %s and date = %s", (symbol, date)).execute()
    return Quote(c.fetchone())

  def previous(self):
    c = Query("SELECT symbol, date, open, high, low, close from quote where symbol = %s and date < %s order by date desc limit 1", (self.symbol, self.date)).execute()
    tuple = c.fetchone()
    return Quote(tuple) if tuple else None
  
  def get_trailing_indicators(self, days):
    return Indicator.get_trailing_indicators(self.symbol, self.date, days)

  def get_day_indicator(self):
    return Indicator.get_indicator(self.symbol, self.date)
    
  def __str__(self):
    return "%s %s close:%s open:%s" % (self.symbol, self.date, self.close, self.open)

class Indicator:

  def __init__(self, tuple):
    (self.symbol,
    self.date,
    self.sma_20,
    self.sma_50,
    self.atr_14
    ) = tuple

  @staticmethod
  def get_indicator(symbol, date):
    c = Query('SELECT symbol, date, sma_20, sma_50, atr_14 FROM indicator i WHERE i.symbol = %s AND i.date = %s', (symbol, date)).execute()
    return Indicator(c.fetchone())

  @staticmethod
  def get_trailing_indicators(symbol, date, days):
    """
      Returns the indicators for the last x days.
    """
    c = Query('SELECT symbol, date, sma_20, sma_50, atr_14 FROM indicator i WHERE i.symbol = %s AND i.date <=%s ORDER BY i.date desc LIMIT %s', (symbol, date, days)).execute()
    indicators = []
    for tuple in c.fetchall():
      indicators.append(Indicator(tuple))
    return indicators
