from talib import RSI, BBANDS, MACD
import pandas as pd
import glob

def work():
    mylist = [f for f in glob.glob("*.csv")]
    for f in mylist:
        load_and_test(f)

def load_and_test(filename):
    df = pd.read_csv(filename)
    print(df.columns)

    close = df['AdjClose']

    try:
        up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        rsi = RSI(close, timeperiod=14)
        # print("RSI (first 10 elements)\n", rsi[14:24])
        macd, macdsignal, macdhistogram = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        #print(type(rsi), type(macd))

        tmpdf = pd.DataFrame()
        tmpdf["DATE"] = df[]
        tmpdf["MACD"] = macd
        tmpdf["MACDSIGNAL"] = macdsignal
        tmpdf["MACDHIST"] = macdhistogram

        print(tmpdf.tail())
    except:
        print(f"EXCEPTION on {filename}!")

if __name__ == '__main__':
    work()