import unittest
from mock import Mock
from mock import patch

from dao import * 
from decimal import Decimal
from find_breakouts import *

class TestFindBreakouts(unittest.TestCase):

    def find_breakout_hh50(self):
      events = [
          Event(Quote({'date':'2010-09-01'}), 'hh20'),
          Event(Quote({'date':'2010-09-20'}), 'hh50'),
          Event(Quote({'date':'2010-11-01'}), 'exit'),
        ]
      self.assertTrue(find_recent_breakout(events, '2010-09-15'))
 
    def find_breakout_hh50_too_old(self):
      events = [
          Event(Quote({'date':'2010-09-01'}), 'hh20'),
          Event(Quote({'date':'2010-09-20'}), 'hh50'),
          Event(Quote({'date':'2010-11-01'}), 'exit'),
        ]
      self.assertFalse(find_recent_breakout(events, '2010-09-25'))
  
    def find_breakout_a_stop(self):
      events = [
          Event(Quote({'date':'2010-09-01'}), 'hh20'),
          Event(Quote({'date':'2010-09-20'}), 'hh50'),
          Event(Quote({'date':'2010-11-01'}), 'stop'),
      ]
      self.assertFalse(find_recent_breakout(events, '2010-09-15'))

    def find_breakout_hh20_too_old(self):
      events = [
          Event(Quote({'date':'2010-09-01'}), 'hh20'),
          Event(Quote({'date':'2010-09-20'}), 'hh50'),
          Event(Quote({'date':'2010-11-01'}), 'exit'),
      ]
      self.assertFalse(find_recent_breakout(events, '2010-09-25'))

    def find_breakout_hh20_preceeded_by_stop(self):
      events = [
          Event(Quote({'date':'2010-08-01'}), 'stop'),
          Event(Quote({'date':'2010-09-01'}), 'hh20'),
          Event(Quote({'date':'2010-09-20'}), 'hh50'),
          Event(Quote({'date':'2010-11-01'}), 'exit'),
      ]
      self.assertTrue(find_recent_breakout(events, '2010-09-15'))

    def find_breakout_hh20_preceeded_by_exit(self):
      events = [
          Event(Quote({'date':'2010-08-01'}), 'exit'),
          Event(Quote({'date':'2010-09-01'}), 'hh20'),
          Event(Quote({'date':'2010-09-20'}), 'hh50'),
          Event(Quote({'date':'2010-11-01'}), 'exit'),
      ]
      self.assertFalse(find_recent_breakout(events, '2010-09-15'))

if __name__ == '__main__':
    unittest.main()
