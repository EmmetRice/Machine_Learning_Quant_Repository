#create calander features table )trading days) in SQL
#EG how mnay trading days arfe left in month after X date?

#THIS CALANDER CAN TRACK SEASONAL AFFECTS
#DO THIS FOR EACH MARKET INVESTIGATING
#from indices where symbol ='from given market'

#table for trading days, ie days the NIFTY has traded

#TRADING DAYS DECIDED FROM DAYS THE NIFTY WAS TRADED!!!!!

create table tdays (
select distinct timestamp as tday from indices where symbol = 'NIFTY'
order by tday asc
);
#asc for ascending


#creating an id to get an integer / count for the number of trade days (ie a column which numbers the days)
#useful for calculating how many trading days are between 2 dates 
alter table tdays add count_id int PRIMARY KEY auto_increment;


#creating trading days table and adding a join of tdays with itself
#first table (a) we are adding the id (count index) and the trading day
#the second table (b) will have the trading day corresponding to the previous day for that id

create table trading_days(
select a.count_id as tday_id,
a.tday as tday,
b.tday as prev_tday
#above we giving our selections from tables below cleaner alias
#and these are the columns we want in the new table
from 
#choosing our left table data from tdays table and giving it alias a
(select count_id, tday from tdays) as a
left join
#now choosing our right table data
(select count_id+1 as count_id from tdays) as b
#as tdays table is sorted in ascending order, earlier dates are given a higher count_id
on a.count_id = b.count_id
);

#against each trading day in this trading_days table will be the previous trading days date
#this is useful for computing the returns for a particular day

#now we need to add columns to this trading_days table for that days data

alter table trading_days
add column year int,
add column month int,
add column day int,
add column day_of_week int,
add column tdays_left_in_month int,
add column tdays_left_in_week int,
add column week_of_year int,
add column tday_in_month int,
add column tday_in_week int;

#can set year month and day data using inbuilt sql functions
update trading_days set year = year(tday);
update trading_days set month = month(tday);
update trading_days set day = day(tday);
update trading_days set day_of_week = weekday(tday);
update trading_days set week_of_year = week(tday);

#to update the other data we need to create a new table

#has maz and min tday date for each month

create table max_min_tday_month(
select year, month, 
min(tday_id) as min_tday,
mac(tday_id) as max_tday
from trading_days GROUP by year, month
);

#tradings days left in month
update trading_days 
set tdays_left_in_month = 
(select max_tday from max_min_tday_month
#setting clause to match the year and months
where 
trading_days.year = max_min_tday_month.year and
trading_days.month = max_min_tday_month.month) 
- tday_id;

#trading day we are in month
update trading_days 
set tdays_in_month = tday_id - 
(select min_tday from max_min_tday_month
#setting clause to match the year and months
where 
trading_days.year = max_min_tday_month.year and
trading_days.month = max_min_tday_month.month) 
;

#NOW FOR WEEK

create table max_min_tday_week (
select year, week_of_year, 
min(tday_id) as min_tday,
mac(tday_id) as max_tday
from trading_days GROUP by year, week_of_year
);

#tradings days left in month
update trading_days 
set tdays_left_in_week = 
(select max_tday from max_min_tday
#setting clause to match the year and months
where 
trading_days.year = max_min_tday_week.year and
trading_days.week = max_min_tday_week.week) 
- tday_id;

#trading day we are in month
update trading_days 
set tdays_in_week = tday_id - 
(select min_tday from max_min_tday_week
#setting clause to match the year and months
where 
trading_days.year = max_min_tday_week.year and
trading_days.week = max_min_tday.week) 
;



#JOINS
#https://www.youtube.com/watch?v=9yeOJ0ZMUYw&t=1s

#INNER JOIN only returns connection (joined) rows 
#when there is a matchging field id in both tables
#LEFT JOIN will return everyrow from left table even if no matching id on right 
#RIGHT JOIN return all row from right table even when no match on left
#WHEN no match, null values are imput in corresponding fields
#FULL / FULL OUTER JOIN is like and left and right join
#MY SQL does not suppoort full join as standard


#EXAMPLE

#select * 
#from person #(left table)
#inner join location #(right table)
#on person.base_id = location.base_id;

#or rather than all columns (SELECT *) choose columns we want by specifiying table and field name
#select person.base_id, location.base_id, person.person_name, location.location_name
#this is wordy so can use aliases
#from person as p
#inner join location as l

# Select p.base_id, l.base_id, p.person_name, l.location_name
#from person #(left table)
#inner join location #(right table)
#on person.base_id = location.base_id;


