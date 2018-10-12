.print Question 1 - nbrost
.echo on
select distinct name, email
from members m,cars c, rides r
where m.email = c.owner
and c.cno = r.cno;
.print Question 2 - nbrost
.echo on
select distinct name, m.email
from members m,cars c, rides r, bookings b
where m.email = c.owner
and m.email = b.email
except
select distinct name, m.email
from members m,cars c, rides r, bookings b
where m.email = c.owner
and m.email = b.email
and m.email = r.driver;
.print Question 3 - nbrost
.echo on
select distinct m.email
from members m, bookings b, locations l, rides r
where m.email = b.email
and b.dropoff = l.lcode
and l.city = "Calgary"
and r.rno = b.rno
and r.rdate > '2018-10-31'
and r.rdate < '2018-12-01';
.print Question 4 - nbrost
.echo on
select requests.rid,requests.email, requests.pickup,requests.dropoff, rides.rno
from requests
join locations as a
on requests.pickup = a.lcode
join locations as c
on requests.dropoff = c.lcode,
rides
join locations as b
on rides.src = b.lcode
join locations as d
on rides.dst =d.lcode
where a.city = b.city
and c.city = d.city
and a.prov = b.prov
and c.prov = d.prov
and requests.rdate = rides.rdate
and rides.price <= requests.amount;
.print Question 5 - nbrost
.echo on
select locations.city, locations.prov
from locations
join rides on rides.dst = locations.lcode
group by locations.city
order by count(*) desc
limit 3;
.print Question 7 - nbrost
.echo on

select rides.rno, rides.price
from rides
join locations as a 
on rides.src = a.lcode
join locations as b 
on rides.dst = b.lcode
where a.city = "Edmonton"
and b.city = "Calgary"
and rides.rdate > "2018-09-31"
and rides.rdate < "2018-11-01"


except
select rides.rno, rides.price
from rides
join bookings as e on rides.rno = e.rno
group by rides.rno
having count(*) < rides.seats
order by rides.price
limit 1;


