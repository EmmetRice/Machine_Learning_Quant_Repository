# now that we have all our data from the NSE,
# we can put it into a database so that its queriable

#we've already created tables for each type of file in a MySQL database
#we'll need to install and use a MySQL connector

#in order to connect python to msql we need to mysql connector module
#this will connect to the mysql database and will give us a CURSOR to apply queries to our database

#download in anaconda terminal using > conda install -c anaconda mysql-connector-python

import mysql.connector
import csv

#now open mysql connection

#it is good practice to first check if established a connection to the database, using if statements


config = {
    'user': 'root',
    'password' : '2112',
    'host' : '127.0.0.1', #get this from the home on mysql
    'database' : 'nse'
}

connection = mysql.connector.connect(**config) #pass all dict parameters in config

#cursors are what execte queries
cursor = connection.cursor()



#File_Name1 = 'B:/Work/StudyFolk/Quant ML Trading course/project_files_downloaded_NSE/unzipped/cm01APR2008bhav.csv/cm01APR2008bhav.csv'
#File_Name2 = 'B:/Work/StudyFolk/Quant ML Trading course/project_files_downloaded_NSE/unzipped/cm02SEP2014bhav.csv/cm02SEP2014bhav.csv'

#1 has 2 columns and is missing totaltrades and isin
#2 has 14 columns

def Num_of_File_Columns (File_Name):
    import csv

    d = ','

    #File_Name1 = 'B:/Work/StudyFolk/Quant ML Trading course/project_files_downloaded_NSE/unzipped/cm01APR2008bhav.csv/cm01APR2008bhav.csv'
    with open(File_Name, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=d)
        #return how many columns
        return (len(next(reader)))



def insertRows (path,fileName, cursor):


    '''function to use a given cursor and a filename
     load and insert all data in the file into the mysql table in our database'''


    delimiter = ','
    #delimiter is comma as we loking at csv files

    #delimiter = r','
    #the 'r' before the quote string ensures that if there are any
    # special meaning to the characters which are being used inside the quotes
    # that they will be ignored

    dateString = '%d-%b-%Y'
    #this is the format of the dates in the NSE files, and this is used to convert
    #strings to dates. as in the csv they are saved as strings
    # This format is for dates like 02-JAN-2006
    #this is the format we want STR_TO_DATE(time, format) in mySQL to also use

    #see https://dev.mysql.com/doc/refman/8.0/en/load-data.html#load-data-field-line-handling
    #for input processing in sql

    #load data: https://docs.memsql.com/v6.8/reference/sql-reference/data-manipulation-language-dml/load-data/
    # http://www.mathcs.emory.edu/~cheung/Courses/377/Oracle/SQL-loader/FAQ.html

    query_CM_short = ('Load data infile %s into table cmstaging fields terminated by %s ignore 1 lines'
                       '(symbol,series,open,high,low,close,last,prevclose,tottrdqty,tottrdval,@timestamp)'
                       'SET timestamp = STR_TO_DATE(@timestamp, %s);')

    query_CM_long = ('Load data infile %s into table cmstaging fields terminated by %s ignore 1 lines'
                      '(symbol,series,open,high,low,close,last,prevclose,tottrdqty,tottrdval,@timestamp,totaltrades,isin)'
                      'SET timestamp = STR_TO_DATE(@timestamp, %s);')


    query_FO = ('Load data infile %s into table fostaging fields terminated by %s ignore 1 lines'
                       '(instrument,symbol,@expiry_dt,strike_pr,option_type,open,high,low,close,settle_pr,contracts,'
                       'val_inlakh,open_int,chg_in_oi,@timestamp)'
                       'SET timestamp = STR_TO_DATE(@timestamp, %s), expiry_dt = STR_TO_DATE(@expiry_dt, %s);')

    # cursor to execute the following statement in MySQL, so it uses MySql Syntax

    if fileName.startswith('cm'):
        try:

            file_to_open = os.path.join(path, fileName)

            with open(file_to_open, 'r'):

                ncol = Num_of_File_Columns (file_to_open)

                if ncol == 12:

                    cursor.execute(query_CM_short, (path+fileName, delimiter, dateString))
                    print('Loaded file {} into database'.format(fileName))
                    connection.commit()
                else:
                    cursor.execute(query_CM_long, (path + fileName, delimiter, dateString))
                    print('Loaded file {} into database'.format(fileName))
                    connection.commit()

        except Exception as e:
            print("MySQL Exception:", e)




    if fileName.startswith('fo'):
        try:
        # cursor to execute the following statement in MySQL, so it uses MySql Syntax
            cursor.execute(query_FO, (path+fileName, delimiter, dateString, dateString))
            print('Loaded file {} into database'.format(fileName))

            connection.commit()

        except Exception as e:
            print("MySQL Exception:", e)
    # %S is variables input the following variables, which are fileName, delimiter, datestring
    # the second string are the field / column names which have to be read
    #  fields terminated %S
    #          to terminate input into that field based on our specified delimiter and move to next column
    # 1gnore 1 lines as this is the header values of the csv file

    # tottrd = total traded
    # @timestamp as this is a timestamp value not a string
    # this @ means we are temporarily putting the date into a variable called timestamp
    # the string data in the variable timestamp is then converted to a date using
    # the mySQL fn STR_TO_DATE()

#path where files are saved and to be extracted from
print('working')

local_extract_file_path = 'B:/Work/StudyFolk/Quant ML Trading course/project_files_downloaded_NSE/unzipped'




#NOW CALLING ABOVEW FUNCTIONS AND RUNNING OVER ALL FILES IN A FOLDER





print('working')
#use the misc operating systems module OS

import os

#to loop over all files in the path

#saved files in individual folders not as just files in local file path directory

#os.listdir(local_extract_file_path) creates a list of all folders/files at that directory level
#but the files we need are inside these forlders so must loop over one directory level lower

for folder_name in os.listdir(local_extract_file_path):

    for file_name in os.listdir(local_extract_file_path + '/' + folder_name):

        if file_name.endswith('.csv'):
                insertRows(local_extract_file_path + '/' + folder_name + '/', file_name, cursor)


        #when ever you write to a database MUST commit to changes,
        #otherwise when cursor is closed all changes are gone

cursor.close()
connection.close()



#now that data is uploaded we need to CLEAN it before using it

#remove any duplicates
#adjust for any symbol changes
# adjust for corporate actions

#remove any duplicate rows
    #create a duplicate table
    #add a UNIQUE INMDEX CONSTRAINT on that table
    #insert rows (ie the data) from the old table into new tables (any duplicates will be ignored)

#adjust for any symbol changes
    #ticker symbol changes, need to update the old history to new symbol
    # download the NSE log of symbol changes file
    #read file row by row and update

    #symbol CSV downloaded from
    #downloaded from https://www1.nseindia.com/corporates/content/securities_info.htm

