# code to parse ticker from yahoo finance

#do not need to class this as only for parsing

#de-construct the URl by first using the urllib.parse.urlparse
#contruct using urllib.parse.unparse

class YahooURL:

    '''Contructs Yahoo URL for Downloading Historical data. inputs: (ticker, start_date, end_date,frequency)
    dates must be in dd-mm-yyyy format, and frequecy input as "daily, weekly, or monthly'''

    url_base =\
        'https://query1.finance.yahoo.com/v7/finance/download' \
        '/%5EGSPC?period1=1514764800&period2=1546300800&interval=1d&events=history'

    # MAKING INSTANCE
    # see the OOP code
    def __init__(self, ticker, start_date, end_date,frequency='daily',
                 path = 'B:\Work\StudyFolk\Quant ML Trading course\Download_test'):

                # this is the instance constructor, where self is the instance name we make and the variables needed

           frequency = frequency.lower()  # convert all string chars to lower case



           if frequency == 'daily':
               self.freq = '1d'
           elif frequency == 'monthly':
               self.freq = '1mo'
           elif frequency == 'weekly':
               self.freq = '1wk'

           else:
                raise ValueError('frequency input must be: Daily, Weekly, or Monthly')


           self.start_date = start_date
           self.end_date = end_date
           self.ticker = ticker
           self.path = path

           #self.new_url = None #intialising new url as empty


    #class methods are known as alternative constructors, ie run the class in a different way
    @classmethod
    def set_base_url(cls, base_url_to_use):
        '''manually change the base url from:
        https://query1.finance.yahoo.com/v7/finance/download
        /%5EGSPC?period1=1514764800&period2=1546300800&interval=1d&events=history'''
        cls.url_base = str(base_url_to_use)




    @staticmethod
    def unxdate(input_date):
        '''method to convert dqte dd-mm-yyyy to UNX date'''
        from datetime import datetime
        UNX_date = str(int(datetime.strptime(str(input_date), "%d-%m-%Y").timestamp()))
        return UNX_date



    def fn_file_path_name (self):

        '''Create file path name based on inputs for class'''

        #path = 'B:\Work\StudyFolk\Quant ML Trading course\Download_test'

        local_file_path = self.path +'\{}_start_{}_end_{}_freq_{}.csv'.\
                format(self.ticker, self.start_date, self.end_date, self.freq)

        local_file_path_extract = self.path +'\{}_start_{}_end_{}_freq_{}.csv'. \
                format(self.ticker, self.start_date, self.end_date, self.freq)

        # above is a good local file path which will automatically name the file path
        #can always write a class method to change this
        return {'save_path' : local_file_path, 'extract_path' : local_file_path_extract}






    def build_yahoo_URL (self): #input likely to be

        #see https://studyfolk.com/play/145454 for how to do if statement wether future of not etc

        ''''Build new url based on class inputs and the base url'''
        from urllib import parse

        #as yahoo url uses UNX time for dates need to convert them, using static method

        UNX_start_date =  YahooURL.unxdate(self.start_date)
        UNX_end_date = YahooURL.unxdate(self.end_date)



        parsed_url = list(parse.urlparse(self.url_base,
            scheme='', allow_fragments=True))
        # parse the Url and save it as a list

        # partsed url in form:
        # scheme, netloc, paths, params, query
        # 'https', 'query1.finance.yahoo.com', '/v7/finance/download/%5EGSPC'
        # can see from comment that the path /v7/finance/download/%5EGSPC has the defualt ticker %5EGSP in it
        # so need to remove it for generality

        #UPDATING PATH WITH NEW PATH

        parsed_url[2] = '/v7/finance/download/'+ self.ticker.replace("^","%5E") #converting to how yahoo puts in URL


        # extract the query string

        qs = parsed_url[4]      #4 as query is the 5th element

        qs = parse.parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace')
        # this creates a dictionary of each variable in the query string
        #this puts ['value'] characters around the value
         #the opposite parse.urlencode(qs) does not put it back correctly due to these added characters

        #removing extra characters
        for value in qs:
            values = str(qs[value])
            values = values.replace('[', '').replace(']', '').replace('\'', '')
            qs[value] = values


        #Update query string with the desired values


        # this is the hard coded variants
        # qs['period1'] = self.start_date
        # qs['period2'] = self.end_date
        # qs['interval'] = self.freq


        #wiull tell us the keys names, but this is NOT dynamic and code from here out is hard coded
        qskeys = list(qs.keys())

        #as long as yahoo order of url query values is the same this should still work
        qs[str(qskeys[0])] = UNX_start_date
        qs[str(qskeys[1])] = UNX_end_date
        qs[str(qskeys[2])] = self.freq


        newqs = parse.urlencode(qs)


        #updating the queary string parse with our updated newqs
        parsed_url[4] = newqs
        #updating


        return str(parse.urlunparse(parsed_url))




    def downloadURL (self):

        local_file_path = YahooURL.fn_file_path_name(self)
        local_file_path = local_file_path['save_path']

        # download URL and store to Local path as a general binary file

        # python library urllib is used

        # def downloadURL (filepath, URL):

        '''Function to download new_url to specified a filepath'''

        from urllib import request #or import urllib.request
        import urllib.error

        #function from urllib to download file

        newurl = YahooURL.build_yahoo_URL(self)

        # we pass in header attribute in the webrequest to make site think we are a manual user not a scraping bot

        # need to get the user agent and otehr values. Set up header dict

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/80.0.3987.149 Safari/537.36 OPR/67.0.3575.115',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image'
                            '/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                  'Host': 'duckduckgo.com'}
        # '' : '',
        # '' : '',
        # '' : '',
        # '' : '',
        # '' : '',
        # '' : '',
        # '' : '',}


        webRequest = urllib.request.Request(newurl, headers= header)
        #webRequest = urllib.request.Request(YahooURL.build_yahoo_URL(self))



        #need to make sure our code doesnt run if URL is broken so we use TRY and EXCEPT
        #as the defualy new_url is None then the code shouldnt work if new_url is not updated

        try:
            page=urllib.request.urlopen(webRequest) #downloads the URL

            #use page.read to read the contents

            contents = page.read()     #the .read() executes the read function from the "page" program

            #the below with condition ensures only runs when the file correctly opens
            #its another fail safe
            with open(local_file_path,"wb") as output: #thios with block closes file even if not explicitly said

                output.write(bytearray(contents))
                #wb is the mode of opening ie write binary contents
                #this uses the write function in the output program and makes the contents output as a local filepath
                # as byte array so we are agnostic to what file type we are downloading, eg zip or csv etc

        #now to write the except block, incase errors
        except urllib.error.URLError as e:  #error now classified as e variable
            #printing error
            print(e.reason)




    def unzip(self):

        local_paths = YahooURL.fn_file_path_name(self)
        local_save_path = local_paths['save+path']
        local_extract_path = local_paths['extract_path']


        #first check if file to be unzipped even exists
        #we import the misc operating system interface module (os)

        import os

        if os.path.exists(local_save_path):
            list_of_files =[]
            #the zip file might contain more than 1 file, so we maintain a list of files extracted

            with open(local_save_path, 'rb') as fhandler: #rb as read binary as zip files are binary
                import zipfile
                zip_file_handler = zipfile.ZipFile(fhandler)
                #this handler from the zipfile library can access and do things to the files within the zip file

                for name in zip_file_handler.namelist():
                    #for loop to iterate over each file within the zip file
                    zip_file_handler.extract(name, local_extract_path) #extracting files as reading them
                    list_of_files.append(local_extract_path+name)

                            #appending to list of files
            print ('Extracted ' + str(len(list_of_files)) + 'from ' + local_save_path)










    #code to make this class an iterator - can be done better using generator functions see python syntax notes
    # MAKING it an ITERATOR

    # def __iter__(self):
    #     return (self)  # just returning the object itself with no changes
    #
    # # as all iterators have an __iter__ method, which will return an iterator
    #
    # # all iterators need a dunder next method
    #
    # def __next__(self):  # so it will remeber its state
    #
    #     # MUST put a fail safe that will stop if runs out of values
    #     if self.value >= self.end:
    #         raise StopIteration
    #
    #     currentvalue = self.value
    #     self.value += 1  # increasing in a step of 1
    #     return currentvalue
