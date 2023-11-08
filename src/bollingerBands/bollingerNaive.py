import pandas as pd
from src.traderBasic import StockAlgorithmDaily
from src.config import DATA_DIR
import os
from src.helperClasses.getTradeLogPath import get_full_tradelog_path


class BollingerNaive(StockAlgorithmDaily):

    def __init__(self, stock_name, band_data_name='Default',identifier=-1, time_period='Daily', reset_indexes=False, step=0):
        # Initialize the superclass
        self.trade_log_dir_full = os.path.join(DATA_DIR, 'tradeData')

        try:
            self.trade_log_dir_ticker = os.path.join(DATA_DIR, 'tradeData', 'allTrades.csv')
        except:
            # Make folder first then try directory
            pass


        super().__init__(stock_name = stock_name, folder_name='bollingerDataNew',reset_indexes = reset_indexes, step = step)

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

        self.leverage = 1

        self.vars = {}

        self.actions = []

        self.identifier = identifier
        self.time_period = time_period
        self.band_data = band_data_name

        self.strategy = "bollinger_naive"

        # print(self.df['Close'])


    def __str__(self):
        # Provide a meaningful string representation of this class
        return f"BollingerNaive"

    def __repr__(self):
        # Provide a string that could be used to recreate this object
        return f"Bollinger(stock_name='{self.stock_name}', reset_indexes={self.reset_indexes}, step={self.step}, rolling_window_length={self.rolling_window_length}, bollinger_band_width={self.bollinger_band_width})"

    # State at which to determine action from
    def get_state(self):
        #1. Upper, Lower, Middle Band
        upper_band = self.df.iloc[self.step][f'Upper_Band_{self.band_data}']
        lower_band = self.df.iloc[self.step][f'Lower_Band_{self.band_data}']
        upper_band_3sd = self.df.iloc[self.step][f'Upper_Band_3SD_{self.band_data}']
        lower_band_3sd = self.df.iloc[self.step][f'Lower_Band_3SD_{self.band_data}']
        middle_band = self.df.iloc[self.step][f'Middle_Band_{self.band_data}']

        curr_close = self.df.iloc[self.step]['Close']

        if self.curr_price != None:
            self.curr_price = curr_close
        else:
            self.curr_price = None

        position_type = self.trade_direction
        band_entry = self.band_entry_type


        # If moving stop loss
        if position_type == 'long':
            stop_loss_price = lower_band_3sd
            target_price = middle_band
        elif position_type == 'short':
            stop_loss_price = upper_band_3sd
            target_price = middle_band
        else:
            stop_loss_price = None
            target_price = None
        # If not:

        # TODO
        # Implement


        state_vars = {
            'Close': curr_close,
            'LowerBand' : lower_band,
            'UpperBand' : upper_band,
            'MiddleBand' : middle_band,
            'PositionType' : position_type,
            'BandEntry' : band_entry,
            'LowerBand3SD' : lower_band_3sd,
            'UpperBand3SD': upper_band_3sd,
            'TargetPrice' : target_price,
            'StopLossPrice': stop_loss_price
        }

        return state_vars


    # Based on the above state, determine action
    def get_and_process_action(self, curr_state):
        # Multiplied from curr_price
        close = curr_state['Close']

        upper_band = curr_state['UpperBand']
        middle_band = curr_state['MiddleBand']
        lower_band = curr_state['LowerBand']
        sl_upper_band = curr_state['UpperBand3SD']
        sl_lower_band = curr_state['LowerBand3SD']
        position_type = curr_state['PositionType']

        stop_loss_price = curr_state['StopLossPrice']
        target_price = curr_state['TargetPrice']

        action_str = ''

        # If in position (long or short)
        if position_type in ['long', 'short']:
            # If price has crossed the middle band, exit position
            if (position_type == 'long' and close >= target_price) or \
               (position_type == 'short' and close <= target_price):
                action_str = self.exit_position()  # You'll need to implement this
            # Elif price is past stop loss
            elif (position_type == 'long' and close < stop_loss_price) or \
                    (position_type == 'short' and close > stop_loss_price):
                action_str = self.exit_position()
            else:
                action_str = 'Hold'
                self.actions.append(0)
        # If not in a position
        elif position_type is None:
            # If action is triggered by price touching the lower or upper band, start position
            if close <= lower_band:
                action_str = 'EnterLong'
                self.start_position('long')  # You'll need to implement this
            elif close >= upper_band:
                action_str = 'EnterShort'
                self.start_position('short')  # You'll need to implement this
            else:
                action_str = 'Wait'
                self.actions.append(0)
        else:
            raise ValueError(f"Invalid position type {position_type}.")


        return action_str
        # If in action (position type != None)
        #    If price has crosses middle band
        #       exit (and save to trade log)
        #    Else
        #       do nothing
        # Else
        #    If action is triggered by price == lower or price == upper
        #        Start action
        #    Else
        #        Do nothing



    def start_position(self, action):
        if action == 'long':
            self.in_trade = True
            self.enter_trade_date = str(self.df.iloc[self.step]["date"])
            self.exit_trade_date = None

            if self.time_period != 'Daily':
                self.enter_trade_time = 'NA'
            else:
                self.enter_trade_time = self.step

            self.exit_trade_time = None
            self.exit_trade_price = None

            self.curr_price = self.df.iloc[self.step]['Close']

            self.enter_trade_price = self.curr_price
            self.trade_direction = 'long'
            self.band_entry_type = 'lower'

            self.actions.append(1)

        elif action == 'short':
            self.in_trade = True
            self.enter_trade_date = str(self.df.iloc[self.step]["date"])
            self.exit_trade_date = None

            if self.time_period != 'Daily':
                self.enter_trade_time = '160000'
            else:
                self.enter_trade_time = self.step

            self.exit_trade_time = None
            self.exit_trade_price = None

            self.curr_price = self.df.iloc[self.step]['Close']

            self.enter_trade_price = self.curr_price
            self.trade_direction = 'short'
            self.band_entry_type = 'upper'

            self.actions.append(-1)
        else:
            raise ValueError(f"Invalid position type {action}.")



    def exit_position(self):
        # print(self.curr_price)
        self.exit_trade_date = str(self.df.iloc[self.step]["date"])
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

        self.trade_log.add_trade(identifier=identifier, time_period=time_period, strategy=strategy, symbol=symbol,
        start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, enter_price=enter_price,
        exit_price=exit_price, trade_type=trade_type, leverage=leverage)

        if trade_type == 'long':
            self.actions.append(2)
            return_str = 'EndLong'
        elif trade_type == 'short':
            self.actions.append(-2)
            return_str = 'EndShort'
        else:
            raise ValueError(f"Invalid position type {trade_type}.")


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

        self.leverage = 1

        return return_str


    def update_step(self, new_step):
        # Update the step (time period) for the strategy
        self.step = new_step

    def save_tradelog(self):
        # Get the trade log DataFrame
        df = self.trade_log.get_trade_dataframe()

        full_tradelog_path = get_full_tradelog_path()

        # Check if the full trade log CSV already exists
        if os.path.exists(full_tradelog_path):
            # If it exists, read it and concatenate with the new log
            full_tradelog_df = pd.read_csv(full_tradelog_path)
            updated_tradelog_df = pd.concat([full_tradelog_df, df], ignore_index=True)
        else:
            # If it doesn't exist, the new log is the full log
            print("Making new full trade-log.")
            updated_tradelog_df = df

        # Save the updated trade log
        updated_tradelog_df.to_csv(full_tradelog_path, index=False)
