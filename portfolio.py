from dao import *
from decimal import *

def f(arg):
  if arg == True:
    return "Yes"
  if arg is False:
    return "No"
  #try:
  if(isinstance(arg, Decimal)):
    return "%8.2f" % arg
  else:
    return arg
  #except TypeError:
  #  return ""
  #except ValueError:
  #  return arg

def ff(tpl):
  return tuple(map(f, tpl))

def print_portfolio(id):
  portfolio = Portfolio.get_portfolio(id)
  positions = portfolio.positions
  print "-------------------------------------------------------------------------------------------------------------------"
  print "Symbol\tDate\tValue\tGain\tShares\tRTR\tClose\tStop\tC Stop\tT Stop\tSell"
  print "-------------------------------------------------------------------------------------------------------------------"
  for p in positions:
    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ff(
      (
      p.symbol, 
      p.current_quote.date,
      p.get_value(portfolio.currency), 
      p.get_gain(), 
      p.shares, 
      p.get_rtr(), 
      p.current_quote.close, 
      p.stop,
      p.get_stop(),
      p.get_trailing_stop(),
      p.should_sell()
      ))
  print "-------------------------------------------------------------------------------------------------------------------"
  print "TOTAL\t\t%s" % (f(portfolio.get_value()))
  print ""
  
print_portfolio(1)
print_portfolio(2)
print_portfolio(3)
