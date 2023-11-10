import pandas as pd
import os
import json
from src.config import DATA_DIR
from pathlib import Path

directory = os.path.join(DATA_DIR, 'priceData')
output_directory = os.path.join(DATA_DIR, 'priceDataTest')


def fill_nan_according_to_rules(directory, output_directory):
    processed_files = []  # Keep track of processed files

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)

            # Skip files where 'date' contains NaN
            if data['date'].isna().any():
                continue

            # Perform the NaN filling operations as described earlier...

            # After operations, save the DataFrame
            output_file_path = os.path.join(output_directory, filename)
            data.to_csv(output_file_path, index=False)
            processed_files.append(filename)  # Add the filename to the list of processed files

    # Write a single log entry at the end of processing
    log_entry = {
        "operation": "NaN replacement",
        "details": f"Processed files with NaN replacement in {output_directory}",
        "files_processed": processed_files
    }
    return log_entry


# Ensure the output directory exists
output_directory = Path(DATA_DIR) / 'priceDataTest'
output_directory.mkdir(parents=True, exist_ok=True)

# Usage
log_info = fill_nan_according_to_rules(directory, output_directory)

# Define the path for your log file
log_file_name = 'majorOpLog.json'  # Change this to your desired log file name
log_file_path = Path(__file__).resolve().parents[2] / 'tests' / log_file_name


# Function to log information to a JSON file
def log_to_json(log_file_path, log_entry):
    # If the file exists and is not empty, load its content. Otherwise, start with an empty list.
    if log_file_path.is_file() and os.path.getsize(log_file_path) > 0:
        with open(log_file_path, 'r') as file:
            try:
                log_data = json.load(file)
            except json.JSONDecodeError:
                log_data = []  # Reset if the file content is not valid JSON
    else:
        log_data = []

    log_data.append(log_entry)

    # Write the updated log data back to the file
    with open(log_file_path, 'w') as file:
        json.dump(log_data, file, indent=4)


# Log the information after processing
log_to_json(log_file_path, log_info)