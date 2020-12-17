from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
import pandas as pd

from tools import lowest


def get_strategy():
    return MacdStrategy


class MacdStrategy(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    S = 12
    L = 26
    H = 9

    def init(self):
        self.rsi = self.I(ta.RSI, pd.Series(self.data.Close))
        self.stochastic = self.I(ta.STOCH, pd.Series(self.data.Close))
        self.macd, self.macd_signal, self.macd_hist = self.I(ta.MACD,
                                                             pd.Series(self.data.Close),
                                                             MacdStrategy.S,
                                                             MacdStrategy.L,
                                                             MacdStrategy.H)

    def next(self):

        # crossover tests [-1] and [-2]
        if crossover(self.macd, self.macd_signal):
            self.position.close()
            self.buy()
        else:
            if crossover(self.macd_signal, self.macd):
                self.position.close()
                self.sell()

