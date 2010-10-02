import unittest
from mock import Mock

from dao import Base 
from dao import Query 
from dao import Quote 
from dao import Quote2
from dao import Position
from dao import Indicator

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
    indicator = Indicator({'atr_14': 1})
    quote.get_day_indicator = Mock(return_value=indicator)
    indicator.atr_stop = 3
    self.assertEqual(7, indicator.calculate_stop(quote))
    
    indicator.atr_stop = 1
    self.assertEqual(9, indicator.calculate_stop(quote))
  
class TestQuery(unittest.TestCase):
  class Dummy(Base):
    pass

  def test_fillone(self):
    query = Query("select a,b,c from bah", ())
    query.keys = Mock(return_value=('a', 'b', 'c'))
    query.fetchone_ = Mock(return_value=('1', '2', '3'))
    dummy = query.fillone(TestQuery.Dummy)
    self.assertTrue(isinstance(dummy, TestQuery.Dummy))
    self.assertTrue(1, dummy.a)
    self.assertTrue(2, dummy.b)
    self.assertTrue(3, dummy.c)

  def test_fillall(self):
    query = Query("select a,b,c from bah", ());
    query.keys = Mock(return_value=('a', 'b'))
  
    values = [('1', '2'),('3', '4'), None]
    values.reverse()

    query.fetchone_ = values.pop
    dummies = query.fillall(TestQuery.Dummy)
    self.assertEquals(2, len(dummies))
    
    self.assertTrue(isinstance(dummies[0], TestQuery.Dummy))
    self.assertTrue(1, dummies[0].a)
    self.assertTrue(2, dummies[0].b)

    self.assertTrue(isinstance(dummies[1], TestQuery.Dummy))
    self.assertTrue(3, dummies[1].a)
    self.assertTrue(4, dummies[1].b)

if __name__ == '__main__':
    Indicator
    unittest.main()
