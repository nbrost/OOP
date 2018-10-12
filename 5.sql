.print Question 5 - nbrost
.echo on
select locations.city, locations.prov
from locations
join rides on rides.dst = locations.lcode
group by locations.city
order by count(*) desc
limit 3;
