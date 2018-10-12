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


