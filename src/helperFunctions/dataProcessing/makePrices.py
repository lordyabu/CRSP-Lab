from config import DATA_DIR
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import numpy as np

directory = os.path.join(DATA_DIR, 'dataDailyTwoCol')


def calculate_return_prices(stock):
    prices = []

    curr_price = 1

    read_dir = os.path.join(directory, stock)

    df = pd.read_csv(read_dir, na_values=[',,']).fillna(0)

    for i in range(len(df.index)):
        curr_price *= (df.iloc[i]['Return'] + 1)
        print(curr_price)
        prices.append(curr_price)

    df['ReturnPrice'] = prices
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv(read_dir)

    print(np.sum(df['Return']))



def calculate_return_prices_all():
    filenames = [f for f in os.listdir(directory) if f.endswith('.csv')]

    num_workers = 8

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Use tqdm for progress bar, starting from the file where "ACLA" is found
        list(tqdm(executor.map(calculate_return_prices, filenames), total=len(filenames)))


def get_ohlc_from_price():
    pass


# calculate_return_prices_all()

calculate_return_prices('AAPL.csv')