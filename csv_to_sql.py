from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, UniqueConstraint
from sqlalchemy.orm import Session, sessionmaker

import pandas as pd
import os
import pathlib
import sys
import sqlite3

engine = create_engine('sqlite:////home/peter/alpha.db', echo=True)
metadata = MetaData()
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class ClosingPrice(Base):
    __tablename__ = "closing_prices"

    id = Column('id', Integer, primary_key=True)
    date = Column('date', String)
    time = Column('time', String)
    name = Column('name', String)
    sectype = Column('sectype', String)
    exchange = Column('exchange', String)
    currency = Column('currency', String)
    open = Column('open', Numeric)
    close = Column('close', Numeric)
    high = Column('high', Numeric)
    low = Column('low', Numeric)
    volume = Column('volume', Numeric)

    def __repr__(self):
        return "<ClosingPrice(date='%s', time='%s', name='%s', sectype='%s', exchange='%s', currency='%s')>" % (self.date, self.time, self.name, self.sectype, self.exchange, self.currency)

def test():
    cp = ClosingPrice(date="20181201", time="000101", name="DEMO", sectype="STK", exchange="DEMO", currency="TRD")
    session.bulk_save_objects([cp])
    session.commit()


if __name__ == '__main__':

    #test()
    #sys.exit()

    closing_prices = Table(
        'closing_prices',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('date', String),
        Column('time', String),
        Column('name', String),
        Column('sectype', String),
        Column('exchange', String),
        Column('currency', String),
        Column('open', Numeric),
        Column('close', Numeric),
        Column('high', Numeric),
        Column('low', Numeric),
        Column('volume', Numeric),

        UniqueConstraint('date', 'time', 'name', 'sectype', 'exchange', 'currency', name='uix_1')
    )
    metadata.create_all(engine)

    conn = engine.connect()

    def update_cp(name, exchange, currency, sectype, date, time, open, close, high, low, volume):
        ins = closing_prices.insert().values(name=name,
                                             exchange=exchange,
                                             currency=currency,
                                             sectype=sectype,
                                             date=date,
                                             time=time,
                                             open=open,
                                             close=close,
                                             high=high,
                                             low=low,
                                             volume=volume)
        ins.compile()
        try:
            result = conn.execute(ins)
        except Exception as ex:
            print("*** Exception ***" + str(ex))

            try:
                print("=== UPDATING INSTEAD ===")
                upd = closing_prices.update().values(name=name,
                                                     exchange=exchange,
                                                     currency=currency,
                                                     sectype=sectype,
                                                     date=date,
                                                     time=time,
                                                     open=open,
                                                     close=close,
                                                     high=high,
                                                     low=low,
                                                     volume=volume)
                upd.compile()
                result = conn.execute(upd)
            except Exception as ex:
                print("*** Exception ***" + str(ex))




    arr = pathlib.Path("../stocktips-dl/data").rglob("*.csv")
    arr = sorted(arr)

    for f in arr:
        b = os.path.basename(f)
        fn, ext = os.path.splitext(b)
        print("Testing " + fn)

        if fn > "RYT":
            df = pd.read_csv(f,
                             parse_dates=["Date"],
                             index_col=["Date"],
                             sep=",",
                             names=["Date", "Time", "Symbol", "SecType", "Exchange", "Currency", "Open", "Close", "High", "Low", "Volume"])


            cps = []
            for index, row in df.iterrows():

                date = str(index)
                date = date.replace("-", "")
                date = date[0:8]

                # update_cp(row['Symbol'],
                #           row['Exchange'],
                #           row['Currency'],
                #           row['SecType'],
                #           date,
                #           row['Time'],
                #           row['Open'],
                #           row['Close'],
                #           row['High'],
                #           row['Low'],
                #           row['Volume'])

                cp = ClosingPrice(date=date, time=row["Time"],
                              name=row['Symbol'],
                              sectype=row['SecType'],
                              exchange=row['Exchange'],
                              currency=row['Currency'],
                              open=row['Open'],
                              close=row['Close'],
                              high=row['High'],
                              low=row['Low'],
                              volume=row['Volume'])

                cps.append(cp)

            session.bulk_save_objects(cps)
            session.commit()



