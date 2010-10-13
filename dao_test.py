import unittest
from mock import Mock
from mock import patch

from decimal import Decimal
from dao import * 

class TestQuote(unittest.TestCase):

  def test_get_latest_quote(self):
    quote = Quote.get_latest_quote('AAPL')
    self.assertEquals('AAPL', quote.symbol)
    self.assertEquals(('2001-01-03'), str(quote.date))

  def test_get_latest_quote(self):
    quote = Quote.get_latest_quote('CASH')
    self.assertEquals('CASH', quote.symbol)
    self.assertEquals(Decimal('1'), quote.close)
    self.assertEquals(Decimal('1'), quote.high)
    self.assertEquals(Decimal('1'), quote.low)
    self.assertEquals(Decimal('1'), quote.open)

  def test_get_latest_quote(self):
    quote = Quote.get_latest_quote('FUNDS')
    self.assertEquals('FUNDS', quote.symbol)
    self.assertEquals(Decimal('1'), quote.close)
    self.assertEquals(Decimal('1'), quote.high)
    self.assertEquals(Decimal('1'), quote.low)
    self.assertEquals(Decimal('1'), quote.open)

  def test_get_latest_quote_not_found(self):
    try:
      Quote.get_latest_quote('abracadabra')
      self.fail("Expected error")
    except Quote.NotFound:
      pass

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

  def test_get_indicator(self):
    quote = Quote({'symbol':'CASH'})
    self.assertEquals(None, quote.get_indicator())
    quote = Quote({'symbol':'FUNDS'})
    self.assertEquals(None, quote.get_indicator())

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

  def test_is_above_20_day_high_false(self):
    quote = Quote({'close': Decimal('10')})
    indicator = Indicator({'hh_20': Decimal('20')})
    quote.get_indicator = Mock(return_value=indicator)
    self.assertFalse(quote.is_above_20_day_high())
 
  def test_is_above_20_day_high_true(self):
    quote = Quote({'close': Decimal('30')})
    indicator = Indicator({'hh_20': Decimal('20')})
    quote.get_indicator = Mock(return_value=indicator)
    self.assertTrue(quote.is_above_20_day_high())
    
  def test_is_below_10_day_low_true(self):
    quote = Quote({'close': Decimal('10')})
    indicator = Indicator({'ll_10': Decimal('20')})
    quote.get_indicator = Mock(return_value=indicator)
    self.assertTrue(quote.is_below_10_day_low())
 
  def test_is_below_10_day_low_false(self):
    quote = Quote({'close': Decimal('30')})
    indicator = Indicator({'ll_10': Decimal('20')})
    quote.get_indicator = Mock(return_value=indicator)
    self.assertFalse(quote.is_below_10_day_low())
 
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
    self.assertEquals(Decimal('115.1'), indicator.atr_14)
    self.assertEquals(Decimal('120.1'), indicator.atr_exp20)
  
  def test_get_trailing_indicators(self):
    indicators = Indicator.get_trailing_indicators('AAPL', '2001-01-02', 2)
    self.assertEquals(2, len(indicators))
    self.assertIndicator(indicators[1])
    self.assertEquals('AAPL', indicators[0].symbol)
    self.assertEquals(('2001-01-02'), str(indicators[0].date))
  
  def test_calculate_stop(self):
    indicator = Indicator({'atr_exp20': Decimal(1)})
    self.assertEqual(8, indicator.calculate_stop(Decimal(10)))
    
    indicator.atr_stop = 1
    self.assertEqual(9, indicator.calculate_stop(Decimal(10)))
  
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
    position = Position.get_position('MIC-SDB.ST', '2010-09-09')
    self.assertTrue(isinstance(position, Position))
    self.assertEquals('MIC-SDB.ST', position.symbol)
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

  @patch("dao.Indicator.get_indicator")
  def test_get_enter_indicator(self, get_indicator):
    position = Position({
        'symbol': 'AAPL',
        'enter_date': '2010-01-01'})
    indicator = Indicator({})
    get_indicator.return_value = indicator
    self.assertEquals(indicator, position.get_enter_indicator())
    get_indicator.assert_called_with('AAPL', '2010-01-01')
 
  def test_get_stop(self):
    position = Position({
        'symbol': 'AAPL',
        'enter_date': '2010-01-01', 
        'enter_price': Decimal('10')})    
    indicator = Indicator({})
    indicator.calculate_stop = Mock(return_value = Decimal(10))
    position.get_enter_indicator = Mock(return_value = indicator)
    position.current_quote = Quote({})
    position.current_quote.is_cash = Mock(return_value = False)
    self.assertEqual(Decimal(10), position.get_stop())
    indicator.calculate_stop.assert_called_with(Decimal('10'))
 
  @patch("dao.Indicator.get_indicator")
  def test_get_stop_for_cash(self, get_indicator):
    position = Position({})    
    position.current_quote = Quote({})
    position.current_quote.is_cash = Mock(return_value = True)
    self.assertEqual('', position.get_stop())
 
  def test_get_open_positions(self):
    positions = Position.get_open_positions(1234)
    self.assertFalse(positions)

    positions = Position.get_open_positions(1)
    self.assertTrue(len(positions)>0)
    for position in positions:
      self.assertTrue(isinstance(position, Position))
      self.assertEquals(None, position.exit_date)
  
  def test_get_gain(self):
    position = Position({
        'shares': 1000, 'enter_price': Decimal('10'),
        'enter_commission': Decimal('99') })    
    position.current_quote = Quote({'close': Decimal('10')})
    self.assertEquals(Decimal('-99'), position.get_gain())
    position.current_quote = Quote({'close': Decimal('11')})
    self.assertEquals(Decimal('901'), position.get_gain())
    
  def test_get_risk(self):
    position = Position({'stop': Decimal('8'),
        'shares': 1000, 'enter_price': Decimal('10'),
        'enter_commission': Decimal('99') })    
    self.assertEquals(2099, position.get_risk())
  
  def test_get_rtr(self):
    position = Position({'stop': Decimal('8'),
        'shares': 1, 'enter_price': Decimal('9'),
        'enter_commission': Decimal('1') })    
    position.current_quote = Quote({'close': Decimal('10')})
    self.assertEquals(0, position.get_rtr())
    position.current_quote = Quote({'close': Decimal('12')})
    self.assertEquals(1, position.get_rtr())
    position.current_quote = Quote({'close': Decimal('14')})
    self.assertEquals(2, position.get_rtr())

  @patch("dao.Currency.get_rate")
  def test_get_value(self, get_rate):
    position = Position({'shares': 10, 'currency': 'USD'})    
    get_rate.return_value = Decimal('7')
    position.current_quote = Quote({'close': Decimal('10')})
    self.assertEquals(700, position.get_value('SEK'))

  def test_should_sell_when_below_stop(self):
    position = Position({})    
    position.current_quote = Quote({'close': Decimal('10')})
    position.get_trailing_stop = Mock(return_value = Decimal('11'))
    self.assertTrue(position.should_sell())

  def test_should_sell_not_when_above_stop(self):
    position = Position({})    
    position.current_quote = Quote({'close': Decimal('10')})
    position.get_trailing_stop = Mock(return_value = Decimal('9'))
    self.assertFalse(position.should_sell())

  def test_should_sell_when_equal_stop(self):
    position = Position({})    
    position.current_quote = Quote({'close': Decimal('10')})
    position.get_trailing_stop = Mock(return_value = Decimal('10'))
    self.assertTrue(position.should_sell())
  
  def test_get_trailing_stop(self):
    position = Position({'stop': Decimal('10')})    
    position.current_quote = Quote({})
    indicator = Indicator({'ll_10': Decimal('20')})
    position.current_quote.get_indicator = Mock(return_value = indicator)
    self.assertEquals(Decimal('20'), position.get_trailing_stop())

  def test_get_trailing_stop_when_ll_10_lower_than_stop(self):
    position = Position({'stop': Decimal('30')})    
    position.current_quote = Quote({})
    indicator = Indicator({'ll_10': Decimal('20')})
    position.current_quote.get_indicator = Mock(return_value = indicator)
    self.assertEquals(Decimal('30'), position.get_trailing_stop())

  def test_get_trailing_stop_when_no_indicator(self):
    position = Position({'stop': Decimal('10')})    
    position.current_quote = Quote({})
    indicator = Indicator({'ll_10': Decimal('20')})
    position.current_quote.get_indicator = Mock(return_value = None)
    self.assertEquals('', position.get_trailing_stop())

class TestPortfolio(unittest.TestCase):

  @patch("dao.Quote.get_latest_quote")
  @patch("dao.Position.get_open_positions")
  def test_get_portfolio(self, get_open_positions, get_latest_quote):
    positions = [
      Position({'symbol': 'AAPL'}), 
      Position({'symbol': 'LUPE.ST'})
    ]
    get_open_positions.return_value = positions
    quotes = [
      Quote({'symbol': 'LUPE.ST'}),
      Quote({'symbol': 'AAPL'})
    ]
    def side_effect(*args, **kwargs):
      return quotes.pop()
    get_latest_quote.side_effect = side_effect
    portfolio = Portfolio.get_portfolio(1)
    self.assertTrue(isinstance(portfolio, Portfolio))
    self.assertEquals(positions, portfolio.positions)
    get_open_positions.assert_called_with(1)
    for position in positions:
      quote = position.current_quote
      self.assertTrue(isinstance(quote, Quote))
      self.assertEquals(quote.symbol, position.symbol)

  def test_get_value(self):
    positions = [
      Position({'symbol': 'AAPL'}), 
      Position({'symbol': 'LUPE.ST'})
    ]
    positions[0].get_value = Mock(return_value = Decimal('60'))
    positions[1].get_value = Mock(return_value = Decimal('40'))
    portfolio = Portfolio({'positions': positions, 'currency': 'EUR'})
    self.assertEquals(100, portfolio.get_value())
    positions[0].get_value.assert_called_with('EUR')
    positions[1].get_value.assert_called_with('EUR')

  def test_load(self):
    portfolio = Portfolio.load(1)
    self.assertEquals(1, portfolio.id)
    self.assertEquals("Avanza", portfolio.name)

if __name__ == '__main__':
    unittest.main()
