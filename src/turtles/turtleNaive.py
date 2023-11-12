from src.helperClasses.unit import Unit
from src.helperClasses.traderBasic import StockAlgorithmDaily
from src.config import DATA_DIR
import os
import pandas as pd

class TurtleNaive(StockAlgorithmDaily):

    def __init__(self, stock_name, rolling_window_name='Default', identifier=-1, time_period='Daily', reset_indexes=False, step=0):
        # Initialize the superclass
        self.trade_log_dir_full = os.path.join(DATA_DIR, 'tradeData')

        try:
            self.trade_log_dir_ticker = os.path.join(DATA_DIR, 'tradeData', 'allTrades.csv')
        except:
            # Make folder first then try directory
            pass


        super().__init__(stock_name = stock_name, folder_name='turtleData',reset_indexes = reset_indexes, step = step)

        self.in_trade = False

        self.active_trades = []

        self.long_units = []
        self.short_units = []

        self.num_short_units_bought = 0
        self.num_long_units_bought = 0


        self.curr_price = None

        self.leverage = 1

        self.vars = {}

        self.actions = []

        self.identifier = identifier
        self.time_period = time_period
        self.rolling_window_data = rolling_window_name

        self.strategy = "turtle_naive"


    def __str__(self):
        # Provide a meaningful string representation of this class
        return f"TurtleNaive"

    def __repr__(self):
        # Provide a string that could be used to recreate this object
        return f"Turtle(stock_name='{self.stock_name}', reset_indexes={self.reset_indexes}, step={self.step}, rolling_window_length={self.rolling_window_length})"

    # State at which to determine action from
    def get_state(self):
        date = self.df['date'].iloc[self.step]

        rolling_min_ten = self.df['Rolling_Min_10'].iloc[self.step]
        rolling_max_ten = self.df['Rolling_Max_10'].iloc[self.step]
        rolling_min_twenty = self.df['Rolling_Min_20'].iloc[self.step]
        rolling_max_twenty = self.df['Rolling_Max_20'].iloc[self.step]

        curr_price = self.df.iloc[self.step]['Close']
        self.curr_price = curr_price

        long_units = self.long_units
        short_units = self.short_units

        state_dict = {
            'Date': date,
            'RollingMin10': rolling_min_ten,
            'RollingMax10': rolling_max_ten,
            'RollingMin20': rolling_min_twenty,
            'RollingMax20': rolling_max_twenty,
            'CurrentPrice': curr_price,
            'LongUnits': long_units,
            'ShortUnits': short_units
        }

        return state_dict


    # Based on the above state, determine action
    def get_action(self, state):
        action_list = []

        # Assuming 'Date' is a key in your state dictionary representing the current day
        current_day = state['Date']

        if pd.isna(state['RollingMax20']):
            # print(f"{current_day}: RollingMax20 is NA, deciding to Wait")
            action_list.append('Wait')
            self.actions.append((state['Date'], action_list))
            return action_list

        if state['CurrentPrice'] > state['RollingMax20']:
            # print(
            #     f"{current_day}: CurrentPrice {state['CurrentPrice']} is greater than RollingMax20 {state['RollingMax20']}, deciding to EnterLong")
            action_list.append('EnterLong')

        if state['CurrentPrice'] < state['RollingMin20']:
            # print(
            #     f"{current_day}: CurrentPrice {state['CurrentPrice']} is less than RollingMin20 {state['RollingMin20']}, deciding to EnterShort")
            action_list.append('EnterShort')

        if state['CurrentPrice'] > state['RollingMax10']:
            if len(state['ShortUnits']) > 0:
                # print(
                #     f"{current_day}: CurrentPrice {state['CurrentPrice']} is greater than RollingMax10 {state['RollingMax10']} and there are short positions, deciding to ExitShort")
                action_list.append('ExitShort')

        if state['CurrentPrice'] < state['RollingMin10']:
            if len(state['LongUnits']) > 0:
                # print(
                #     f"{current_day}: CurrentPrice {state['CurrentPrice']} is less than RollingMax10 {state['RollingMax10']} and there are long positions, deciding to ExitLong")
                action_list.append('ExitLong')

        if len(action_list) == 0:
            # print(f"{current_day}: No conditions met, deciding to Wait")
            action_list.append('Wait')

        self.actions.append((state['Date'], action_list))
        return action_list

    def process_action(self, actions, curr_price):
        curr_date = str(self.df.iloc[self.step]["date"])
        if self.time_period == 'Daily':
            curr_time = 0
        else:
            curr_time = self.df.iloc[self.step]['time']

        self.actions.append(actions)

        for action in actions:
            if action == 'EnterLong':
                buy_unit = Unit('long', curr_price, curr_date, 0)
                self.long_units.append(buy_unit)
                self.num_long_units_bought += 1
            elif action == 'EnterShort':
                short_unit = Unit('short', curr_price, curr_date, 0)
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
                    trade_type = unit.pos_type
                    leverage = self.leverage

                    self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy,
                                             symbol=symbol,
                                             start_date=start_date, end_date=end_date, start_time=start_time,
                                             end_time=end_time, enter_price=enter_price,
                                             exit_price=exit_price, trade_type=trade_type, leverage=leverage)

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
                    exit_price = curr_price
                    trade_type = unit.pos_type
                    leverage = self.leverage

                    self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy,
                                             symbol=symbol,
                                             start_date=start_date, end_date=end_date, start_time=start_time,
                                             end_time=end_time, enter_price=enter_price,
                                             exit_price=exit_price, trade_type=trade_type, leverage=leverage)

                self.clear_short_positions()
            elif action == 'Wait':
                pass
            else:
                raise ValueError("Invalid Action")



    def clear_long_positions(self):
        self.long_units = []


    def clear_short_positions(self):
        self.short_units = []


    def update_step(self, new_step):
        # Update the step (time period) for the strategy
        self.step = new_step