import numpy as np
import pandas as pd
import os
import json
from src.config import DATA_DIR, PRICE_DATA_DIR
from tqdm import tqdm
import traceback
from concurrent.futures import ThreadPoolExecutor

directory = PRICE_DATA_DIR
save_directory = os.path.join(DATA_DIR, 'priceDataOHLC')
five_min_directory = os.path.join(DATA_DIR, 'dataFiveMin', '.csv')


def calculate_ohlc(date, stock_name=None, actual_price=None, actual_end_price=None, args=None):
    try:
        file_path = os.path.join(five_min_directory, f"Day_{date}.csv")
        df = pd.read_csv(file_path, usecols=[stock_name])

        if not actual_price:
            curr_price = 1
        else:
            curr_price = round(actual_price, 2)

        # Convert the returns to a NumPy array and handle NaN values
        returns = df[f'{stock_name}'].to_numpy()
        returns = np.nan_to_num(returns)  # Replace NaN with 0

        prices = curr_price * np.cumprod(1 + returns)

        high_price = round(np.max(prices), 10)
        low_price = round(np.min(prices), 10)

        open_price = actual_price

        # Ensure the close price is not higher than the high or lower than the low
        close_price = actual_end_price

        # Replace high and low prices if the open or close prices are outside the current range
        high_price = max(high_price, open_price, close_price)
        low_price = min(low_price, open_price, close_price)

        return open_price, high_price, low_price, close_price

    except Exception as e:
        return actual_price, max(actual_price, actual_end_price), min(actual_price, actual_end_price), actual_end_price

def get_individual_ohlc(stock_name: str):
    # Construct the file path for the stock's CSV file
    file_path = os.path.join(directory, f"{stock_name}.csv")

    save_path = os.path.join(save_directory, f"{stock_name}.csv")

    # Check if the file exists
    if os.path.exists(file_path):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Initialize lists to hold OHLC values
        opens, highs, lows, closes = [], [], [], []

        for index, row in df.iterrows():
            # Use 'date' and 'OPENPRC' from the row to calculate OHLC
            open, high, low, close = calculate_ohlc(row['date'], stock_name=stock_name, actual_price=row['OPENPRC'], actual_end_price=row['PRC'])

            # Append the values to the lists
            opens.append(open)
            highs.append(high)
            lows.append(low)
            closes.append(close)

        # Create new columns in the DataFrame from the lists
        df['Open'] = opens
        df['High'] = highs
        df['Low'] = lows
        df['Close'] = closes

        # Save the updated DataFrame back to the CSV file
        df.to_csv(save_path, index=False)
        print(f"OHLC data added and saved for {stock_name}.")
    else:
        print(f"The file for {stock_name} does not exist in the directory.")



def get_all_ohlc(directory):
    # Get all CSV filenames
    filenames = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Flag to determine if processing should start
    start_processing = False

    # Function to process a single file
    def process_file(filename):
        # nonlocal start_processing  # Refer to the outer scope variable
        stock_name = filename.replace('.csv', '')  # Remove the extension to get the stock name

        # if stock_name == "A":
        #     print('starting')
        #     start_processing = True
        start_processing = True
        if start_processing:
            print(f"Starting {stock_name}")
            get_individual_ohlc(stock_name)  # Call the function with the stock name

    # Number of threads to use (you can adjust this based on your system's capabilities)
    num_workers = 24

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Use tqdm for progress bar, starting from the file where "ACLA" is found
        list(tqdm(executor.map(process_file, filenames), total=len(filenames), initial=filenames.index('A.csv')))


def get_all_ohlc_normal(directory):
    for filename in tqdm(os.listdir(directory)):
        # Assuming you only want to process files with a specific extension, e.g., .csv
        if filename.endswith('.csv'):
            stock_name = filename.replace('.csv', '')  # Remove the extension to get the stock name
            get_individual_ohlc(stock_name)  # Call the function with the stock name
        else:
            continue  # Skip files that do not end with .csv



def get_ohlc(individual_stock=None):
    if individual_stock:
        get_individual_ohlc(individual_stock)
    else:
        get_all_ohlc(directory=directory)


# get_individual_ohlc('ADBLC')


get_ohlc()