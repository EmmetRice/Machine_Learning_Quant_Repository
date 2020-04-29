import urllib
from urllib.parse import urlparse

# code to identify URL

baseurl = input("input base URL")

# https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1553005033&period2=1584627433&interval=1d&events=history

url_parts = list(urlparse(baseurl))
print(url_parts)
print(url_parts[0]) #eg http
print(url_parts[1])
print(url_parts[2])
print(url_parts[3])
print(url_parts[4])