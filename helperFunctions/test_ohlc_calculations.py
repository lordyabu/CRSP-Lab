import unittest
import os
import pandas as pd

from config import DATA_DIR

directory_test = os.path.join(DATA_DIR, 'dataDailyTwoCol')
five_min_directory = os.path.join(DATA_DIR, 'dataFiveMin', '.csv')


class MyTestCase(unittest.TestCase):
    def test_something(self, stock='AAPL', loose=True):
        if loose:
            places_close = 2
        else:
            places_close = 5
        test_days = ['Day_20030102', 'Day_20110511', 'Day_20170315', 'Day_20190610', 'Day_20201214', 'Day_20201231']

        file_path_test = os.path.join(directory_test, f"{stock}.csv")
        df_test = pd.read_csv(file_path_test)



        for day in test_days:
            file_path_five = os.path.join(five_min_directory, f"{day}.csv")
            df_five = pd.read_csv(file_path_five)

            # Retrieve the row for the specific day
            row = df_test.loc[df_test['Day'] == day].squeeze()

            # Now you can access the Close, High, Open, and Low values for that day
            check_open = row['Open']
            check_high = row['High']
            check_low = row['Low']
            check_close = row['Close']

            # Getting data from yahoo finance for 2019 date
            if day =='Day_20190610':
                # Convert historical data to relative changes
                historical_open = 47.95
                historical_relative = {
                    'Open': 1,  # Opening price relative to itself is always 1
                    'High': 48.84 / historical_open,
                    'Low': 47.90 / historical_open,
                    'Close': 48.15 / historical_open,
                }

                # Compare using assertAlmostEqual
                self.assertAlmostEqual(check_close, historical_relative['Close'], places=places_close)
                self.assertAlmostEqual(check_high, historical_relative['High'], places=places_close)
                self.assertAlmostEqual(check_open, historical_relative['Open'], places=places_close)
                self.assertAlmostEqual(check_low, historical_relative['Low'], places=places_close)

                print("TESTED HISTORICAL DAY")
            else:
                prices = []
                curr_price = 1
                for i in range(0, len(df_five)):
                    return_val = df_five.iloc[i][stock] + 1

                    curr_price *= return_val

                    prices.append(curr_price)

                open_check = prices[0]
                high_check = max(prices)
                low_check = min(prices)
                close_check = prices[-1]

                self.assertAlmostEqual(check_open, open_check, places=places_close)
                self.assertAlmostEqual(check_high, high_check, places=places_close)
                self.assertAlmostEqual(check_low, low_check, places=places_close)
                self.assertAlmostEqual(check_close, close_check, places=places_close)



if __name__ == '__main__':
    unittest.main()
