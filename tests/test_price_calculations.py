import unittest
import pandas as pd
import json
import os
from src.config import DATA_DIR

directory = os.path.join(DATA_DIR, 'priceData')
valid_directory = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')

class MyTestCase(unittest.TestCase):

    def test_stocks_have_positive_prices(self):
        # Open the JSON file and load it into a variable
        with open(valid_directory, 'r') as f:
            valid_stock_data = json.load(f)

        # Extract valid stock names from the JSON data
        valid_stock_names = valid_stock_data['valid_files']

        # Iterate over the stock names
        for stock_filename in valid_stock_names:
            stock_directory = os.path.join(directory, stock_filename)
            stock_df = pd.read_csv(stock_directory)

            prices = stock_df['PRC']

            # Check if all prices are greater than 0 using a pandas Series method
            self.assertTrue((prices > 0).all(), f"Stock {stock_filename} has non-positive prices")

# Run the tests
if __name__ == '__main__':
    unittest.main()
