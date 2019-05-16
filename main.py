import psycopg2
import sys, os
import numpy as np
import pandas as pd
from config.creds import creds
from tools.analysis import get_surges, filter_per_value
from datetime import datetime, timedelta

# 1) Set up database connection
conn_string = "host=" + creds['PGHOST'] + " port=" + "5432" + " dbname=" \
              + creds['PGDATABASE'] + " user=" + creds['PGUSER'] \
              + " password=" + creds['PGPASSWORD']
conn = psycopg2.connect(conn_string)
print("Connected!")

# 2) Make geographic query

sql = 'select id, pickup_time, fare, EXTRACT(DOW FROM pickup_time), pg_catalog.time(pickup_time) AS time from trips_trip where fare>80 and EXTRACT(DOW FROM pickup_time)=1;'
df = pd.read_sql(sql, conn)

print("1 ============")
print(df.head())

print("2 ============")

df = df[['pickup_time', 'fare']]
print(df.head())

print("3 ============")

df.rename(columns={'pickup_time': 'datetime', 'fare': 'value'}, inplace=True)
print(df.head())

# Get surge estimate
# days = [
#     '2017-01-30 05:14:27', '2017-01-30 06:17:16',
#     '2017-01-30 07:38:02', '2017-01-30 08:03:08',
#     '2017-01-30 09:38:12', '2017-01-30 10:22:01',
#     '2017-01-30 11:38:12', '2017-01-30 12:22:01',
#     '2017-01-30 13:38:12', '2017-01-30 14:22:01',
#     '2017-01-30 15:38:12', '2017-01-30 16:22:01'
#     # '2017-01-30 06:22:01'
# ]
#
# np.random.seed(seed=1111)
# data = [2, 2, 2, 2, 2, 3, 2, 2, 5, 3, 2, 2]
#
# df = pd.DataFrame({'datetime': days, 'value': data})
# df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
# df = df.set_index('datetime')
#
# print("3 ============")
# print(df.head())
#
# print("4 ============")
# surge = get_surges(df, resample_period='15M')
# print(surge)
#
# print("5 ============")
# output = filter_per_value(surge, 'surge', True)
# print(output)