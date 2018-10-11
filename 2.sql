.print Question 1 - nbrost
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
