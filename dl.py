import pandas_datareader.data as web
from talib import RSI, BBANDS, MACD
import quandl
import pandas as pd
import numpy as np
import scipy
import csv
from urllib.request import urlopen

quandl.ApiConfig.api_key = 'x8C1JXgxZsKYd_i8-zvz'

url = 'https://s3.amazonaws.com/quandl-production-static/end_of_day_us_stocks/ticker_list.csv'
df = pd.read_csv(url)

print(df.head())

start = '1975-01-01'
end = '2020-12-02'

count = 0
maxcount = 10

for symbol in df['Ticker'].tolist():
    print(f"Loading {symbol}")
    try:
        price = web.DataReader(name=symbol, data_source='quandl', start=start, end=end)
        price.to_csv(f"./DL/{symbol}.csv", index=True)
    except:
        print(f"Error DL {symbol}")
