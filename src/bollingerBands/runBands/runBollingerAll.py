from src.config import DATA_DIR
from src.bollingerBands.bollingerNaive import BollingerNaive
from src.bollingerBands.bollingerNaiveTwo import BollingerNaiveTwo
import os
import json
from tqdm import tqdm



def run_all_bollinger_trades_naive_one(identifier):
    """
    Executes Bollinger Band-based trading strategies across a list of valid stocks.

    This function reads a list of valid stock filenames and applies the BollingerNaive trading strategy to each.
    For each stock, it iteratively makes trading decisions, processes actions, and updates steps based on the state
    of the trading data until the end of the dataset. The trade log for each stock is then saved.

    Args:
        identifier (str): A unique identifier for the trading session or strategy.
    """

    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for stock in tqdm(valid_stocks, desc='Processing stocks'):

        boll = BollingerNaive(stock_name=f'{stock}', band_data_name='Default', identifier=f'{identifier}', time_period='Daily',
                              reset_indexes=False, step=0, moving_stop_loss=True)

        while boll.step != len(boll.df.index):
            state = boll.get_state()
            action = boll.get_action(state)
            boll.process_action(action)
            boll.update_step(boll.step + 1)

        boll.save_tradelog()

def run_all_bollinger_trades_naive_two(identifier):
    """
    Executes Bollinger Band-based trading strategies across a list of valid stocks.

    This function reads a list of valid stock filenames and applies the BollingerNaive trading strategy to each.
    For each stock, it iteratively makes trading decisions, processes actions, and updates steps based on the state
    of the trading data until the end of the dataset. The trade log for each stock is then saved.

    Args:
        identifier (str): A unique identifier for the trading session or strategy.
    """

    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for stock in tqdm(valid_stocks, desc='Processing stocks'):

        boll = BollingerNaiveTwo(stock_name=f'{stock}', band_data_name='Default', identifier=f'{identifier}', time_period='Daily',
                              reset_indexes=False, step=0, moving_stop_loss=True)

        while boll.step != len(boll.df.index):
            state = boll.get_state()
            action = boll.get_action(state)
            boll.process_action(action, state)
            # boll.process_action(action)
            boll.update_step(boll.step + 1)

        boll.save_tradelog()


# run_all_bollinger_trades('test2bollinger')