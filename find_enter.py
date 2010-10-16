import dao

for quote in dao.Quote.get_latest_quotes():
  if quote.is_above_20_day_high():
    print "||||||||||||||||||||||| Should enter %s " % quote.symbol
    print quote
    print quote.
  else:
    print "Leave %s " % quote.symbol
