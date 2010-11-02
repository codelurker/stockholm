import unittest
from mock import Mock
from mock import patch

from dao import * 
from decimal import Decimal
from find_breakout import *

def find_recent_breakouts(events, not_older_than):

  if(events[-1].type == 'stop'):
    return False

if __name__ == '__main__':
    unittest.main()
