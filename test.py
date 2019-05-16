import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tools.analysis import get_surges, filter_per_value
from tools.macros import process

# date_today = datetime.now()
#
# days = [
#     '2017-01-30 05:14:27-00', '2017-01-30 06:17:16-06',
#     '2017-01-30 07:38:02-05', '2017-01-30 08:03:08-06',
#     '2017-01-30 09:38:12-06', '2017-01-30 10:22:01-06',
#     '2017-01-30 11:38:12-06', '2017-01-30 12:22:01-06',
#     '2017-01-30 13:38:12-06', '2017-01-30 14:22:01-06',
#     '2017-01-29 15:38:12-00', '2017-01-30 16:22:01-02'
#     # '2017-01-30 06:22:01'
# ]

# days = [
#     '05:14:27-00', '06:17:16-06',
#     '07:38:02-05', '08:03:08-06',
#     '09:38:12-06', '10:22:01-06',
#     '11:38:12-06', '12:22:01-06',
#     '13:38:12-06', '14:22:01-06',
#     '15:38:12-00', '16:22:01-02'
#     # '2017-01-30 06:22:01'
# ]

# np.random.seed(seed=1111)
# data = [2, 2, 2, 2, 2, 3, 2, 2, 5, 3, 2, 2]
#
# df = pd.DataFrame({'datetime': days, 'value': data})
#
# df = process(df)
#
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

# surge = get_surges(df, resample_period='2H')
# print(surge)
#
# output = filter_per_value(surge, 'surge', True)
# print(output)