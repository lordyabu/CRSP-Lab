# This script features the BollingerNaive class, an extension of the StockAlgorithmDaily class, designed to implement a Bollinger Band-based trading strategy.
# The class encapsulates the logic for making trading decisions based on Bollinger Bands, handling the entry and exit of trades,
# updating the strategy's state, and processing actions for each step in the trading data.
# It offers functionality to evaluate the current market state, decide on trading actions (like entering long or short positions),
# and process these actions through the trading period.

from src.helperClasses.traderBasic import StockAlgorithmDaily
from src.config import DATA_DIR, BOLLINGER_DATA_NAME, TRANSACTION_COST_PCT, TRANSACTION_COST_DOLLAR
import os
from src.helperClasses.unit import Unit


class BollingerNaiveTwo(StockAlgorithmDaily):

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
            'Close': curr_close,
            'NextPriceOpen': next_price_open,
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


        if  close <= lower_band and action_list[0] != 'ExitLong':
            action_list.append('EnterLong')
        elif close >= upper_band and action_list[0] != 'ExitShort':
            action_list.append('EnterShort')

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