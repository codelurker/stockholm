import unittest
from mock import Mock
from mock import patch

from dao import * 
from decimal import Decimal
from turtle import *

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
