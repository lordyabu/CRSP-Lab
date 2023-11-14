import pandas as pd
import os
import json
from datetime import datetime
from src.config import DATA_DIR
from src.helperClasses.tradeLog import TradeLog
from abc import ABC, abstractmethod
from src.helperFunctions.tradeLog.getTradeLogPath import get_full_tradelog_path

class StockAlgorithmDaily(ABC):
    """
    Abstract base class for daily stock trading algorithms.

    This class provides a framework for implementing stock trading algorithms, including methods for data loading,
    action processing, step updating, and trade log saving. It maintains the state and history of actions, manages the trade log,
    and calculates total profit and loss (PnL).

    Attributes:
        stock_name (str): Name of the stock.
        df (pandas.DataFrame): DataFrame holding the stock data.
        trade_log (TradeLog): Instance of TradeLog for logging trades.
        reset_indexes (bool): Flag to reset DataFrame indexes.
        step (int): Current step in the algorithm.
        action_history (list): List to track the history of actions.
        total_pnl (float): Total profit and loss.

    Abstract Methods:
        __str__: Return a string representation of the algorithm's state.
        __repr__: Return a string representation of the algorithm for debugging.
        get_state: Retrieve the current state of the algorithm.
        get_action: Determine the next action for the algorithm.
        process_action: Process an action given by the algorithm.
        update_step: Update the step of the algorithm.

    Methods:
        save_tradelog: Saves the trade log to a CSV file.
        load_data: Loads the stock data from a CSV file.
    """
    def __init__(self, stock_name, folder_name=None, reset_indexes=False, step=0):
        self.stock_name = stock_name
        self.df = None
        self.trade_log = TradeLog()
        self.reset_indexes = reset_indexes
        self.step = step

        assert isinstance(step, int)

        self.total_pnl = 0
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
    def get_action(self):
        pass

    @staticmethod
    def process_action(self, action):
        pass


    @abstractmethod
    def update_step(self, new_step):
        pass

    def save_tradelog(self):
        df = self.trade_log.get_trade_dataframe()
        full_tradelog_path = get_full_tradelog_path()

        # Check if the full trade log CSV already exists
        if os.path.exists(full_tradelog_path):
            # If it exists, read it without setting an index
            full_tradelog_df = pd.read_csv(full_tradelog_path)

            # Check if 'TradeIndex' is in the columns of the loaded DataFrame
            if 'TradeIndex' in full_tradelog_df.columns:
                # If 'TradeIndex' exists, make sure it is the DataFrame index
                full_tradelog_df.set_index('TradeIndex', inplace=True)

            # Concatenate the new DataFrame to the existing one, aligning on 'TradeIndex'
            updated_tradelog_df = pd.concat([full_tradelog_df, df]).reset_index(drop=True)
        else:
            # If it doesn't exist, the new log is the full log
            print("Making new full trade-log.")
            updated_tradelog_df = df

        # Ensure 'TradeIndex' is a column in the DataFrame and set it as the index
        if 'TradeIndex' not in updated_tradelog_df.columns:
            updated_tradelog_df.reset_index(inplace=True)
            updated_tradelog_df.rename(columns={'index': 'TradeIndex'}, inplace=True)

        # Save the updated trade log with 'TradeIndex' as a column
        updated_tradelog_df.to_csv(full_tradelog_path, index=False)

    def load_data(self, file_dir):
        """
        Loads stock data from a specified directory.

        This method loads data for a given stock, filters it based on a date range, and asserts the data length matches the expected number of timesteps.
        It raises an exception if the stock is not in the list of valid stock filenames.

        Args:
            file_dir (str): The directory where the stock data is stored.

        Raises:
            ValueError: If the stock name is not in the list of valid stock filenames.
        """

        # Load valid filenames, date range, and num_timesteps
        valid_filenames_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
        with open(valid_filenames_path, 'r') as file:
            helper_data = json.load(file)
            valid_filenames = helper_data['valid_files']
            start_date = datetime.strptime(helper_data['start_date'], '%Y%m%d')
            end_date = datetime.strptime(helper_data['end_date'], '%Y%m%d')
            num_timesteps = helper_data['num_timesteps']

        # Check if the stock_name is in the valid_filenames
        if f'{self.stock_name}.csv' in valid_filenames:
            file_path = os.path.join(DATA_DIR, f'{file_dir}', f'{self.stock_name}.csv')
            data = pd.read_csv(file_path)

            data['Date'] = pd.to_datetime(data['date'], format='%Y%m%d')

            # Filter data based on date range
            self.df = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

            # Reset index if required
            if self.reset_indexes:
                self.df.reset_index(drop=True, inplace=True)

            # Assert the length of the DataFrame is equal to num_timesteps
            assert len(self.df) == num_timesteps, "DataFrame length does not match expected number of timesteps."

        else:
            raise ValueError(f"Stock name {self.stock_name} is not in the list of valid stock filenames.")


