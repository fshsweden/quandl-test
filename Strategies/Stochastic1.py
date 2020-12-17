from backtesting import Strategy
from backtesting.lib import cross, crossover
import talib as ta
import pandas as pd

from tools import SMA


def get_strategy():
    return StochasticStrategy1


class StochasticStrategy1(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    KINDEX=0 # slowK
    DINDEX=1 # slowD

    def init(self):
        # self.rsi = self.I(ta.RSI, pd.Series(self.data.Close))
        self.stochastic = self.I(ta.STOCHF, pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close))
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):

        # helpers
        K = self.stochastic[self.KINDEX][-1]   # the stochastic indicator
        D = self.stochastic[self.DINDEX][-1]   # the slow MA3 of K
        yK = self.stochastic[self.KINDEX][-2]
        yD = self.stochastic[self.DINDEX][-2]
        C = self.data.Close[-1]

        # If was under 20 and crossed up and now over 20 = BUY SIGNAL

        if crossover([yK, K], [yD, D]):
            if yK <= 20:
                self.position.close()
                self.buy(sl=0.97 * C)
        else:
            if crossover([yD, D], [yK, K]):
                if yK >= 80:
                    self.position.close()
                    self.sell(sl=1.03 * C)

