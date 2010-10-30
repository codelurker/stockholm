import unittest
from mock import Mock
from mock import patch

from dao import * 
from decimal import Decimal
from turtle import *

class TestTurtleHandlers(unittest.TestCase):

  def test_handle_entry_close_below_20_day_high(self):
    handlers = TurtleHandlers()
    
    quote = Quote({'close': 80})
    indicator = Indicator({'hh_20': 100})
    quote.get_indicator = Mock(return_value = indicator)
     
    self.assertFalse(handlers.handle_entry(quote))

  def test_handle_entry_breakout_20_and_prev_breakout_looser_does_open_position(self):
    handlers = TurtleHandlers()
    
    quote = Quote({})
    handlers.is_20_breakout = Mock(return_value = True)
    handlers.is_prev_20_breakout_looser = Mock(return_value = True)

    self.assertTrue(handlers.handle_entry(quote))
   
  def test_handle_entry_breakout_20_and_not_prev_breakout_looser_does_not_open_position(self):
    handlers = TurtleHandlers()
    
    quote = Quote({})
    handlers.is_20_breakout = Mock(return_value = True)
    handlers.is_prev_20_breakout_looser = Mock(return_value = False)

    self.assertFalse(handlers.handle_entry(quote))
 
  def test_handle_entry_breakout_20_and_not_prev_breakout_looser_and_breakout_50_does_open_position(self):
    handlers = TurtleHandlers()
    
    quote = Quote({})
    handlers.is_20_breakout = Mock(return_value = True)
    handlers.is_prev_20_breakout_looser = Mock(return_value = False)
    handlers.is_50_breakout = Mock(return_value = True)

    self.assertTrue(handlers.handle_entry(quote))
    

class TestTurtle(unittest.TestCase):

  @patch('turtle.TurtleHandlers.handle_units')
  @patch('turtle.TurtleHandlers.handle_exit')
  @patch('turtle.TurtleHandlers.handle_stop')
  @patch('turtle.has_position')
  def test_handle_quote_handle_stop(self,
      has_position, 
      handle_stop, 
      handle_exit, 
      handle_units):

    has_position.return_value = True
    handle_stop.return_value = True
    quote = Quote({})

    handle_quote(quote)

    handle_stop.assert_called_with(quote)
    self.assertFalse(handle_exit.called)
    self.assertFalse(handle_units.called)
 

  @patch('turtle.TurtleHandlers.handle_units')
  @patch('turtle.TurtleHandlers.handle_exit')
  @patch('turtle.TurtleHandlers.handle_stop')
  @patch('turtle.has_position')
  def test_handle_quote_handle_exit(self, 
      has_position, 
      handle_stop, 
      handle_exit, 
      handle_units):

    has_position.return_value = True
    handle_stop.return_value = False
    handle_exit.return_value = True
    quote = Quote({})

    handle_quote(quote)

    handle_stop.assert_called_with(quote)
    self.assertFalse(handle_units.called)


  @patch('turtle.TurtleHandlers.handle_units')
  @patch('turtle.TurtleHandlers.handle_exit')
  @patch('turtle.TurtleHandlers.handle_stop')
  @patch('turtle.has_position')
  def test_handle_quote_handle_units(self, 
      has_position, 
      handle_stop, 
      handle_exit, 
      handle_units):

    has_position.return_value = True
    handle_stop.return_value = False
    handle_exit.return_value = False
    quote = Quote({})

    handle_quote(quote)

    handle_stop.assert_called_with(quote)
    handle_exit.assert_called_with(quote)
    handle_units.assert_called_with(quote)

  @patch('turtle.TurtleHandlers.handle_entry')
  @patch('turtle.has_position')
  def test_handle_quote_handle_units(self, 
      has_position, 
      handle_entry):

    has_position.return_value = False
    quote = Quote({})

    handle_quote(quote)

    handle_entry.assert_called_with(quote)
    
if __name__ == '__main__':
    unittest.main()
