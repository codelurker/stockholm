mysqldump -u root stocks >dump.sql
mysql -u root stocks < fixture.sql
python dao_test.py
mysql -u root stocks < dump.sql
