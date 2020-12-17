def test():
    cp = ClosingPrice(date="20181201", time="000101", name="DEMO", sectype="STK", exchange="DEMO", currency="TRD")
    session.bulk_save_objects([cp])
    session.commit()


    # def update_cp(name, exchange, currency, sectype, date, time, open, close, high, low, volume):
    #     ins = closing_prices.insert().values(name=name,
    #                                          exchange=exchange,
    #                                          currency=currency,
    #                                          sectype=sectype,
    #                                          date=date,
    #                                          time=time,
    #                                          open=open,
    #                                          close=close,
    #                                          high=high,
    #                                          low=low,
    #                                          volume=volume)
    #     ins.compile()
    #     try:
    #         result = conn.execute(ins)
    #     except Exception as ex:
    #         print("*** Exception ***" + str(ex))
    #
    #         try:
    #             print("=== UPDATING INSTEAD ===")
    #             upd = closing_prices.update().values(name=name,
    #                                                  exchange=exchange,
    #                                                  currency=currency,
    #                                                  sectype=sectype,
    #                                                  date=date,
    #                                                  time=time,
    #                                                  open=open,
    #                                                  close=close,
    #                                                  high=high,
    #                                                  low=low,
    #                                                  volume=volume)
    #             upd.compile()
    #             result = conn.execute(upd)
    #         except Exception as ex:
    #             print("*** Exception ***" + str(ex))


    #arr = pathlib.Path("../stocktips-dl/data").rglob("*.csv")

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

def load_from_database():
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
