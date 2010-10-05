from dao import *
from decimal import *

getcontext().prec = 8
portfolio = Portfolio.get_portfolio(1)
positions = portfolio.positions
def f(arg):
  if arg == True:
    return "Yes"
  if arg == False:
    return ""
  try:
    float(arg)
    return "%6.2f" % arg
  except TypeError:
    return ""
  except ValueError:
    return arg

def ff(tpl):
  return tuple(map(f, tpl))

print "%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s" % ('Symbol', 'Value', 'Gain', 'Shares', 'RTR', 'Close', 'Lowest low 20 day')
print "-------------------------------------------------------------------------------------------------------------------"
for p in positions:
  print "%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s" % ff(
    (p.symbol, p.get_value(portfolio.currency), p.get_gain(), 
    p.shares, p.get_rtr(), p.current_quote.close, p.get_trailing_stop(), p.should_sell()))
print "-------------------------------------------------------------------------------------------------------------------"
print "TOTAL\t\t%s" % (f(portfolio.get_value()))
