mysql -u root stocks  -v -f <quotes.sql
mysql -u root stocks  -v -f <indicators.sql
mysql -u root stocks  -v -f <positions.sql
mysql -u root stocks  -v -f <portfolio.sql
python download.py
python indicators.py
python portfolio.py | expand -t 12
