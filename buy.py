import ystockquote
import time
import datetime
from datetime import date
import MySQLdb
import dao
from dao import Position
db=MySQLdb.connect(host="localhost", user="robcos",
                      passwd="robcos", db="stocks")


 #print("[%s] %s mavg20=%s mavg50=%s" % (symbol, date, days, sma_50))

total = 100000
#stocks = 0
symbol = 'LUPE.ST'
position = None
for quote in dao.Quote.get_quotes(symbol):
  print "\nSimulating %s" % quote.date
  if position:
    print "I already have a position for %s" % symbol
    if quote.has_met_stop(position):
      print "Selling %s" % quote
      position = None
    # total = total + (stocks * float(quote.close))
    #  position.value = 0
  else:
    over = quote.is_over_sma50_7()
    if over:
      print "No position for %s on %s. Let's get one" % (quote.symbol, quote.date)
      indicator = quote.get_day_indicator()
      position = Position({'symbol': symbol})
      if indicator.atr_14:
      #  print "%s quote over sma50 on %s" % (quote.symbol, quote.date)
      #  stop = float(quote.close) - float(indicator.atr_14) * float(0.1);
      #  stocks = float(total/2)/float(quote.close)
      #  position.value = stocks * float(quote.close)
      #  total = total - position.value
      #  print "Buying %s, stop at %s, position %s" % (quote, stop, position.value)
  #print "Total %s, position %s, %s" % (total, position.value, quote)
    else:
      print "Bad day, pass"
  if total <0:
    exit("BOOM")
#total = total + position.value
#print "Total %s, position %s, %s" % (total, position.value, quote)
