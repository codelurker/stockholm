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
  
  def test_get_quotes(self):
    Quote.start_date = '2001-01-0' # Beginning of fixtures
    quotes = Quote.get_quotes('AAPL')
    found = False
    for quote in quotes:
      self.assertTrue(isinstance(quote, Quote))
      self.assertEquals('AAPL', quote.symbol)
      try:
        self.assertQuote(quote)
        found = True
      except AssertionError:
        pass
    self.assertTrue(found)

  def test_previous(self):
    quote = Quote.get_quote('AAPL', '2001-01-02')
    self.assertQuote(quote.previous())

  def test_get_indicator(self):
    quote = Quote({'symbol':'AAPL', 'date':'2001-01-02'})
    indicator = Indicator({})
    Indicator.get_indicator = Mock(return_value=indicator)
    self.assertEquals(indicator, quote.get_indicator())
    Indicator.get_indicator.assert_called_with('AAPL', '2001-01-02') 

  def test_get_trailing_indicators(self):
    quote = Quote({'symbol':'AAPL', 'date':'2001-01-02'})
    indicators = Indicator({})
    Indicator.get_trailing_indicators = Mock(return_value=indicators)
    self.assertEquals(indicators, quote.get_trailing_indicators(7))
    Indicator.get_trailing_indicators.assert_called_with('AAPL', '2001-01-02', 7) 
 
  def test_set_tr(self):
    Quote.set_tr('AAPL', '2001-01-02', '1234')
    quote = Quote.get_quote('AAPL', '2001-01-02')
    self.assertEquals(Decimal('1234'), quote.tr)
    
    Quote.set_tr('AAPL', '2001-01-02', '5678')
    quote = Quote.get_quote('AAPL', '2001-01-02')
    self.assertEquals(Decimal('5678'), quote.tr)

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
    self.assertEqual(7, indicator.calculate_stop(quote))
    
    indicator.atr_stop = 1
    self.assertEqual(9, indicator.calculate_stop(quote))
  
class TestQuery(unittest.TestCase):
  class Dummy(Base):
    pass

  def test_keys(self):
    query = Query("select a,b,c from bah", ())
    self.assertEquals(['a', 'b', 'c'], query.keys_())
    query = Query("select a,b,c  from bah", ())
    self.assertEquals(['a', 'b', 'c'], query.keys_())

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

class TestPosition(unittest.TestCase):
  def test_get_position(self):
    position = Position.get_position('MILL', '2010-09-09')  
    self.assertTrue(isinstance(position, Position))
    self.assertEquals('MILL', position.symbol)
    self.assertEquals('2010-09-09', str(position.enter_date))
    self.assertEquals('2010-09-29', str(position.exit_date))
    self.assertEquals('SEK', position.currency)
    self.assertEquals(Decimal('1'), position.currency_rate)
    self.assertEquals(Decimal('719.50'), position.enter_price)
    self.assertEquals(Decimal('647'), position.exit_price)
    self.assertEquals(Decimal('99'), position.enter_commission)
    self.assertEquals(Decimal('99'), position.exit_commission)
    self.assertEquals(Decimal('30'), position.shares)
    self.assertEquals(Decimal('602'), position.stop)
    self.assertEquals(1, position.portfolio_id)

  def test_open(self):
    Position.open('AAPL', 'SEK', 1, '2001-02-03', 200, 99, 2000, 180)
    position = Position.get_position('AAPL', '2001-02-03')  
    self.assertEquals('AAPL', position.symbol)
    self.assertEquals('2001-02-03', str(position.enter_date))
    self.assertEquals(None, position.exit_date)
    self.assertEquals('SEK', position.currency)
    self.assertEquals(Decimal('1.0'), position.currency_rate)
    self.assertEquals(Decimal('200'), position.enter_price)
    self.assertEquals(None, position.exit_price)
    self.assertEquals(Decimal('99'), position.enter_commission)
    self.assertEquals(None, position.exit_commission)
    self.assertEquals(Decimal('2000'), position.shares)
    self.assertEquals(Decimal('180'), position.stop)

  def test_get_open_positions(self):
    positions = Position.get_open_positions()
    for position in positions:
      self.assertTrue(isinstance(position, Position))
      self.assertEquals(None, position.exit_date)
      
 
if __name__ == '__main__':
    unittest.main()
