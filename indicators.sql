DROP TABLE indicator;
CREATE TABLE indicator (
  symbol varchar(8) not null,
  date date not null,
  sma_20 decimal(10, 5) not null,
  sma_50 decimal(10, 5) not null,
  primary key (symbol, date)
);
