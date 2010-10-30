import ystockquote
import time
import datetime
import math
from datetime import date
from decimal import Decimal
import MySQLdb
from dao import Position
from dao import Quote
db=MySQLdb.connect(host="localhost", user="robcos",
                      passwd="robcos", db="stocks")


 #print("[%s] %s mavg20=%s mavg50=%s" % (symbol, date, days, sma_50))

total = 100000
currency = 'USD'
#stocks = 0
#symbol = 'LUPE.ST'
symbol = 'AAPL'
symbol = 'RIO.L'
symbol = 'SYSR.ST'
position = None
skip = 20
for quote in Quote.get_quotes(symbol):
  skip = skip -1
  if skip > 0:
    continue
  print "\nSimulating %s" % quote
  print "%s" % quote.get_indicator()
  if position:
    position.current_quote = quote
    #print "I already have a position for %s" % symbol
    #if quote.is_below_10_day_low(position):
    if quote.has_met_stop(position):
      print "STOP MET %s" % position.get_stop()
      print "Selling %s" % position
      print "Loss %s" % position.get_gain()
      total = total + position.get_value(currency)
      position = None
    elif quote.is_below_10_day_low():
      print "10 day low MET %s" % position.get_trailing_stop()
      print "Selling %s" % position
      print "Gain %s" % position.get_gain()
      total = total + position.get_value(currency)
      position = None
    # total = total + (stocks * float(quote.close))
    #  position.value = 0
  else:
    over = quote.is_above_20_day_high()
    if over:
      risk = Decimal(total/100)
      shares = Position.get_shares(quote, risk)
      #print "Stop %s, Risk %s, Portfolio max risk %s" % (stop, shares * indicator.atr_exp20 * 2, risk)
      position = Position.open(symbol, currency, 1, quote.date, quote.close,
         Decimal('9'), shares)
      position.current_quote = quote
      position.is_long = True
      print "Opened %s" % position
      #position = Position({'symbol': symbol, 'is_long': True, 'current_quote': quote})
      #position.stop = indicator.calculate_stop(quote)
      print "Buy  %s" % (position)
      #if indicator.atr_14:
      #  print "%s quote over sma50 on %s" % (quote.symbol, quote.date)
      #  stop = float(quote.close) - float(indicator.atr_14) * float(0.1);
      #  stocks = float(total/2)/float(quote.close)
      #  position.value = stocks * float(quote.close)
      total = total - position.get_value(currency)
      #  print "Buying %s, stop at %s, position %s" % (quote, stop, position.value)
  #print "Total %s, position %s, %s" % (total, position.value, quote)
    else:
      #print "Bad day, pass"
      pass
  #print "Total %s" % (total)
  if total < 0:
    exit("BOOM")
if position:
  print "Adding current gain"
  total = total + position.get_value(currency)
print "Total %s" % (total)

