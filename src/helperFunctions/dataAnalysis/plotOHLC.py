# This script includes a function for plotting open, close, high, and low prices of a stock from a CSV file.
# It uses matplotlib to create a line plot for a selected range of data points. The function reads data from
# a specified directory and visualizes specific price trends for a stock.

import os.path
import pandas as pd
import matplotlib.pyplot as plt
from src.config import DATA_DIR

directory = os.path.join(DATA_DIR, 'priceDataOHLCSplitTest', 'AAPL.csv')

def plot_ohlc_apple():
    """
    Plots open, close, high, and low prices of a stock from a CSV file.

    This function reads stock price data from a CSV file and uses matplotlib to plot the open, close, high, and low prices
    for a specific range of data points. It visualizes these price trends to aid in analysis.

    """
    df = pd.read_csv(directory)

    plt.plot(df['OPENPRC'][300 : 350], label='Open Price')
    plt.plot(df['PRC'][300 : 350], label='Closing Price')
    plt.plot(df['High'][300 : 350], label='High Price')
    plt.plot(df['Low'][300 : 350], label='Low Price')

    plt.legend()
    plt.show()

    print(df['Low'][325 : 330])
    print(df['OPENPRC'][325 : 330])

plot_ohlc_apple()
