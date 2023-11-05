from backtesting import Backtest, Strategy
from bollingerBands.bollingerNaive import BollingerNaive
import warnings
warnings.filterwarnings('ignore')
from backTesting.configBT import stock_to_check

class BollingerNaiveStrategy(Strategy):
    def init(self):
        self.boll = BollingerNaive(stock_name=f'{stock_to_check}', band_data_name='Default', identifier='test1', time_period='Daily',
                                   reset_indexes=False, step=0)
        self.entry_price = 0

        # Hack. Will break if there is an action that is first. Don't know why it's +2 instead of +1,
        # but it won't work otherwise
        state = self.boll.get_state()
        self.action = self.boll.get_and_process_action(state)
        self.boll.update_step(self.boll.step + 2)



    def next(self):
        if self.boll.step == len(self.boll.df.index):
            return
        state = self.boll.get_state()
        current_price = self.data.Close[-1]  # Assuming 'Close' is the closing price column
        self.action = self.boll.get_and_process_action(state)


        if self.action == 'EnterLong':
            # print(f'Enter Long at {self.boll.df.iloc[self.boll.step]["Day"]} at price {current_price}')
            self.buy(size=1)
            self.entry_price = current_price
        elif self.action == 'EnterShort':
            # print(f'Enter Short  at {self.boll.df.iloc[self.boll.step]["Day"]} at price {current_price}')
            self.sell(size=1)
            self.entry_price = current_price
        elif self.action == 'EndLong' or self.action == 'EndShort':
            # print(f'Exit position at {self.boll.df.iloc[self.boll.step]["Day"]}  at price {current_price}')
            self.position.close()
        elif self.action == 'Wait' or self.action == 'Hold':
            pass
        else:
            raise ValueError(f"Invalid Action: {self.action}")

        self.boll.update_step(self.boll.step + 1)

