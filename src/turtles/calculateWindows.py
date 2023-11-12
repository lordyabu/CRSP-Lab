import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from src.config import DATA_DIR

class TurtleWindows:
    def __init__(self, data_directory, name='Default'):
        self.data_directory = data_directory
        self.name = name
        self.save_dir = os.path.join(DATA_DIR, 'turtleData')

    def __str__(self):
        return self.name

    def calculate_turtle_windows(self, df):
        df['Rolling_Max_10'] = df['High'].shift(1).rolling(window=10).max()
        df['Rolling_Min_10'] = df['Low'].shift(1).rolling(window=10).min()
        df['Rolling_Max_20'] = df['High'].shift(1).rolling(window=20).max()
        df['Rolling_Min_20'] = df['Low'].shift(1).rolling(window=20).min()
        df['Rolling_Max_55'] = df['High'].shift(1).rolling(window=55).max()
        df['Rolling_Min_55'] = df['Low'].shift(1).rolling(window=55).min()
        return df

    def calculate_individual_window(self, stock_name):
        file_path = os.path.join(self.data_directory, f"{stock_name}")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = self.calculate_turtle_windows(df)

            # Save the DataFrame back to CSV
            save_path = os.path.join(self.save_dir, f"{stock_name}")
            df.to_csv(save_path, index=False)

            # print(f"Turtle Windows calculated and saved for {stock_name}.")
        else:
            print(f"The file for {stock_name} does not exist in the directory.")

    def calculate_all_windows(self):
        filenames = [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]
        num_workers = 8
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(tqdm(executor.map(self.calculate_individual_window, filenames), total=len(filenames)))


# # Example Usage:
# directory = os.path.join(DATA_DIR, 'priceDataOHLCSplitTest')
# turtle_windows = TurtleWindows(data_directory=directory)
# # turtle_windows.calculate_individual_window('AAPL.csv')
# turtle_windows.calculate_all_windows()