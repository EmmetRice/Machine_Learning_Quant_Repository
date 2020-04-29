#create a table to hold the NSE bhav copy files
#the table will need to have columns which map to the file

create database NSE;
use NSE;

#for cash cm values

#column names and data types, and must match csv file
create table cmStaging (
symbol VARCHAR(256),
series VARCHAR(256), 
open float,
high float,
low float,
close float,
last float,
prevclose float,
tottrdqty float,
tottrdval float,
timestamp date,
totaltrades float,
isin varchar(256)
);

#similarly for the Fo (forward)  bliav copy files

create table foStaging (
instrument varchar(256),
symbol varchar(256),
expiry_dt date,
strike_pr float,
option_type varchar(256),
open float,
high float,
low float,
close float,
settle_pr float,
contracts float,
val_inlakh float,
open_int float,
chg_in_ol float,
timestamp date
);





    
    
    
    
    