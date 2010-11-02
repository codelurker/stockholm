import unittest
from mock import Mock
from mock import patch

from dao import * 
from decimal import Decimal
from turtle import *

class TestTurtleSystem(unittest.TestCase):

  def test_handle_entry_not_breakout_20_does_not_open_position(self):
    handlers = TurtleSystem()
    
    quote = Quote({})
    handlers.is_20_breakout = Mock(return_value = False)
    handlers.open_position = Mock()
     
    self.assertFalse(handlers.handle_entry(quote))
    self.assertFalse(handlers.open_position.called)

  def test_handle_entry_breakout_20_and_prev_breakout_looser_does_open_position(self):
    handlers = TurtleSystem()
    
    quote = Quote({})
    handlers.is_20_breakout = Mock(return_value = True)
    handlers.is_prev_20_breakout_looser = Mock(return_value = True)
    handlers.open_position = Mock()

    self.assertTrue(handlers.handle_entry(quote))
    handlers.open_position.assert_called_with(quote)
   
  def test_handle_entry_breakout_20_and_not_prev_breakout_looser_does_not_open_position(self):
    handlers = TurtleSystem()
    
    quote = Quote({})
    handlers.is_20_breakout = Mock(return_value = True)
    handlers.is_prev_20_breakout_looser = Mock(return_value = False)
    handlers.is_50_breakout = Mock(return_value = False)
    handlers.open_position = Mock()

    self.assertFalse(handlers.handle_entry(quote))
    self.assertFalse(handlers.open_position.called)
 
  def test_handle_entry_breakout_20_and_not_prev_breakout_looser_and_breakout_50_does_open_position(self):
    handlers = TurtleSystem()
    
    quote = Quote({})
    handlers.is_20_breakout = Mock(return_value = True)
    handlers.is_prev_20_breakout_looser = Mock(return_value = False)
    handlers.is_50_breakout = Mock(return_value = True)
    handlers.open_position = Mock()

    self.assertTrue(handlers.handle_entry(quote))
    handlers.open_position.assert_called_with(quote)

  @patch('dao.Position.open')
  @patch('dao.Position.get_shares')
  def test_open_position(self, get_shares, open):
    handlers = TurtleSystem()
    handlers.commision = 99
    handlers.currency = 'USD'
    handlers.currency_rate = 1.2
    handlers.account = 100000
    self.assertFalse(handlers.position)

    quote = Quote({'symbol': 'AAPL'})
    next_quote = Quote({'open': 100, 'date': '10/01/10'})
    quote.next = Mock(return_value = next_quote)
    position = Position({});
    open.return_value = position
    get_shares.return_value = 1000
    handlers.get_risk = Mock(return_value = 1000)

    handlers.open_position(quote)

    self.assertTrue(handlers.position)
    open.assert_called_with('AAPL', 'USD', 1.2, '10/01/10', 100, 99, 1000)
    get_shares.assert_called_with(quote, 1000)

  def test_get_risk(self):
    handlers = TurtleSystem()
    handlers.total = Decimal('100000')
    
    self.assertEquals(Decimal('1000'), handlers.get_risk())
    
class TestTurtle(unittest.TestCase):

  @patch('turtle.TurtleSystem.handle_units')
  @patch('turtle.TurtleSystem.handle_exit')
  @patch('turtle.TurtleSystem.handle_stop')
  @patch('turtle.TurtleSystem.has_position')
  def test_handle_quote_handle_stop(self,
      has_position, 
      handle_stop, 
      handle_exit, 
      handle_units):

    has_position.return_value = True
    handle_stop.return_value = True
    quote = Quote({})

    handle_quote(quote, TurtleSystem())

    handle_stop.assert_called_with(quote)
    self.assertFalse(handle_exit.called)
    self.assertFalse(handle_units.called)
 

  @patch('turtle.TurtleSystem.handle_units')
  @patch('turtle.TurtleSystem.handle_exit')
  @patch('turtle.TurtleSystem.handle_stop')
  @patch('turtle.TurtleSystem.has_position')
  def test_handle_quote_handle_exit(self, 
      has_position, 
      handle_stop, 
      handle_exit, 
      handle_units):

    has_position.return_value = True
    handle_stop.return_value = False
    handle_exit.return_value = True
    quote = Quote({})

    handle_quote(quote, TurtleSystem())

    handle_stop.assert_called_with(quote)
    self.assertFalse(handle_units.called)


  @patch('turtle.TurtleSystem.handle_units')
  @patch('turtle.TurtleSystem.handle_exit')
  @patch('turtle.TurtleSystem.handle_stop')
  @patch('turtle.TurtleSystem.has_position')
  def test_handle_quote_handle_units(self, 
      has_position, 
      handle_stop, 
      handle_exit, 
      handle_units):

    has_position.return_value = True
    handle_stop.return_value = False
    handle_exit.return_value = False
    quote = Quote({})

    handle_quote(quote, TurtleSystem())

    handle_stop.assert_called_with(quote)
    handle_exit.assert_called_with(quote)
    handle_units.assert_called_with(quote)

  @patch('turtle.TurtleSystem.handle_entry')
  @patch('turtle.TurtleSystem.has_position')
  def test_handle_quote_handle_units(self, 
      has_position, 
      handle_entry):

    has_position.return_value = False
    quote = Quote({})

    handle_quote(quote, TurtleSystem())

    handle_entry.assert_called_with(quote)
    
if __name__ == '__main__':
    unittest.main()
