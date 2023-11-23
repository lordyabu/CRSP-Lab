# This script includes the 'run_all_boxle_trades' function, which automates the execution of the boxle trading strategy
# across a range of stocks listed in a JSON file. For each stock, it iteratively processes trading data,
# making decisions and updating steps based on the boxleNaive class, until all data points are processed.
# The trade log for each stock is saved upon completion.

from src.config import DATA_DIR
from src.boxStrategy.boxNaive import DarvasTrader
import os
import json
from tqdm import tqdm


def run_all_box_trades(identifier):
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for stock in tqdm(valid_stocks, desc='Processing stocks'):
        box = DarvasTrader(stock_name=f'{stock}',identifier=f'{identifier}', time_period='Daily', reset_indexes=False, step=0)

        while box.step != len(box.df.index):
            state = box.get_state()
            action = box.get_action(state)
            box.process_action(action, state['CurrentPrice'])
            box.update_step(box.step + 1)

        box.save_tradelog()


# run_all_box_trades('boxtest1')