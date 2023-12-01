from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
from src.nonTrades.nonTradeLogFunctions import extract_nontrades
from src.config import DATA_DIR
import os
import json
import pandas as pd

def combine_data(base_name, strategy=None, identifier=None, num_prev_prices=50, drop_nans=False, splits=None):
    non_strategy_name = f"NonTrade{strategy}"
    non_identifier = f"NonTrade{identifier}_{splits}"

    # non_identifier = 'NonTradetest1turtle'

    trades = extract_trades(identifier=identifier)

    print(len(trades.index))
    non_trades = extract_nontrades(identifier=non_identifier)

    print(len(non_trades.index))

    # Add 'is_trade' column
    trades['is_trade'] = 1
    non_trades['is_trade'] = 0

    # Combine the dataframes
    combined_data = pd.concat([trades, non_trades], ignore_index=True)

    # Set 'Strategy' and 'Identifier' columns to 'Mixed'
    combined_data['Strategy'] = f'Mixed{strategy}'
    combined_data['Identifier'] = f'Mixed{identifier}'

    # Add 'PrevPrice_0' as a copy of 'EnterPrice'
    combined_data['PrevPrice_0'] = combined_data['EnterPrice']

    # Select the PrevPrice columns based on num_prev_prices
    prev_price_cols = [f"PrevPrice_{i}" for i in range(0, num_prev_prices + 1)]  # Include PrevPrice_0
    other_cols = [col for col in combined_data.columns if not col.startswith('PrevPrice_')]
    combined_data = combined_data[other_cols + prev_price_cols]

    # Drop rows where PrevPrice columns have NaNs
    if drop_nans:
        combined_data.dropna(subset=prev_price_cols, inplace=True)

    # Load the start and end dates
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Construct the filename and save path
    filename = f"{splits}_combined_{identifier}_{start_date}_to_{end_date}_doctest_numP{num_prev_prices}.csv"
    full_deep_path = os.path.join(DATA_DIR, 'deepData', base_name, filename)

    # Save the combined dataframe
    combined_data.to_csv(full_deep_path, index=False)

# combine_data(base_name='deepBollinger', identifier='test1bollinger', num_prev_prices=20, drop_nans=True)
# combine_data(base_name='deepTurtle', strategy='turtle_naive', identifier='test1turtles',
#              num_prev_prices=20, drop_nans=True)

# combine_data(base_name='deepBox', strategy='box_naive', identifier='test1box', num_prev_prices=20, drop_nans=True)

