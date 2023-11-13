from src.config import DATA_DIR
from src.turtles.turtleNaive import TurtleNaive
import os
import json
from tqdm import tqdm\


def run_all_turtle_trades(identifier):
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    for stock in tqdm(valid_stocks, desc='Processing stocks'):
        turt = TurtleNaive(stock_name=f'{stock}', rolling_window_name='Default',identifier=f'{identifier}', time_period='Daily', reset_indexes=False, step=0)

        while turt.step != len(turt.df.index):
            state = turt.get_state()
            action = turt.get_action(state)
            turt.process_action(action, state['CurrentPrice'])
            turt.update_step(turt.step + 1)

        turt.save_tradelog()


# run_all_turtle_trades('test6turtle')
