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




total = 100000
currency = 'USD'
#stocks = 0
#symbol = 'LUPE.ST'
symbol = 'AAPL'
symbol = 'RIO.L'
symbol = 'SYSR.ST'

def run():
  for quote in Quote.get_quotes(symbol):
    #print "\nSimulating %s" % quote
    #print "%s" % quote.get_indicator()
    handle_quote(quote)
 
def handle_quote(quote):
  if (has_position(quote)):
    handle_stop(quote) or handle_exit(quote) or handle_units(quote)
  else:
    # Check entries
    handle_entry(quote)
     
# open_position(quote)
  
# if (handle_20_breakout(quote) and handle_prev_20_breakout(quote))
#  or handle_50_breakout(quote):
    
def handle_entry(quote):
  pass

def has_position(quote):
  return True

def handle_stop(quote):
  pass

def handle_exit(quote):
  pass

def handle_units(quote):
  print "handle_units"

def handle_20_breakout(quote):
  pass

def handle_prev_20_breakout(quote):
  pass

def handle_50_breakout(quote):
  pass

if __name__ == '__main__':
  run()
