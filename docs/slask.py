momentum_window = 125
minimum_momentum = 40

#Momentum score function
def momentum_score(ts):
    x = np.arange(len(ts))
    log_ts = np.log(ts)
    regress = stats.linreggress(x, log_ts)
    annualized_slope = (np.power(np.exp(regress[0]), 252) - 1) * 100
    return annualized_slope * (regress[2] ** 2)

def x():
    df['momentum'] = df.groupby('symbol')['close'].rolling(
        momentum_window,
        min_periods = minimum_momentum
    ) .apply(momentum_score).reset_index(level=0, drop=True)

inv_sentiment = quandl.get('AAII/AAII_SENTIMENT', start_date='2001-01-01', end_date='2020-11-19')
print(inv_sentiment.columns)
print(inv_sentiment)

us_stocks = pd.read_csv('https://s3.amazonaws.com/quandl-production-static/end_of_day_us_stocks/ticker_list.csv', error_bad_lines=False)
# print(us_stocks.columns)
# print(us_stocks['Ticker'].tolist())

nasdaq_omx_indexes = pd.read_csv("https://s3.amazonaws.com/quandl-production-static/nasdaqomx/indexes.csv", error_bad_lines=False, delimiter='|')
# print(nasdaq_omx_indexes.columns)
# print(nasdaq_omx_indexes['SYMBOL'].tolist())



print("All rows and second to last column")
print(df.iloc[:, 0:3])
print("Index[0]")
print(df.index[1:5])

#df_T = df.DataFrame(df.iloc[:,-2])


#df.plot()
#plt.show()



start = '2015-04-22'
end = '2020-12-02'

symbol = 'MCD'
max_holding = 100
price = web.DataReader(name=symbol, data_source='quandl', start=start, end=end)
price = price.iloc[::-1]
price = price.dropna()
close = price['AdjClose'].values
