# This script defines a function to perform major data processing operations on stock price data.
# It includes options to fill NaN values, enforce positive values in the data, and log these operations.
# The processed data is saved in a specified output directory, and the log of operations can be saved to a JSON file.
# For more details on major operations see ./notes/DataPreprocessing.txt

import os
from src.config import PRICE_DATA_DIR, RAW_PRICE_DATA_DIR
from pathlib import Path
from src.helperFunctions.dataPreprocessing.replaceNaNs import fill_nan_according_to_rules
from src.helperFunctions.dataPreprocessing.forcePositives import force_positives
from src.helperFunctions.tradeLog.logInfo import log_to_json

directory = RAW_PRICE_DATA_DIR
output_directory = Path(PRICE_DATA_DIR)
output_directory.mkdir(parents=True, exist_ok=True)
log_file_name = 'majorOpLog.json'
log_file_path = Path(__file__).resolve().parents[2] / 'tests' / log_file_name

def major_operations(NaNs=False, positive=False, save_to_log=True):
    """
    Performs major data processing operations on stock price data and optionally logs the operations.

    This function can fill NaN values and/or ensure positive values in the data, based on the parameters provided.
    The operations performed are logged if 'save_to_log' is set to True. The results of these operations are
    appended to a log file.

    Args:
        NaNs (bool): If True, NaN values in the data will be filled according to predefined rules.
        positive (bool): If True, negative values in the data will be converted to positive values.
        save_to_log (bool): If True, the operations performed (and their outcomes) will be logged in a JSON file.

    """
    log_info = []

    if NaNs:
        log_info.append(fill_nan_according_to_rules(directory, output_directory))
    if positive:
        input_dir = output_directory if NaNs else directory
        log_info.append(force_positives(input_dir, output_directory))

    if save_to_log:
        log_to_json(log_file_path, log_info)

