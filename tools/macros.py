import pandas as pd


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
