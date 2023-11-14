from src.bollingerBands.bollingerNaive import BollingerNaive


def run_single_bollinger():
    """
    Executes the Bollinger Band-based trading strategy for a single stock.

    This function creates an instance of the BollingerNaive class for the stock 'GOOG',
    then iteratively processes the trading data through the entire dataset.
    It manages the trading state, actions, and steps for each point in the data,
    and finally, it saves the trade log upon completion.

    """
    boll = BollingerNaive(stock_name='GOOG', band_data_name='Default', identifier='test4past50', time_period='Daily',
                          reset_indexes=False, step=0)

    while boll.step != len(boll.df.index):
        state = boll.get_state()
        action = boll.get_action(state)
        boll.process_action(action)

        boll.update_step(boll.step + 1)

    boll.save_tradelog()
