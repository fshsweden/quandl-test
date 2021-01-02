from backtesting import Strategy
from backtesting.lib import crossover
from tools import SMA
from talib import EMA


def get_strategy():
    return EmaCrossStrategy


class EmaCrossStrategy(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 9
    n2 = 21

    def init(self):
        # Precompute the two moving averages
        self.ma1 = self.I(EMA, self.data.Close, self.n1)
        self.ma2 = self.I(EMA, self.data.Close, self.n2)

    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.ma1, self.ma2):
            self.position.close()
            self.buy(sl=self.data.Close * 0.95)

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.ma2, self.ma1):
            self.position.close()
            self.sell(sl=self.data.Close * 1.05)
