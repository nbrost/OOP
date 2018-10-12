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

