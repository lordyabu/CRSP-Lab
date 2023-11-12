import unittest
import os
import pandas as pd
import json
from src.config import DATA_DIR

directory_test = os.path.join(DATA_DIR, 'priceDataOHLCSplitTest')
five_min_directory = os.path.join(DATA_DIR, 'dataFiveMin', '.csv')

valid_directory = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')


class MyTestCase(unittest.TestCase):



    # Make sure all columns are filled, if not show what stocks, columns are not filled in the valid set

    def test_all_vals_field(self):
        errors = []  # List to accumulate assertion errors

        with open(valid_directory, 'r') as f:
            valid_stock_data = json.load(f)

        valid_stock_names = valid_stock_data['valid_files']

        for stock_filename in valid_stock_names:
            try:
                stock_directory = os.path.join(directory_test, stock_filename)
                stock_df = pd.read_csv(stock_directory)

                # Ensure 'date' column exists for referencing
                if 'date' not in stock_df.columns:
                    errors.append(f"Error: 'date' column missing in {stock_filename}")
                    continue  # Skip this file because 'date' column is necessary for further checks

                for field in ['Open', 'High', 'Low', 'Close']:
                    if field not in stock_df.columns:
                        errors.append(f"Error: {field} column missing in {stock_filename}")
                    elif stock_df[field].dtype != float:
                        errors.append(f"Error: {field} column in {stock_filename} is not of type float")
                    else:
                        # Check for NaN values
                        nan_indices = stock_df[stock_df[field].isna()].index
                        if not nan_indices.empty:
                            first_nan_index = nan_indices[0]
                            date_at_nan = stock_df.at[first_nan_index, 'date']
                            errors.append(
                                f"Error: {field} column in {stock_filename} contains NaN value at date: {date_at_nan}")

                        # Check for negative values
                        negative_values = stock_df[stock_df[field] < 0]
                        if not negative_values.empty:
                            first_negative_index = negative_values.index[0]
                            date_at_negative = stock_df.at[first_negative_index, 'date']
                            errors.append(
                                f"Error: {field} column in {stock_filename} contains negative value at date: {date_at_negative}, {negative_values}")

            except Exception as e:
                errors.append(f"Exception: Error processing {stock_filename}: {str(e)}")

        # After all files are processed, check if there were any errors collected
        if errors:
            error_message = "\n".join(errors)
            self.fail(f"Test failed with the following errors:\n{error_message}")

    def test_specifics(self, stock='AAPL', loose=True):
        errors = []  # List to collect errors

        places_close = 2 if loose else 5
        test_dates = [20030103, 20110511, 20170315, 20190610, 20201214, 20201231]

        file_path_test = os.path.join(directory_test, f"{stock}.csv")

        df_test = pd.read_csv(file_path_test)
        df_test = df_test.reset_index()

        for date_val in test_dates:
            try:
                file_path_five = os.path.join(five_min_directory, f'Day_{date_val}.csv')
                df_five = pd.read_csv(file_path_five)

                if date_val in df_test['date'].values:
                    row = df_test[df_test['date'] == date_val]
                else:
                    errors.append(f"Date {date_val} not found in df_test for stock {stock}")
                    continue  # Skip to the next date

                # Access the Close, High, Open, and Low values for that date
                check_open = round(row['Open'].values[0], 2)
                check_high = round(row['High'].values[0], 2)
                check_low = round(row['Low'].values[0], 2)
                check_close = round(row['Close'].values[0], 2)

                if date_val == 20201231:
                    historical_relative = {'Open': round(134.08, 1), 'High': round(134.74, 1), 'Low': round(131.72, 1), 'Close': round(132.69, 1)}
                    try:
                        self.assertAlmostEqual(check_close, historical_relative['Close'], places=places_close)
                        self.assertAlmostEqual(check_high, historical_relative['High'], places=places_close)
                        self.assertAlmostEqual(check_open, historical_relative['Open'], places=places_close)
                        self.assertAlmostEqual(check_low, historical_relative['Low'], places=places_close)
                    except AssertionError as e:
                        errors.append(f"Historical data test failed for {stock} on {date_val}: {str(e)}")
                else:
                    curr_price = check_open
                    prices = [curr_price]
                    for i in range(len(df_five)):
                        return_val = df_five.iloc[i][stock] + 1
                        curr_price *= return_val
                        prices.append(curr_price)

                    open_check = round(prices[0], 2)
                    high_check = round(max(prices), 2)
                    low_check = round(min(prices), 2)
                    close_check = round(prices[-1], 2)

                    try:
                        self.assertAlmostEqual(check_open, open_check, places=places_close)
                        self.assertAlmostEqual(check_high, high_check, places=places_close)
                        self.assertAlmostEqual(check_low, low_check, places=places_close)
                        self.assertAlmostEqual(check_close, close_check, places=places_close)
                    except AssertionError as e:
                        errors.append(f"Non-historical data test failed for {stock} on {date_val}: {str(e)}")

            except Exception as e:
                errors.append(f"Error processing stock {stock} on {date_val}: {str(e)}")

        # Assert no errors were found
        assert not errors, "Errors occurred:\n" + "\n".join(errors)



if __name__ == '__main__':
    unittest.main()
