import unittest
import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_DIR
import os

directory = os.path.join(DATA_DIR, 'dataDailyTwoCol')

aapl = os.path.join(directory, 'AAPL.csv')



class MyTestCase(unittest.TestCase):
    def test_something(self):
        df_aapl = pd.read_csv(aapl)

        plt.plot(df_aapl['Day'], df_aapl['ReturnPrice'])

        plt.show()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
