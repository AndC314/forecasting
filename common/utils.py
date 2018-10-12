import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

ALLOWED_TIME_COLUMN_TYPES = [pd.Timestamp, pd.DatetimeIndex,
                             datetime.datetime, datetime.date]


def is_datetime_like(x):
    return any(isinstance(x, col_type)
               for col_type in ALLOWED_TIME_COLUMN_TYPES)


def get_datetime_col(df, datetime_colname):
    """
    Helper function for extracting the datetime column as datetime type from
    a data frame.
    """
    if datetime_colname in df.index.names:
        datetime_col = df.index.get_level_values(datetime_colname)
    elif datetime_colname in df.columns:
        datetime_col = df[datetime_colname]
    else:
        raise Exception('Column or index {0} does not exist in the data '
                        'frame'.format(datetime_colname))

    if not is_datetime_like(datetime_col):
        try:
            datetime_col = pd.to_datetime(df[datetime_colname],
                                          format=DATETIME_FORMAT)
        except:
            raise Exception('Column or index {0} can not be converted to '
                            'datetime type.'.format(datetime_colname))
    return datetime_col


def get_month_day_range(date):
    """
    Return the first date and last date of the month of the given date.
    """
    # Replace the date in the original timestamp with day 1
    first_day = date + relativedelta(day=1)
    # Replace the date in the original timestamp with day 1
    # Add a month to get to the first day of the next month
    # Subtract one day to get the last day of the current month
    last_day = date + relativedelta(day=1, months=1, days=-1, hours=23)
    return first_day, last_day


def split_train_validation(df, fct_horizon, datetime_colname):
    """
    Split the input dataframe into train and validate folds based
    on the forecast creation time(fct) and forecast horizon specified
    by fct_horizon.
    :param df: The whole input data frame.
    :param fct_horizon: list of tuples in the format of (fct, (forecast_horizon_start, forecast_horizon_end))
    :param datetime_colname: name of the datetime column
    Note:
        df[datetime_colname] needs to be a datetime type.
    """
    i_round = 0
    for fct, horizon in fct_horizon:
        i_round += 1
        train = df.loc[df[datetime_colname] < fct, ].copy()
        validation = df.loc[(df[datetime_colname] >= horizon[0]) & (df[datetime_colname] <= horizon[1]), ].copy()

        yield i_round, train, validation


def add_datetime(input_datetime, unit, add_count):
    if unit == 'year':
        new_datetime = input_datetime + relativedelta(years=add_count)
    elif unit == 'month':
        new_datetime = input_datetime + relativedelta(months=add_count)
    elif unit == 'week':
        new_datetime = input_datetime + relativedelta(weeks=add_count)
    elif unit == 'day':
        new_datetime = input_datetime + relativedelta(days=add_count)
    elif unit == 'hour':
        new_datetime = input_datetime + relativedelta(hours=add_count)
    elif unit == 'minute':
        new_datetime = input_datetime + relativedelta(minutes=add_count)
    else:
        raise Exception('Invalid backtest step unit, {}, provided. Valid step units are'
                        'year, month, week, day, hour, and minute'.format(unit))
    return new_datetime