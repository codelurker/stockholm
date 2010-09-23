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
  quotes = prices[1:]
  if (len(quotes) < days):
    print "\n##### Warning: Could not load enough days of data (found %s quotes but requested %s)\n" % (len(quotes), days)
  for l in quotes:
    #quotes.append(float(p[4]))
    print "%s %s" % (l[date_], l[close])
    insert(symbol, l[date_], l[close], l[open])
  return quotes

def get_idx(headers, query):
    for index, item in enumerate(headers):
      if (item == query):
        return index
    print("Could not find requested header [%s]" % query)
    print("Available ones are %s" % headers)
    exit()

def insert(symbol, date, close, open):
  c = db.cursor()
  c.execute("INSERT INTO quote (date, symbol, close, open) VALUES (%s, %s, %s, %s)",
               (date, symbol, close, open))

def build_mavg(symbol, date):
  c = db.cursor()
  days = 20
  c.execute("SELECT symbol, avg(close) from (select symbol, date, close as close from quote where date <= %s and symbol =%s order by date desc limit %s) as avf2", (date, symbol, days))
  (symbol, avg) = c.fetchone()
  print("buil mavg20 [%s] %s %s" % (symbol, date, avg))
  if(symbol == None):
    return
  
  c.execute("INSERT INTO indicator (date, symbol, sma_20) VALUES (%s, %s, %s)",
               (date, symbol, avg))
  days = 50
  c.execute("SELECT symbol, avg(close) from (select symbol, date, close as close from quote where date <= %s and symbol =%s order by date desc limit %s) as avf2", (date, symbol, days))
  (symbol, avg) = c.fetchone()
  print("buil mavg [%s] %s %s" % (symbol, date, avg))
  c.execute("UPDATE indicator set sma_50 = %s where date = %s and symbol = %s",
               (avg, date, symbol))

def build_mavgs():
  c = db.cursor()
  c.execute("SELECT distinct symbol FROM quote")
  symbols = c.fetchall()
  c.execute("SELECT distinct date FROM quote order by date")
  dates = c.fetchall()
  for (symbol,) in symbols:
    for (date,) in dates:
      print("buil mavg [%s] %s" % (symbol, date))
      build_mavg(symbol, date)
#
prices('LUPE.ST', 365)
#prices('AAPL', 365)
#prices('GOOG', 365)
#build_mavg('AAPL', '2010-08-07', 20)
#build_mavg('AAPL', '2010-08-06', 20)
#build_mavg('AAPL', '2010-08-05', 20)
#build_mavgs()
