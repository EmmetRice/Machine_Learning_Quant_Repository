import mysql.connector

config = {
    'user': 'root',
    'password' : '2112',
    'host' : '127.0.0.1', #get this from the home on mysql
    'database' : 'nse'
}

connection = mysql.connector.connect(**config) #pass all dict parameters in config

#cursors are what execte queries
cursor = connection.cursor()


cursor.execute('set autocommit = 1')
cursor.execute('set global max_allowed_packet = 1073741824')
#getting split tickers
cursor.execute('select distinct symbol from cmSplits;')
symbol_with_splits = cursor.fetchall()
#WE ARE GETTIGN THIS FROM OUR DATABASE
#MYSQL ALWAYS RETURNS TUPLES

#iterate through and compute adjusted prices

adjusted_prices_all = []
#a list to hold lists, each containg symbol, date and adjusted price

for symbol in symbol_with_splits:
    symbol = list(symbol)[0]
    #cursor returns rows in tuples, fist element will be the symbol
    print(symbol)
    #fetching splits that occured for that symbol from the cmSplits table
    cursor.execute('select symbol, split_date,old_FV,new_FV from cmSplits where symbol = %s;',(symbol,))
    #NOTE had to pass (symbol,) variable in the query as a tuple with a second missing element ', '
    #this is just sql syntax when writting a query on the cursor
    splits = cursor.fetchall() #fetch all from the sql result of our cursor execution


    #for each symbol also fetch complete historical price data
    cursor.execute('select symbol,timestamp,close from temp_cmstaging where symbol = %s;', (symbol,))
    prices=cursor.fetchall()


    #now we have a list of splits and all the un-adjusted prices for each symbol
    #go through the prices and if the prices are from a date before the split date
    #the adjust the price by scaling it by the ratio of newFV : oldFV

    for price in prices:
        price = list(price)
        for split in splits:
            #check date of split against current price date
            if split[1] >= price[1]:
                #adjusting older prices to the equivalent post split price
                price[2] = price[2]*(split[3]/split[2])
        adjusted_prices_all.append(price)

print('\n Created adjusted prices list \n')
#ONCE WE ARE DONE COMPUTING ADJUSTED PRICES WE NEED TO PUT THEM BACK INTO THE DATABASE
# create a new table for the tickers and their adjusted closing prices
#we will retroactively  replace the tickers which had a split with this adjusted prices all

cursor.execute('create table cm_adjusted_price (symbol varchar(256),timestamp date, close float);')
connection.commit()
#adding an index to this table so symbol and date will be unique (no duplicates rows)
cursor.execute('alter table cm_adjusted_price add unique index id (symbol, timestamp)')
connection.commit()
#import the required fields from the cleaned cmstaging table

print('\n finished \n')

print('\n inserting temp cmstaging data into adjusted \n')

cursor.execute('insert ignore into cm_adjusted_price select symbol,timestamp,close from temp_cmstaging;')
connection.commit()

print('\n finished \n')

#need to adjust these prices in this table using our python list
#go through row by row

print('\n replacing with adjusted close \n')


for price in adjusted_prices_all:
    price_row_tuple = (price[0], price[1], price[2])
    #now REPLACE the unadjusted prices in the table
    cursor.execute('replace into cm_adjusted_price values(%s,%s,%s)',price_row_tuple)
    connection.commit()

print('\n finished \n')