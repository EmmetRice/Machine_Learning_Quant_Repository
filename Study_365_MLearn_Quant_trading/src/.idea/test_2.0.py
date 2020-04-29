source = os.path.join('source_files', 'aws_bills', 'march-bill-original-2019.csv')
try:
    with open(source) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        insert_sql = """ INSERT INTO billing_info (InvoiceId, PayerAccountId, LinkedAccountId, RecordType, RecordId, ProductName, RateId, SubscriptionId, PricingPlanId, UsageType, Operation, AvailabilityZone, ReservedInstance, ItemDescription, UsageStartDate, UsageEndDate, UsageQuantity, BlendedRate, BlendedCost, UnBlendedRate, UnBlendedCost, ResourceId, Engagement, Name, Owner, Parent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        #for row in csv_reader:
        for row_idx, row in enumerate(csv_reader):
            try:
                cursor.execute(insert_sql,row)
                #cursor.executemany(insert_sql, 100)
                mydb.commit()
                print('row', row_idx, 'inserted with LinkedAccountId', row[2], 'at', datetime.now().isoformat())
            except Exception as e:
                print("MySQL Exception:", e)
        print("Done importing data.")








BRYAN

Consider building the query dynamically to ensure the number of placeholders matches your table and CSV file format. Then it's just a matter of ensuring your table and CSV file are correct, instead of checking that you typed enough ? placeholders in your code.

The following example assumes

CSV file contains column names in the first line
Connection is already built
File name is test.csv
Table name is MyTable
Python 3
...
with open ('test.csv', 'r') as f:
    reader = csv.reader(f)
    columns = next(reader)
    query = 'insert into MyTable({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    cursor = connection.cursor()
    for data in reader:
        cursor.execute(query, data)
    cursor.commit()

    I modified the code written above by Brian as follows since the one posted above
    wouldny work on the delimited files that I was trying to upload. The line row.pop() can also be ignored as it was necessary only for the set of files that I was trying to upload.


    def upload_table(path, filename, delim, cursor):
        """
        Function to upload flat file to sqlserver
        """
        tbl = filename.split('.')[0]
        cnt = 0
        with open(path + filename, 'r') as f:
            reader = csv.reader(f, delimiter=delim)
            for row in reader:
                row.pop()  # can be commented out
                row = ['NULL' if val == '' else val for val in row]
                row = [x.replace("'", "''") for x in row]
                out = "'" + "', '".join(str(item) for item in row) + "'"
                out = out.replace("'NULL'", 'NULL')
                query = "INSERT INTO " + tbl + " VALUES (" + out + ")"
                cursor.execute(query)
                cnt = cnt + 1
                if cnt % 10000 == 0:
                    cursor.commit()
            cursor.commit()
        print("Uploaded ")