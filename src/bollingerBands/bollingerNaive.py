# This script features the BollingerNaive class, an extension of the StockAlgorithmDaily class, designed to implement a Bollinger Band-based trading strategy. 
# The class encapsulates the logic for making trading decisions based on Bollinger Bands, handling the entry and exit of trades, 
# updating the strategy's state, and processing actions for each step in the trading data. 
# It offers functionality to evaluate the current market state, decide on trading actions (like entering long or short positions), 
# and process these actions through the trading period. 

from src.helperClasses.traderBasic import StockAlgorithmDaily
from src.config import DATA_DIR, BOLLINGER_DATA_NAME
import os


class BollingerNaive(StockAlgorithmDaily):

    def __init__(self, stock_name, band_data_name='Default', identifier=-1, time_period='Daily', reset_indexes=False,
                 step=0, moving_stop_loss=True):
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

        self.trade_log_dir_full = os.path.join(DATA_DIR, 'tradeData')
        self.in_trade = False
        self.enter_trade_date = None
        self.exit_trade_date = None
        self.enter_trade_time = None
        self.exit_trade_time = None
        self.enter_trade_price = None
        self.exit_trade_price = None
        self.trade_direction = None
        self.band_entry_type = None
        self.curr_price = None
        self.stop_loss_price = None
        self.previous_prices = None
        self.leverage = 1
        self.vars = {}

        # Not being used currently for anything
        self.actions = []
        #

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

        upper_band = self.df.iloc[self.step][f'Upper_Band_{self.band_data}']
        lower_band = self.df.iloc[self.step][f'Lower_Band_{self.band_data}']
        upper_band_3sd = self.df.iloc[self.step][f'Upper_Band_3SD_{self.band_data}']
        lower_band_3sd = self.df.iloc[self.step][f'Lower_Band_3SD_{self.band_data}']
        middle_band = self.df.iloc[self.step][f'Middle_Band_{self.band_data}']

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

        state_vars = {
            'Close': curr_close,
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
            if close <= lower_band:
                action_str = 'EnterLong'
            elif close >= upper_band:
                action_str = 'EnterShort'
            else:
                action_str = 'Wait'
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
        trade_type = self.trade_direction
        leverage = self.leverage
        previous_prices = self.previous_prices

        self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy, symbol=symbol,
                                 start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time,
                                 enter_price=enter_price, exit_price=exit_price, trade_type=trade_type,
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
