drop table if exists requests;
drop table if exists enroute;
drop table if exists bookings;
drop table if exists rides;
drop table if exists locations;
drop table if exists cars;
drop table if exists members;

PRAGMA foreign_keys = ON;

create table members (
  email		char(15),
  name		char(20),
  phone		char(12),
  primary key (email)
);
create table cars (
  cno		int,
  make		char(12),
  model		char(12),
  year		int,
  seats		int,
  owner		char(15),
  primary key (cno),
  foreign key (owner) references members
);
create table locations (
  lcode		char(5),
  city		char(16),
  prov		char(16),
  address	char(16),
  primary key (lcode)
);
create table rides (
  rno		int,
  price		int,
  rdate		date,
  seats		int,
  lugDesc	char(10),
  src		char(5),
  dst		char(5),
  driver	char(15),
  cno		int,
  primary key (rno),
  foreign key (src) references locations,
  foreign key (dst) references locations,
  foreign key (driver) references members,
  foreign key (cno) references cars
);
create table bookings (
  bno		int,
  email		char(15),
  rno		int,
  cost		int,
  seats		int,
  pickup	char(5),
  dropoff	char(5),
  primary key (bno),
  foreign key (email) references members,
  foreign key (rno) references rides,
  foreign key (pickup) references locations,
  foreign key (dropoff) references locations
);
create table enroute (
  rno		int,
  lcode		char(5),
  primary key (rno,lcode),
  foreign key (rno) references rides,  
  foreign key (lcode) references locations
);  
create table requests (
  rid		int,
  email		char(15),
  rdate		date,
  pickup	char(5),
  dropoff	char(5),
  amount	int,
  primary key (rid),
  foreign key (email) references members,
  foreign key (pickup) references locations,
  foreign key (dropoff) references locations
);


