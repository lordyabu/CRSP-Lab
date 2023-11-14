# This script includes the 'run_all_turtle_trades' function, which automates the execution of the Turtle trading strategy
# across a range of stocks listed in a JSON file. For each stock, it iteratively processes trading data,
# making decisions and updating steps based on the TurtleNaive class, until all data points are processed.
# The trade log for each stock is saved upon completion.

from src.config import DATA_DIR
from src.turtles.turtleNaive import TurtleNaive
import os
import json
from tqdm import tqdm


def run_all_turtle_trades(identifier):
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for stock in tqdm(valid_stocks, desc='Processing stocks'):
        turt = TurtleNaive(stock_name=f'{stock}',identifier=f'{identifier}', time_period='Daily', reset_indexes=False, step=0)

        while turt.step != len(turt.df.index):
            state = turt.get_state()
            action = turt.get_action(state)
            turt.process_action(action, state['CurrentPrice'])
            turt.update_step(turt.step + 1)

        turt.save_tradelog()


