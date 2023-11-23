from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
from src.nonTrades.nonTradeLogFunctions import extract_nontrades
from src.config import DATA_DIR
import os
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def scaling(strategy):
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Construct the filename and save path
    filename = f"combined_{strategy}_{start_date}_to_{end_date}_doctest.csv"
    full_deep_path = os.path.join(DATA_DIR, 'deepData', filename)

    df = pd.read_csv(full_deep_path)
    scaler = MinMaxScaler()

    # Apply MinMax scaling to each row's previous 50 prices
    for index, row in df.iterrows():
        prev_prices = row[[f'PrevPrice_{i}' for i in range(1, 51)]].values.reshape(-1, 1)
        scaled_prices = scaler.fit_transform(prev_prices).flatten()
        df.loc[index, [f'PrevPrice_{i}' for i in range(1, 51)]] = scaled_prices

    # Optionally, save the scaled dataframe
    filename_save = f"combined_{strategy}_{start_date}_to_{end_date}_doctest_scaled.csv"
    full_deepsave_path = os.path.join(DATA_DIR, 'deepData', filename_save)

    df.to_csv(full_deepsave_path, index=False)







