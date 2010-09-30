import unittest
from mock import Mock

from dao import Quote 
from dao import Quote2
from dao import Position
from dao import Indicator2

class TestQuote(unittest.TestCase):

  def test_has_met_stop_long(self):
    position = Position({'symbol': 'EXAMPLE', 'stop': 10})
    position.is_long = True 
    q  = Quote(('EXAMPLE', '2010-01-78', 10, 12, 8, 9))

    q.close = 9
    self.assertFalse(q.has_met_stop(position))
    q.close = 10
    self.assertTrue(q.has_met_stop(position))
    q.close = 11
    self.assertTrue(q.has_met_stop(position))

  def test_has_met_stop_short(self):
    position = Position({'symbol': 'EXAMPLE', 'stop': 10})
    position.is_long = False 
    q  = Quote(('EXAMPLE', '2010-01-78', 10, 12, 8, 9))

    q.close = 9
    self.assertTrue(q.has_met_stop(position))
    q.close = 10
    self.assertTrue(q.has_met_stop(position))
    q.close = 11
    self.assertFalse(q.has_met_stop(position))

class TestIndicator(unittest.TestCase):

  def test_calculate_stop(self):
    quote  = Quote2({'close': 10})
    indicator = Indicator2({'atr_14': 1})
    quote.get_day_indicator = Mock(return_value=indicator)
    indicator.atr_stop = 3
    self.assertEqual(7, indicator.calculate_stop(quote))
    
    indicator.atr_stop = 1
    self.assertEqual(9, indicator.calculate_stop(quote))
  
if __name__ == '__main__':
    unittest.main()
