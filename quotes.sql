DROP TABLE quote;
CREATE TABLE quote (
  symbol varchar(20) not null,
  date date not null,
  close decimal(10, 5) not null,
  high decimal(10, 5) not null,
  low decimal(10, 5) not null,
  open decimal(10, 5) not null,
  tr decimal(10, 5) default null,
  primary key (symbol, date)
);
