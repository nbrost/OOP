.print Question 1 - nbrost
.echo on
select  city
from requests
join locations as a
on requests.pickup = a.lcode;
/*join rides as b
on b.src = locations.lcode
where a.city = b.city;*/

