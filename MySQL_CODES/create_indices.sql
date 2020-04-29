#CREATING AND INSERTING INDEX / INDICES HISTORICAL DATA into DB
#eg from yahoo finance
create table indicies(
name varchar(256),
timestamp date,
open float,
high float,
close float
);

#well use 2 data sources for each index
#yahoo finance has price data 2008+ for NIFTY
#the NSE has the data for the NIFTY 2006 and 2007

#first datasource YAHOO

#from 1 jan 2008 to last date of our data

#after downloaded data from yahoo for nifty and saved to a file we bulk load data

load data local infile '/FILE/NAME'
into table indices
fields terminated by ',' #the delimiter
ignore 1 lines #the header
(@Date, open,high,low,close,@trded,@turnover)
#note not using all data from file (not last 2 columns so we put them @trded to be assigned to a variable and then ignored)
set timestamp = str_to_date(@Date, '%Y-%m-%d'), 
name = 'NIFTY';

#SECOND DATA SOURCE IS THE NSE india
#jan 1st 2007 to dec 31st 2007 (NSE only allows one year at a time)
#download for 2006 year as well

load data local infile
'FILE/PATH'
into table indices
fields terminated by ',' ignore 1 lines
(@Date,open,high,low,close,@trded,@turnover)
#note date format on nse is different
set timestamp = str_to_date(@Date, '%d-%b-%Y'), 
name = 'NIFTY';

#input all indces into this table

#then insert these indices table into the cm_adjusted_prices table so we can compare our model to how the indces did 
#create a new table for international stocks & indices
#have 2 tables one for indices and stocks for india
#one for indices and stocks for international markets








