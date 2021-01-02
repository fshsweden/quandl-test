from backtesting import Backtest
import argparse
import sys
from sqlalchemy.orm import sessionmaker
import Schema
import pandas as pd

from datetime import datetime
import ntpath
import os
import sys
import importlib.util
import tools as t

parser = argparse.ArgumentParser(description="Strategy Backtesting App")
parser.add_argument("--dbtype", default="mysql", help="database type, for example mysql or sqlite")
parser.add_argument("--dbconn", default="mysqlconnector", help="database connector, for example mysqlconnector")
parser.add_argument("--dbpath", default="alpha.db", help="path and filename of database")
parser.add_argument("--dbhost", default="localhost", help="database hostname")
parser.add_argument("--dbuser", default="algo", help="database username")
parser.add_argument("--dbpass", default="mysecretpassword", help="database user password")
parser.add_argument("--dbschema", default="algo", help="database schema")
parser.add_argument("--echosql", action='store_true', help="Echo all SQL to console")

parser.add_argument("--ticker", default="ALL", help="List of comma-separated tickers")

try:
    args = parser.parse_args()
except argparse.ArgumentError:
    parser.print_help()
    sys.exit(2)

Schema.migrate(args)
engine = Schema.get_engine()

Session = sessionmaker(bind=engine)
session = Session()


def get_all_tickers():
    table_df = pd.read_sql_query(
        f"SELECT distinct name FROM closing_prices",
        con=engine,
        index_col=None
    )
    return table_df["name"]


#
#
#
def load_prices_from_db(ticker):
    table_df = pd.read_sql_query(
        f"SELECT date as Date, open as Open, close as Close, high as High, low as Low, volume as Volume FROM closing_prices where name='{ticker}' order by date ",
        con=engine,
        index_col='Date',
        parse_dates=[
            'Date'
        ]
    )

    return table_df

def update_min_max_vol(product, minv, meanvol, medianvol, maxv):

    try:
        session.query(Schema.Product) \
            .filter(Schema.Product.name == product) \
            .update({Schema.Product.minvol: minv,
                     Schema.Product.meanvol: meanvol,
                     Schema.Product.medianvol: medianvol,
                     Schema.Product.maxvol: maxv })
        session.commit()
    except:
        session.rollback()


if __name__ == '__main__':

    run = None

    if args.ticker == "ALL":
        tickers = get_all_tickers()
    else:
        tickers = args.ticker.split(",")

    # Now test all tickers using this strategy
    for ticker in tickers:
        df = load_prices_from_db(ticker)
        hv = t.hv(df["Close"], 30)
        print(f"{ticker} HV(30) = {round(hv.min(),2)} - {round(hv.max(),2)}")
        update_min_max_vol(ticker,
                           hv.min(),
                           hv.mean(),
                           hv.median(),
                           hv.max())