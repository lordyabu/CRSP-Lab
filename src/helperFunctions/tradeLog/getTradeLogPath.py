# This script defines a function to construct the full path for a trade log file.
# The function reads start and end dates from a JSON file containing metadata about valid stock filenames,
# and then creates a path for a trade log file named according to these dates.
# The trade log file is assumed to contain trading data within the specified date range.

from src.config import DATA_DIR
import os
import json


def get_full_tradelog_path():
    """
    Constructs the full path for a trade log file based on the start and end dates stored in a JSON file.

    This function reads a JSON file containing metadata about valid stock filenames, extracts the start and end dates,
    and then constructs a filename for a trade log. The filename is formed by appending the start and end dates to a base string.
    The full path to this trade log file is then returned.

    Returns:
        str: The full path to the trade log file. The filename is formatted as 'allTrades_{start_date}_to_{end_date}_example.csv',
             where {start_date} and {end_date} are replaced with the actual dates from the JSON file.
    """
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract start_date and end_date
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Construct the filename with the start and end dates
    filename = f"allTrades_{start_date}_to_{end_date}_doctest2.csv"
    full_tradelog_path = os.path.join(DATA_DIR, 'tradeData', filename)

    return full_tradelog_path



def get_full_ml_tradelog_path():
    """
    Constructs the full path for a trade log file based on the start and end dates stored in a JSON file.

    This function reads a JSON file containing metadata about valid stock filenames, extracts the start and end dates,
    and then constructs a filename for a trade log. The filename is formed by appending the start and end dates to a base string.
    The full path to this trade log file is then returned.

    Returns:
        str: The full path to the trade log file. The filename is formatted as 'allTrades_{start_date}_to_{end_date}_example.csv',
             where {start_date} and {end_date} are replaced with the actual dates from the JSON file.
    """
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract start_date and end_date
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Construct the filename with the start and end dates
    filename = f"tst_ML_allTrades_{start_date}_to_{end_date}_doctest2.csv"
    full_tradelog_path = os.path.join(DATA_DIR, 'tradeData', filename)

    return full_tradelog_path
