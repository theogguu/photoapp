#
# Main program for photoapp program using AWS S3 and RDS to
# implement a simple photo application for photo storage and
# viewing.
#
# Authors:
#   Steven Gu
#   Prof. Joe Hummel (initial template)
#   Northwestern University
#   Spring 2023
#

import datatier  # MySQL database access
import awsutil  # helper functions for AWS
import boto3  # Amazon AWS

import uuid
import pathlib
import logging
import sys
import os

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img


###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """
  print()
  print(">> Enter a command:")
  print("   0 => end")
  print("   1 => stats")
  print("   2 => users")
  print("   3 => assets")
  print("   4 => download")
  print("   5 => download and display")
  print("   6 => upload")
  print("   7 => add user")

  try:
    cmd = int(input())
  except:
    cmd = 10000 # invalid command
  return cmd


###################################################################
#
# 1 - stats
#
def stats(bucketname, bucket, endpoint, dbConn):
  """
  Prints out S3 and RDS info: bucket name, # of assets, RDS 
  endpoint, and # of users and assets in the database
  
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """
  #
  # bucket info:
  #
  print("S3 bucket name:", bucketname)

  assets = bucket.objects.all()
  print("S3 assets:", len(list(assets)))

  #
  # MySQL info:
  #
  print("RDS MySQL endpoint:", endpoint)

  sql_count_users = "select count(*) from users";
  sql_count_assets = "select count(*) from assets";

  row_users = datatier.retrieve_one_row(dbConn, sql_count_users)
  row_assets = datatier.retrieve_one_row(dbConn, sql_count_assets)
  if row_users is None or row_assets is None:
    print("Database operation failed...")
  elif row_users == () or row_assets == ():
    print("Unexpected query failure...")
  else:
    print("# of users: {}".format(row_users[0]))
    print("# of assets: {}".format(row_assets[0]))
    
#
# 2 - users
#
def users(dbConn):
  sql = "select * from users order by userid desc"
  rows = datatier.retrieve_all_rows(dbConn, sql)
  for entry in rows:
    print("User id: {}".format(entry[0]))
    print("\tEmail: {}".format(entry[1]))
    print("\tName: {} , {}".format(entry[3], entry[2]))
    print("\tFolder: {}".format(entry[4]))

#
# 3 - assets
#
def assets(dbConn):
  sql = "select * from assets order by assetid desc"
  rows = datatier.retrieve_all_rows(dbConn, sql)
  for entry in rows:
    print("Asset id: {}".format(entry[0]))
    print("\tUser id: {}".format(entry[1]))
    print("\tOriginal name: {}".format(entry[2]))
    print("\tKey name: {}".format(entry[3]))

#
# 4 - download
# download() returns the filename downloaded (for reusability).
#
def download(bucket, dbConn):
  input_id = input("Enter asset id>\n")
  bucketkey = "select bucketkey from assets where assetid = {}".format(input_id)
  assetname = "select assetname from assets where assetid = {}".format(input_id)
  
  bucketquery = datatier.retrieve_one_row(dbConn, bucketkey)
  #try perform action instead.
  
# unsuccessful assetid query
  if not bucketquery: 
    print("No such asset...")
    return
  
  # proceed with download
  else: 
    filename = datatier.retrieve_one_row(dbConn, assetname)[0]
    print(bucketquery[0])
    random_name = awsutil.download_file(bucket, bucketquery[0])
    
    # os.rename does not replace the file if it already exists.
    os.replace(random_name, filename) 
    print("Downloaded from S3 and saved as \' {} \'".format(filename))
    return filename # for reusability
    
#
# 5 - download and display 
#
def download_and_display(bucket, dbConn):
  filename = download(bucket, dbConn)
  if not filename:
    return
  
  image = img.imread(filename)
  plt.imshow(image)
  plt.show()

#
# 6 - upload
#
def upload(bucket, dbConn):
  # find file
  local_filename = input("Enter local filename>\n")
  if not os.path.exists(local_filename):
    print("Local file \' {} \' does not exist...".format(local_filename))
    return
  
  # find user bucket, and new asset id
  user_id = input("Enter user id>\n")
  user_bucket_sql = "select bucketfolder from users where userid = {}".format(user_id)
  max_asset_id_sql = "select max(assetid) from assets"
  user_bucket = datatier.retrieve_one_row(dbConn, user_bucket_sql)
  max_asset_id = datatier.retrieve_one_row(dbConn, max_asset_id_sql)
  if not user_bucket:
    print("No such user...")
    return
  
  # the upload path for file
  dest = user_bucket[0] + "/" + str(uuid.uuid4()) + ".jpg" # bucket/key.jpg
  awsutil.upload_file(local_filename, bucket, dest)
  print("Uploaded and stored in S3 as ' {} '".format(dest))
  
  # upload to RDS
  upload_sql = """insert into assets
  (userid, assetname, bucketkey) 
  values (\'{}\', \'{}\', \'{}\')
  """.format(str(user_id), local_filename, dest) 
  datatier.perform_action(dbConn, upload_sql)
  print("Recorded in RDS under asset id {}".format(int(max_asset_id[0])+1))

#
# 7 - add_user
#
def add_user(dbConn):
  email = input("Enter user's email>\n")
  last_name = input("Enter user's last name>\n")
  first_name = input("Enter user's first name>\n")
  
  new_user_id_sql = "select max(userid) from users"
  insert_sql = """insert into users (email, lastname, firstname, bucketfolder)
  values ( \'{}\', \'{}\', \'{}\', \'{}\')
  """.format(email, last_name, first_name, str(uuid.uuid4()))
  
  max_id = datatier.retrieve_one_row(dbConn, new_user_id_sql)[0]
  datatier.perform_action(dbConn, insert_sql)
  print("Recorded in RDS under user id {}".format(str(max_id+1)))
#########################################################################
# main
#
print('** Welcome to PhotoApp **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'photoapp-config'
# 
print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-config),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print("**ERROR: config file '", config_file, "' does not exist, exiting")
  sys.exit(0)

#
# gain access to our S3 bucket:
#
s3_profile = 's3-read-write'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

boto3.setup_default_session(profile_name=s3_profile)

configur = ConfigParser()
configur.read(config_file)
bucketname = configur.get('s3', 'bucket_name')

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketname)

#
# now let's connect to our RDS MySQL server:
#
endpoint = configur.get('rds', 'endpoint')
portnum = int(configur.get('rds', 'port_number'))
username = configur.get('rds', 'user_name')
pwd = configur.get('rds', 'user_pwd')
dbname = configur.get('rds', 'db_name')

dbConn = datatier.get_dbConn(endpoint, portnum, username, pwd, dbname)

if dbConn is None:
  print('**ERROR: unable to connect to database, exiting')
  sys.exit(0)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  match cmd:
    case 1:
      stats(bucketname, bucket, endpoint, dbConn)
    case 2:
      users(dbConn)
    case 3:
      assets(dbConn)
    case 4:
      download(bucket, dbConn)
    case 5:
      download_and_display(bucket, dbConn)
    case 6:
      upload(bucket, dbConn)
    case 7:
      add_user(dbConn)
    case default:
      print("** Unknown command, try again...")
      
  cmd = prompt()

#
# done
#
print()
print('** done **')
