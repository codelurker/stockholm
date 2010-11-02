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


def get_entry_price_and_stop(quote):
  """ 
    Returns a tuple with the entry price and the stop you would need to use
    if you opened a position on then next day
  """
  entry_price = quote.next().open
  stop = quote.get_indicator().calculate_stop(entry_price)
  return (entry_price, stop)

def find_events(symbol):
  events = []
  quote = Quote.get_quotes(symbol)[0]
  stop = None
  entry_price = None
  hh50 = False
  hh20 = False
  while quote:
    prev = quote
    quote = quote.next()
    
    if not quote: # no more data
      if entry_price:
        print "Still winning ", entry_price, hh50, hh20
        events.append(Event(prev, 'exit', prev.close))
      continue
    
    if not hh50 and quote.is_above_50_day_high():
      print "Found a hh50 event %s" % quote
      events.append(Event(quote, 'hh50'))
      hh50 = True
      if entry_price == None:
        (entry_price, stop) = get_entry_price_and_stop(quote)

    if not hh20 and quote.is_above_20_day_high():
      print "Found a hh20 event %s" % quote
      events.append(Event(quote, 'hh20'))
      hh20 = True
      if entry_price == None:
        (entry_price, stop) = get_entry_price_and_stop(quote)

    if(hh20 and quote.low < stop): # hit the stop
      print "Found a stop event %s" % quote
      events.append(Event(quote, 'stop', stop))
      stop = None 
      entry_price = None
      hh50 = None 
      hh20 = None
      continue

    if(hh20 and quote.close > entry_price and quote.close < quote.get_indicator().ll_10 ): # exit
      print "Found a exit event %s" % quote
      events.append(Event(quote, 'exit', quote.get_indicator().ll_10))
      stop = None 
      entry_price = None
      hh50 = None 
      hh20 = None
      continue
  print "Found %s events for ticker %s" %(len(events), symbol)
  print 
  return events

class Event():
  def __init__(self, quote, type, stop=None):
    self.quote = quote
    self.type = type
    self.stop = stop

  def __str__(self):
    return "%s:%s:%s" % (self.quote.date, self.type, self.stop)

   
class TurtleSystem():
  positions = []
  
  def __init__(self, symbol, currency='SEK', currency_rate=1, enter_commission=Decimal('99')):
    self.diff = 0
    self.currency = currency
    self.currency_rate = currency_rate
    self.enter_commission = enter_commission
    self.events = find_events(symbol)
    for event in self.events: print "Event(Quote({'date':%s}), '%s')," % (event.quote.date, event.type)

  def run(self, total):
    self.total = total
    for idx, event in enumerate(self.events):
      self.handle_event(event, idx)
    print "At the end..."
    print 
    print "Capital: %10.f %s" % (self.total, self.currency)
    print "Gain:    %10.f %s" % (self.diff, self.currency)
    print "-------- %10.2f %%" % (self.diff/self.total*100)
   
  def handle_event(self, event, idx):
    if (self.has_position(event)):
      self.handle_stop(event) or self.handle_exit(event)
    else:
    # Check entries
      self.handle_entry(event, idx)
 
  def is_prev_event_a_stop(self, idx):
    if idx > 0:
      if self.events[idx-1].type == 'stop':
        return True
    return False
 
  def handle_entry(self, event, idx):
    enter = False
    if (event.type == 'hh50'):
      print "Found a hh50", event
      enter = True
    if (event.type == 'hh20'):
      print "Found a hh20", event
      enter = self.is_prev_event_a_stop(idx)
    if enter:
      self.open_position(event.quote)
      print self.positions[-1]
      self.handle_units(event, idx)

  def get_risk(self):
    return Decimal(self.total/100)

  def open_position(self, quote):
    shares = Position.get_shares(quote, self.get_risk())
    next_quote = quote.next()
    print "opening on next day", next_quote
    self.positions.append(Position.open(
        quote.symbol, 
        self.currency, 
        self.currency_rate, 
        next_quote.date,
        next_quote.open,
        self.enter_commission,
        shares))

  def has_position(self, quote):
    return len(self.positions)>0

  def handle_stop(self, event):
    if event.type == 'stop':
      print "Stopping", event
      print
      for p in self.positions:
        self.diff += p.get_net_gain(event.stop)
      self.positions = []

  def handle_exit(self, event):
    if event.type == 'exit':
      print "Exiting", event
      print 
      for p in self.positions:
        self.diff += p.get_net_gain(event.stop)
      self.positions = []
    pass

  def handle_units(self, event, idx):
    next_event = self.events[idx+1]
    while True:
      idx +=1
      next_event = self.events[idx]
      if next_event.type == 'exit' or next_event.type == 'stop':
        break

    quote = event.quote
    while quote.date < next_event.quote.date:
      quote = quote.next()
      indicator = quote.get_indicator()
      if quote.close > self.positions[-1].enter_price + indicator.atr_exp20/2:
        if(len(self.positions)<4):
          self.open_position(quote)
          print self.positions[-1]

if __name__ == '__main__':
  print '----------------------------------------------'
  #symbol = 'GOOG'
  #symbol = 'AAPL'
  #symbol = 'MIC-SDB.ST'
  #symbol = 'ENRO.ST'
  #symbol = 'BP.L'
  #symbol = 'RIO.L'
  #symbol = 'BLT.L'
  TurtleSystem(symbol='ENRO.ST').run(total=Decimal('300000'))
