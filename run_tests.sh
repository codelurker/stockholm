mysqldump -u root stocks >dump.sql
mysql -u root stocks < fixture.sql
python dao_test.py
mysqldump -u root stocks <dump.sql >/dev/null
