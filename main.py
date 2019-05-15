import psycopg2
import sys, os
import numpy as np
import pandas as pd
from config.creds import creds

print(creds)

# Set up a connection to the postgres server.
# conn_string = "host=" + creds['PGHOST'] + " port=" + "5432" + " dbname=" \
#               + creds['PGDATABASE'] + " user=" + creds['PGUSER'] \
#               + " password=" + creds['PGPASSWORD']
# conn = psycopg2.connect(conn_string)
# print("Connected!")
#
#
# sql = 'select * from trips_trip'
# df = pd.read_sql(sql, conn)
#
# print(df.head())