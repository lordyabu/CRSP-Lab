from src.turtles.turtleNaive import TurtleNaive



def run_stuffs():
    turt = TurtleNaive(stock_name='GOOG', rolling_window_name='Default',identifier='testGOOGturtle', time_period='Daily', reset_indexes=False, step=0)

    while turt.step != len(turt.df.index):
        state = turt.get_state()
        action = turt.get_action(state)
        turt.process_action(action, state['CurrentPrice'])

        turt.update_step(turt.step + 1)

    turt.save_tradelog()




run_stuffs()