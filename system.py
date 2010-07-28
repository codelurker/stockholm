import ystockquote
import time
import datetime
from datetime import date
#print ystockquote.get_price('SAND.ST')

def mavg(symbol, days):
  to = date.today()
  Xdays = 280
  _from = to - datetime.timedelta(days=days)
  to = to.strftime("%Y%m%d")
  _from = _from.strftime("%Y%m%d")
  prices = ystockquote.get_historical_prices(symbol, _from, to)
  #print prices
  quotes = []
  for p in prices[1:]:
    quotes.append(float(p[4]))
  #print sum(quotes)
  #print len(quotes)
  return sum(quotes)/len(quotes)

def over_mavg(symbol):
  price = float(ystockquote.get_price(symbol))
  days = 20
  _mavg = mavg(symbol, days) 
  if price < _mavg:
    #print "** SELL %s! Price %s is smaller than mavg(%s)=%s" % (symbol, price, days, _mavg)
    return False
  else:
    #print "KEEP %s! Price %s is larger than mavg(%s)=%s" % (symbol, price, days, _mavg)
    return True

def volatility(symbol):
  return 1
def check(symbol):
  _raising = raising(symbol) 
  _over_mavg = over_mavg(symbol)
  _volatility = volatility(symbol)
  if(_raising and
     _over_mavg):
    print "BUY or keep %s" % symbol
  if(not _over_mavg):
    print "SELL %s" % symbol
  
  
def raising(symbol):
  return float(ystockquote.get_change(symbol))>0

check('SAND.ST')
check('AZN.ST')
check('LUPE.ST')
check('TEL2-A.ST')
check('TLSN.ST')
check('AZA.ST')
check('SEB-A.ST')
