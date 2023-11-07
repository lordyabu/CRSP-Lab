import os.path

import pandas as pd

from config import DATA_DIR
import matplotlib.pyplot as plt


directory = os.path.join(DATA_DIR, 'priceDataOHLC', 'AAL.csv')


def plot_stuffs():
    df = pd.read_csv(directory)

    plt.plot(df['OPENPRC'][100 : 150], label='Open Price')
    plt.plot(df['PRC'][100 : 150], label='Closing Price')
    plt.plot(df['High'][100 : 150], label='High Price')
    plt.plot(df['Low'][100 : 150], label='Low Price')

    plt.legend()
    plt.show()

    print(df['Low'][125 : 130])
    print(df['OPENPRC'][125 : 130])

plot_stuffs()