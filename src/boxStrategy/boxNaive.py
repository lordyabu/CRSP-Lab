from src.helperClasses.unit import Unit
from src.helperClasses.traderBasic import StockAlgorithmDaily
from src.config import DATA_DIR, BOX_DATA_DIR
import os
import pandas as pd

class DarvasTrader(StockAlgorithmDaily):
    def __init__(self, stock_name, identifier=-1, time_period='Daily', reset_indexes=False, step=0):
        """
        Initializes the BoxNaive trading strategy instance. (Currently only does longs because profits off of parabolic price movement)

        Args:
            stock_name (str): The name of the stock to be traded.
            identifier (int or str): Unique identifier for the trading session. Defaults to -1.
            time_period (str): The time period for trading (e.g., 'Daily'). Defaults to 'Daily'.
            reset_indexes (bool): Whether to reset DataFrame indexes. Defaults to False.
            step (int): Initial step or time period in the trading data. Defaults to 0.
        """

        # Initialize the superclass
        super().__init__(stock_name = stock_name, folder_name=BOX_DATA_DIR,reset_indexes = reset_indexes, step = step)


        # There are less state variables for turtles because using Unit class for trades found in
        # helperClasses/Unit

        self.in_box = False
        self.in_trade = False
        self.active_trades = []
        self.long_units = []
        self.short_units = []
        self.num_short_units_bought = 0
        self.num_long_units_bought = 0
        self.prev_price = None
        self.curr_price = None
        self.leverage = 1
        self.vars = {}
        self.actions = []
        self.identifier = identifier
        self.time_period = time_period
        self.strategy = "box_naive"


    def __str__(self):
        return f"BoxNaive"

    def __repr__(self):
        return f"DarvasTrader(stock_name='{self.stock_name}', reset_indexes={self.reset_indexes}, step={self.step})"
    def get_state(self):
        """
        Retrieves the current state of the market for decision-making.

        Returns:
            dict: A dictionary containing the current market state, including prices and rolling window values.
        """
        date = self.df['date'].iloc[self.step]


        top_box = self.df['Box_Top'].iloc[self.step]
        bottom_box = self.df['Box_Bottom'].iloc[self.step]

        prev_in_box = self.in_box

        if top_box:
            self.in_box = True

        in_box = self.in_box

        prev_price = self.curr_price
        self.prev_price = prev_price

        curr_price = self.df.iloc[self.step]['Close']
        self.curr_price = curr_price

        long_units = self.long_units
        short_units = self.short_units

        state_dict = {
            'Date': date,
            'PrevInBox': prev_in_box,
            'InBox': in_box,
            'TopBox': top_box,
            'BottomBox': bottom_box,
            'PreviousPrice': prev_price,
            'CurrentPrice': curr_price,
            'LongUnits': long_units,
            'ShortUnits': short_units
        }

        return state_dict


    def get_action(self, state):
        if not state['InBox'] and state['PrevInBox']:
            if state['CurrentPrice'] > state['PreviousPrice']:
                return "EnterLong"
            else:
                return "ExitLong"
        else:
            return "Wait"

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

        self.actions.append(actions)

        previous_prices_index = max(0, self.step - 50)
        previous_prices = self.df['Close'][previous_prices_index:self.step].tolist()

        for action in actions:

            if action == 'EnterLong':
                buy_unit = Unit('long', curr_price, curr_date, curr_time, previous_prices)
                self.long_units.append(buy_unit)
                self.num_long_units_bought += 1
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
                    trade_type = unit.pos_type
                    leverage = self.leverage
                    previous_prices = unit.previous_prices

                    self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy,
                                             symbol=symbol,
                                             start_date=start_date, end_date=end_date, start_time=start_time,
                                             end_time=end_time, enter_price=enter_price,
                                             exit_price=exit_price, trade_type=trade_type, leverage=leverage ,previous_prices=previous_prices)

                self.clear_long_positions()
            elif action == 'Wait':
                pass
            else:
                raise ValueError("Invalid Action")

    def clear_long_positions(self):
        """
        Clears all long positions.
        """
        self.long_units = []

    def update_step(self, new_step):
        """
        Updates the current step in the trading strategy.

        Args:
            new_step (int): The new step or time period to update to.
        """
        self.step = new_step