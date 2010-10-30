import ystockquote
import download
import time
from datetime import datetime
from _mysql_exceptions import IntegrityError
import MySQLdb
import indicators

db=MySQLdb.connect(host="localhost", user="robcos",
                      passwd="robcos", db="stocks")

def download_last_quote(symbol):
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
  
c = db.cursor()
c.execute("SELECT distinct symbol FROM position")
rows = c.fetchall()
for (symbol,) in rows:
  download_last_quote(symbol)

indicators.build_indicators()
