# The MLTurtleNaive class, extending StockAlgorithmDaily, implements a simplified Turtle trading strategy for stock markets.
# It manages trading positions, decision-making based on market state, and execution of trading actions in line with the Turtle strategy.
# Key features include tracking and updating long and short positions, determining trade actions based on rolling window calculations,
# processing these actions, and maintaining a step-wise approach through the trading dataset.
# The class is designed to simulate and analyze the Turtle trading strategy's performance for specific stocks over time.
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from src.helperClasses.unit import Unit
from src.helperClasses.traderBasic import MLStockAlgorithmDaily
from src.config import DATA_DIR, TURTLE_DATA_NAME, TRANSACTION_COST_PCT, TRANSACTION_COST_DOLLAR
import os
import pandas as pd


def find_rows_by_date_and_stock(df, date_column, stock_column, target_date, target_stock):
    """
    Search for rows in a DataFrame that match a specific date and stock symbol.

    Args:
        df (pandas.DataFrame): The DataFrame to search.
        date_column (str): The name of the column containing dates.
        stock_column (str): The name of the column containing stock symbols.
        target_date (str): The date to search for, in 'YYYYMMDD' format.
        target_stock (str): The stock symbol to search for.

    Returns:
        pandas.DataFrame: A DataFrame containing the rows with the matching date and stock symbol.
    """
    # Convert the target_date to datetime
    target_date = pd.to_datetime(target_date, format='%Y%m%d')

    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], format='%Y-%m-%d')

    #
    # print(df.iloc[0][date_column].type)

    # Filter the DataFrame for the target date and stock
    matching_rows = df[(df[date_column] == target_date) & (df[stock_column] == target_stock)]

    if len(matching_rows) == 0:
        return 0, 0
    elif len(matching_rows) == 1:
        return matching_rows.iloc[0]['Prediction'], matching_rows.iloc[0]['Actual']
    else:
        for i, row in matching_rows.iterrows():
            if row['Prediction'] == 1:
                return 1, matching_rows.iloc[0]['Actual']

        return 0, matching_rows.iloc[0]['Actual']



class MLTurtleNaive(MLStockAlgorithmDaily):

    def __init__(self, stock_name, identifier=-1, time_period='Daily', reset_indexes=False, step=0, ml_to_use=None, split_to_do=None):
        """
        Initializes the TurtleNaive trading strategy instance.

        Args:
            stock_name (str): The name of the stock to be traded.
            identifier (int or str): Unique identifier for the trading session. Defaults to -1.
            time_period (str): The time period for trading (e.g., 'Daily'). Defaults to 'Daily'.
            reset_indexes (bool): Whether to reset DataFrame indexes. Defaults to False.
            step (int): Initial step or time period in the trading data. Defaults to 0.
        """

        # Initialize the superclass
        super().__init__(stock_name = stock_name, folder_name=TURTLE_DATA_NAME,reset_indexes = reset_indexes, step = step)

        self.ml_trade_df = pd.read_csv(r'C:\Users\theal\PycharmProjects\ensembleLegends\src\deepReplication\modeling\mlTurtleData\{}_predictions_test1turtles_{}.csv'.format(ml_to_use, split_to_do))



        # There are less state variables for turtles because using Unit class for trades found in
        # helperClasses/Unit

        self.in_trade = False
        self.active_trades = []
        self.long_units = []
        self.short_units = []
        self.num_short_units_bought = 0
        self.num_long_units_bought = 0
        self.curr_price = None
        self.next_open_price = None
        self.leverage = 1
        self.vars = {}
        self.actions = []
        self.identifier = identifier
        self.time_period = time_period
        self.strategy = "turtle_naive"



    def __str__(self):
        return f"TurtleNaive"

    def __repr__(self):
        return f"Turtle(stock_name='{self.stock_name}', reset_indexes={self.reset_indexes}, step={self.step})"

    # State at which to determine action from
    def get_state(self):
        """
        Retrieves the current state of the market for decision-making.

        Returns:
            dict: A dictionary containing the current market state, including prices and rolling window values.
        """
        date = self.df['date'].iloc[self.step]

        trade_action, actual_result = find_rows_by_date_and_stock(self.ml_trade_df, 'Date', 'Stock', date, self.stock_name)
        rolling_min_ten = self.df['Rolling_Min_10'].iloc[self.step]
        rolling_max_ten = self.df['Rolling_Max_10'].iloc[self.step]

        curr_price = self.df.iloc[self.step]['Close']
        self.curr_price = curr_price

        try:
            next_open_price = self.df.iloc[self.step + 1]['Open']
        except:
            next_open_price = curr_price

        self.next_open_price = next_open_price

        long_units = self.long_units
        short_units = self.short_units

        state_dict = {
            'Date': date,
            'TradeAction': trade_action,
            'ActualAction': actual_result,
            'RollingMin10': rolling_min_ten,
            'RollingMax10': rolling_max_ten,
            'CurrentPrice': curr_price,
            'NextOpenPrice': next_open_price,
            'LongUnits': long_units,
            'ShortUnits': short_units
        }

        return state_dict


    # Based on the above state, determine action
    def get_action(self, state):
        """
        Determines the trading action to take based on the current market state.

        Args:
            state (dict): The current state of the market.

        Returns:
            list: A list of actions to be taken.
        """
        action_list = []

        if state['TradeAction'] == 1:
            previous_prices_index = max(0, self.step - 20)
            previous_prices = self.df['Close'][previous_prices_index:self.step + 1].tolist()

            # Transform the list to a 2D array
            previous_prices_2d = np.array(previous_prices).reshape(-1, 1)

            # Initialize and apply the Min-Max Scaler
            scaler = MinMaxScaler()
            scaled_prices_2d = scaler.fit_transform(previous_prices_2d)

            # Convert back to a list
            scaled_prices = [price[0] for price in scaled_prices_2d]

            if scaled_prices[-1] > .9:
                action_list.append('EnterLong')
            elif scaled_prices[-1] < .1:
                action_list.append('EnterShort')
            else:

                print(state['Date'] ,state['TradeAction'], state['CurrentPrice'],previous_prices_2d, scaled_prices)
                # raise ValueError("Theoretically probably shouldn't trade here")
                print("Theoretically probably shouldn't trade here")
                action_list.append("Wait")

        if state['CurrentPrice'] > state['RollingMax10']:
            if len(state['ShortUnits']) > 0:
                action_list.append('ExitShort')

        if state['CurrentPrice'] < state['RollingMin10']:
            if len(state['LongUnits']) > 0:
                action_list.append('ExitLong')

        if len(action_list) == 0:
            action_list.append('Wait')

        # print(action_list, state['TradeAction'], state['ActualAction'], state["Date"])
        return action_list

    def process_action(self, actions, curr_price):
        """
        Processes the given trading actions.

        Args:
            actions (list): A list of actions to be processed.
            curr_price (float): The current price of the stock.
        """
        curr_date = str(self.df.iloc[self.step]["date"])
        if self.time_period == 'Daily':
            curr_time = 0
        else:
            curr_time = self.df.iloc[self.step]['time']


        try:
            next_open_price = self.df.iloc[self.step + 1]['Open']
        except:
            next_open_price = curr_price

        self.actions.append(actions)

        previous_prices_index = max(0, self.step - 50)
        previous_prices = self.df['Close'][previous_prices_index:self.step].tolist()

        for action in actions:

            if action == 'EnterLong':
                buy_unit = Unit('long', curr_price, next_open_price, curr_date, curr_time, previous_prices)
                self.long_units.append(buy_unit)
                self.num_long_units_bought += 1
            elif action == 'EnterShort':
                short_unit = Unit('short', curr_price, next_open_price, curr_date, curr_time, previous_prices)
                self.short_units.append(short_unit)
                self.num_short_units_bought += 1
            elif action == 'ExitLong':
                assert len(self.long_units) > 0
                for unit in self.long_units:
                    identifier = self.identifier
                    time_period = self.time_period
                    strategy = self.strategy
                    symbol = self.stock_name
                    start_date = unit.start_date
                    end_date = curr_date
                    start_time = unit.start_time
                    end_time = curr_time
                    enter_price = unit.enter_price
                    exit_price = curr_price
                    enter_price_open = unit.enter_price_open
                    exit_price_open = next_open_price
                    trade_type = unit.pos_type
                    transaction_cost_pct = TRANSACTION_COST_PCT + (TRANSACTION_COST_PCT / len(self.long_units))
                    transaction_cost_dollar = TRANSACTION_COST_DOLLAR + (TRANSACTION_COST_DOLLAR / len(self.long_units))
                    leverage = self.leverage
                    previous_prices = unit.previous_prices

                    self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy,
                                             symbol=symbol,
                                             start_date=start_date, end_date=end_date, start_time=start_time,
                                             end_time=end_time, enter_price=enter_price, enter_price_open=enter_price_open, exit_price_open=exit_price_open,
                                             exit_price=exit_price, trade_type=trade_type, transaction_cost_pct=transaction_cost_pct, transaction_cost_dollar=transaction_cost_dollar,
                                             leverage=leverage ,previous_prices=previous_prices)

                self.clear_long_positions()
            elif action == 'ExitShort':
                assert len(self.short_units) > 0
                for unit in self.short_units:
                    identifier = self.identifier
                    time_period = self.time_period
                    strategy = self.strategy
                    symbol = self.stock_name
                    start_date = unit.start_date
                    end_date = curr_date
                    start_time = unit.start_time
                    end_time = curr_time
                    enter_price = unit.enter_price
                    enter_price_open = unit.enter_price_open
                    exit_price = curr_price
                    exit_price_open = next_open_price
                    trade_type = unit.pos_type
                    transaction_cost_pct = TRANSACTION_COST_PCT + (TRANSACTION_COST_PCT / len(self.short_units))
                    transaction_cost_dollar = TRANSACTION_COST_DOLLAR + (TRANSACTION_COST_DOLLAR / len(self.short_units))
                    leverage = self.leverage
                    previous_prices = unit.previous_prices

                    self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy,
                                             symbol=symbol,
                                             start_date=start_date, end_date=end_date, start_time=start_time,
                                             end_time=end_time, enter_price=enter_price,exit_price=exit_price,
                                             enter_price_open=enter_price_open, exit_price_open=exit_price_open,
                                             trade_type=trade_type, transaction_cost_pct=transaction_cost_pct, transaction_cost_dollar=transaction_cost_dollar,leverage=leverage, previous_prices=previous_prices)

                self.clear_short_positions()
            elif action == 'Wait':
                pass
            else:
                raise ValueError("Invalid Action")



    def clear_long_positions(self):
        """
        Clears all long positions.
        """
        self.long_units = []


    def clear_short_positions(self):
        """
        Clears all short positions.
        """
        self.short_units = []


    def update_step(self, new_step):
        """
        Updates the current step in the trading strategy.

        Args:
            new_step (int): The new step or time period to update to.
        """
        self.step = new_step