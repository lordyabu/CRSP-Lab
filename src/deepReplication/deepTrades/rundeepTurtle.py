from src.deepReplication.deepTrades.deepTurtle import MLTurtleNaive
from src.config import DATA_DIR
import os
import json
from tqdm import tqdm
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_turtle_single():
    turt = MLTurtleNaive(stock_name='GOOG',identifier='testGOOGturtle', time_period='Daily', reset_indexes=False, step=2000, ml_to_use='Naive', split_to_do="34_33_33")

    while turt.step != len(turt.df.index):
        state = turt.get_state()
        action = turt.get_action(state)
        turt.process_action(action, state['CurrentPrice'])

        turt.update_step(turt.step + 1)

    turt.save_tradelog()

def run_turtle_trade_for_stock(stock, identifier, ml_to_use, split_to_do):
    try:
        turt = MLTurtleNaive(stock_name=f'{stock}', identifier=f'{ml_to_use}_{split_to_do}_{identifier}', time_period='Daily',
                             reset_indexes=False, step=2000, ml_to_use=ml_to_use, split_to_do=split_to_do)

        while turt.step != len(turt.df.index):
            state = turt.get_state()
            action = turt.get_action(state)
            turt.process_action(action, state['CurrentPrice'])
            turt.update_step(turt.step + 1)

        turt.save_tradelog()
    except Exception as e:
        print(f"Error processing {stock}: {e}")


def run_all_turtle_trades(identifier):
    split_to_do = "34_33_33"
    mls_to_use = ["Naive","Naive Bayes", "Log Reg", "KNN", "RFC", "NN"]

    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for ml_to_use in mls_to_use:
        print(f"Running analysis with {ml_to_use}")

        for stock in tqdm(valid_stocks, desc=f"Processing with {ml_to_use}"):
            run_turtle_trade_for_stock(stock, identifier, ml_to_use, split_to_do)

        print(f"Completed analysis with {ml_to_use}")

if __name__ == '__main__':
    run_all_turtle_trades('test1mlturtles')