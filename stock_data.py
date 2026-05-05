import pandas as pd
import yfinance as yf
import datetime as dt

def stock_data_get(stock_id):
    end = dt.datetime.now() - dt.timedelta(days = 1)
    start = dt.datetime(end.year - 1, end.month, end.day)
    df = yf.download(stock_id, start, end)
    df.columns = df.columns.get_level_values(0)
    df['stock_id'] = stock_id
    df = df.reset_index()
    return df   