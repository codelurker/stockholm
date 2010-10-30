#!/bin/bash
#http://www.etfsecurities.com/en/securities/etfs_securities.asp

function prices {
symbol=$1
  wget -q "http://finance.yahoo.com/d/quotes.csv?s=$symbol=X&t=2d&f=sd1l1" -O -
}
	
prices "SEKGBP"
prices "EURGBP"
prices "USDGBP"
