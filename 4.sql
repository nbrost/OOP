.print Question 1 - nbrost
.echo on
select distinct r.rid, r.email, r.pickup, r.dropoff, ri.rno, l.city
from rides ri, requests r, locations l
where r.rdate = ri.rdate
and r.amount >= ri.price
and r.pickup= l.lcode
and l.city in (select l.city
		from rides ri, locations l
		where ri.src = l.lcode)
and r.dropoff in (select 
;

