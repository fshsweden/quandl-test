from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd
from backtesting import Backtest
import glob
import os
import pathlib


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()


class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()


#arr = os.listdir("../stocktips-dl/")
arr = pathlib.Path().glob("../stocktips-dl/data/*.csv")
for f in arr:
    b = os.path.basename(f)
    fn, ext = os.path.splitext(b)
    print("Testing " + fn)

    df = pd.read_csv(f,
                 parse_dates=["Date"],
                 index_col=["Date"],
                 sep=",",
                 names=["Date", "Time", "Symbol", "SecType", "Exchange", "Currency", "Open", "Close", "High", "Low",
                        "Volume"])

    bt = Backtest(df.iloc[-250:], SmaCross, cash=10_000, commission=.002)
    stats = bt.run()

    numtrades = stats['# Trades']
    ann_return = stats['Return (Ann.) [%]']
    sharpe = stats['Sharpe Ratio']

    if numtrades >= 10 and sharpe > 1.2:
        print("--- A WINNER ---")
        print(f"# Trades: {numtrades}")
        print(f"Annualized return: {ann_return}")
        print(f"Sharpe Ratio: {sharpe}")

    #print(stats['_trades'])
    #bt.plot()
