import unittest
import pandas as pd
import json
import os
from src.config import DATA_DIR

directory = os.path.join(DATA_DIR, 'priceDataTest')
valid_directory = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')

class MyTestCase(unittest.TestCase):

    def test_all_vals_field(self):
        errors = []  # List to accumulate assertion errors

        with open(valid_directory, 'r') as f:
            valid_stock_data = json.load(f)

        valid_stock_names = valid_stock_data['valid_files']

        for stock_filename in valid_stock_names:
            try:
                stock_directory = os.path.join(directory, stock_filename)
                stock_df = pd.read_csv(stock_directory)

                # Ensure 'date' column exists for referencing
                if 'date' not in stock_df.columns:
                    errors.append(f"Error: 'date' column missing in {stock_filename}")
                    continue  # Skip this file because 'date' column is necessary for further checks

                for field in ['PRC', 'OPENPRC']:
                    if field not in stock_df.columns:
                        errors.append(f"Error: {field} column missing in {stock_filename}")
                    elif stock_df[field].dtype != float:
                        errors.append(f"Error: {field} column in {stock_filename} is not of type float")
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

        # After all files are processed, check if there were any errors collected
        if errors:
            error_message = "\n".join(errors)
            self.fail(f"Test failed with the following errors:\n{error_message}")

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
