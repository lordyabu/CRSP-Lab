# This script features the BollingerNaive class, an extension of the StockAlgorithmDaily class, designed to implement a Bollinger Band-based trading strategy.
# The class encapsulates the logic for making trading decisions based on Bollinger Bands, handling the entry and exit of trades,
# updating the strategy's state, and processing actions for each step in the trading data.
# It offers functionality to evaluate the current market state, decide on trading actions (like entering long or short positions),
# and process these actions through the trading period.
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from src.helperClasses.traderBasic import MLStockAlgorithmDaily
from src.config import DATA_DIR, BOLLINGER_DATA_NAME, TRANSACTION_COST_PCT, TRANSACTION_COST_DOLLAR, DEEP_PREDICTION_BOLLINGER_ONE
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
class MLBollingerNaive(MLStockAlgorithmDaily):

    def __init__(self, stock_name, band_data_name='Default', identifier=-1, time_period='Daily', reset_indexes=False,
                 step=0, moving_stop_loss=True, ml_to_use=None, split_to_do=None):
        """
        Initializes the BollingerNaive trading strategy instance.

        Args:
            stock_name (str): The name of the stock to be traded.
            band_data_name (str): Identifier for the Bollinger Band data. Defaults to 'Default'.
            identifier (int or str): Unique identifier for the trading session. Defaults to -1.
            time_period (str): The time period for trading (e.g., 'Daily'). Defaults to 'Daily'.
            reset_indexes (bool): Whether to reset DataFrame indexes. Defaults to False.
            step (int): Initial step or time period in the trading data. Defaults to 0.
            moving_stop_loss (bool): Flag to use moving stop-loss. Defaults to True.
        """

        super().__init__(stock_name=stock_name, folder_name=BOLLINGER_DATA_NAME, reset_indexes=reset_indexes, step=step)

        bollinger_one_path = os.path.join(DEEP_PREDICTION_BOLLINGER_ONE, '{}_predictions_test11bollinger_{}.csv'.format(ml_to_use, split_to_do))

        self.ml_trade_df = pd.read_csv(bollinger_one_path)

        self.in_trade = False
        self.enter_trade_date = None
        self.exit_trade_date = None
        self.enter_trade_time = None
        self.exit_trade_time = None
        self.enter_trade_price = None
        self.exit_trade_price = None
        self.enter_trade_price_open = None
        self.exit_trade_price_open = None
        self.trade_direction = None
        self.band_entry_type = None
        self.curr_price = None
        self.stop_loss_price = None
        self.previous_prices = None
        self.leverage = 1
        self.vars = {}

        # Not being used currently for anything
        self.actions = []

        self.identifier = identifier
        self.time_period = time_period
        self.band_data = band_data_name
        self.strategy = "bollinger_naive_dynamic_sl"
        self.moving_stoploss = moving_stop_loss

    def __str__(self):
        return f"BollingerNaiveDynamicSL"

    def __repr__(self):

        return f"Bollinger(stock_name='{self.stock_name}', reset_indexes={self.reset_indexes}, step={self.step})"

    # State at which to determine action from
    def get_state(self):
        """
        Retrieves the current state of the market for decision-making.

        Returns:
            dict: A dictionary containing the current market state, including prices and Bollinger Band values.
        """
        date = self.df['date'].iloc[self.step]

        upper_band = self.df.iloc[self.step][f'Upper_Band_{self.band_data}']
        lower_band = self.df.iloc[self.step][f'Lower_Band_{self.band_data}']
        upper_band_3sd = self.df.iloc[self.step][f'Upper_Band_3SD_{self.band_data}']
        lower_band_3sd = self.df.iloc[self.step][f'Lower_Band_3SD_{self.band_data}']
        middle_band = self.df.iloc[self.step][f'Middle_Band_{self.band_data}']

        trade_action, actual_result = find_rows_by_date_and_stock(self.ml_trade_df, 'Date', 'Stock', date, self.stock_name)


        curr_close = self.df.iloc[self.step]['Close']
        self.curr_price = curr_close

        position_type = self.trade_direction
        band_entry = self.band_entry_type

        if position_type == 'long':
            if not self.moving_stoploss:
                stop_loss_price = self.stop_loss_price
            else:
                self.stop_loss_price = lower_band_3sd
                stop_loss_price = lower_band_3sd

            target_price = middle_band
        elif position_type == 'short':
            if not self.moving_stoploss:
                stop_loss_price = self.stop_loss_price
            else:
                self.stop_loss_price = upper_band_3sd
                stop_loss_price = upper_band_3sd
            target_price = middle_band
        else:
            stop_loss_price = None
            target_price = None

        print(date,trade_action, actual_result)

        state_vars = {
            'Date': date,
            'Close': curr_close,
            'TradeAction': trade_action,
            'ActualResult': actual_result,
            'LowerBand': lower_band,
            'UpperBand': upper_band,
            'MiddleBand': middle_band,
            'PositionType': position_type,
            'BandEntry': band_entry,
            'LowerBand3SD': lower_band_3sd,
            'UpperBand3SD': upper_band_3sd,
            'TargetPrice': target_price,
            'StopLossPrice': stop_loss_price
        }

        return state_vars

    # Based on the above state, determine action
    def get_action(self, curr_state):
        """
        Determines the trading action to take based on the current market state.

        Args:
            curr_state (dict): The current state of the market.

        Returns:
            str: A string representing the trading action to be taken.
        """
        close = curr_state['Close']
        upper_band = curr_state['UpperBand']
        lower_band = curr_state['LowerBand']
        position_type = curr_state['PositionType']
        stop_loss_price = curr_state['StopLossPrice']
        target_price = curr_state['TargetPrice']
        action_str = ""

        if position_type in ['long', 'short']:
            if position_type == 'long':
                if close >= target_price:
                    action_str = 'ExitLong'
                elif close < stop_loss_price:
                    action_str = 'ExitLong'
                else:
                    action_str = 'Hold'
            elif position_type == 'short':
                if close <= target_price:
                    action_str = 'ExitShort'
                elif close > stop_loss_price:
                    action_str = 'ExitShort'
                else:
                    action_str = 'Hold'
        elif position_type is None:
            if curr_state['TradeAction'] == 1:
                previous_prices_index = max(0, self.step - 20)
                previous_prices = self.df['Close'][previous_prices_index:self.step + 1].tolist()

                # Transform the list to a 2D array
                previous_prices_2d = np.array(previous_prices).reshape(-1, 1)

                # Initialize and apply the Min-Max Scaler
                scaler = MinMaxScaler()
                scaled_prices_2d = scaler.fit_transform(previous_prices_2d)

                # Convert back to a list
                scaled_prices = [price[0] for price in scaled_prices_2d]

                if scaled_prices[-1] > .8:
                    action_str = "EnterShort"
                elif scaled_prices[-1] < .2:
                    action_str = "EnterLong"
                else:

                    print(curr_state['Date'], curr_state['TradeAction'], curr_state['CurrentPrice'], previous_prices_2d, scaled_prices)
                    # raise ValueError("Theoretically probably shouldn't trade here")
                    print("Theoretically probably shouldn't trade here")
                    action_str = "Wait"
            else:
                action_str = "Wait"
        else:
            raise ValueError(f"Invalid position type {position_type}.")

        return action_str

    def process_action(self, action_str):
        """
        Processes a given trading action.

        Args:
            action_str (str): A string representing the trading action to be processed.
        """
        sl_upper_band = self.df.iloc[self.step][f'Upper_Band_3SD_{self.band_data}']
        sl_lower_band = self.df.iloc[self.step][f'Lower_Band_3SD_{self.band_data}']

        if action_str == 'EnterLong' and self.in_trade:
            raise ValueError("Cannot enter long while in trade")

        if action_str == 'EnterShort' and self.in_trade:
            raise ValueError("Cannot enter short while in trade")

        if action_str == 'ExitLong' and not self.in_trade:
            raise ValueError("Cannot exit long while not in long")

        if action_str == 'ExitShort' and not self.in_trade:
            raise ValueError("Cannot exit short while not in short")

        if action_str == 'EnterLong':
            self.actions.append(1)
            self.start_position('long')
            self.stop_loss_price = sl_lower_band
        elif action_str == 'EnterShort':
            self.actions.append(-1)
            self.start_position('short')
            self.stop_loss_price = sl_upper_band
        elif action_str == 'ExitLong' or action_str == 'ExitShort':
            self.exit_position()
        elif action_str == 'Hold':
            self.actions.append(0)
        elif action_str == 'Wait':
            self.actions.append(0)
        else:
            raise ValueError(f"Invalid action string {action_str}.")

    def start_position(self, action):
        """
        Starts a new trading position based on the specified action.

        Args:
            action (str): The action to start the position ('long' or 'short').
        """
        self.in_trade = True
        self.curr_price = self.df.iloc[self.step]['Close']


        previous_prices_index = max(0, self.step - 50)
        self.previous_prices = self.df['Close'][previous_prices_index:self.step].tolist()
        self.enter_trade_date = str(self.df.iloc[self.step]["date"])

        if self.time_period != 'Daily':
            self.enter_trade_time = '160000'
        else:
            self.enter_trade_time = self.step
        self.enter_trade_price = self.curr_price

        # On the rare case we enter a position on the last day of the dataset
        try:
            self.enter_trade_price_open = self.df.iloc[self.step + 1]['Open']
        except:
            self.enter_trade_price_open = self.enter_trade_price

        if action == 'long':
            self.trade_direction = 'long'
            self.band_entry_type = 'lower'
        elif action == 'short':
            self.trade_direction = 'short'
            self.band_entry_type = 'upper'
        else:
            raise ValueError(f"Invalid position type {action}.")

    def exit_position(self):
        """
        Exits the current trading position and logs the trade details.

        Returns:
            str: A string indicating the type of position that was closed.
        """
        self.exit_trade_date = str(self.df.iloc[self.step]["date"])
        self.curr_price = self.df.iloc[self.step]['Close']
        self.exit_trade_price = self.curr_price

        # On the rare case we enter a position on the last day of the dataset
        try:
            self.exit_trade_price_open = self.df.iloc[self.step + 1]['Open']
        except:
            self.exit_trade_price_open = self.exit_trade_price

        if self.time_period != 'Daily':
            self.exit_trade_time = '160000'
        else:
            self.exit_trade_time = self.step

        identifier = self.identifier
        time_period = self.time_period
        strategy = self.strategy
        symbol = self.stock_name
        start_date = self.enter_trade_date
        end_date = self.exit_trade_date
        start_time = self.enter_trade_time
        end_time = self.exit_trade_time
        enter_price = self.enter_trade_price
        exit_price = self.exit_trade_price
        enter_price_open = self.enter_trade_price_open
        exit_price_open = self.exit_trade_price_open
        trade_type = self.trade_direction
        leverage = self.leverage
        previous_prices = self.previous_prices

        # Because this trades 1 unit at a time we can calculate transaction costs below as follows
        self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy, symbol=symbol,
                                 start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time,
                                 enter_price=enter_price, exit_price=exit_price, enter_price_open=enter_price_open,
                                 exit_price_open=exit_price_open,trade_type=trade_type,
                                 transaction_cost_pct=TRANSACTION_COST_PCT * 2, transaction_cost_dollar=TRANSACTION_COST_DOLLAR * 2,
                                 leverage=leverage,
                                 previous_prices=previous_prices)

        # If the current trade is a long, add 2 too actions, else -2
        # Note. This(self.actions) is not being used currently
        if trade_type == 'long':
            self.actions.append(2)
        elif trade_type == 'short':
            self.actions.append(-2)
        else:
            raise ValueError(f"Invalid position type {trade_type}.")
        #

        self.in_trade = False
        self.enter_trade_date = None
        self.exit_trade_date = None
        self.enter_trade_time = None
        self.exit_trade_time = None
        self.enter_trade_price = None
        self.exit_trade_price = None
        self.enter_trade_price_open = None
        self.exit_trade_price_open = None
        self.trade_direction = None
        self.band_entry_type = None
        self.curr_price = None
        self.stop_loss_price = None
        self.previous_prices = None
        self.leverage = 1

    def update_step(self, new_step):
        """
        Updates the current step in the trading strategy.

        Args:
            new_step (int): The new step or time period to update to.
        """
        self.step = new_step
