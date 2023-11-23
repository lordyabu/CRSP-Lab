from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
from src.nonTrades.nonTradeLogFunctions import extract_nontrades
from src.config import DATA_DIR
import os
import json
import pandas as pd

def combine_data(strategy, identifier):
    non_strategy_name = f"NonTrade{strategy}"
    non_identifier = f"NonTrade{identifier}"

    trades = extract_trades(strategy=strategy, identifier=identifier)
    non_trades = extract_nontrades(strategy=non_strategy_name, identifier=non_identifier)

    # Add 'is_trade' column
    trades['is_trade'] = 1
    non_trades['is_trade'] = 0

    # Combine the dataframes
    combined_data = pd.concat([trades, non_trades], ignore_index=True)

    # Set 'Strategy' and 'Identifier' columns to 'Mixed'
    combined_data['Strategy'] = f'Mixed{strategy}'
    combined_data['Identifier'] = f'Mixed{identifier}'

    # Load the start and end dates
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Construct the filename and save path
    filename = f"combined_{strategy}_{start_date}_to_{end_date}_doctest.csv"
    full_deep_path = os.path.join(DATA_DIR, 'deepData', filename)

    # Save the combined dataframe
    combined_data.to_csv(full_deep_path, index=False)





