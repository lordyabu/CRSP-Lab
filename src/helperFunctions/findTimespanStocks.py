import pandas as pd
import os
import json
from src.config import DATA_DIR, PRICE_DATA_DIR, OHLC_DATA_DIR

directory = OHLC_DATA_DIR
save_directory = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')


def save_stock_filenames_in_timespan_daily(start='20100104', end='20201231', exclude_nan=True, exclude_negative=True):
    """
    Save the filenames of stock files that are valid into a JSON file.
    A file is considered valid if it contains both the start and end dates, does not contain NaN values in 'date' (if exclude_nan is True),
    and does not contain negative values in 'PRC' and 'OPENPRC' (if exclude_positive is True).
    """

    # Clear the JSON file at the start
    with open(save_directory, 'w') as json_file:
        json_file.write("[]")

    # Get the number of timesteps for AAPL
    aapl_path = os.path.join(directory, 'AAPL.csv')
    aapl_data = pd.read_csv(aapl_path)
    aapl_data['date'] = aapl_data['date'].astype(str).str.replace('Day_', '')
    filtered_aapl_data = aapl_data[(aapl_data['date'] >= start) & (aapl_data['date'] <= end)]
    num_timesteps = len(filtered_aapl_data)

    # Initialize a list to hold the names of the files that fulfill the requirements
    valid_files = []

    # Loop over every file in the directory
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)
            data['date'] = data['date'].astype(str)

            if start in data['date'].values and end in data['date'].values:
                filtered_data = data[(data['date'] >= start) & (data['date'] <= end)]

                if len(filtered_data) == num_timesteps:
                    if not exclude_nan or not data[['PRC', 'OPENPRC', 'Close', 'Low', 'High', 'Open']].isnull().any(axis=1).any():
                        if not exclude_negative or (data['PRC'].ge(0).all() and data['OPENPRC'].ge(0).all()) and (data['High'].ge(0).all()) and (data['Low'].ge(0).all()):
                            valid_files.append(filename)
                        else:
                            print('neg')
                    else:
                        print('nan')
                else:
                    print('not same step')
            else:
                print('no date')

    # Save the list of filenames to the JSON file
    with open(save_directory, 'w') as json_file:
        json_data = {
            'valid_files': valid_files,
            'start_date': start,
            'end_date': end,
            'num_timesteps': num_timesteps,
            'exclude_nan': exclude_nan,
            'exclude_positive': exclude_negative,
            'num_stocks': len(valid_files)
        }
        json.dump(json_data, json_file, indent=4)

start = '20100104'
end = '20201231'
exclude_nan = True
exclude_negative = True
print("Performing timespan operations...")
save_stock_filenames_in_timespan_daily(start=start, end=end, exclude_nan=exclude_nan, exclude_negative=exclude_negative)