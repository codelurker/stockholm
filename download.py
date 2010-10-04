import ystockquote
import time
import datetime
from datetime import date
import MySQLdb

db=MySQLdb.connect(host="localhost", user="robcos",
                      passwd="robcos", db="stocks")
def prices(symbol, days):
  """
  Get the prices in the X days for the given symbol
  
  Returns an array
  """
  ## adjust for weekends
  days_adjusted = days/5*3 + days  
 
  to = date.today()
  _from = to - datetime.timedelta(days=days_adjusted)
  to = to.strftime("%Y%m%d")
  _from = _from.strftime("%Y%m%d")
  prices = ystockquote.get_historical_prices(symbol, _from, to)
  headers = prices[0]
  close = get_idx(headers, 'Close')
  date_ = get_idx(headers, 'Date')
  open = get_idx(headers, 'Open')
  high = get_idx(headers, 'High')
  low = get_idx(headers, 'Low')
  quotes = prices[1:]
  if (len(quotes) < days):
    print "\n##### Warning: Could not load enough days of data (found %s quotes but requested %s)\n" % (len(quotes), days)
  for l in quotes:
    #quotes.append(float(p[4]))
    print "%s %s" % (l[date_], l[close])
    insert(symbol, l[date_], l[close], l[high], l[low], l[open])
  return quotes

def get_idx(headers, query):
    for index, item in enumerate(headers):
      if (item == query):
        return index
    print("Could not find requested header [%s]" % query)
    print("Available ones are %s" % headers)
    exit()

def insert(symbol, date, close, high, low, open):
  c = db.cursor()
  c.execute("INSERT INTO quote (date, symbol, close, high, low, open) VALUES (%s, %s, %s, %s, %s, %s)",
               (date, symbol, close, high, low, open))

prices('LUPE.ST', 565)
prices('AAPL', 565)
prices('GOOG', 565)
prices('AXIS.ST', 565)
prices('MIC-SDB.ST', 565)
prices('BOL.ST', 565)
