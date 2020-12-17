import csv
import urllib.request
import codecs
import pandas as pd
import talib as ta
from talib.abstract import *
import numpy as np
import matplotlib.pyplot as plt
from backtesting.test import GOOG

def backtest():
    print(GOOG.tail())

def handle_csv_stream(csv_string):
    lines = csv_string.splitlines()
    csvfile = csv.reader(lines)
    for line in csvfile:
        print(line[0])  # do something with line

def pandas_macd(file_path):
    df = pd.read_csv(file_path,
                     parse_dates=["Date"],
                     index_col=["Date"],
                     sep=",",
                     names=["Date", "Time", "Symbol", "SecType", "Exchange", "Currency", "Open", "Close", "High", "Low", "Volume"])

    df["% change"] = df["Close"].pct_change()
    df["200 sma"] = df["Close"].rolling(window=200).mean().round(5)
    df["50 sma"] = df["Close"].rolling(window=50).mean().round(5)

    df["Criteria 1"] = df["Close"] >= df["200 sma"]
    df["Criteria 2"] = True == (df["50 sma"] >= df["200 sma"]) | df["Criteria 1"]

    df["Buy and Hold"] = 100*(1+df["% change"]).cumprod()
    df["200 sma model"] = 100*(1+df["Criteria 1"].shift(1)*df["% change"]).cumprod()
    df["200 sma + crossover model"] = 100 * (1 + df["Criteria 2"].shift(1) * df["% change"]).cumprod()

    # 200 sma model's returns
    start_model1 = df["200 sma model"].iloc[200]
    end_model1 = df["200 sma model"].iloc[-1]
    years = (df["200 sma model"].count()+1-200)/ 252
    model1_average_return = (end_model1/start_model1)**(1/years)-1
    print("200 sma model yields an average of", model1_average_return*100, '% per year')

    dfnew = pd.DataFrame()
    df['MA20'] = ta.SMA(df['Close'], 20)

    dfnew['MA20'] = df['MA20']
    dfnew['Close'] = df['Close']

    df['EMA20'] = ta.SMA(df['Close'], 20)
    df['MA50'] = ta.SMA(df['Close'], 50)
    df['EMA50'] = ta.SMA(df['Close'], 50)

    df['MACD'], df['MACD-SIGNAL'], df['MACD-HIST'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    df = df.iloc[-300:]
    df[['MACD', 'MACD-SIGNAL']].plot(figsize=(12, 12))
    plt.show()


    print(df.tail(30))
    # df.apply(lambda c: talib.EMA(c, 2))


def test1():
    my_file_handle=open("../stocktips-dl/data/AAPL.csv")
    data = my_file_handle.read()
    handle_csv_stream(data)

def test2():
    pandas_macd("../stocktips-dl/data/CZZ.csv")
    print(ta.get_function_groups())


if __name__ == '__main__':
    backtest()

