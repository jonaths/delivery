import psycopg2
import sys, os
import numpy as np
import pandas as pd
from config.creds import creds
from tools.analysis import get_surges, filter_per_value
from datetime import datetime, timedelta
from tools.macros import process


# INPUTS -----------------------------------------------------------------
weekday = 1
location = 'LA'  # still not using this info

# 1) Set up database connection ------------------------------------------
conn_string = "host=" + creds['PGHOST'] + " port=" + "5432" + " dbname=" \
              + creds['PGDATABASE'] + " user=" + creds['PGUSER'] \
              + " password=" + creds['PGPASSWORD']

conn = psycopg2.connect(conn_string)
print("Connected!")

# 2) Make geographic query -----------------------------------------------


with open('locations/losangeles.json') as json_file:
    json_location = json_file.read()

polygon_str = '\'' + str(json_location) + '\''

# Still have to remove fare where and include location information
# sql = 'select ' \
#         'id, ' \
#         'pickup_time, ' \
#         'pickup_location, ' \
#         'fare, ' \
#         'EXTRACT(DOW FROM pickup_time) ' \
#       'from trips_trip ' \
#       'where ' \
#         'fare > 20 and ' \
#         'ST_Contains(ST_GEOMFROMTEXT(' + '\'POLYGON((10 0, 11 1, 11 2, 10 0))\'' + '), pickup_location) and ' \
#         'EXTRACT(DOW FROM pickup_time)=' + str(weekday) + ';'

# polygon_str = '\'' + '{"type":"Point","coordinates":[-48.23456,20.12345]}' + '\''


# sql = 'select ' \
#         'id, ' \
#         'pickup_time, ' \
#         'pickup_location, ' \
#         'fare, ' \
#         'EXTRACT(DOW FROM pickup_time) ' \
#       'from trips_trip ' \
#       'where ' \
#         'fare > 20 and ' \
#         'ST_Contains(ST_GeomFromGeoJSON(' + polygon_str + '), ST_GeomFromText(\'POINT(-118.31451416015625 33.895497227123876)\', 0)) ' \
#          ';'

sql = 'select ' \
        'id, ' \
        'pickup_time, ' \
        'pickup_location, ' \
        'fare, ' \
        'EXTRACT(DOW FROM pickup_time) ' \
      'from trips_trip ' \
      'where ' \
        'fare > 20 and ' \
        'ST_Contains(ST_SetSRID(ST_GeomFromGeoJSON(' + polygon_str + '), 4326), pickup_location) and ' \
        'EXTRACT(DOW FROM pickup_time)=' + str(weekday) + ';'

print(sql)


df = pd.read_sql(sql, conn)
print(df.head())

# SELECT POINT_LOCATION
# FROM LOCATIONS_TABLE
# WHERE ST_Contains(ST_GEOMFROMTEXT('POLYGON((P1.X P1.Y, P2.X P2.Y, ...))'), LOCATIONS_TABLE.POINT_LOCATION);
