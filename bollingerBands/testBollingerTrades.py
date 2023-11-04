import unittest
from config import DATA_DIR
import os
import pandas as pd

return_data_path = os.path.join(DATA_DIR, 'dataDailyTwoCol', 'AAPL.csv')
trade_data_path = os.path.join(DATA_DIR, 'tradeData', 'allTrades_20100104_to_20201231.csv')

class BollingerTests(unittest.TestCase):

    def setUp(self):
        print()
        self.trade_df = pd.read_csv(trade_data_path)
        self.price_df = pd.read_csv(return_data_path)
        self.price_df['Day'] = pd.to_datetime(self.price_df['Day'], format='Day_%Y%m%d')
        self.test_count = 0

    def test_multiple_trades(self):
        test_trades = [
            {'start_date': 'Day_20100119', 'end_date': 'Day_20100120', 'identifier': 'test1'},
            {'start_date': 'Day_20120925', 'end_date': 'Day_20120927', 'identifier': 'test1'},
            {'start_date': 'Day_20140103', 'end_date': 'Day_20140106', 'identifier': 'test1'},
            {'start_date': 'Day_20161101', 'end_date': 'Day_20161102', 'identifier': 'test1'},
            {'start_date': 'Day_20180911', 'end_date': 'Day_20180912', 'identifier': 'test1'},
            {'start_date': 'Day_20191029', 'end_date': 'Day_20191031', 'identifier': 'test1'},
            {'start_date': 'Day_20200921', 'end_date': 'Day_20200923', 'identifier': 'test1'},
        ]
        for test_trade in test_trades:
            self._test_pnl_calculation(test_trade)

    def _test_pnl_calculation(self, test_trade):

        test_start_date = test_trade['start_date']
        test_end_date = test_trade['end_date']
        identifier = test_trade['identifier']
        stock_name = 'AAPL'
        strategy = 'bollinger_naive'
        timeperiod = 'Daily'

        specific_trade = self.trade_df[
            (self.trade_df['StartDate'] == test_start_date) &
            (self.trade_df['EndDate'] == test_end_date) &
            (self.trade_df['Identifier'] == identifier) &
            (self.trade_df['Symbol'] == stock_name) &
            (self.trade_df['Strategy'] == strategy) &
            (self.trade_df['TimePeriod'] == timeperiod)
        ]
        pnl_from_trade = specific_trade['PnL'].iloc[0] if not specific_trade.empty else 0
        position_dir = specific_trade['TradeType'].iloc[0] if not specific_trade.empty else 0
        price_chunk = self.get_chunk_df(self.price_df, test_start_date, test_end_date)
        pnl_from_prices = self.calculate_pnl(price_chunk, position_dir)

        try:
            self.assertAlmostEqual(pnl_from_trade, pnl_from_prices, places=5)
            print(f"Trade {identifier} from {test_start_date} to {test_end_date}: PASS")
        except AssertionError as e:
            print(f"Trade {identifier} from {test_start_date} to {test_end_date}: FAIL - {e}")


    @staticmethod
    def get_chunk_df(df, start_date, end_date):
        start_date = pd.to_datetime(start_date, format='Day_%Y%m%d')
        end_date = pd.to_datetime(end_date, format='Day_%Y%m%d')
        mask = (df['Day'] >= start_date) & (df['Day'] <= end_date)
        return df.loc[mask]

    @staticmethod
    def calculate_pnl(df, direction):
        starting_price = 1
        count = 0
        for i, row in df.iterrows():
            return_rate = row['Return']
            if count != 0:
                starting_price *= (1 + return_rate)
            count += 1

        long_return = starting_price - 1

        if direction == 'long':
            return long_return
        elif direction == 'short':
            return long_return * -1
        else:
            raise ValueError(f"Direction not specified correctly: {direction}")

if __name__ == '__main__':
    unittest.main()
