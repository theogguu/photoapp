import pymysql
import sys
import uuid
# print(uuid.uuid4())

ENDPOINT = "mysql-cs310.cs4bnd9lvwts.us-east-1.rds.amazonaws.com"
USER = "admin"
PASSWORD = "1haveasecretpassword"
DBNAME = "sys" # sys is the default database #suggested "photoapp"

print('starting...')
try:
    dbconn = pymysql.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, database=DBNAME, port=3306)
    cursor = dbconn.cursor()
    cursor.execute("SELECT now()")
    
    create_tables = """
    CREATE DATABASE photoapp;
    USE photoapp;

    DROP TABLE IF EXISTS assets;
    DROP TABLE IF EXISTS users;

    CREATE TABLE users
    (
        userid       int not null AUTO_INCREMENT,
        email        varchar(128) not null,
        lastname     varchar(64) not null,
        firstname    varchar(64) not null,
        bucketfolder varchar(48) not null,  -- random, unique name (UUID)
        PRIMARY KEY (userid),
        UNIQUE      (email),
        UNIQUE      (bucketfolder)
    );

    ALTER TABLE users AUTO_INCREMENT = 80001;  -- starting value

    CREATE TABLE assets
    (
        assetid      int not null AUTO_INCREMENT,
        userid       int not null,
        assetname    varchar(128) not null,  -- original name from user
        bucketkey    varchar(128) not null,  -- random, unique name in bucket
        PRIMARY KEY (assetid),
        FOREIGN KEY (userid) REFERENCES users(userid),
        UNIQUE      (bucketkey)
    );

    ALTER TABLE assets AUTO_INCREMENT = 1001;  -- starting value
    """
    cursor.executescript(create_tables)
    cursor.execute("SELECT * FROM users")
    query_results = cursor.fetchall()
    print(query_results)

except Exception as e:
    print("Database connection failed due to {}".format(e))
    sys.exit(-1)
    
cursor.close()
dbconn.close()
print()
print('done')
