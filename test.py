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



date_today = datetime.now()
days = [
    '2017-01-30 05:14:27', '2017-01-30 06:17:16',
    '2017-01-30 07:38:02', '2017-01-30 08:03:08',
    '2017-01-30 09:38:12', '2017-01-30 10:22:01',
    '2017-01-30 11:38:12', '2017-01-30 12:22:01',
    '2017-01-30 13:38:12', '2017-01-30 14:22:01',
    '2017-01-30 15:38:12', '2017-01-30 16:22:01'
    # '2017-01-30 06:22:01'
]

np.random.seed(seed=1111)
data = [2, 2, 2, 2, 2, 3, 2, 2, 5, 3, 2, 2]

df = pd.DataFrame({'datetime': days, 'value': data})
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.set_index('datetime')

# print(df)
#
# resampled = df.resample('H').sum()
#
# print(resampled)
#
# rolling = resampled.rolling(4).mean()
# resampled['rolling'] = rolling
# resampled['diff'] = (resampled['value'] - resampled['rolling']) / resampled['rolling']
# resampled['surge'] = resampled['diff'] > 0.25
#
# print(resampled)

surge = get_surges(df)
print(surge)