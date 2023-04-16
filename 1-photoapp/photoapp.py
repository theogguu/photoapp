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
    
<<<<<<< HEAD
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
        
    
    
=======
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
>>>>>>> 32497205e46f3453d9f5a8b971e47f8c493a1550
    query_results = cursor.fetchall()
    print(query_results)

except Exception as e:
    print("Database connection failed due to {}".format(e))
    sys.exit(-1)
    
cursor.close()
dbconn.close()
print()
print('done')
