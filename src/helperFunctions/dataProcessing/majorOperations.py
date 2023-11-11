import pandas as pd
import os
import json
from src.config import DATA_DIR, PRICE_DATA_DIR
from pathlib import Path
from src.helperFunctions.dataProcessing.replaceNaNs import fill_nan_according_to_rules
from src.helperFunctions.dataProcessing.forcePositives import force_positives
from src.helperFunctions.logInfo import log_to_json

directory = os.path.join(DATA_DIR, 'priceDataSplit')
output_directory = Path(PRICE_DATA_DIR)
output_directory.mkdir(parents=True, exist_ok=True)
log_file_name = 'majorOpLog.json'
log_file_path = Path(__file__).resolve().parents[2] / 'tests' / log_file_name

def major_operations(NaNs=False, positive=False, save_to_log=True):
    log_info = []

    if NaNs:
        log_info.append(fill_nan_according_to_rules(directory, output_directory))
    if positive:
        input_dir = output_directory if NaNs else directory
        log_info.append(force_positives(input_dir, output_directory))

    if save_to_log:
        log_to_json(log_file_path, log_info)

