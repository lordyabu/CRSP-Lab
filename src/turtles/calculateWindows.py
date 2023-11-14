# This script features the TurtleWindows class, which is tailored to calculate Turtle Trading window data for stock prices.
# The class offers functionalities to compute rolling maximum and minimum values over various window lengths,
# an essential aspect of the Turtle Trading system. It includes methods to process this data for an individual stock,
# as well as a bulk processing capability utilizing multithreading to handle multiple stock files efficiently.
# The computed data is saved for further analysis.

import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from src.config import DATA_DIR, TURTLE_DATA_DIR

class TurtleWindows:
    def __init__(self, data_directory, name='Default'):
        """
        Initializes the TurtleWindows instance.

        Args:
            data_directory (str): The directory where stock data files are stored.
            name (str): The name of the TurtleWindows instance. Defaults to 'Default'.
        """
        self.data_directory = data_directory
        self.name = name
        self.save_dir = TURTLE_DATA_DIR

    def __str__(self):
        return self.name

    def calculate_turtle_windows(self, df):
        """
        Calculates Turtle Trading window data for a given DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing stock data with 'High' and 'Low' columns.

        Returns:
            pd.DataFrame: The DataFrame with added columns for rolling maxima and minima.
        """

        df['Rolling_Max_10'] = df['High'].shift(1).rolling(window=10).max()
        df['Rolling_Min_10'] = df['Low'].shift(1).rolling(window=10).min()
        df['Rolling_Max_20'] = df['High'].shift(1).rolling(window=20).max()
        df['Rolling_Min_20'] = df['Low'].shift(1).rolling(window=20).min()
        df['Rolling_Max_55'] = df['High'].shift(1).rolling(window=55).max()
        df['Rolling_Min_55'] = df['Low'].shift(1).rolling(window=55).min()
        return df

    def calculate_individual_window(self, stock_name):
        """
        Calculates and saves Turtle Trading window data for an individual stock.

        Args:
            stock_name (str): The name of the stock file to process.
        """
        file_path = os.path.join(self.data_directory, f"{stock_name}")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = self.calculate_turtle_windows(df)

            save_path = os.path.join(self.save_dir, f"{stock_name}")
            df.to_csv(save_path, index=False)

        else:
            print(f"The file for {stock_name} does not exist in the directory.")

    def calculate_all_windows(self):
        """
        Calculates Turtle Trading window data for all stock files in the specified directory.
        Utilizes multithreading for concurrent processing.
        """
        filenames = [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]
        num_workers = 8
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(tqdm(executor.map(self.calculate_individual_window, filenames), total=len(filenames)))

