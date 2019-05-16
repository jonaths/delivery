import psycopg2
import sys, os
import numpy as np
import pandas as pd
from config.creds import creds
from tools.analysis import get_surges, filter_per_value
from datetime import datetime, timedelta
from tools.macros import process


# 1) Set up database connection ------------------------------------------
conn_string = "host=" + creds['PGHOST'] + " port=" + "5432" + " dbname=" \
              + creds['PGDATABASE'] + " user=" + creds['PGUSER'] \
              + " password=" + creds['PGPASSWORD']
conn = psycopg2.connect(conn_string)
print("Connected!")

# 2) Make geographic query -----------------------------------------------

sql = 'select id, pickup_time, fare, EXTRACT(DOW FROM pickup_time) ' \
      'from trips_trip ' \
      'where fare>20 and EXTRACT(DOW FROM pickup_time)=1;'
df = pd.read_sql(sql, conn)

# 3) Setup columns -------------------------------------------------------

df = df[['pickup_time', 'fare']]

df.rename(columns={'pickup_time': 'datetime', 'fare': 'value'}, inplace=True)

# 4) Estimate surge ------------------------------------------------------
df = process(df)

surge = get_surges(df, resample_period='30T', rolling_window=3, surge_threshold=0.60)

output = filter_per_value(surge, 'surge', True)

print("Estimated surges today:")
print(output)