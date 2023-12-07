# This script features the BollingerNaive class, an extension of the StockAlgorithmDaily class, designed to implement a Bollinger Band-based trading strategy.
# The class encapsulates the logic for making trading decisions based on Bollinger Bands, handling the entry and exit of trades,
# updating the strategy's state, and processing actions for each step in the trading data.
# It offers functionality to evaluate the current market state, decide on trading actions (like entering long or short positions),
# and process these actions through the trading period.

from src.helperClasses.traderBasic import MLStockAlgorithmDaily
from src.config import DATA_DIR, BOLLINGER_DATA_NAME, TRANSACTION_COST_PCT, TRANSACTION_COST_DOLLAR, DEEP_PREDICTION_BOLLINGER_TWO
import os
from src.helperClasses.unit import Unit
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

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

class MLBollingerNaiveTwo(MLStockAlgorithmDaily):

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
            ml_to_use (str): Which ML strategy to use.
            split_to_do (str): Which Split to use.
        """

        super().__init__(stock_name=stock_name, folder_name=BOLLINGER_DATA_NAME, reset_indexes=reset_indexes, step=step)
        bollinger_two_path = os.path.join(DEEP_PREDICTION_BOLLINGER_TWO, '{}_predictions_test22bollinger_{}.csv'.format(ml_to_use, split_to_do))

        self.ml_trade_df = pd.read_csv(bollinger_two_path)

        self.in_trade = False
        self.curr_price = None
        self.next_price_open = None
        self.stop_loss_price = None
        self.leverage = 1
        self.vars = {}

        self.identifier = identifier
        self.time_period = time_period
        self.band_data = band_data_name

        self.long_units = []
        self.short_units = []
        self.num_short_units_bought = 0
        self.num_long_units_bought = 0


        self.moving_stoploss = moving_stop_loss
        if moving_stop_loss:
            self.strategy = "bollinger_naive_dynamic_sl"
        else:
            self.strategy = "bollinger_naive_static_sl"


    def __str__(self):
        if self.moving_stoploss:
            return f"BollingerNaiveDynamicSL"
        else:
            return f"BollingerNaiveStaticSL"

    def __repr__(self):
        return f"Bollinger(stock_name='{self.stock_name}', reset_indexes={self.reset_indexes}, step={self.step})"

    # State at which to determine action from
    def get_state(self):
        """
        Retrieves the current state of the market for decision-making.

        Returns:
            dict: A dictionary containing the current market state, including prices and Bollinger Band values.
        """

        date = str(self.df['date'].iloc[self.step])


        upper_band = self.df.iloc[self.step][f'Upper_Band_{self.band_data}']
        lower_band = self.df.iloc[self.step][f'Lower_Band_{self.band_data}']
        upper_band_3sd = self.df.iloc[self.step][f'Upper_Band_3SD_{self.band_data}']
        lower_band_3sd = self.df.iloc[self.step][f'Lower_Band_3SD_{self.band_data}']
        middle_band = self.df.iloc[self.step][f'Middle_Band_{self.band_data}']

        trade_action, actual_result = find_rows_by_date_and_stock(self.ml_trade_df, 'Date', 'Stock', date, self.stock_name)


        curr_close = self.df.iloc[self.step]['Close']
        self.curr_price = curr_close

        # Edge case on last instance of dataset
        try:
            next_price_open = self.df.iloc[self.step + 1]['Open']
        except:
            next_price_open = curr_close

        self.next_price_open = next_price_open

        if len(self.long_units) > 0 and len(self.short_units) == 0:
            position_type = 'long'
        elif len(self.short_units) > 0 and len(self.long_units) == 0:
            position_type = 'short'
        elif len(self.long_units) == 0 and len(self.short_units) == 0:
            position_type = None
        else:
            raise ValueError("Can't have long and short units simultaneously")


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

        previous_prices_index = max(0, self.step - 50)
        previous_prices = self.df['Close'][previous_prices_index:self.step].tolist()

        state_vars = {
            'Date': date,
            'TradeAction': trade_action,
            'ActualAction': actual_result,
            'Close': curr_close,
            'NextOpenPrice': next_price_open,
            'LowerBand': lower_band,
            'UpperBand': upper_band,
            'MiddleBand': middle_band,
            'PositionType': position_type,
            'LowerBand3SD': lower_band_3sd,
            'UpperBand3SD': upper_band_3sd,
            'TargetPrice': target_price,
            'StopLossPrice': stop_loss_price,
            'PreviousPrices': previous_prices
        }

        return state_vars

    # Based on the above state, determine action
    def get_action(self, curr_state):
        """
        Determines the trading actions to take based on the current market state.

        Args:
            curr_state (dict): The current state of the market.

        Returns:
            list: A list of strings representing the trading actions to be taken.
        """
        close = curr_state['Close']
        upper_band = curr_state['UpperBand']
        lower_band = curr_state['LowerBand']
        position_type = curr_state['PositionType']
        stop_loss_price = curr_state['StopLossPrice']
        target_price = curr_state['TargetPrice']

        action_list = []

        if position_type in ['long', 'short']:
            if position_type == 'long':
                if close >= target_price:
                    action_list.append('ExitLong')
                elif close < stop_loss_price:
                    action_list.append('ExitLong')
                else:
                    action_list.append('Wait')
            elif position_type == 'short':
                if close <= target_price:
                    action_list.append('ExitShort')
                elif close > stop_loss_price:
                    action_list.append('ExitShort')
                else:
                    action_list.append('Wait')
        else:
            action_list.append('Null')


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
                action_list.append("EnterShort")
            elif scaled_prices[-1] < .2:
                action_list.append("EnterLong")
            else:

                # print(curr_state['Date'], curr_state['TradeAction'], curr_state['Close'], previous_prices_2d,
                #       scaled_prices)
                # raise ValueError("Theoretically probably shouldn't trade here")
                # print("Theoretically probably shouldn't trade here")
                action_list.append("Wait")

        return action_list

    def process_action(self, actions, state):
        """
        Processes a given trading action.

        Args:
            action_str (str): A string representing the trading action to be processed.
        """
        curr_price = state['Close']
        next_price_open = state['NextOpenPrice']
        curr_date = state['Date']
        curr_time = 0
        previous_prices = state['PreviousPrices']


        for action in actions:
            if action == 'EnterLong':
                assert len(self.short_units) == 0
                buy_unit = Unit('long', curr_price, next_price_open, curr_date, curr_time, previous_prices)
                self.long_units.append(buy_unit)
                self.num_long_units_bought += 1
            elif action == 'EnterShort':
                assert len(self.long_units) == 0
                short_unit = Unit('short', curr_price, next_price_open, curr_date, curr_time, previous_prices)
                self.short_units.append(short_unit)
                self.num_short_units_bought += 1
            elif action == 'ExitLong':
                assert len(self.long_units) > 0 and len(self.short_units) == 0
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
                    enter_price_open = unit.enter_price_open
                    exit_price = curr_price
                    exit_price_open = next_price_open
                    trade_type = unit.pos_type
                    transaction_cost_pct = TRANSACTION_COST_PCT + (TRANSACTION_COST_PCT / len(self.long_units))
                    transaction_cost_dollar = TRANSACTION_COST_DOLLAR + (TRANSACTION_COST_DOLLAR / len(self.long_units))
                    leverage = self.leverage
                    previous_prices = unit.previous_prices

                    self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy,
                                             symbol=symbol,
                                             start_date=start_date, end_date=end_date, start_time=start_time,
                                             end_time=end_time, enter_price=enter_price,exit_price=exit_price,
                                             enter_price_open=enter_price_open, exit_price_open=exit_price_open,
                                             trade_type=trade_type, transaction_cost_pct=transaction_cost_pct,
                                        transaction_cost_dollar=transaction_cost_dollar,leverage=leverage ,previous_prices=previous_prices)

                self.clear_long_positions()
            elif action == 'ExitShort':
                assert len(self.short_units) > 0 and len(self.long_units) == 0
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
                    exit_price_open = next_price_open
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
                                             trade_type=trade_type, transaction_cost_pct=transaction_cost_pct,
                                        transaction_cost_dollar=transaction_cost_dollar,leverage=leverage ,previous_prices=previous_prices)

                self.clear_short_positions()
            elif action == 'Wait' or action == "Null":
                pass
            else:
                raise ValueError("Invalid Action")




    def update_step(self, new_step):
        """
        Updates the current step in the trading strategy.

        Args:
            new_step (int): The new step or time period to update to.
        """
        self.step = new_step


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