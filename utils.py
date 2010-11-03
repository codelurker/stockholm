#!/usr/bin/env python

class Event():
  def __init__(self, quote, type, stop=None):
    self.quote = quote
    self.type = type
    self.stop = stop

  def __str__(self):
    return "%s:%s:%s" % (self.quote.date, self.type, self.stop)
