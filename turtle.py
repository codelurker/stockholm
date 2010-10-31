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
"""

symbol = 'GOOG'
symbol = 'RIO.L'
symbol = 'AAPL'
#symbol = 'SYSR.ST'

events = None

def find_events():
  events = []
  quote = Quote.get_quotes(symbol)[0]
  stop = None
  entry_price = None
  hh50 = False
  hh20 = False
  while quote:
    quote = quote.next()
    
    if not hh20 and quote.is_above_20_day_high():
      print "Found a hh20 event %s" % quote
      indicator = quote.get_indicator()
      events.append(Event(quote, 'hh20'))
      entry_price = quote.next().open
      stop = indicator.calculate_stop(entry_price)
      hh20 = True

    if not hh50 and quote.is_above_50_day_high():
      print "Found a hh50 event %s" % quote
      hh50 = True
      events.append(Event(quote, 'hh50'))

    if not quote: # no more data
      print "Still winning ", quote
      events.append(Event(quote, 'exit'))
      continue
    
    if(hh20 and quote.close < stop): # hit the stop
      print "Found a stop event %s" % quote
      events.append(Event(quote, 'stop'))
      #print stop
      stop = None 
      entry_price = None
      hh50 = None 
      hh20 = None
      continue

    if(hh20 and quote.close > entry_price and quote.close < quote.get_indicator().ll_10 ): # exit
      print "Found a exit event %s" % quote
      events.append(Event(quote, 'exit'))
      #print quote.get_indicator()
      #print stop
      stop = None 
      entry_price = None
      hh50 = None 
      hh20 = None
      #print
      continue

  return events

class Event():
  def __init__(self, quote, type):
    self.quote = quote
    self.type = type

  def __str__(self):
    return "%s:%s" % (self.quote.date, self.type)

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
    #print "handle_units"
    pass

  def is_20_breakout(self, quote):
    return quote.is_above_20_day_high()
  
  def is_50_breakout(self, quote):
    return False and quote.is_above_50_day_high()

  def is_prev_20_breakout_looser(self, quote):
    print quote
    for idx, b in enumerate(events):
      if quote.date == b.quote.date:
        if idx > 0:
          if events[idx-1].type != True:
            print "breakout %s is good" % quote
    print "breakout %s is bad" % quote
    return False
  

def handle_20_breakout(quote):
  pass

def handle_prev_20_breakout(quote):
  pass

def handle_50_breakout(quote):
  pass

if __name__ == '__main__':
  events = find_events()
  #print events
  #run()
