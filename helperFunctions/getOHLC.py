import numpy as np
import pandas as pd
import os
import json
from config import DATA_DIR
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

directory = os.path.join(DATA_DIR, 'dataDailyTwoCol')
save_directory = os.path.join(DATA_DIR, 'dataDailyTwoCol')
five_min_directory = os.path.join(DATA_DIR, 'dataFiveMin', '.csv')


def calculate_ohlc(day, stock_name=None, actual_price=None, args=None):
    file_path = os.path.join(five_min_directory, f"{day}.csv")
    df = pd.read_csv(file_path, usecols=[stock_name])

    if not actual_price:
        curr_price = 1
    else:
        curr_price = actual_price

    # Convert the returns to a NumPy array and handle NaN values
    returns = df[f'{stock_name}'].to_numpy()
    returns = np.nan_to_num(returns)  # Replace NaN with 0

    prices = curr_price * np.cumprod(1 + returns)

    # Calculate OHLC using the price series
    open_price = round(prices[0], 10)
    high_price = round(np.max(prices), 10)
    low_price = round(np.min(prices), 10)
    close_price = round(prices[-1], 10)  # Adjust the close price calculation

    return open_price, high_price, low_price, close_price

def get_individual_ohlc(stock_name: str):
    # Construct the file path for the stock's CSV file
    file_path = os.path.join(directory, f"{stock_name}.csv")

    # Check if the file exists
    if os.path.exists(file_path):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Initialize lists to hold OHLC values
        opens, highs, lows, closes = [], [], [], []

        # Enumerate over the 'Day' column
        for day in df['Day']:
            # print(day)
            # Calculate OHLC using your custom function (replace with the actual logic)
            open, high, low, close = calculate_ohlc(day, stock_name=stock_name)

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
        df.to_csv(file_path, index=False)
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
        nonlocal start_processing  # Refer to the outer scope variable
        stock_name = filename.replace('.csv', '')  # Remove the extension to get the stock name

        if stock_name == "FPFC":
            start_processing = True

        if start_processing:
            get_individual_ohlc(stock_name)  # Call the function with the stock name

    # Number of threads to use (you can adjust this based on your system's capabilities)
    num_workers = 8

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Use tqdm for progress bar, starting from the file where "ACLA" is found
        list(tqdm(executor.map(process_file, filenames), total=len(filenames), initial=filenames.index('ACLA.csv')))


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