# 1. TRUE RANGE / N / PDN
# 2. Daollar Volatility Adjustment
# 3. Volatility adjusted position units (Not as important for purpose of project) / Units as measure of risk

# 4. Entries. Is N calculated using 55 instead of 20?
from dataclasses import dataclass
import pandas as pd


@dataclass
class Unit:
    pos_type: str
    enter_price: float

class basic_turtle_class:
    def __init__(self):
        self.sum_pnl_returns = 0
        self.num_completed_units = 0

        self.sum_pnl_all = 0

        self.num_long_units_bought = 0
        self.num_short_units_bought = 0

        self.actions_taken = []


        self.long_units = []
        self.short_units = []
        self.df = pd.read_csv("AAPLTurtle.csv", index_col=[0])

        self.step = 0

        self.rolling_window_length_enter = 20
        self.rolling_window_length_exit = 10

    def get_state(self):
        date = self.df['date'].iloc[self.step]

        rolling_min_ten = self.df['Rolling_Min_10'].iloc[self.step]
        rolling_max_ten = self.df['Rolling_Max_10'].iloc[self.step]
        rolling_min_twenty = self.df['Rolling_Min_20'].iloc[self.step]
        rolling_max_twenty = self.df['Rolling_Max_20'].iloc[self.step]

        curr_price = self.df.iloc[self.step]['Close']

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

    def get_actions(self, state):
        action_list = []

        # Assuming 'Date' is a key in your state dictionary representing the current day
        current_day = state['Date']

        if pd.isna(state['RollingMax20']):
            print(f"{current_day}: RollingMax20 is NA, deciding to Wait")
            action_list.append('Wait')
            self.actions_taken.append((state['Date'], action_list))
            return action_list

        if state['CurrentPrice'] > state['RollingMax20']:
            print(
                f"{current_day}: CurrentPrice {state['CurrentPrice']} is greater than RollingMax20 {state['RollingMax20']}, deciding to EnterLong")
            action_list.append('EnterLong')

        if state['CurrentPrice'] < state['RollingMin20']:
            print(
                f"{current_day}: CurrentPrice {state['CurrentPrice']} is less than RollingMin20 {state['RollingMin20']}, deciding to EnterShort")
            action_list.append('EnterShort')

        if state['CurrentPrice'] > state['RollingMax10']:
            if len(state['ShortUnits']) > 0:
                print(
                    f"{current_day}: CurrentPrice {state['CurrentPrice']} is greater than RollingMax10 {state['RollingMax10']} and there are short positions, deciding to ExitShort")
                action_list.append('ExitShort')

        if state['CurrentPrice'] < state['RollingMin10']:
            if len(state['LongUnits']) > 0:
                print(
                    f"{current_day}: CurrentPrice {state['CurrentPrice']} is less than RollingMax10 {state['RollingMax10']} and there are long positions, deciding to ExitLong")
                action_list.append('ExitLong')

        if len(action_list) == 0:
            print(f"{current_day}: No conditions met, deciding to Wait")
            action_list.append('Wait')

        self.actions_taken.append((state['Date'], action_list))
        return action_list

    def process_actions(self, actions, curr_price):
        for action in actions:
            if action == 'EnterLong':
                buy_unit = Unit('long', curr_price)
                self.long_units.append(buy_unit)
                self.num_long_units_bought += 1
            elif action == 'EnterShort':
                short_unit = Unit('short', curr_price)
                self.short_units.append(short_unit)
                self.num_short_units_bought += 1
            elif action == 'ExitLong':
                assert len(self.long_units) > 0
                for unit in self.long_units:
                    simple_return = ((curr_price - unit.enter_price) / unit.enter_price) * 100
                    self.sum_pnl_returns += simple_return
                    self.num_completed_units += 1

                self.clear_long_positions()
            elif action == 'ExitShort':
                assert len(self.short_units) > 0
                for unit in self.short_units:
                    simple_return = ((unit.enter_price - curr_price) / curr_price) * 100
                    self.sum_pnl_returns += simple_return
                    self.num_completed_units += 1

                self.clear_short_positions()
            elif action == 'Wait':
                pass
            else:
                raise ValueError("Invalid Action")

        print(self.sum_pnl_returns)

    def save_to_csv(self):
        # Convert the list of actions to a DataFrame
        actions_df = pd.DataFrame(self.actions_taken, columns=['date', 'Actions'])

        # Merge actions DataFrame with the original DataFrame on 'Date'
        merged_df = pd.merge(self.df, actions_df, on='date', how='left')

        # Save to CSV
        merged_df.to_csv('AAPLTurtleTrades.csv', index=False)
    def clear_long_positions(self):
        self.long_units = []


    def clear_short_positions(self):
        self.short_units = []
    def update_step(self, step):
        self.step = step


    def increment_step(self):
        self.step += 1


    def calculate_current_positions(self, curr_price):
        self.sum_pnl_all = self.sum_pnl_returns

        for unit in self.long_units:
            simple_return = ((curr_price - unit.enter_price) / unit.enter_price) * 100

            self.sum_pnl_all += simple_return


        for unit in self.short_units:
            simple_return = ((unit.enter_price - curr_price) / curr_price) * 100
            self.sum_pnl_all += simple_return


aapl_turtle = basic_turtle_class()

while(aapl_turtle.step < len(aapl_turtle.df.index)):
    state = aapl_turtle.get_state()
    actions = aapl_turtle.get_actions(state)
    aapl_turtle.process_actions(actions, state['CurrentPrice'])
    aapl_turtle.increment_step()


aapl_turtle.calculate_current_positions(state['CurrentPrice'])
aapl_turtle.save_to_csv()

print(aapl_turtle.sum_pnl_returns, aapl_turtle.sum_pnl_all, aapl_turtle.num_completed_units)




