import pandas_datareader.data as web
from talib import RSI, BBANDS, MACD
import quandl

start = '2015-04-22'
end = '2020-12-02'

symbol = 'MCD'
max_holding = 100
price = web.DataReader(name=symbol, data_source='quandl', start=start, end=end)
price = price.iloc[::-1]
price = price.dropna()
close = price['AdjClose'].values
up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
rsi = RSI(close, timeperiod=14)

print("RSI (first 10 elements)\n", rsi[14:24])

macd = MACD(close)
print(macd)

import matplotlib
import matplotlib.pyplot as plt
df = quandl.get('CHRIS/MCX_CL1', start_date='2020-01-01', end_date='2020-12-02')
#res["mavg(50)"] = res[]
#print(type(res))

print("All rows and second to last column")
print(df.iloc[:, 0:3])
print("Index[0]")
print(df.index[1:5])

#df_T = df.DataFrame(df.iloc[:,-2])


#df.plot()
#plt.show()

