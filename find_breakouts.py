#!/usr/bin/env python

from dao import Quote
from decimal import Decimal
from datetime import date
from datetime import datetime
from datetime import timedelta
from turtle import find_events

def find_recent_breakout(events, not_older_than):
  # We need at least a eod, a hh20 and a previous event or
  # a eod, a hh50 and hh50
  if len(events) < 3: 
    return False

  last_event = events[-1]
  if(last_event.type != 'eod'):
    return False

  # Good, we are still in a breakout.
  # When did it start ?
  breakout_start = events[-2]
  
  if breakout_start.quote.date < not_older_than:
    return False
  if breakout_start.type == 'hh50' or events[-3].type == 'stop':
    return breakout_start

if __name__ == '__main__':
  for quote in Quote.get_latest_quotes('%.L'):
    breakout = find_recent_breakout(find_events(quote.symbol), date.today() - timedelta(days=5))
    if breakout:
      print 'Found breakout for %s %s' % (quote.symbol, breakout)
