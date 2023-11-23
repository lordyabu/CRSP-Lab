from src.helperClasses.trade import Trade
from src.helperClasses.nontrade import NonTrade
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class TradeLog:
    """
    Represents a log of trading operations, managing a collection of 'Trade' objects.

    This class provides methods to add new trades to the log, calculate the total profit and loss (PnL),
    the total PnL percentage, and to export the trade data into a Pandas DataFrame for further analysis.

    Attributes:
        trades (list of Trade): A list to store 'Trade' objects.

    Methods:
        add_trade: Adds a new trade to the log.
        get_total_pnl: Calculates the total PnL from all trades in the log.
        get_total_pnl_percent: Calculates the total PnL percentage from all trades in the log.
        get_trade_dataframe: Converts the trade log into a Pandas DataFrame.
    """
    trades: list = field(default_factory=list)

    def add_trade(self, identifier, time_period, strategy, symbol, start_date, end_date, start_time, end_time,
                  enter_price, exit_price, trade_type, leverage=1, previous_prices=None):
        """
        Adds a new trade to the trade log.

        Args:
            identifier (str): Unique identifier for the trade.
            time_period (str): Time period of the trade.
            strategy (str): Trading strategy used.
            symbol (str): Stock symbol.
            start_date (str): Start date of the trade.
            end_date (str): End date of the trade.
            start_time (int): Start time of the trade.
            end_time (int): End time of the trade.
            enter_price (float): Price at which the trade was entered.
            exit_price (float): Price at which the trade was exited.
            trade_type (str): Type of trade ('long' or 'short').
            leverage (float): Leverage used in the trade, defaults to 1.
            previous_prices (list, optional): Previous prices related to the trade, defaults to None.
        """
        trade = Trade(identifier=identifier, time_period=time_period, strategy=strategy, symbol=symbol,
                      start_date=start_date, end_date=end_date,
                      start_time=start_time, end_time=end_time, enter_price=enter_price, exit_price=exit_price,
                      trade_type=trade_type,
                      leverage=leverage, previous_prices=previous_prices)
        self.trades.append(trade)


    def add_non_trade(self, identifier, time_period, strategy, symbol, start_date, end_date, start_time, end_time,
                  enter_price, exit_price, trade_type, leverage=1, previous_prices=None):
        """
        Adds a new non trade to the trade log.

        Args:
            identifier (str): Unique identifier for the trade.
            time_period (str): Time period of the trade.
            strategy (str): Trading strategy used.
            symbol (str): Stock symbol.
            start_date (str): Start date of the trade.
            end_date (str): End date of the trade.
            start_time (int): Start time of the trade.
            end_time (int): End time of the trade.
            enter_price (float): Price at which the trade was entered.
            exit_price (float): Price at which the trade was exited.
            trade_type (str): Type of trade ('long' or 'short').
            leverage (float): Leverage used in the trade, defaults to 1.
            previous_prices (list, optional): Previous prices related to the trade, defaults to None.
        """
        nontrade = NonTrade(identifier=identifier, time_period=time_period, strategy=strategy, symbol=symbol,
                      start_date=start_date, end_date=end_date,
                      start_time=start_time, end_time=end_time, enter_price=enter_price, exit_price=exit_price,
                      trade_type=trade_type,
                      leverage=leverage, previous_prices=previous_prices)

        self.trades.append(nontrade)

    def get_total_pnl(self):
        """
        Calculates the total profit and loss (PnL) from all trades in the log.

        Returns:
            float: The total PnL from all trades.
        """
        return sum(trade.pnl for trade in self.trades)

    def get_total_pnl_percent(self):
        """
        Calculates the total profit and loss (PnL) percentage from all trades in the log.

        Returns:
            float: The total PnL percentage from all trades.
        """
        return sum(trade.pnl_percent for trade in self.trades)

    def get_trade_dataframe(self):
        """
        Converts the trade log into a Pandas DataFrame for analysis.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from all trades in the log.
        """
        trades_data = []
        for count, trade in enumerate(self.trades, start=0):
            trade_dict = {
                'TradeIndex': count,
                'Identifier': trade.identifier,
                'TimePeriod': trade.time_period,
                'Strategy': trade.strategy,
                'Symbol': trade.symbol,
                'StartDate': trade.start_date,
                'StartTime': trade.start_time,
                'EndDate': trade.end_date,
                'EndTime': trade.end_time,
                'EnterPrice': round(trade.enter_price, 2),
                'ExitPrice': round(trade.exit_price, 2),
                'TradeType': trade.trade_type,
                'Leverage': trade.leverage,
                'PnL': round(trade.pnl, 2),
                'PnL%': round(trade.pnl_percent, 2)
            }

            # Reverse the previous prices list so that PrevPrice_1 is the most recent
            reversed_previous_prices = [round(price, 3) for price in reversed(trade.previous_prices or [])]

            # Adding previous prices as individual columns
            for i, price in enumerate(reversed_previous_prices, 1):
                trade_dict[f'PrevPrice_{i}'] = price

            trades_data.append(trade_dict)

        df = pd.DataFrame(trades_data)
        return df



    def get_non_trade_dataframe(self):
        """
        Converts the trade log into a Pandas DataFrame for analysis.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from all trades in the log.
        """
        trades_data = []
        for count, trade in enumerate(self.trades, start=0):
            trade_dict = {
                'TradeIndex': count,
                'Identifier': trade.identifier,
                'TimePeriod': trade.time_period,
                'Strategy': trade.strategy,
                'Symbol': trade.symbol,
                'StartDate': trade.start_date,
                'StartTime': trade.start_time,
                'EndDate': trade.end_date,
                'EndTime': trade.end_time,
                'EnterPrice': round(trade.enter_price, 2),
                'ExitPrice': trade.exit_price,
                'TradeType': trade.trade_type,
                'Leverage': trade.leverage,
                'PnL': trade.pnl,
                'PnL%': trade.pnl_percent
            }

            # Reverse the previous prices list so that PrevPrice_1 is the most recent
            reversed_previous_prices = [round(price, 3) for price in reversed(trade.previous_prices or [])]

            # Adding previous prices as individual columns
            for i, price in enumerate(reversed_previous_prices, 1):
                trade_dict[f'PrevPrice_{i}'] = price

            trades_data.append(trade_dict)

        df = pd.DataFrame(trades_data)
        return df
