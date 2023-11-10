from src.config import DATA_DIR
import os
import json

def get_full_tradelog_path():
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract start_date and end_date
    start_date = data.get('start_date').replace('Day_', '')
    end_date = data.get('end_date').replace('Day_', '')

    # Construct the filename with the start and end dates
    filename = f"allTrades_{start_date}_to_{end_date}.csv"
    full_tradelog_path = os.path.join(DATA_DIR, 'tradeData', filename)

    return full_tradelog_path