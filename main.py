import psycopg2
import sys, os
import numpy as np
import pandas as pd
from config.creds import creds
from tools.analysis import get_surges, filter_per_value
from datetime import datetime, timedelta
from tools.macros import process, to_text

# INPUTS -----------------------------------------------------------------
weekday = 0  # assumes it is today
hour = 10  # what time is it now
tz_name = 'America/Los_Angeles'  # results localization
location_file = 'locations/losangeles.json'  # here are the area boundaries
min_fare = 10  # only consider fares larger than this
resample_period = '30T'  # how to aggregate data (30T means each 30 minutes)

# 1) Set up database connection ------------------------------------------
conn_string = "host=" + creds['PGHOST'] + " port=" + "5432" + " dbname=" \
              + creds['PGDATABASE'] + " user=" + creds['PGUSER'] \
              + " password=" + creds['PGPASSWORD']

conn = psycopg2.connect(conn_string)
print("Connected!")

# 2) Make geographic query -----------------------------------------------

with open(location_file) as json_file:
    json_location = json_file.read()

polygon_str = '\'' + str(json_location) + '\''

# postgres query
sql = 'select ' \
        'id, ' \
        'pickup_time, ' \
        'pickup_location, ' \
        'fare, ' \
        'EXTRACT(DOW FROM pickup_time) ' \
      'from trips_trip ' \
      'where ' \
        'fare > ' + str(min_fare) + ' and ' \
        'ST_Contains(ST_SetSRID(ST_GeomFromGeoJSON(' + polygon_str + '), 4326), pickup_location) and ' \
        'EXTRACT(DOW FROM pickup_time)=' + str(weekday) + ';'


df = pd.read_sql(sql, conn)

# 3) Setup columns -------------------------------------------------------

df = df[['pickup_time', 'fare']]

df.rename(columns={'pickup_time': 'datetime', 'fare': 'value'}, inplace=True)

# 4) Estimate surge ------------------------------------------------------
df = process(df)

# group data in 30 min bins, consider surge if current total fares are bigger than
# 60% of the current rolling window of 90 minutes. This can be adjusted.
surge = get_surges(df, resample_period=resample_period, rolling_window=3, surge_threshold=0.20)

output = filter_per_value(surge, 'surge', True)

print("Estimated surges today:")
# output includes 2 important columns
# date_hours_minutes: the time the surge starts. it ends one resample_period afterwards
# diff: the expected larger revenue
print(output)

to_text(output, hour, resample_period, tz_name)
