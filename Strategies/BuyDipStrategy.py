from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
import pandas as pd

from tools import lowest


def get_strategy():
    return BuyDipStrategy


class BuyDipStrategy(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    cci_tp = 10
    adr_tp = 10

    def init(self):
        # Precompute the

        # self.macd = self.I(ta.MACD, pd.Series(self.data.Close), 12, 26, 9)
        # self.scci = self.I(ta.CCI, pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close), self.cci_tp)
        # self.sadr = self.I(ta.ATR, pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close), self.adr_tp)
        self.low10 = self.I(lowest, pd.Series(self.data.Close), self.n1)

    def next(self):

        if self.position.is_long:
            if self.position.pl_pct < 0.05:
                self.position.close()
        else:
            # Low < low10  (or as expressed here: low10 > Low)
            # short trades, and buy the asset
            if crossover(self.low10, self.data.Low):
                self.buy()
