from dao import *
from decimal import *
getcontext().prec = 8
portfolio = Portfolio.get_portfolio(1)
positions = portfolio.positions
def f(arg):
  return "%10.2f" % arg

print "%s\t\t%s\t\t%s\t\t%s\t\t%s" % ('Symbol', 'Value', 'Gain', 'Shares', 'RTR')
print "---------------------------------------------------------------------------"
for p in positions:
  print "%s\t\t%s\t%s\t%s\t%s" % (p.symbol, f(p.get_value(portfolio.currency)), f(p.get_gain()), f(p.shares), f(p.get_rtr()))

print "---------------------------------------------------------------------------"
print "TOTAL\t\t%s" % (f(portfolio.get_value()))
