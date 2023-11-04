import pandas as pd
import os
import json
from datetime import datetime
from config import DATA_DIR
from helperClasses.tradeLog import TradeLog
from abc import ABC, abstractmethod


class StockAlgorithmDaily(ABC):
    def __init__(self, stock_name, folder_name=None, reset_indexes=False, step=0, rolling_window_length=-1):
        self.stock_name = stock_name
        self.df = None


        self.trade_log = TradeLog()

        self.reset_indexes = reset_indexes



        # Starting at time = 0
        self.step = step

        # Rolling window length
        assert isinstance(step, int)


        self.rolling_window_length = rolling_window_length

        # DO AFTER DATACLASS ---------------------------------------
        if self.step == 0:
            if self.rolling_window_length > self.step:
                # THROW WARNING
                print("Setting step to ")
                self.step = self.rolling_window_length
        self.action_history = []
        # ----------------------------------------------------------

        self.total_pnl = 0

        # Loads self.df
        self.load_data(file_dir=folder_name)

    @abstractmethod
    def __str__(self):
        pass


    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def get_and_process_action(self):
        pass


    @abstractmethod
    def update_step(self, new_step):
        pass

    @abstractmethod
    def save_tradelog(self):
        pass


    def save_tradelog(self, indiviudal=False):

        # 1. Get trade df from trade-log
        # 2. Open either combined or individual file
        # 3. Save accordingly


        if indiviudal:
            print("NOT IMPLEMENTED YET")
            pass
        else:
            print("NOT IMPLEMENTED YET")



    def load_data(self, file_dir):
        """Loads data from a file if the stock name is valid. For validity rules see findTimespanStocks.py"""

        # Load valid filenames, date range, and num_timesteps
        valid_filenames_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
        with open(valid_filenames_path, 'r') as file:
            helper_data = json.load(file)
            valid_filenames = helper_data['valid_files']
            start_date = datetime.strptime(helper_data['start_date'], 'Day_%Y%m%d')
            end_date = datetime.strptime(helper_data['end_date'], 'Day_%Y%m%d')
            num_timesteps = helper_data['num_timesteps']

        # Check if the stock_name is in the valid_filenames
        if f'{self.stock_name}.csv' in valid_filenames:
            file_path = os.path.join(DATA_DIR, f'{file_dir}', f'{self.stock_name}.csv')
            data = pd.read_csv(file_path)
            data['Date'] = pd.to_datetime(data['Day'].str.replace('Day_', ''), format='%Y%m%d')

            # Filter data based on date range
            self.df = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

            # Reset index if required
            if self.reset_indexes:
                self.df.reset_index(drop=True, inplace=True)

            # Assert the length of the DataFrame is equal to num_timesteps
            assert len(self.df) == num_timesteps, "DataFrame length does not match expected number of timesteps."

        else:
            raise ValueError(f"Stock name {self.stock_name} is not in the list of valid stock filenames.")


# Usage
# try:
#     stock_algorithm = StockAlgorithmDaily(stock_name="AAPL", reset_indexes=False)
#     print(stock_algorithm.df)
#     stock_algorithm_two = StockAlgorithmDaily(stock_name="ACM", reset_indexes=True)
#     print(stock_algorithm_two.df)
# except ValueError as e:
#     print(e)
