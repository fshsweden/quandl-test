from sqlalchemy import create_engine
import pymysql
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Strategy Backtesting App")
parser.add_argument("--dbtype", default="mysql", help="database type, for example mysql or sqlite")

sqlEngine       = create_engine('mysql+pymysql://algo:mysecretpassword@127.0.0.1', pool_recycle=3600)
dbConnection    = sqlEngine.connect()


frame           = pd.read_sql("select * from algo.products", dbConnection);
pd.set_option('display.expand_frame_repr', False)
print(frame)
frame.to_csv("products.csv", index=False)

names = frame["name"]
for n in names:
    print(n)
    f = pd.read_sql(f"select * from algo.closing_prices where name = '{n}'", dbConnection);
    del f['id']
    f.to_csv(f"csv/{n}.csv", index=False)

dbConnection.close()

