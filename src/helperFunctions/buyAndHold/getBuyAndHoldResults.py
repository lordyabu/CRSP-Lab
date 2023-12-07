# This get's the buy and hold results of the trades
import pandas as pd

from src.config import DATA_DIR, OHLC_DATA_DIR
from src.turtles.turtleNaive import TurtleNaive
import os
import json
from tqdm import tqdm
import numpy as np

def run_all_hold_trades():
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    all_returns = []

    for stock in tqdm(valid_stocks, desc='Processing stocks'):
        # if stock == 'AAPL' or stock == 'AAPL.csv':
        #     return
        path = os.path.join(OHLC_DATA_DIR, f'{stock}.csv')

        stock_df = pd.read_csv(path)

        entry_row = stock_df[stock_df['date'] == 20100104]
        if not entry_row.empty:
            enter_price = entry_row.iloc[0]['PRC']
        else:
            print(f"Entry date not found for {stock}")
            continue

        exit_row = stock_df[stock_df['date'] == 20201231]
        if not exit_row.empty:
            exit_price = exit_row.iloc[0]['PRC']
        else:
            print(f"Exit date not found for {stock}")
            continue

        pnl = (exit_price / enter_price) - 1

        all_returns.append(pnl)

        print(stock, pnl, enter_price, exit_price)


    print(sum(all_returns), np.mean(all_returns))



run_all_hold_trades()


