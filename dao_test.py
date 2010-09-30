import unittest

from dao import Quote 
from dao import Position

class TestQuote(unittest.TestCase):

  def test_has_met_stop_long(self):
    position = Position(('EXAMPLE', 10))
    position.is_long = True 
    position.stop = 10 
    q  = Quote(('EXAMPLE', '2010-01-78', 10, 12, 8, 9))

    q.close = 9
    self.assertFalse(q.has_met_stop(position))
    q.close = 10
    self.assertTrue(q.has_met_stop(position))
    q.close = 11
    self.assertTrue(q.has_met_stop(position))

  def test_has_met_stop_short(self):
    position = Position(('EXAMPLE', 10))
    position.is_long = False 
    position.stop = 10 
    q  = Quote(('EXAMPLE', '2010-01-78', 10, 12, 8, 9))

    q.close = 9
    self.assertTrue(q.has_met_stop(position))
    q.close = 10
    self.assertTrue(q.has_met_stop(position))
    q.close = 11
    self.assertFalse(q.has_met_stop(position))


if __name__ == '__main__':
    unittest.main()
