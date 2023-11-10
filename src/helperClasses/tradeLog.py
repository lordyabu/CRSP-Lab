from src.helperClasses.trade import Trade
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class TradeLog:
    trades: list = field(default_factory=list)

    def add_trade(self, identifier, time_period, strategy, symbol, start_date, end_date, start_time, end_time, enter_price, exit_price, trade_type, leverage=1):
        trade = Trade(identifier=identifier, time_period=time_period, strategy=strategy, symbol=symbol, start_date=start_date, end_date=end_date, start_time=start_time,
                      end_time=end_time, enter_price=enter_price, exit_price=exit_price, trade_type=trade_type, leverage=leverage)
        self.trades.append(trade)

    def get_total_pnl(self):
        return sum(trade.pnl for trade in self.trades)


    def get_total_pnl_percent(self):
        return sum(trade.pnl_percent for trade in self.trades)

    def get_trade_dataframe(self):
        # Can change order if needed
        trades_data = [
            {'Identifier': trade.identifier, 'TimePeriod': trade.time_period, 'Strategy': trade.strategy, 'Symbol': trade.symbol, 'StartDate': trade.start_date,
             'StartTime': trade.start_time, 'EndDate': trade.end_date, 'EndTime': trade.end_time, 'EnterPrice': round(trade.enter_price, 2),
             'ExitPrice': round(trade.exit_price, 2), 'TradeType': trade.trade_type,
             'Leverage': trade.leverage, 'PnL': round(trade.pnl, 2), 'PnL%': round(trade.pnl_percent, 2)}
            for trade in self.trades
        ]
        df = pd.DataFrame(trades_data)
        return df









# Create a TradeLog instance
# trade_log = TradeLog()
#
#
# trade_log.add_trade(date='20201108', time=160000, strategy='bol',symbol="AAPL", enter_price=100, exit_price=110, trade_type="long")
# trade_log.add_trade(date='20201109', time=90000, strategy='bol',symbol="GOOG", enter_price=1500, exit_price=1400, trade_type="short", leverage=2)
# trade_log.add_trade(date='20201110', starttime=70000, strategy='bol',symbol="TSLA", enter_price=600, exit_price=650, trade_type="long")
#
# # Print out the total PnL
# print("Total PnL:", trade_log.get_total_pnl())
#
# # Get the trade DataFrame and print it
# trade_df = trade_log.get_trade_dataframe()
# print(trade_df)
#
# # Print out the TradeLog
# print(trade_log)
