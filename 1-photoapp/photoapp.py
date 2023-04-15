import pymysql
import sys
import uuid
# print(uuid.uuid4())

ENDPOINT = "photoapp-steven-gu.s3.us-east-2.amazonaws.com"
USER = "admin"
PASSWORD = "1haveasecretpassword"
DBNAME = "sys" # sys is the default database #suggested "photoapp"

print('starting...')
try:
    dbconn = pymysql.connect(ENDPOINT, USER, PASSWORD, DBNAME)
    cursor = dbconn.cursor()
    cursor.execute("SELECT now()")
    
    sql_create_database = """CREATE DATABASE photoapp
    --
    -- inserts one user and one asset into respective tables:
    --
    -- NOTE: userid in users table is automatically generated, so we
    -- don't provide a userid. Likewise for assetid in assets table.
    --

    USE photoapp;

    INSERT INTO 
    users(email, lastname, firstname, bucketfolder)
    values('pooja.sarkar@company.com', 'sarkar', 'pooja', 
            '6b0be043-1265-4c80-9719-fd8dbcda8fd4');

    INSERT INTO 
    assets(userid, assetname, bucketkey)
    values(80001,
            'A3-mac-2016.JPG',
            '6b0be043-1265-4c80-9719-fd8dbcda8fd4/af986381-55ac-4bf2-85b3-ff4a29047226.jpg');
    """
    
    cursor.execute(sql_create_database)
        
    
    
    query_results = cursor.fetchall()
    print(query_results)

except Exception as e:
    print("Database connection failed due to {}".format(e))
    sys.exit(-1)
    
cursor.close()
dbconn.close()
print()
print('done')
