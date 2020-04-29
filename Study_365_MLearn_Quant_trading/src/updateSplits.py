#UPDATE DB TABLE FOR CORPRORATE ACTIONS _ STOCK SPLITS

#anomalies in stock prices which are caused by corproate actions which are not diue to market actions
#ie jumps which arte not due to the investment value changing
#see text file

#stock split data is not as easy to find as historical price data
#eg site: moneycontrol.com for NSE india stock market - given in a HTML file

#need 3 data points for adjusting previous data for stock splits
    #1. old facevalue #2 new facevalue #3. date occured
    #ration of old Fv : New FV gives us the adjustment multiplier needed

#NOTE yahoo financal database already adjusts for corproate actions historical



#as we are using NSE data, the HTML file from moneycontrol.com has already been downloaded

#we'll use 'BeautifulSoup' python module to parse the html file and the links to company name to get the NSE ticker symbol
#for that company for each stock




split_data = 'file:///B:/Work/StudyFolk/Quant%20ML%20Trading%20course/Quant%20trading/Splits.html'

from bs4 import BeautifulSoup
#BS is a python library we can use to parse HTML
#see bsoup documentation dir(bs4)
from urllib import request
import urllib.error

page_contents=urllib.request.urlopen(split_data).read()
soup = BeautifulSoup(page_contents, 'html.parser')

#BS find text in html between tokens

#here our data is in the form of cells, and cell is contained between the token 'td'

cells = soup.findAll('td')

print(int(len(cells)/4))

# all the HTML cells in one list, each cell conatins company, oldFV,newFV,splitdate
#all these rows are concatenated together in the list
#so every 4th element is a new row, ie a new companies data


def getSymbol(web_url):
    '''given a link from moneycontrol.com, will fetch the NSE ticker name for company'''

    try:
        page_contents = urllib.request.urlopen(web_url).read()
        soup = BeautifulSoup(page_contents, 'html.parser')
        # x = soup.find_all('ctag', {'class': 'mob-hide'}) \ #choose all data within this HTML class (see inspect element)
        #         [0].text.split('|') \ #select first element and split into list
        #         [1].split(':') \ #select 2nd element of list and split again
        #         [1] #select second element
        return soup.find_all('ctag', {'class': 'mob-hide'})\
                [0].text.split('|')\
                [1].split(':')[1]

        #had to update class due to changing moneycontrol.com html code, old one below

        #return soup.findALL('div',{'class':'FL gry10'})[0].text.split('｜')[1].split(':')[1]
                                                        #first element with this div class in HTML token
                                                                            #second symbol for NSE
                                                                                        #symbol is after NSE:
        #this is where the symbol is contained in moneycontrol.com and then get the NSE symbol from column 2

        #on moneycontrol.com the NSE ticker name when 'inspect element' on the page shows us the HTML tokeen with the code
        #AND HIGHLIGHTS 'fl GRY10' as where its stored
        #the elements in the text list are "BSE: 532521 ｜ NSE: PALREDTECH .....etc"
    except urllib.error.URLError as e:  # error now classified as e variable
        # printing error
        print(e.reason)

#create a list of lists
#lists contain: company name, old fairvalue, new fairvalue, split date, NSE ticker symbol

comapany_row_data = []

for i in range(int(len(cells)/4)):
    #divided by 4 as every 4th element is a new company data (blocks of 4)
    if i==0:
        #skip over file header row
        #course did this with an if statement, doubt this is the best way
        #probably restrict the i range statement or use a next statement instead
        continue
    else:
        current_company_row =[] #list to hold current row company data
        try:
            for j in range(4): #seperate information from each company row
                current_company_row.append(cells[4 * i + j].text)
            #we have the first 4 elements of our row, name, oldfv,newfv,splitdate
            #but still need tickersymbol
            #call our parsing function, call the company name (every 4th index) which is also a  hyperlink
            symbol = getSymbol(cells[4*i].a['href']).strip() #remove whitespace around symbol
            #looking for the href token which refers to url
            #check if return is blank (ie company NOT on the NSE so skip it)
            if symbol == '':
                continue
            current_company_row.append(symbol)
            #then add the current comapny data as a list to the greater list
            comapany_row_data.append(current_company_row)
        except:
            continue #error might occur becuase money control page down or parsed, so we skip it

        print (current_company_row)


#now have a list of splits
#need to iterate through them and compute the adjusted prices

#but first lets put this splits data into a table in our data base

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

#create table to hold split data

cursor.execute('create table cmSplits'
               '(company varchar(256), old_FV float, new_FV float, split_date date, symbol varchar(256));')
connection.commit()

from datetime import datetime
for company_row in comapany_row_data:
    #create tuple to hold company data
    company_row_tuple = (company_row[0], float(company_row[1]), float(company_row[2])
                         ,datetime.strptime(company_row[3], '%d-%m-%Y'), company_row[4])
                        #name, old fv, new fv, split date, ticker symbol
    cursor.execute('insert into cmSplits values(%s,%s,%s,%s,%s)', company_row_tuple)
    connection.commit()

#all the split data is now stored in the data base NSE.
#now read this database table symbol by symbol and compute the adjusted prices for the temp_cmsstaging

#running alot of queries so tweaking sql server so not limited and put to sleep

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
    splits = list(cursor.fetchall) #fetch all from the sql result of our cursor execution

    #for each symbol also fetch complete historical price data
    cursor.execute('select symbol,timestamp,close from temp_cmstaging where symbol = %s;', (symbol,))
    prices=list(cursor.fetchall)

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

#ONCE WE ARE DONE COMPUTING ADJUSTED PRICES WE NEED TO PUT THEM BACK INTO THE DATABASE
# create a new table for the tickers and their adjusted closing prices
#we will retroactively  replace the tickers which had a split with this adjusted prices all

cursor.execute('create table cm_adjusted_price (symbol varchar(256),timestamp date, close float);')
connection.commit()
#adding an index to this table so symbol and date will be unique (no duplicates rows)
cursor.execute('alter table cm_adjusted_price add unique index id (symbol, timestamp)')
connection.commit()
#import the required fields from the cleaned cmstaging table

cursor.execute('insert ignore into cm_adjusted_price (select symbol, timestamp, close from temp_cmstaging;')
connection.commit()

#need to adjust these prices in this table using our python list
#go through row by row

for price in adjusted_prices_all:
    price_row_tuple = (price[0], price[1], price[2])
    #now REPLACE the unadjusted prices in the table
    cursor.execute('replace into cm_adjusted_price values(%s,%s,%s)',price_row_tuple)
    connection.commit()



