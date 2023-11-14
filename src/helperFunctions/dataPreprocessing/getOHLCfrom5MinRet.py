# This script is designed to calculate and process Open, High, Low, Close (OHLC) data for stock prices.
# It includes functions to calculate OHLC values from price data, process individual stocks, process all stocks in a directory,
# and determine whether to process a single stock or all stocks based on input. The script handles data reading, calculation,
# and saving the processed data back to CSV files.

import numpy as np
import pandas as pd
import os
from src.config import PRICE_DATA_DIR, OHLC_DATA_DIR, FIVE_MIN_DIR
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

directory = PRICE_DATA_DIR
save_directory = OHLC_DATA_DIR
five_min_directory = FIVE_MIN_DIR


def calculate_ohlc(date, stock_name=None, actual_price=None, actual_end_price=None):
    """
    Calculate the OHLC (Open, High, Low, Close) values for a given stock on a specific date.

    The function uses price data from a CSV file to calculate the OHLC values. If actual prices are not provided,
    default values are used.

    Args:
        date (str): The date for which OHLC values are to be calculated.
        stock_name (str, optional): The name of the stock. Defaults to None.
        actual_price (float, optional): The actual opening price of the stock. Defaults to None.
        actual_end_price (float, optional): The actual closing price of the stock. Defaults to None.

    Returns:
        tuple: A tuple containing the calculated open, high, low, and close prices.
    """
    try:
        # Gets df of returns on specific day
        file_path = os.path.join(five_min_directory, f"Day_{date}.csv")
        df = pd.read_csv(file_path, usecols=[stock_name])

        if not actual_price:
            curr_price = 1
        else:
            curr_price = round(actual_price, 2)

        # Uses numpy to calculate all prices simultaneously
        returns = df[f'{stock_name}'].to_numpy()
        returns = np.nan_to_num(returns)

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
    """
    Processes OHLC data for an individual stock and saves it to a CSV file.

    This function reads stock price data, calculates OHLC values using `calculate_ohlc`, and saves the updated data
    back to a CSV file. It checks if the file for the given stock exists before processing.

    Args:
        stock_name (str): The name of the stock to process.
    """
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
            open, high, low, close = calculate_ohlc(row['date'], stock_name=stock_name, actual_price=row['OPENPRC'],
                                                    actual_end_price=row['PRC'])

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
        # print(f"OHLC data added and saved for {stock_name}.")
    else:
        print(f"The file for {stock_name} does not exist in the directory.")


def get_all_ohlc(directory):
    """
    Processes OHLC data for all stocks in a given directory using multithreading.

    This function iterates over all CSV files in the specified directory and calculates OHLC values for each stock.
    The calculations are performed concurrently using ThreadPoolExecutor for improved performance.

    Args:
        directory (str): The directory containing the stock files to process.
    """
    # Get all CSV filenames
    filenames = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Function to process a single file
    def process_file(filename):
        # nonlocal start_processing  # Refer to the outer scope variable
        stock_name = filename.replace('.csv', '')  # Remove the extension to get the stock name
        get_individual_ohlc(stock_name)

    # Number of threads to use (you can adjust this based on your system's capabilities)
    num_workers = 24

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Use tqdm for progress bar, starting from the file where "ACLA" is found
        list(tqdm(executor.map(process_file, filenames), total=len(filenames), initial=filenames.index('A.csv')))


def get_ohlc(individual_stock=None):
    """
    Determines whether to process OHLC data for an individual stock or all stocks.

    Based on the provided argument, this function either processes OHLC data for a single stock or all stocks in a directory.

    Args:
        individual_stock (str, optional): The name of the individual stock to process. If None, all stocks in the directory are processed. Defaults to None.
    """
    if individual_stock:
        get_individual_ohlc(individual_stock)
    else:
        get_all_ohlc(directory=directory)

