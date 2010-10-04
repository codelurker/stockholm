from dao import *

portfolio = Portfolio.get_portfolio(1)
positions = portfolio.positions
for p in positions:
  print "%s\t%s\t\t%s\t%s\t\t%s" % (p.symbol, p.get_risk(), p.get_gain(), p.shares, p.get_rtr())
