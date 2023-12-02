# The TurtleNaive class, extending StockAlgorithmDaily, implements a simplified Turtle trading strategy for stock markets.
# It manages trading positions, decision-making based on market state, and execution of trading actions in line with the Turtle strategy.
# Key features include tracking and updating long and short positions, determining trade actions based on rolling window calculations,
# processing these actions, and maintaining a step-wise approach through the trading dataset.
# The class is designed to simulate and analyze the Turtle trading strategy's performance for specific stocks over time.

from src.helperClasses.unit import Unit
from src.helperClasses.traderBasic import StockAlgorithmDaily
from src.config import DATA_DIR, TURTLE_DATA_NAME, TRANSACTION_COST_PCT, TRANSACTION_COST_DOLLAR
import os
import pandas as pd

class TurtleNaive(StockAlgorithmDaily):

    def __init__(self, stock_name, identifier=-1, time_period='Daily', reset_indexes=False, step=0):
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

        rolling_min_ten = self.df['Rolling_Min_10'].iloc[self.step]
        rolling_max_ten = self.df['Rolling_Max_10'].iloc[self.step]
        rolling_min_twenty = self.df['Rolling_Min_20'].iloc[self.step]
        rolling_max_twenty = self.df['Rolling_Max_20'].iloc[self.step]

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
            'RollingMin10': rolling_min_ten,
            'RollingMax10': rolling_max_ten,
            'RollingMin20': rolling_min_twenty,
            'RollingMax20': rolling_max_twenty,
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

        if pd.isna(state['RollingMax20']):
            action_list.append('Wait')
            self.actions.append((state['Date'], action_list))
            return action_list

        if state['CurrentPrice'] > state['RollingMax20']:
            action_list.append('EnterLong')

        if state['CurrentPrice'] < state['RollingMin20']:
            action_list.append('EnterShort')

        if state['CurrentPrice'] > state['RollingMax10']:
            if len(state['ShortUnits']) > 0:
                action_list.append('ExitShort')

        if state['CurrentPrice'] < state['RollingMin10']:
            if len(state['LongUnits']) > 0:
                action_list.append('ExitLong')

        if len(action_list) == 0:
            action_list.append('Wait')

        self.actions.append((state['Date'], action_list))
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