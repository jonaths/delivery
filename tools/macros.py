import pandas as pd
from datetime import timedelta
import sys


def process(df):
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    df['datetime_hour'] = df['datetime'].dt.hour
    df['datetime_minute'] = df['datetime'].dt.minute
    df['date_hours_minutes'] = pd.to_datetime(pd.Timestamp("today").strftime("%Y-%m-%d")) \
                               + pd.to_timedelta(df.datetime_hour, unit='h') \
                               + pd.to_timedelta(df.datetime_minute, unit='m')
    df = df.set_index('date_hours_minutes')
    df.drop(['datetime', 'datetime_hour', 'datetime_minute'], axis=1, inplace=True)
    return df


def to_text(df, hour, window_size, tz_name):
    converted = df.tz_localize('utc').tz_convert(tz_name)
    converted['h'] = converted.index.strftime('%H').astype('int32')

    next_surges = converted[converted['h'] >= int(hour)]

    if len(next_surges) > 0:
        next_surge = next_surges.iloc[0]
    else:
        print("===================================================")
        print('Bad luck! No surges today for you. ')
        print("===================================================")

        return

    print(next_surge.name)

    if window_size == '30T':
        end_datetime = next_surge.name + timedelta(minutes = 30)
        end_hour = str(end_datetime.hour) + ':' + str(end_datetime.minute)
    else:
        raise Exception('I do not understand this window size. ')

    if next_surge['h'] == hour:
        answer = 'Theres a surge right now and it will end at ' + str(end_hour) + '. Expect it to be ' + \
                 str(round(next_surge['diff'] * 100)) + '% better than the average. '
    else:
        answer = 'A surge starts at ' + str(next_surge['h']) + ' and it will end at ' + str(end_hour) + '. Expect it to be ' + \
                 str(round(next_surge['diff'] * 100)) + '% better than the average. '

    print("===================================================")
    print(answer)
    print("===================================================")

    return
