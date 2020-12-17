import numpy as np
import talib as ta

inputs = {
    'open': np.random.random(100),
    'high': np.random.random(100),
    'low': np.random.random(100),
    'close': np.random.random(100),
    'volume': np.random.random(100)
}

close = np.random.random(100)

output = ta.SMA(close)

print(output)

from talib import MA_Type

upper, middle, lower = ta.BBANDS(close, matype=MA_Type.T3)

print(upper)
