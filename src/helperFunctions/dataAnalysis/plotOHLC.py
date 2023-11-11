import os.path

import pandas as pd

from src.config import DATA_DIR
import matplotlib.pyplot as plt


directory = os.path.join(DATA_DIR, 'priceDataOHLCTest', 'AAPL.csv')


def plot_stuffs():
    df = pd.read_csv(directory)

    plt.plot(df['OPENPRC'][300 : 350], label='Open Price')
    plt.plot(df['PRC'][300 : 350], label='Closing Price')
    plt.plot(df['High'][300 : 350], label='High Price')
    plt.plot(df['Low'][300 : 350], label='Low Price')

    plt.legend()
    plt.show()

    print(df['Low'][325 : 330])
    print(df['OPENPRC'][325 : 330])

plot_stuffs()