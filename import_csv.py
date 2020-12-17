from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String, Numeric, UniqueConstraint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

import argparse
import pandas as pd
import os
import pathlib
import sys
import Schema

parser = argparse.ArgumentParser(description="")


parser = argparse.ArgumentParser(description="Loader program that imports CSV files from IB into a database table")

parser.add_argument("--dbtype", default="mysql", help="database type, for example mysql or sqlite")
parser.add_argument("--dbconn", default="mysqlconnector", help="database connector, for example mysqlconnector")
parser.add_argument("--dbpath", default="alpha.db", help="path and filename of database")
parser.add_argument("--dbuser", default="algo", help="database username")
parser.add_argument("--dbpass", default="mysecretpassword", help="database user password")
parser.add_argument("--dbschema", default="algo", help="database schema")

parser.add_argument("--echosql", action='store_true')

parser.add_argument("--csv", required=True, help="location of CSV files")
parser.add_argument("--batch", default=True, action='store_true', help="Save all entries per instrument in one COMMIT")


try:
    args = parser.parse_args()
except argparse.ArgumentError:
    parser.print_help()
    sys.exit(2)

Schema.migrate(args)
engine =Schema.get_engine()

Session=sessionmaker(bind=engine)
session=Session()


def load_csv(f):
    b = os.path.basename(f)
    fn, ext = os.path.splitext(b)
    print("Loading " + b)

    df = pd.read_csv(f,
                     parse_dates=["Date"],
                     index_col=["Date"],
                     sep=",",
                     names=["Date", "Time", "Symbol", "SecType", "Exchange", "Currency", "Open", "Close", "High", "Low",
                            "Volume"])

    if args.batch:
        save_dataframe_batch(f, df)
    else:
        print("Saving data one line at a time")
        save_dataframe_one_by_one(f, df)


def load_csv_folder(csvpath):
    arr = pathlib.Path(f"{csvpath}").rglob("*.csv")
    arr = sorted(arr)

    for f in arr:
        load_csv(f)


def save_dataframe_one_by_one(fn, df):
    dupes = 0
    for index, row in df.iterrows():
        date = str(index)
        date = date.replace("-", "")
        date = date[0:8]

        cp = Schema.ClosingPrice(date=date, time=row["Time"],
                          name=row['Symbol'],
                          sectype=row['SecType'],
                          exchange='',  # row['Exchange'],
                          currency=row['Currency'],
                          open=row['Open'],
                          close=row['Close'],
                          high=row['High'],
                          low=row['Low'],
                          volume=row['Volume'])

        try:
            session.add(cp)
            session.flush()
            session.commit()
        except IntegrityError as err:
            # print("Integrity Exception:", err)
            # print(row)
            dupes = dupes + 1
            session.rollback()
        except Exception as e:
            print("Commit Exception:", e)
            print(row)
            session.rollback()

    if (dupes > 0):
        print(f"{fn} had {dupes} duplicates that where not saved ")

def save_dataframe_batch(fn, df):
    cps = []

    # print("Collecting data from dataframe")
    for index, row in df.iterrows():
        date = str(index)
        date = date.replace("-", "")
        date = date[0:8]

        cp = Schema.ClosingPrice(date=date, time=row["Time"],
                          name=row['Symbol'],
                          sectype=row['SecType'],
                          exchange='', # row['Exchange'],
                          currency=row['Currency'],
                          open=row['Open'],
                          close=row['Close'],
                          high=row['High'],
                          low=row['Low'],
                          volume=row['Volume'])

        cps.append(cp)

    print(f"Saving {len(cps)} rows")

    try:
        session.bulk_save_objects(cps)
        session.flush()
    except IntegrityError as e:
        session.rollback()
        print("Integrity Error:", e)
        print(row)
    except Exception as e:
        session.rollback()
        print("Commit Exception:", e)
        print(row)
    else:
        session.commit()


if __name__ == '__main__':

    load_csv_folder(args.csv)
    # load_csv("/home/peter/dev/FSHProjects/stocktips-data/IMPORT/FILES-A/ABEV.csv")

