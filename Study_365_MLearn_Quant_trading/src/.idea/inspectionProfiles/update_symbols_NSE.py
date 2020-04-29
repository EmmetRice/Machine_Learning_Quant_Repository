# script that can read symbols that have changed
# using the symbols csv abd update our data in the prod tables

#set up DB connection

import mysql.connector
import csv

#now open mysql connection
def Update_NSE_symbols(db_table):
    import mysql.connector
    import csv

    '''retroactively changes old symbol names in NSE database table to new symbol name from csv file
    db_table should be a string'''

    config = {
        'user': 'root',
        'password' : '2112',
        'host' : '127.0.0.1', #get this from the home on mysql
        'database' : 'nse'
    }

    connection = mysql.connector.connect(**config) #pass all dict parameters in config

    #cursors are what execte queries
    cursor = connection.cursor()

    symbol_update_fileName = 'B:/Work/StudyFolk/Quant ML Trading course/symbolchange.csv'
    #need to read file row by row ato extract old and new symbol data

    LineNum = 0

    print('running...')
    with open (symbol_update_fileName, 'r') as csvfile:
        #r = read
        #get a csv handler from the csv module and use it to read the file
        LineReader = csv.reader(csvfile, delimiter = ',' , quotechar= "\"")
        #\ tells python to read as symbol the " symbol noty as syntax
        #quote char deals with strings and how they are specified, wether enclosed in quotes or not

        for row in LineReader:
            LineNum+=1 #add 1 each loop
            if LineNum ==1: #ie if header
                continue

            oldsymbol =row[1]
            newsymbol=row[2]

            print('ATEMPTING old sybol: {} \t new symbol: {}'.format(oldsymbol, newsymbol))

            try:
                #now write script which will run in mysql
                #cursor.execute ('update %s set symbol = %s where symbol = %s', (db_table,newsymbol, oldsymbol))
                cursor.execute('update temp_fostaging set symbol = %s where symbol = %s', (newsymbol, oldsymbol))
                print('DONE old sybol: {} \t new symbol: {}'.format(oldsymbol, newsymbol))

            except Exception as e:
                print("MySQL Exception:", e)
            # except:
            #     continue
            #     #if an error occurs just move on
            finally: #will always execute
                connection.commit()

    cursor.close()
    connection.close()
    print('finished')


Update_NSE_symbols('temp_cmstaging')

