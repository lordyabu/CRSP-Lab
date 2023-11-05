import pandas as pd
from config import DATA_DIR
from bollingerNaive import BollingerNaive
import os
import json
from tqdm import tqdm  # Import tqdm


def run_stuffs():
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for stock in tqdm(valid_stocks, desc='Processing stocks'):  # Add tqdm here with a description
        boll = BollingerNaive(stock_name=f'{stock}', band_data_name='Default', identifier='test1', time_period='Daily',
                              reset_indexes=False, step=0)

        while boll.step != len(boll.df.index):
            state = boll.get_state()
            boll.get_and_process_action(state)

            boll.update_step(boll.step + 1)

        boll.save_tradelog()


run_stuffs()
