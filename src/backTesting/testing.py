from backtesting import Backtest
from src.config import DATA_DIR
import pandas as pd
import os
import json
import warnings
from configBackTest import stock_to_check
warnings.filterwarnings('ignore')
from src.bollingerBands.bollingerBacktest import BollingerNaiveStrategy



def get_filtered_data(stock_name):

    # Load start_date and end_date from JSON file
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        date_data = json.load(json_file)

    # Extract start_date and end_date and convert them to datetime
    start_date = pd.to_datetime(date_data.get('start_date').replace('Day_', ''), format='%Y%m%d')
    end_date = pd.to_datetime(date_data.get('end_date').replace('Day_', ''), format='%Y%m%d')

    # Load stock data from CSV file
    file_path = os.path.join(DATA_DIR, 'priceDataOHLC', f'{stock_name}.csv')
    stock_data = pd.read_csv(file_path)
    stock_data['Date'] = pd.to_datetime(stock_data['date'], format='%Y%m%d')

    # Filter the stock_data based on the start_date and end_date
    filtered_stock_data = stock_data[(stock_data['Date'] >= start_date) & (stock_data['Date'] <= end_date)]

    has_nan_in_close = filtered_stock_data['Close'].isna().any()
    # print(has_nan_in_close)

    # Check for different types in 'Close' column
    close_types = filtered_stock_data['Close'].apply(type).unique()
    # print(close_types)

    # Assume 'Return' column exists in filtered_stock_data, handle NaNs, and convert to 'Close' price
    filtered_stock_data['Close'] = filtered_stock_data['Close']
    filtered_stock_data['Open'] = filtered_stock_data['Close']
    filtered_stock_data['High'] = filtered_stock_data['Close']
    filtered_stock_data['Low'] = filtered_stock_data['Close']


    # print(filtered_stock_data['Close'])
    filtered_stock_data.set_index('Date', inplace=True)

    return filtered_stock_data



def main(stock_name):
    filtered_stock_data = get_filtered_data(stock_name)
    bt = Backtest(filtered_stock_data, BollingerNaiveStrategy, cash=1000000, commission=0)
    stats = bt.run()
    bt.plot()

    print(stats)


if __name__ == '__main__':
    stock_name = stock_to_check
    main(stock_name)