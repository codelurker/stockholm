DROP TABLE indicator;
CREATE TABLE indicator (
  symbol varchar(20) not null,
  date date not null,
  sma_20 decimal(10, 5) not null,
  sma_50 decimal(10, 5) not null,
  atr_14 decimal(10, 5) default null,
  atr_exp20 decimal(10, 5) default null,
  ll_10 decimal(10, 5) default null, -- Lowest low in the last 10 days
  hh_20 decimal(10, 5) default null, -- Highest high in the last 20 days
  primary key (symbol, date)
);
