import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_surges(df, resample_period='H', rolling_window=4, surge_threshold=0.25):
    """
    Calculates surges according to a moving average and threshold criteria
    :param df: the dataframe with a datetime and value column
    :param resample_period: if the surge is going to be calculated
        per hour (H) per 15 min (15M), etc.
    :param rolling_window: the larger the window the larger the value so that a
        surge is considered.
    :param surge_threshold: the lower the threshold more surges are calculated
    :return:
    """
    surge_df = df.resample(resample_period).sum()
    rolling = surge_df.rolling(rolling_window).mean()
    surge_df['rolling'] = rolling
    surge_df['diff'] = (surge_df['value'] - surge_df['rolling']) / surge_df['rolling']
    surge_df['surge'] = surge_df['diff'] > surge_threshold
    return surge_df


def filter_per_value(df, column_name, matching_value):
    """
    Returns rows from pandas dataframe which match a certain value
    :param df:
    :param column_name:
    :param matching_value:
    :return:
    """
    matches = df[column_name] == matching_value
    return df[matches]

# select id,pickup_time,fare,EXTRACT(DOW FROM pickup_time), pg_catalog.time(pickup_time) AS time
# from trips_trip
# where
# fare>80 and EXTRACT(DOW FROM pickup_time)=1;

# np.random.seed(seed=1111)
# data = [2, 2, 2, 2, 2, 3, 2, 2, 5, 3, 2, 2]

# df = pd.DataFrame({'datetime': days, 'value': data})
# df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
# df['datetime_hour'] = df['datetime'].dt.hour
# df['datetime_minute'] = df['datetime'].dt.minute
# df['date_hours_minutes'] = pd.to_datetime(pd.Timestamp("today")) + pd.to_timedelta(df.datetime_hour, unit='h')
# df = df.set_index('datetime')

# pd.to_datetime(pd.Timestamp("today").strftime("%Y-%m-%d"))