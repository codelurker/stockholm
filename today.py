import ystockquote
import download
import time
from datetime import datetime
from _mysql_exceptions import IntegrityError
import indicators

from connection import db

def prices(symbol):
  """
     Downloads and stores the latest quote for the given symbol
  """
 
  all = ystockquote.get_all(symbol)
  try:
    download.insert(symbol, 
      datetime.strptime(all['date'], '"%m/%d/%Y"').strftime('%Y-%m-%d'),
      all['price'], 
      all['high'], 
      all['low'], 
      all['open'])
  except IntegrityError:
    print "Quote for %s already stored" % symbol
  except ValueError:
    print "Quote for %s could not be downloaded" % symbol
  
if __name__ == '__main__':
  c = db.cursor()
  c.execute("SELECT distinct symbol FROM position")
  rows = c.fetchall()
  for (symbol,) in rows:
    prices(symbol)
  indicators.build_indicators()
