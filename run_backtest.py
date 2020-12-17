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

def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

strategies = []
path_list = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk('./Strategies') for filename in filenames if filename.endswith('.py')]
for p in path_list:
    # file_path = 'Strategies/Stochastic1.py'
    file_path = p

    #module_name = 'StochasticStrategy1'
    module_name = ntpath.basename(file_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    strategy_class = module.get_strategy()
    # res = dir(module)
    strategies.append(strategy_class)

# from Strategies.* import *

# Run these strategies:
# strategies = [MacdStrategy, BuyDipStrategy, SmaCrossStrategy]
# strategies = [SmaCrossStrategy]
# strategies = [module.StochasticStrategy1]
# strategies = [MacdStrategy]

# keywords
BT_START = "Start"
BT_END = "End"
BT_DURATION = "Duration"
BT_EXPOSURE_TIME = "Exposure Time [%]"
BT_EQUITY_FINAL = "Equity Final [$]"
BT_EQUITY_PEAK = "Equity Peak [$]"
BT_RETURN_PCT = "Return [%]"
BT_BUY_AND_HOLD_RET_PCT = "Buy & Hold Return [%]"
BT_RET_ANN_PCT = "Return (Ann.) [%]"
BT_VOL_ANN_PCT = "Volatility (Ann.) [%]"
BT_SHARPE = "Sharpe Ratio"
BT_SORTINO = "Sortino Ratio"
BT_CALMAR = "Calmar Ratio"
BT_MAX_DRAWDOWN_PCT = "Max. Drawdown [%]"
BT_AVG_DRAWDOWN_PCT = "Avg. Drawdown [%]"
BT_MAX_DRAWDOWN_DUR = "Max. Drawdown Duration"
BT_AVG_DRAWDOWN_DUR = "Avg. Drawdown Duration"
BT_TRADES = "# Trades"
BT_WIN_RATE_PCT = "Win Rate [%]"
BT_BEST_TRADE_PCT = "Best Trade [%]"
BT_WORST_TRADE_PCT = "Worst Trade [%]"
BT_AVG_TRADE_PCT = "Avg. Trade [%]"
BT_MAX_TRADE_DUR = "Max. Trade Duration"
BT_AVG_TRADE_DUR = "Avg. Trade Duration"
BT_PROFIT_FACTOR = "Profit Factor"
BT_EXPECTANCY_PCT = "Expectancy [%]"
BT_SQN = "SQN"
BT_STRATEGY = "_strategy"
BT_EQUITY_CURVE = "_equity_curve"

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
parser.add_argument("-s", "--strategys", default="ALL", help="List of comma-separated tickers")

parser.add_argument("--plot", default=False, action='store_true', help="Save plot to HTML page")
parser.add_argument("--saveresult", default=False, action='store_true', help="Save result (incl trades) to database")
parser.add_argument("--showresult", default=False, action='store_true', help="Show result (no trades) on console")
parser.add_argument("-v", "--verbose", default=False, action='store_true', help="Show status messages while executing app")

parser.add_argument("--commission", type=restricted_float, default=0.002, help="Commission expressed as a float. 0.002 = 0.2%%")
parser.add_argument("--slippage", type=restricted_float, default=0.002, help="Slippage expressed as a float. 0.002 = 0.2%%")
parser.add_argument("-d", "--days", type=int, default=504, help="Days to backtest")

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
    table_df=pd.read_sql_query(
        f"SELECT distinct name FROM closing_prices",
        con=engine,
        index_col=None
    )
    return table_df["name"]


#
#
#
def load_prices_from_db(ticker):
    table_df=pd.read_sql_query(
        f"SELECT date as Date, open as Open, close as Close, high as High, low as Low, volume as Volume FROM closing_prices where name='{ticker}' order by date ",
        con=engine,
        index_col='Date',
        parse_dates=[
            'Date'
        ]
    )

    return table_df


def save_stats(run, ticker, strat, product_data, stats):

    p=session.query(Schema.Product).filter_by(name=ticker).first()

    srr=Schema.StrategyRunResult(
        date=run.date,
        time=run.time,

        strategy_run = run,

        product=p,

        # All output from strat follows here:
        # Start                     2004-08-19 00:00:00
        start=str(stats["Start"]),
        # End                       2013-03-01 00:00:00
        end=str(stats["End"]),
        # Duration                   3116 days 00:00:00
        duration=str(stats["Duration"]),
        # Exposure Time [%]                     93.9944
        exposure_time=stats["Exposure Time [%]"],
        # Equity Final [$]                      51959.9
        equity_final=stats["Equity Final [$]"],
        # Equity Peak [$]                       75787.4
        equity_peak=stats["Equity Peak [$]"],
        # Return [%]                            419.599
        period_return=stats["Return [%]"],
        # Buy & Hold Return [%]                 703.458
        buyandhold=stats["Buy & Hold Return [%]"],
        # Return (Ann.) [%]                      21.328
        annual_return=stats["Return (Ann.) [%]"],
        # Volatility (Ann.) [%]                 36.5383
        annual_volatility=stats["Volatility (Ann.) [%]"],
        # Sharpe Ratio                         0.583718
        sharpe_ratio=stats["Sharpe Ratio"],
        # Sortino Ratio                         1.09239
        sortino_ratio=stats["Sortino Ratio"],
        # Calmar Ratio                         0.444518
        calmar_ratio=stats["Calmar Ratio"],
        # Max. Drawdown [%]                    -47.9801
        max_drawdown=stats["Max. Drawdown [%]"],
        # Avg. Drawdown [%]                    -5.92585
        avg_drawdown=stats["Avg. Drawdown [%]"],
        # Max. Drawdown Duration      584 days 00:00:00
        max_drawdown_duration=str(stats["Max. Drawdown Duration"]),
        # Avg. Drawdown Duration       41 days 00:00:00
        avg_drawdown_duration=str(stats["Avg. Drawdown Duration"]),
        # # Trades                                   65
        num_trades=stats["# Trades"],
        # Win Rate [%]                          46.1538
        win_rate=stats["Win Rate [%]"],
        # Best Trade [%]                         53.596
        best_trade=stats["Best Trade [%]"],
        # Worst Trade [%]                      -18.3989
        worst_trade=stats["Worst Trade [%]"],
        # Avg. Trade [%]                        2.35371
        avg_trade=stats["Avg. Trade [%]"],
        # Max. Trade Duration         183 days 00:00:00
        max_trade_duration=str(stats["Max. Trade Duration"]),
        # Avg. Trade Duration          46 days 00:00:00
        avg_trade_duration=str(stats["Avg. Trade Duration"]),
        # Profit Factor                         2.08802
        profit_factor=0, # stats["Profit Factor"],
        # Expectancy [%]                        8.79171
        expectancy=0, # stats["Expectancy [%]"],
        # SQN                                  0.916893
        sqn=0, #stats["SQN"],
        # _strategy                            SmaCross
        strategy=str(stats["_strategy"]),
        # _equity_curve                           Eq...
        equity_curve="Equity Curve here" # str(stats["_equity_curve"])
    )

    session.add(srr)

    for index, row in stats["_trades"].iterrows():
        # print(row)
        srrt = Schema.StrategyRunResultTrades(
            date=date,
            time=time,

            strategy_run_result=srr,

            Size=row["Size"],
            EntryBar=row["EntryBar"],
            ExitBar=row["ExitBar"],
            EntryPrice=row["EntryPrice"],
            ExitPrice=row["ExitPrice"],
            EntryTime=row["EntryTime"],
            ExitTime=row["ExitTime"],
            PnL=row["PnL"],
            ReturnPct=row["ReturnPct"],
            Duration=row["Duration"].days)

        session.add(srrt)

    try:
        session.commit()
    except Exception as e:
        session.rollback()

        # re-throw
        raise e


if __name__ == '__main__':

    do_save = False

    if args.ticker == "ALL":
        tickers=get_all_tickers()
    else:
        tickers = args.ticker.split(",")

    if do_save:
        now = datetime.now()  # current date and time
        date = now.strftime("%Y%d%m")
        time = now.strftime("%H:%M:%S")

        run = Schema.StrategyRun(
            description="Test",
            date=date,
            time=time
        )
        session.add(run)
        session.commit()

    # Testing strategies one by one
    for strat in strategies:

        # Now test all tickers using this strategy
        for ticker in tickers:

            df = load_prices_from_db(ticker)

            try:
                if args.verbose:
                    print(f"Backtesting {ticker} using {strat.__name__}")

                days = int(args.days)

                bt = Backtest(df.iloc[-args.days:],
                              strat,
                              cash=10_000,
                              commission=args.commission + args.slippage)
                stats = bt.run()
                if stats is not None:
                    if args.saveresult:
                        print("Saving stats for ", ticker, " ", stats[BT_WIN_RATE_PCT])
                    if args.showresult:
                        print(f"{ticker}")
                        print(f"{stats}")
                    if args.plot and len(tickers) < 5:
                        bt.plot()

            except Exception as ex:
                print(f"Error {ex} when backtesting using {strat}")
