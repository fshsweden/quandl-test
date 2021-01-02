from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Session, sessionmaker, relationship
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
import mysql.connector

Base = declarative_base()


#
#
#
class Product(Base):
    __tablename__ = "products"

    id = Column('id', Integer, primary_key=True)

    name = Column('name', String(80))   # symbol
    sectype = Column('sectype', String(3))
    currency = Column('currency', String(3))

    exchange = Column('exchange', String(80)) # primary exchange? or a list of exchanges???

    minvol = Column('minvol', Numeric(14,4))
    maxvol = Column('maxvol', Numeric(14,4))
    meanvol = Column('meanvol', Numeric(14,4))
    medianvol = Column('medianvol', Numeric(14,4))

    def __repr__(self):
        return "<StrategyRunResult(date='%s', time='%s', name='%s', sectype='%s', exchange='%s', currency='%s')>" % (self.date, self.time)


#
# What is this for really??????
#
class Trade(Base):
    __tablename__ = "trades"

    id = Column('id', Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey('products.id'))

    Size = Column('open', Numeric(14, 4))
    EntryBarOpen = Column('entrybar_open', Numeric(14, 4))
    EntryBarHigh = Column('entrybar_high', Numeric(14, 4))
    EntryBarLow = Column('entrybar_low', Numeric(14, 4))
    EntryBarClose = Column('entrybar_close', Numeric(14, 4))

    ExitBarOpen = Column('exitbar_open', Numeric(14, 4))
    ExitBarHigh = Column('exitbar_high', Numeric(14, 4))
    ExitBarLow = Column('exitbar_low', Numeric(14, 4))
    ExitBarClose = Column('exitbar_close', Numeric(14, 4))

    EntryPrice = Column('entryprice', Numeric(14, 4))
    ExitPrice = Column('exitprice', Numeric(14, 4))

    PnL = Column('pnl', Numeric(14, 4))
    ReturnPct = Column('returnpct', Numeric(14, 4))

    EntryTime = Column('entrytime', String(10))
    ExitTime = Column('exittime', String(10))
    Duration = Column('duration', String(20))

    ##UniqueConstraint(  should be strategy+date+time or possibly strategy+sequence-number  )

    def __repr__(self):
        return "<Trade()>"

#
#
#
class ClosingPrice(Base):
    __tablename__ = "closing_prices"

    id = Column('id', Integer, primary_key=True)
    date = Column('date', String(10))
    time = Column('time', String(10))

    name = Column('name', String(80))
    sectype = Column('sectype', String(3))
    exchange = Column('exchange', String(80))
    currency = Column('currency', String(3))

    open = Column('open', Numeric(14, 4))
    close = Column('close', Numeric(14, 4))
    high = Column('high', Numeric(14, 4))
    low = Column('low', Numeric(14, 4))
    volume = Column('volume', Numeric(14, 0))

    __table_args__ = (UniqueConstraint('name', 'sectype', 'currency', 'exchange', 'date', 'time'),)

    def __repr__(self):
        return "<ClosingPrice(date='%s', time='%s', name='%s', sectype='%s', exchange='%s', currency='%s')>" % (self.date, self.time, self.name, self.sectype, self.exchange, self.currency)

#
#
#
class StrategyRun(Base):
    __tablename__ = "strategy_run"

    id = Column('id', Integer, primary_key=True)
    description = Column(String(80))   # why this run was made (can be blank)
    date = Column('date', String(10))
    time = Column('time', String(10))

    # Bidirectional
    strategy_run_results = relationship('StrategyRunResult', back_populates="strategy_run")

    def __repr__(self):
        return "<StrategyRun(date='%s', time='%s')>" % (self.date, self.time)

#
#
#
class StrategyRunResult(Base):
    __tablename__ = "strategy_run_result"

    id = Column('id', Integer, primary_key=True)
    date = Column(String(10))
    time = Column(String(10))

    # Bidirectional
    strategy_run_id = Column(Integer, ForeignKey('strategy_run.id'))
    strategy_run = relationship('StrategyRun', back_populates="strategy_run_results")

    # Unidirectional
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product')

    # All output from strat follows here:
    # Start                     2004-08-19 00:00:00
    start = Column('start', String(20))
    # End                       2013-03-01 00:00:00
    end = Column('end', String(20))
    # Duration                   3116 days 00:00:00
    duration = Column('duration', String(20))
    # Exposure Time [%]                     93.9944
    exposure_time = Column('exposure_time', Numeric(14, 4))
    # Equity Final [$]                      51959.9
    equity_final = Column('equity_final', Numeric(14, 4))
    # Equity Peak [$]                       75787.4
    equity_peak = Column('equity_peak', Numeric(14, 4))
    # Return [%]                            419.599
    period_return = Column('period_return', Numeric(14, 4))
    # Buy & Hold Return [%]                 703.458
    buyandhold = Column('buyandhold', Numeric(14, 4))
    # Return (Ann.) [%]                      21.328
    annual_return = Column('annual_return', Numeric(14, 4))
    # Volatility (Ann.) [%]                 36.5383
    annual_volatility = Column('annual_volatility', Numeric(14, 4))
    # Sharpe Ratio                         0.583718
    sharpe_ratio = Column('sharpe_ratio', Numeric(14, 4))
    # Sortino Ratio                         1.09239
    sortino_ratio = Column('sortino_ratio', Numeric(14, 4))
    # Calmar Ratio                         0.444518
    calmar_ratio = Column('calmar_ratio', Numeric(14, 4))
    # Max. Drawdown [%]                    -47.9801
    max_drawdown = Column('max_drawdown', Numeric(14, 4))
    # Avg. Drawdown [%]                    -5.92585
    avg_drawdown = Column('avg_drawdown', Numeric(14, 4))
    # Max. Drawdown Duration      584 days 00:00:00
    max_drawdown_duration = Column('max_drawdown_duration', String(20))
    # Avg. Drawdown Duration       41 days 00:00:00
    avg_drawdown_duration = Column('avg_drawdown_duration', String(20))
    # # Trades                                   65
    num_trades = Column('num_trades', Integer)
    # Win Rate [%]                          46.1538
    win_rate = Column('win_rate', Numeric(14, 4))
    # Best Trade [%]                         53.596
    best_trade = Column('best_trade', Numeric(14, 4))
    # Worst Trade [%]                      -18.3989
    worst_trade = Column('worst_trade', Numeric(14, 4))
    # Avg. Trade [%]                        2.35371
    avg_trade = Column('avg_trade', Numeric(14, 4))
    # Max. Trade Duration         183 days 00:00:00
    max_trade_duration = Column('max_trade_duration', String(20))
    # Avg. Trade Duration          46 days 00:00:00
    avg_trade_duration = Column('avg_trade_duration', String(20))
    # Profit Factor                         2.08802
    profit_factor = Column('profit_factor', Numeric(14, 4))
    # Expectancy [%]                        8.79171
    expectancy = Column('expectancy', Numeric(14, 4))
    # SQN                                  0.916893
    sqn = Column('sqn', Numeric(14, 4))
    # _strategy                            SmaCross
    strategy = Column('strategy', String(80))
    # _equity_curve                           Eq...
    equity_curve = Column('equity_curve', String(80))       # ??

    # _trades                       Size  EntryB...
    strategy_run_result_trades = relationship('StrategyRunResultTrades', back_populates="strategy_run_result")
    # UniqueConstraint('name', 'sectype', 'currency', 'exchange')

    def __repr__(self):
        return "<StrategyRunResult(date='%s', time='%s', name='%s', sectype='%s', exchange='%s', currency='%s')>" % (self.date, self.time)


class StrategyRunResultTrades(Base):
    __tablename__ = "strategy_run_result_trades"

    id = Column('id', Integer, primary_key=True)
    date = Column(String(10))
    time = Column(String(10))

    # symbol
    strategy_run_result_id = Column(Integer, ForeignKey('strategy_run_result.id'))
    strategy_run_result = relationship('StrategyRunResult', back_populates="strategy_run_result_trades")

    Size = Column('size', Integer)
    EntryBar = Column('entrybar', Numeric(14, 4))
    ExitBar = Column('exitbar', Numeric(14, 4))
    EntryPrice = Column('entryprice', Numeric(14, 4))
    ExitPrice = Column('exitprice', Numeric(14, 4))
    EntryTime = Column('entrytime', String(20))
    ExitTime = Column('exittime', String(20))
    PnL = Column('pnl', Numeric(14, 4))
    ReturnPct = Column('returnpct', Numeric(14, 4))
    Duration = Column('duration', Integer)



engine = None

#
#
#
def migrate(args):
    global engine

    print(f"Connecting to database...")
    # engine = create_engine(f"{dbtype}:///{dbpath}", echo=True)

    # if args.dbtype == "mysql"
    #   args.dbusername
    #   args.dbpassword
    #   args.dbname

    #engine = create_engine("mysql+mysqlconnector://algo:mysecretpassword@localhost/algo?charset=utf8mb4", echo=False)
    engine = create_engine(f"{args.dbtype}+{args.dbconn}://{args.dbuser}:{args.dbpass}@{args.dbhost}/{args.dbschema}?charset=utf8mb4", echo=args.echosql)
    print(f"Applying ORM structure...")
    Base.metadata.create_all(engine)

def get_engine():
    return engine