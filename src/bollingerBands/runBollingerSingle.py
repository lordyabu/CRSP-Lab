import pandas as pd

from bollingerNaive import BollingerNaive



def run_stuffs():
    boll = BollingerNaive(stock_name='AAPL', band_data_name='Default',identifier='test4', time_period='Daily', reset_indexes=False, step=0)

    while boll.step != len(boll.df.index):
        state = boll.get_state()
        boll.get_and_process_action(state)

        boll.update_step(boll.step + 1)

    boll.save_tradelog()




run_stuffs()