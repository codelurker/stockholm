#mysql -u root stocks  -v -f <quotes.sql
#mysql -u root stocks  -v -f <indicators.sql
#mysql -u root stocks  -v -f <portfolios.sql
#mysql -u root stocks  -v -f <positions.sql
#mysql -u root stocks  -v -f <my_portfolios.sql
python otherstocks.py
python omx-large-cap.py
python omx-mid-cap.py
python omx30.py
python footsie-350.py

python indicators.py
mysqldump -u root stocks >dump.sql
python portfolio.py | expand -t 12
