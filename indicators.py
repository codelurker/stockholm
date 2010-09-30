import ystockquote
import time
import datetime
from datetime import date
import MySQLdb
import dao

db=MySQLdb.connect(host="localhost", user="robcos",
                      passwd="robcos", db="stocks")

def build_averages(symbol, date):
  c = db.cursor()
  
  c.execute("SELECT avg(close) from (select close as close from quote where date <= %s and symbol =%s order by date desc limit %s) as avf2", (date, symbol, 20))
  (sma_20, ) = c.fetchone()
  c.execute("SELECT avg(close) from (select close as close from quote where date <= %s and symbol =%s order by date desc limit %s) as avf2", (date, symbol, 50))
  (sma_50, ) = c.fetchone()
  c.execute("SELECT avg(tr) from (select tr from quote where date <= %s and symbol =%s order by date desc limit %s) as avf2", (date, symbol, 14))
  (atr_14, ) = c.fetchone()
  c.execute("INSERT INTO indicator (date, symbol, sma_20, sma_50, atr_14) VALUES (%s, %s, %s, %s, %s)", (date, symbol, sma_20, sma_50, atr_14))

def build_indicators():
  c = db.cursor()
  c.execute("select q.symbol, q.date from quote q left outer join indicator i on (q.date=i.date AND q.symbol=i.symbol) where i.symbol is null")
  for (symbol, date) in c.fetchall():
    build_atr(symbol, date)
  c.execute("select q.symbol, q.date from quote q left outer join indicator i on (q.date=i.date AND q.symbol=i.symbol) where i.symbol is null")
  for (symbol, date) in c.fetchall():
    build_averages(symbol, date)

def build_atr(symbol, date):
  quote = dao.Quote.get_quote(symbol, date)
  prev = quote.previous()
  if prev == None:
    print "quote %s has no prev" % (quote)
    return
  tr = max(quote.high, prev.close) - min(quote.low, prev.close)
  #print "%s %s %s" % (tr, quote, prev)
  dao.Quote.set_tr(symbol, date, tr)
  
build_indicators()