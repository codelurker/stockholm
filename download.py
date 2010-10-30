import ystockquote
import time
import datetime
from datetime import date
from connection import db

start_date='20100101'
def prices(symbol):
  """
  Loads the prices from the start date for the given symbol
  Only new quotes are downloaded.
  """
  to = date.today().strftime("%Y%m%d")
  c = db.cursor()
  c.execute("SELECT DATE_ADD(max(date), INTERVAL 1 DAY) FROM quote where symbol = %s",
               (symbol))
  (_from, ) = c.fetchone()
  if _from == date.today():
    print "Skipping %s" % symbol
    return
  print "Downloading %s" % symbol
  if _from is None: 
    _from = start_date
  else:
    _from = _from.strftime("%Y%m%d")
  prices = ystockquote.get_historical_prices(symbol, _from, to)
  headers = prices[0]
  try:
    close = get_idx(headers, 'Close')
    date_ = get_idx(headers, 'Date')
    open = get_idx(headers, 'Open')
    high = get_idx(headers, 'High')
    low = get_idx(headers, 'Low')
    quotes = prices[1:]
    for l in quotes:
      #print "%s %s" % (l[date_], l[close])
      insert(symbol, l[date_], l[close], l[high], l[low], l[open])
    print "Inserted %s new quotes for %s" % (len(quotes), symbol)
  except:
    print "Could not download %s" % symbol

def get_idx(headers, query):
    for index, item in enumerate(headers):
      if (item == query):
        return index
    #print("Could not find requested header [%s]" % query)
    #print("Available ones are %s" % headers)
    raise "Eror ind downloading quote"

def insert(symbol, date, close, high, low, open):
  c = db.cursor()
  c.execute("INSERT INTO quote (date, symbol, close, high, low, open) VALUES (%s, %s, %s, %s, %s, %s)",
               (date, symbol, close, high, low, open))
