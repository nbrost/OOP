.print Question 1 - nbrost
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
