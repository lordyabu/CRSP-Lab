# This script features a function dedicated to executing the Turtle trading strategy for a single stock.
# Utilizing the TurtleNaive class, it processes trading data for a specified stock, applying the Turtle strategy
# step-by-step through the dataset. The function manages the trading state and actions, updates steps based on market conditions,
# and concludes by saving the trade log. This script is particularly useful for analyzing the performance of the Turtle strategy
# on an individual stock basis, providing insights into the effectiveness of the strategy for specific market scenarios.


from src.turtles.turtleNaive import TurtleNaive



def run_turtle_single():
    turt = TurtleNaive(stock_name='GOOG', rolling_window_name='Default',identifier='testGOOGturtle', time_period='Daily', reset_indexes=False, step=0)

    while turt.step != len(turt.df.index):
        state = turt.get_state()
        action = turt.get_action(state)
        turt.process_action(action, state['CurrentPrice'])

        turt.update_step(turt.step + 1)

    turt.save_tradelog()
