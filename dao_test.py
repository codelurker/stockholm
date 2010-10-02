import unittest
from mock import Mock

from decimal import Decimal
from dao import Base 
from dao import Query 
from dao import Quote 
from dao import Position
from dao import Indicator

class TestQuote(unittest.TestCase):

  def test_has_met_stop_long(self):
    position = Position({'stop': 10})
    position.is_long = True 
    q  = Quote({})

    q.close = 9
    self.assertFalse(q.has_met_stop(position))
    q.close = 10
    self.assertTrue(q.has_met_stop(position))
    q.close = 11
    self.assertTrue(q.has_met_stop(position))

  def test_has_met_stop_short(self):
    position = Position({'stop': 10})
    position.is_long = False 
    q  = Quote({})

    q.close = 9
    self.assertTrue(q.has_met_stop(position))
    q.close = 10
    self.assertTrue(q.has_met_stop(position))
    q.close = 11
    self.assertFalse(q.has_met_stop(position))
    
  def test_get_quote_not_found(self):
    quote = Quote.get_quote('----', '2001-01-01')
    self.assertEquals(None, quote)
  
  def test_get_quote(self):
    quote = Quote.get_quote('AAPL', '2001-01-01')
    self.assertQuote(quote)
  
  def assertQuote(self, quote):
    self.assertEquals('AAPL', quote.symbol)
    self.assertEquals(('2001-01-01'), str(quote.date))
    self.assertEquals(Decimal('100.1'), quote.close)
    self.assertEquals(Decimal('110.1'), quote.high)
    self.assertEquals(Decimal('120.1'), quote.low)
    self.assertEquals(Decimal('130.1'), quote.open)

class TestIndicator(unittest.TestCase):
  
  def test_get_indicator(self):
    indicator = Indicator.get_indicator('AAPL', '2001-01-01')
    self.assertIndicator(indicator)

  def assertIndicator(self, indicator):
    self.assertTrue(isinstance(indicator, Indicator))
    self.assertEquals('AAPL', indicator.symbol)
    self.assertEquals(('2001-01-01'), str(indicator.date))
    self.assertEquals(Decimal('100.1'), indicator.sma_20)
    self.assertEquals(Decimal('110.1'), indicator.sma_50)
    self.assertEquals(Decimal('120.1'), indicator.atr_14)
  
  def test_get_trailing_indicators(self):
    indicators = Indicator.get_trailing_indicators('AAPL', '2001-01-02', 2)
    self.assertEquals(2, len(indicators))
    self.assertIndicator(indicators[1])
    self.assertEquals('AAPL', indicators[0].symbol)
    self.assertEquals(('2001-01-02'), str(indicators[0].date))
  
  def test_calculate_stop(self):
    quote  = Quote({'close': 10})
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
    query.execute = Mock()
    query.keys_ = Mock(return_value=('a', 'b', 'c'))
    query.fetchone_ = Mock(return_value=('1', '2', '3'))

    dummy = query.fillone(TestQuery.Dummy)
    self.assertTrue(isinstance(dummy, TestQuery.Dummy))
    self.assertTrue(1, dummy.a)
    self.assertTrue(2, dummy.b)
    self.assertTrue(3, dummy.c)

  def test_fillall(self):
    query = Query("select a,b,c from bah", ());
    query.execute = Mock()
    query.keys_ = Mock(return_value=('a', 'b'))
  
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
    unittest.main()
