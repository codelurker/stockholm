#!/usr/bin/env python

from decimal import Decimal

def find_recent_breakout(events, not_older_than):

  last_event = events[-1]
  if(last_event.type != 'eod'):
    return False

  # Good, we are still in a breakout.
  # When did it start ?
  breakout_start = events[-2]
  
  if breakout_start.quote.date < not_older_than:
    return False

  if breakout_start.type == 'hh50':
    return True
  else:
    return events[-3].type == 'stop'

if __name__ == '__main__':
  pass
