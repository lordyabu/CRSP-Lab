from src.helperClasses.unit import Unit
from src.helperClasses.traderBasic import StockAlgorithmDaily
from src.config import OHLC_DATA_DIR, DATA_DIR, TRANSACTION_COST_PCT, TRANSACTION_COST_DOLLAR
import json
import os
import pandas as pd
from pandas import date_range
from tqdm import tqdm
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades, extract_trades_auxillary, extract_trades_specific_df
import random
from src.helperClasses.tradeLog import TradeLog
from src.nonTrades.nonTradeLogFunctions import get_full_nontradelog_path, save_nontradelog, update_nontrade_index



def get_date_list(start_date, end_date):
    """
    Generates a list of dates based on trading days from the AAPL stock data.

    Args:
        OHLC_DATA_DIR (str): The directory where OHLC data files are stored.
        start_date (str): The start date in 'YYYYMMDD' format.
        end_date (str): The end date in 'YYYYMMDD' format.

    Returns:
        List[str]: A list of dates in 'YYYYMMDD' format based on actual trading days.
    """
    aapl_path = os.path.join(OHLC_DATA_DIR, 'AAPL.csv')
    aapl_data = pd.read_csv(aapl_path)

    # Convert the 'date' column in AAPL data to datetime for filtering
    aapl_data['date'] = pd.to_datetime(aapl_data['date'], format='%Y%m%d')

    # Convert string dates to pandas datetime for comparison
    start = pd.to_datetime(start_date, format='%Y%m%d')
    end = pd.to_datetime(end_date, format='%Y%m%d')

    # Filter dates between start and end dates
    filtered_dates = aapl_data[(aapl_data['date'] >= start) & (aapl_data['date'] <= end)]

    # Format dates back to string in 'YYYYMMDD' format
    return [date.strftime('%Y%m%d') for date in filtered_dates['date']]


def get_shortest_distance(trades, random_date):
    """
    Finds the shortest distance in days between a given date and a list of trade start dates.

    Args:
        trades (pd.DataFrame): DataFrame containing trades with a 'StartDate' column.
        random_date (str): The date in 'YYYYMMDD' format to compare against.

    Returns:
        int: The shortest distance in days.
    """
    # Convert random date to datetime
    random_date = pd.to_datetime(random_date, format='%Y%m%d')

    # Calculate differences in days and find the minimum
    differences = abs(trades['StartDate'] - random_date).dt.days
    shortest_distance = differences.min()

    return shortest_distance

# ToDo (DONE)
# replace extract_trades_auxillary with extract_trades
def get_non_trades(strategy, identifier, min_distance, short_distance, medium_distance, long_distance, splits):
    assert sum(splits) == 100, "The sum of splits percentages must equal 100."

    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]
    start_date = data['start_date']
    end_date = data['end_date']

    all_dates = get_date_list(start_date, end_date)

    non_trade_log = TradeLog()

    for stock in tqdm(valid_stocks, desc='Processing stocks'):
        # if stock == "AAPL":
        #     return

        trades = extract_trades_specific_df(identifier=identifier, stock_name=f"{stock}", sort_by='EndDate')

        num_non_trades = len(trades)

        num_short = int(num_non_trades * splits[0] / 100)
        num_medium = int(num_non_trades * splits[1] / 100)
        num_long = num_non_trades - num_short - num_medium

        stock_path = os.path.join(OHLC_DATA_DIR, f"{stock}.csv")
        stock_data = pd.read_csv(stock_path)
        stock_data['date'] = pd.to_datetime(stock_data['date'], format='%Y%m%d')

        # Process non-trades for each split
        process_non_trades(stock, trades, all_dates, stock_data, non_trade_log,
                           num_short, min_distance, short_distance, identifier, strategy, splits)

        process_non_trades(stock, trades, all_dates, stock_data, non_trade_log,
                           num_medium, short_distance, medium_distance, identifier, strategy, splits)

        process_non_trades(stock, trades, all_dates, stock_data, non_trade_log,
                           num_long, medium_distance, long_distance, identifier, strategy, splits)


    save_nontradelog(non_trade_log)


def process_non_trades(stock, trades, all_dates, stock_data, non_trade_log, num_trades, min_dist, max_dist, identifier, strategy, splits):
    count = 0
    while count < num_trades:
        random_date = random.choice(all_dates)
        shortest_distance = get_shortest_distance(trades, random_date)

        if min_dist <= shortest_distance <= max_dist:
            random_date_dt = pd.to_datetime(random_date, format='%Y%m%d')
            stock_data['date'] = pd.to_datetime(stock_data['date'], format='%Y%m%d')
            price_data = stock_data[stock_data['date'] == random_date_dt]

            assert not price_data.empty, "No matching date found in stock_data."
            enter_price_index = price_data.index[0]
            enter_price = price_data['PRC'].iloc[0]

            # On the rare occasions it enters on the last day of the dataset use the existing closing price
            try:
                enter_price_open = stock_data['OPENPRC'].iloc[enter_price_index + 1]
            except:
                enter_price_open = enter_price

            previous_prices = stock_data.loc[max(0, enter_price_index - 50):enter_price_index - 1, 'PRC'].tolist()

            non_trade_log.add_non_trade(
                identifier=f'NonTrade{identifier}_{splits[0]}_{splits[1]}_{splits[2]}', time_period='Daily', strategy=f'NonTrade{strategy}',
                symbol=stock.split(".")[0], start_date=random_date, end_date='NA',
                start_time='160000', end_time='NA', enter_price=enter_price,exit_price='NA', enter_price_open=enter_price_open, exit_price_open='NA',
                trade_type='NA', transaction_cost_pct=TRANSACTION_COST_PCT, transaction_cost_dollar=TRANSACTION_COST_DOLLAR,leverage=1, previous_prices=previous_prices
            )

            count += 1


get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test1bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[34, 33, 33]) # DONE and TESTED fo pre_open / doctest
# get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test1bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[80, 10, 10]) # DONE and TESTED for for pre_open / doctest
# get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test1bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 80, 10])
# get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test1bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 10, 80])

get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test2bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[34, 33, 33]) # DONE and TESTED for pre_open / doctest
# get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test2bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[80, 10, 10])
# get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test2bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 80, 10])
# get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test2bollinger', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 10, 80])

get_non_trades(strategy='turtle_naive', identifier='test1turtles', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[34, 33, 33])
# get_non_trades(strategy='turtle_naive', identifier='test1turtles', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[80, 10, 10])
# get_non_trades(strategy='turtle_naive', identifier='test1turtles', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 80, 10])
# get_non_trades(strategy='turtle_naive', identifier='test1turtles', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 10, 80])

get_non_trades(strategy='box_naive', identifier='test1box', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[34, 33, 33])
# get_non_trades(strategy='box_naive', identifier='test1box', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[80, 10, 10])
# get_non_trades(strategy='box_naive', identifier='test1box', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 80, 10])
# get_non_trades(strategy='box_naive', identifier='test1box', min_distance=1, short_distance=3, medium_distance=5, long_distance=10, splits=[10, 10, 80])

update_nontrade_index(get_full_nontradelog_path())
