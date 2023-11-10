import unittest
import pandas as pd
import json
import os
from src.config import DATA_DIR, PRICE_DATA_DIR

directory = PRICE_DATA_DIR
valid_directory = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')

class TestMajorOp(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMajorOp, self).__init__(*args, **kwargs)
        self.test_NaNs = False
        self.test_positives = False


    def set_test_flags(self, test_NaNs, test_positives):
        self.test_NaNs = test_NaNs
        self.test_positives = test_positives

    def test_NaNs_major_op(self):
        if not self.test_NaNs:
            return

        errors = []

        with open(valid_directory, 'r') as f:
            valid_stock_data = json.load(f)

        valid_stock_names = valid_stock_data['valid_files']

        for stock_filename in valid_stock_names:
            try:
                stock_directory = os.path.join(directory, stock_filename)
                stock_df = pd.read_csv(stock_directory)

                if 'date' not in stock_df.columns:
                    errors.append(f"Error: 'date' column missing in {stock_filename}")
                    continue

                for field in ['PRC', 'OPENPRC']:
                    if field not in stock_df.columns:
                        first_nan_index = nan_indices[0]
                        date_at_nan = stock_df.at[first_nan_index, 'date']
                        errors.append(f"Error: {field} column missing in {stock_filename} at date: {date_at_nan}")
                    elif stock_df[field].dtype != float:
                        first_nan_index = nan_indices[0]
                        date_at_nan = stock_df.at[first_nan_index, 'date']
                        errors.append(f"Error: {field} column in {stock_filename} is not of type float at date: {date_at_nan}")
                    else:
                        # Check for NaN values and get the 'date' value at the first index where NaN is found
                        nan_indices = stock_df[stock_df[field].isna()].index
                        if not nan_indices.empty:
                            first_nan_index = nan_indices[0]
                            date_at_nan = stock_df.at[first_nan_index, 'date']
                            errors.append(
                                f"Error: {field} column in {stock_filename} contains NaN value at date: {date_at_nan}")

            except Exception as e:
                errors.append(f"Exception: Error processing {stock_filename}: {str(e)}")

        if errors:
            error_message = "\n".join(errors)
            self.fail(f"Test failed with the following errors:\n{error_message}")

    def test_positive_major_op(self):
        if not self.test_positives:
            return


        with open(valid_directory, 'r') as f:
            valid_stock_data = json.load(f)

        valid_stock_names = valid_stock_data['valid_files']

        for stock_filename in valid_stock_names:
            stock_directory = os.path.join(directory, stock_filename)
            stock_df = pd.read_csv(stock_directory)

            prices = stock_df['PRC']

            # Check if all prices are greater than 0 using a pandas Series method
            self.assertTrue((prices > 0).all(), f"Stock {stock_filename} has non-positive prices")

# Run the tests
if __name__ == '__main__':
    unittest.main()
