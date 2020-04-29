from YahoohistoricaldataURLtest import BuildYahooURL
from DownloadURL import downloadURL



#date in YYYY-MM-DD
# daily = 1d
# weekly = 1wk
# monthly = 1mo



if __name__ == "__main__":
    ticker = "^GSPC"
    startdate = "2019-01-01"
    enddate = "2019-07-01"
    freq = "1mo"
    yahooURL = BuildYahooURL(ticker, startdate, enddate, freq)
    print(yahooURL)

    LocalFilePath = "/Users/emmet/pytest/gspc2019test.csv"

    downloadURL(LocalFilePath, yahooURL)
