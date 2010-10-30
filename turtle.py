import ystockquote
import time
import datetime
import math
from datetime import date
from decimal import Decimal
from dao import Position
from dao import Quote
from connection import db

"""
  A backtesting implementation of the Turtle's breakout system.
  Observe as we cannot short, we assume we either go long or
  get out of the market.
  
  Entry:
    1) 20 day breakout: Buy 1 unit of stocks when a **close** price exceedes the high of 
       the previous 20 days and the last breakout would have hit a stop. (*)
    
    2) 50 day breakout: If the trade was rejected according to rule 1,
       buy 1 unit after a 50 day breakout in any case.

  Adding units:
    Add to the position 1 more unit if the trade is winning 1/2 the atr until
    the maximum number of allowed units (4) 
    
    Example:
      atr = 10
      -- price 100 --
      unit1 price = 100 => stop 80

      -- price 105 --
      unit1 price = 100 => stop 85
      unit2 price = 105 => stop 85

  Position sizing (how much is 1 unit of stocks):
    Buy as many stocks so that your per trade inital risk is 1% of your total 
    capital.
  
    Example:
      capital = 100.000$, atr = 10, risk = 1.000$, entry price = 100$

      ==> stop = 80$ (100 - 10 * 2)
        so if the trade hits the stop you will lose 20$ per stock
        You can buy 1.000$ / 20$ = 50 stocks
  
  Stop:
    Exit a trade if the **price** (not the close) is lower than the entry price - 2 * atr. 
    If more units are bought, the stop is 2 * atr below the price of the last unit
  
  Exit:
    10 day breakout: When the **price** (not the close) is lower of the lowest of the previous 10 days sell
    all units.

Notes
*) There is an extra rule if you are shorting which I'm omitting here
  
"""

#symbol = 'LUPE.ST'
#symbol = 'AAPL'
#symbol = 'RIO.L'
symbol = 'SYSR.ST'

def run():
  handlers = TurtleHandlers()
  for quote in Quote.get_quotes(symbol):
    #print "\nSimulating %s" % quote
    #print "%s" % quote.get_indicator()
    handle_quote(quote, handlers)
 
def handle_quote(quote, handlers):
  if (handlers.has_position(quote)):
    handlers.handle_stop(quote) or (
        handlers.handle_exit(quote)) or (
        handlers.handle_units(quote))
  else:
    # Check entries
    handlers.handle_entry(quote)
     
class TurtleHandlers():
  position = None
  currency = 'SEK'
  currency_rate = 1
  commission = Decimal('99')
  total = Decimal('1')
  
  def handle_entry(self, quote):
    enter = self.is_20_breakout(quote)
    #if enter: print "breakout %s" % quote
    enter = enter and (self.is_prev_20_breakout_looser(quote) or
        self.is_50_breakout(quote))
    enter and self.open_position(quote)
    return enter

  def get_risk(self):
    return Decimal(self.total/100)

  def open_position(self, quote):

    shares = Position.get_shares(quote, self.get_risk())
    next_quote = quote.next()
    self.position = Position.open(
        quote.symbol, 
        self.currency, 
        self.currency_rate, 
        next_quote.date,
        next_quote.open,
        self.commission,
        shares)

  def has_position(self, quote):
    return self.position != None

  def handle_stop(self, quote):
    pass

  def handle_exit(self, quote):
    pass

  def handle_units(self, quote):
    print "handle_units"

  def is_20_breakout(self, quote):
    return quote.is_above_20_day_high()
  
  def is_50_breakout(self, quote):
    return False and quote.is_above_50_day_high()

  def is_prev_20_breakout_looser(self, quote):
    while True:
      quote = quote.previous()
      if quote.is_above_20_day_high():
        break
    print quote

def handle_20_breakout(quote):
  pass

def handle_prev_20_breakout(quote):
  pass

def handle_50_breakout(quote):
  pass

if __name__ == '__main__':
  run()
