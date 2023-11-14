# This script includes a function for plotting open, close, high, and low prices of a stock from a CSV file.
# It uses matplotlib to create a line plot for a selected range of data points. The function reads data from
# a specified directory and visualizes specific price trends for a stock.

import os.path
import pandas as pd
import matplotlib.pyplot as plt
from src.config import DATA_DIR

directory = os.path.join(DATA_DIR, 'priceDataOHLC', 'AAPL.csv')

def plot_ohlc_apple():
    """
    Plots open, close, high, and low prices of AAPL stock from a CSV file.

    This function reads stock price data from a CSV file and uses matplotlib to plot the open, close, high, and low prices
    for a specific range of data points (3000 to 3050). It visualizes these price trends to aid in analysis, with the date
    used as the x-axis.
    """
    # Assuming 'directory' is a global variable pointing to the CSV file
    global directory
    df = pd.read_csv(directory)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')


    # Adjust the range for plotting
    start_index = 3000
    end_index = 3050

    plt.figure(figsize=(12, 6))
    plt.plot(df['date'][start_index:end_index], df['OPENPRC'][start_index:end_index], label='Open Price')
    plt.plot(df['date'][start_index:end_index], df['PRC'][start_index:end_index], label='Closing Price')
    plt.plot(df['date'][start_index:end_index], df['High'][start_index:end_index], label='High Price')
    plt.plot(df['date'][start_index:end_index], df['Low'][start_index:end_index], label='Low Price')

    plt.legend()
    plt.title('AAPL Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


plot_ohlc_apple()
