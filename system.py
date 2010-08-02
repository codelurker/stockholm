import ystockquote
import time
import datetime
from datetime import date

def prices(symbol, days):
  """
  Get the prices in the X days for the given symbol
  
  Returns an array
  """
 
  to = date.today()
  _from = to - datetime.timedelta(days=days)
  to = to.strftime("%Y%m%d")
  _from = _from.strftime("%Y%m%d")
  prices = ystockquote.get_historical_prices(symbol, _from, to)
  quotes = []
  for p in prices[1:]:
    quotes.append(float(p[4]))
  return quotes

def mavg(quotes):
  return sum(quotes)/len(quotes)

def min_quote(symbol, days):
  return min(quotes)
  
def over_mavg(price, quotes):
  _mavg = mavg(quotes) 
  return price >= _mavg

def check(symbol):
  days = 20
  quotes = prices(symbol, days) 
  _raising = raising(symbol) 
  _price = float(ystockquote.get_price(symbol))
  _over_mavg = over_mavg(_price, quotes)
  _min = min(quotes)
  #print "%s min %s, now %s" % (symbol, _min, _price)

  if(_raising and
     _over_mavg):
    print "<div style=color:green>Raising and over mavg: BUY %s</div>" % symbol
    return

  if(not _over_mavg):
    print "<div style=color:red>Not over mavg: SELL %s</div>" % symbol
    return
  
  if(_price <= _min):
    print "<div style=color:red>Under 20 day min: SELL %s</div>" % symbol
    return
  
  print "<div>No matching condition for %s</div>" % symbol
  

# buy signals
# raising
# over mavg

# sell signal
# not raising AND under mavg
# OR
# down to 20 day minimum
  
def raising(symbol):
  return float(ystockquote.get_change(symbol))>0

print 'Content-Type: text/html'
print ''
print '<body>'

check('SAND.ST')
check('AZN.ST')
check('LUPE.ST')
check('TEL2-A.ST')
check('TLSN.ST')
check('AZA.ST')
check('SEB-A.ST')



print '<h2>Retail & Services</h2>'
check('ELUX-B.ST')
check('HMB.ST')
check('ENRO.ST')
check('CLAS-B.ST')

print '<h2>Energi</h2>'
check('LUPE.ST')
check('AOIL-SDB.ST')
check('CCOR-B.ST')
check('ENQ.ST')
 
print '<h2>Telecom</h2>'
check('TEL2-A.ST')
check('TEL2-B.ST')
check('TLSN.ST')
check('MIC-SDB.ST')
 
print '<h2>IT</h2>'
check('EWRK.ST')
check('KNOW.ST')
check('AXIS.ST')
check('ERIC-A.ST')
 
print '<h2>Industri</h2>'
check('SAND.ST')
check('SWEC-A.ST')
check('SWEC-B.ST')
check('ATCO-A.ST')
 
print '<h2>Materials</h2>'
check('BOL.ST')
check('HOLM-A.ST')
check('LUMI-SDB.ST')
check('SSAB-A.ST')
 
print '<h2>Pharmaceutical</h2>'
check('AZN.ST')
check('ORX.ST')
check('BIOG-B.ST')
check('ACTI.ST')
 
print '<h2>Finance</h2>'
check('SEB-A.ST')
check('AZA.ST')
check('SWED-A.ST')
check('BURE.ST')
 
print '</body>'

