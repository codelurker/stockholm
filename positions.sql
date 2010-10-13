DROP TABLE position;
CREATE TABLE position (
  symbol varchar(20) not null,
  currency varchar(3) not null,
  currency_rate decimal(10, 5) not null, -- How do I convert to the portfolio currency ?
  enter_date date not null,
  exit_date date default null,
  enter_price decimal(10, 5) not null,
  exit_price decimal(10, 5) default null,
  enter_commission decimal(10, 5) not null, -- In the portfolio currency
  exit_commission decimal(10, 5) default null, -- In the portfolio currency
  shares decimal(10, 5) not null,
  portfolio_id integer not null, -- In the portfolio currency
  primary key (portfolio_id, symbol, enter_date)
);
