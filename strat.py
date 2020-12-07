from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd
from backtesting import Backtest
import glob
import os
import pathlib
#from talib import MACD, ATR, CCI
import talib as ta

def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    r = pd.Series(values).rolling(n).mean()
    #print(type(r))  # pandas.core.series.Series
    return r

def lowest(values, n):
    """
    Return lowest value in series for last n days
    """
    try:
        # m = values[-n:].min()
        m = pd.Series(values).rolling(n).min()
        # print(type(m))
        return m
    except:
        print(f"Error when finding min of {values}")
        return None


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


class BuyDip(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    cci_tp = 10
    adr_tp = 10

    def init(self):
        # Precompute the

        self.macd = self.I(ta.MACD, pd.Series(self.data.Close), 12, 26, 9)
        self.scci = self.I(ta.CCI, pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close), self.cci_tp)
        self.sadr = self.I(ta.ATR, pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close), self.adr_tp)
        self.low10 = self.I(lowest, pd.Series(self.data.Close), self.n1)

    def next(self):

        if self.position.is_long:
            if self.position.pl_pct < 0.05:
                self.position.close()
        else:
            # Low < low10  (or as experssed here: low10 > Low)
            # short trades, and buy the asset
            if crossover(self.low10, self.data.Low):
                self.buy()


# arr = os.listdir("../stocktips-dl/")
arr = pathlib.Path("../stocktips-dl/data").rglob("*.csv")
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

    #
    # We need at least 30 days of data
    #
    if len(df.index) >= 30:
        #bt = Backtest(df.iloc[-250:], SmaCross, cash=10_000, commission=.002)
        bt = Backtest(df.iloc[-250:], BuyDip, cash=10_000, commission=.002 + .002)  # Add slippage!
        stats = bt.run()

        # Start                     2004-08-19 00:00:00
        # End                       2013-03-01 00:00:00
        # Duration                   3116 days 00:00:00
        # Exposure Time [%]                     93.9944
        # Equity Final [$]                      51959.9
        # Equity Peak [$]                       75787.4
        # Return [%]                            419.599
        # Buy & Hold Return [%]                 703.458
        # Return (Ann.) [%]                      21.328
        # Volatility (Ann.) [%]                 36.5383
        # Sharpe Ratio                         0.583718
        # Sortino Ratio                         1.09239
        # Calmar Ratio                         0.444518
        # Max. Drawdown [%]                    -47.9801
        # Avg. Drawdown [%]                    -5.92585
        # Max. Drawdown Duration      584 days 00:00:00
        # Avg. Drawdown Duration       41 days 00:00:00
        # # Trades                                   65
        # Win Rate [%]                          46.1538
        # Best Trade [%]                         53.596
        # Worst Trade [%]                      -18.3989
        # Avg. Trade [%]                        2.35371
        # Max. Trade Duration         183 days 00:00:00
        # Avg. Trade Duration          46 days 00:00:00
        # Profit Factor                         2.08802
        # Expectancy [%]                        8.79171
        # SQN                                  0.916893
        # _strategy                            SmaCross
        # _equity_curve                           Eq...
        # _trades                       Size  EntryB...

        numtrades = stats['# Trades']
        ann_return = stats['Return (Ann.) [%]']
        sharpe = stats['Sharpe Ratio']
        buyandhold = stats["Buy & Hold Return [%]"]

        if numtrades >= 10 and sharpe > 1.2:
            print("--- A WINNER ---")
            print(f"# Trades: {numtrades}")
            print(f"Annualized return: {ann_return}")
            print(f"Buy and Hold: {buyandhold}")
            print(f"Sharpe Ratio: {sharpe}")

        # print(stats['_trades'])
        # bt.plot()
