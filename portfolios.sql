DROP TABLE portfolio;
CREATE TABLE portfolio (
  id integer not null, 
  name varchar(20) not null unique,
  currency varchar(3) not null,
  primary key (id)
);
