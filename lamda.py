import boto3
import codecs
import json
import re
import ast
import sys
import logging
import pymysql

#rds settings
rds_host  = "database-1.cfvieomujhur.us-east-1.rds.amazonaws.com"
name = "admin"
password = "admin2021"
db_name = "assignment"
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

print('Loading main function')
def lambda_handler(event, context):
       #part1
       message = event['Records'][0]['Sns']['Message']
       message_str = json.dumps(message)
       email_id = re.findall(r"[A-Za-z0-9._%+-]+"
                     r"@[A-Za-z0-9.-]+"
                     r"\.[A-Za-z]{2,4}"
                     r"\.[A-Za-z]{2,4}", message_str)
       phone_number = re.findall(r'\b\d{10}\b', message_str, flags=0)
       postal_code = re.findall(r'\b\d{5}\b', message_str, flags=0)
       # printing the list output
       if email_id:
         print(str(email_id) + " " + str(phone_number) + " " + str(postal_code))
       
       #part2
       """
       This function fetches content from MySQL RDS instance
       """

       item_count = 0
       QUERY_STATUS = "No Data"
       with conn.cursor() as cur:
          try:
             cur.execute("create table if not exists details ( phone int NOT NULL, email varchar(255) NOT NULL, postal int NOT NULL, created_ts datetime)")
             cur.execute('insert into details (phone, email, postal, created_ts) values(%s, %s, %s, %s)', (phone_number, email, postal_code, datetime.now()))
             conn.commit()
             print("Record inserted successfully into details table")
             QUERY_STATUS = "Successful"
          except mysql.connector.Error as error:
             print("Failed to insert into MySQL table {}".format(error))
             QUERY_STATUS = "Failed"
          print(QUERY_STATUS)
          cur.execute("SELECT  MAX(created_ts) FROM details")
          for QUERY_EXECUTION_TIMESTAMP in cur:
             print(QUERY_EXECUTION_TIMESTAMP)
          cur.execute("create table if not exists audit ( created_ts datetime NOT NULL, query_status varchar(255) NOT NULL)")
          cur.execute('insert into audit (created_ts, query_status) values(%s, %s)', (QUERY_EXECUTION_TIMESTAMP, QUERY_STATUS))
          conn.commit()