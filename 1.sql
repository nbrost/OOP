.print Question 1 - nbrost
.echo on
select distinct name, email
from members m,cars c, rides r
where m.email = c.owner
and c.cno = r.cno;
