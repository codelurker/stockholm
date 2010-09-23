DROP TABLE quote;
CREATE TABLE quote (
  symbol varchar(8) not null,
  date date not null,
  close decimal(10, 5) not null,
  open decimal(10, 5) not null,
  primary key (symbol, date)
);
