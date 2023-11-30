from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
from src.nonTrades.nonTradeLogFunctions import extract_nontrades
from src.config import DATA_DIR
import os
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
def scaling(base_name, strategy, num_prev_price, splits):
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Construct the filename and save path
    filename = f"{splits}_combined_{strategy}_{start_date}_to_{end_date}_doctest_numP{num_prev_price}.csv"
    full_deep_path = os.path.join(DATA_DIR, 'deepData', f'deep{base_name}',filename)

    # Read the CSV file with low_memory=False
    df = pd.read_csv(full_deep_path, low_memory=False)

    # print(df.iloc[0])


    scaler = MinMaxScaler()

    # Apply MinMax scaling to each row's previous 50 prices
    # count = 0
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Scaling"):
        prev_prices = row[[f'PrevPrice_{i}' for i in range(0, num_prev_price + 1)]].values.reshape(-1, 1)
        scaled_prices = scaler.fit_transform(prev_prices).flatten()
        df.loc[index, [f'PrevPrice_{i}' for i in range(0, num_prev_price + 1)]] = scaled_prices

        # count += 1
        # if count > 10:
        #     break
    # print(df.iloc[0])
    filename_save = f"{splits}_scaled_combined_{strategy}_{start_date}_to_{end_date}_doctest_numP{num_prev_price}.csv"
    full_deepsave_path = os.path.join(DATA_DIR, 'deepData', f'deep{base_name}', filename_save)

    df.to_csv(full_deepsave_path, index=False)


# scaling(base_name='Bollinger', strategy='bollinger_naive_dynamic_sl', num_prev_price=20)
# scaling(base_name='Turtle', strategy='turtle_naive', num_prev_price=20)
# scaling(base_name='Box', strategy='box_naive', num_prev_price=20)