
from urllib.parse import urlparse
from urllib.parse import urljoin
from datetime import datetime  # importing the class

def BuildYahooURL (symbol,startdate,enddate,freq):

    # symbol, startdate, enddate, freq = input("Enter in one line seperated using commas\n..."
    #                                          "The tikcer symbol, the start & end dates in form YYYY-MM-DD\n..."
    #                                          "and the frequency (1d, 1wk, 1mo)\n").split(',')
    #
    # code to identify URL
    OGURL = "https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1"

    # https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1553005033&period2=1584627433&interval=1d&events=history
    url_parts = list(urlparse(OGURL))


    #from this we see that the base URL is url_parts[0]+{1}
    #path has form /v7/finance/download/SYMBOL
    #where symbol is our ticker
    #and arguments {4} of form
    #period1=1553005033&period2=1584627433&interval=1d&events=history

    #period1 is start date and P2 is end date in terms of UNX time
    #interval 1d ia daily, 1mo is monthly, 1wk is weekly

    #yahoo for indecies will need to replace symbol's carats (^) with %5E

    #symbol = input("Enter historical data SYmbol")


    symbol = symbol.replace("^","%5E") #converting to how yahoo puts in URL
    startdate = str(int(datetime.strptime(startdate, "%Y-%m-%d").timestamp())) #converting to UNX
    enddate = str(int(datetime.strptime(enddate, "%Y-%m-%d").timestamp()))

    baseURL = str(url_parts[0]) + '://'+ str(url_parts[1])+'/v7/finance/download/'
    print(baseURL)

    newurl = baseURL + symbol + '?period1=' + startdate +'&period2=' + enddate + '&interval'+ freq + '&events=history'
    return newurl






#CAN USE URLLIB top construct urls