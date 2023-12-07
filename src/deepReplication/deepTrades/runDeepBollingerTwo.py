from src.config import DATA_DIR
from src.deepReplication.deepTrades.deepBollingerTwo import MLBollingerNaiveTwo
import os
import json
from tqdm import tqdm

def run_all_bollinger_two_trades(identifier, ml_strategies):
    """
    Executes Bollinger Band-based trading strategies across a list of valid stocks for different machine learning strategies.

    This function reads a list of valid stock filenames and applies the BollingerNaive trading strategy to each stock
    for each specified ML strategy. For each stock and ML strategy, it iteratively makes trading decisions, processes actions,
    and updates steps based on the state of the trading data until the end of the dataset. The trade log for each stock
    is then saved.

    Args:
        identifier (str): A unique identifier for the trading session or strategy.
        ml_strategies (list): A list of machine learning strategies to be used.
    """
    split_to_do = "34_33_33"

    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for ml_to_use in ml_strategies:
        for stock in tqdm(valid_stocks, desc=f'Processing stocks for {ml_to_use}'):
            boll = MLBollingerNaiveTwo(stock_name=f'{stock}', band_data_name='Default', identifier=f'{ml_to_use}_{split_to_do}_{identifier}',
                                    time_period='Daily', reset_indexes=False, step=2000, moving_stop_loss=True,
                                    split_to_do=split_to_do, ml_to_use=ml_to_use)

            while boll.step != len(boll.df.index):
                state = boll.get_state()
                action = boll.get_action(state)
                boll.process_action(action, state)
                boll.update_step(boll.step + 1)

            boll.save_tradelog()

# Example usage
run_all_bollinger_two_trades('test1mlbollinger22', ["Naive","Naive Bayes", "Log Reg", "KNN", "RFC", "NN"])
