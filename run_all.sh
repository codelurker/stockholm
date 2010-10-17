mysql -u root stocks  -v -f <quotes.sql
mysql -u root stocks  -v -f <indicators.sql
mysql -u root stocks  -v -f <portfolios.sql
mysql -u root stocks  -v -f <positions.sql
mysql -u root stocks  -v -f <my_portfolios.sql
python otherstocks.py
python omx-large-cap.py
python omx-mid-cap.py
python omx30.py
python footsie350.py

python indicators.py
python portfolio.py | expand -t 12
