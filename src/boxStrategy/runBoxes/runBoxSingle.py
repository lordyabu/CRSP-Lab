from src.boxStrategy.boxNaive import DarvasTrader



def run_box_single():
    box = DarvasTrader(stock_name='TSLA', identifier='testTSLAbox', time_period='Daily', reset_indexes=False, step=0)

    while box.step != len(box.df.index):
        state = box.get_state()
        action = box.get_action(state)
        box.process_action(action, state['CurrentPrice'])

        box.update_step(box.step + 1)

    box.save_tradelog()


run_box_single()