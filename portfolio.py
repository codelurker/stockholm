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

def separator():
  print "---------------------------------------------------------------------------------------------------------------------------------------------------------------"

def print_portfolio(id):
  portfolio = Portfolio.get_portfolio(id)
  positions = portfolio.positions
  
  print "\nPortfolio: %s" % portfolio.name
  separator()
  print "Symbol\tEnter Date\tDate\tValue\tGain\tShares\tRTR\tEnter Price\tClose\tStop\tATR EXP 20\tT Stop\tATR Stop\tShould sell?"
  separator()
  for p in positions:
    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ff(
      (
      p.symbol, 
      p.enter_date,
      p.current_quote.date,
      p.get_value(portfolio.currency), 
      p.get_gain(), 
      p.shares, 
      #p.get_max(), 
      p.get_rtr(), 
      p.enter_price,
      p.current_quote.close, 
      p.get_stop(),
      p.get_enter_indicator().atr_exp20,
      p.get_trailing_stop(),
      p.get_atr_trailing_stop(),
      p.should_sell()
      ))
  separator()
  print "TOTAL\t\t\t%s" % (f(portfolio.get_value()))
  
print_portfolio(1)
print_portfolio(2)
print_portfolio(3)
