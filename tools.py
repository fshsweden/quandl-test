from math import sqrt

import pandas as pd
import numpy as np

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
        m = pd.Series(values).rolling(n).min()
        return m
    except:
        print(f"Error when finding min of {values}")
        return None

def hv(values, n):
    """
    Return lowest value in series for last n days
    """
    try:
        rtn = pd.Series(values) / pd.Series(values).shift(1)
        logrtn = np.log(rtn)
        std = logrtn.rolling(n).std()
        std = std * sqrt(252)
        return std
    except:
        print(f"Error when finding min of {values}")
        return None

def test_hv(df):
    # calculate daily logarithmic return
    df['returns'] = df['close'] / df['close'].shift(-1)
    df['log_returns'] = np.log(df['returns'])
    df['daily_std'] = df['log_returns'].rolling(21).std()
    df['ann_std'] = df['daily_std'] * 252 ** 0.5    # Note x^0.5 == SQRT(x)
    return df


def test():
    df = pd.DataFrame()
    df['close'] = pd.Series(
        [
            153.899643,
            153.068451,
            152.751816,
            154.077759,
            155.759949,
            155.759949,
            155.730255,
            157.006729,
            157.293686,
            155.938049,
            156.04689,
            158.936279,
            156.95726,
            157.362961,
            155.928177,
            158.411835,
            160.390869,
            159.648727,
            161.568405,
            160.43045,
            161.469452,
            164.428116,
            165.348358,
            164.754654,
            163.963043,
            164.972351,
            163.309952,
            160.578888,
            163.725555,
            166.278503,
            170.968826,
            168.445557,
            172.552048,
            178.231873,
            178.014191,
            181.705093,
            181.962357,
            186.721939,
            182.506607,
            182.773773,
            181.784271,
            183.407059,
            185.267365,
            185.822998,
            182.985229,
            177.200607,
            169.560516

        ]
    )
    df = test_hv(df)
    print("=== correct ===")
    print(df.head(100))
    print("=== ------- ===")

    s2 = hv(df['close'], 21)
    print("=== check ===")
    print(s2)
    print("=== ----- ===")

if __name__ == '__main__':
    test()