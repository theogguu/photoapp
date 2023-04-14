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
    query_results = cursor.fetchall()
    print(query_results)

except Exception as e:
    print("Database connection failed due to {}".format(e))
    sys.exit(-1)
    
cursor.close()
dbconn.close()
print()
print('done')
