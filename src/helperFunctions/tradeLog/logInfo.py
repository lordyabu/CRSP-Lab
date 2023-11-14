# This script provides a function to log data entries into a JSON file.
# It takes a log file path and a list of log entries, appending the new entries to the existing content of the file.
# If the file doesn't exist or isn't valid JSON, it starts with an empty list.

import json
import os
from pathlib import Path
def log_to_json(log_file_path, log_entries):
    """
    Appends a list of entries to a specified JSON log file, creating or resetting it if necessary.

    This function checks if the specified log file exists and contains valid JSON. If so, it loads the existing log data,
    appends the new entries to it, and then writes the updated data back to the file. If the file doesn't exist or contains invalid JSON,
    it starts with an empty log and adds the new entries.

    Args:
        log_file_path (str or Path): Path to the log file. Can be a string or a Path object.
        log_entries (list): A list of entries (dictionaries) to log.

    """
    # Convert string path to Path object if necessary
    log_file_path = Path(log_file_path) if isinstance(log_file_path, str) else log_file_path

    # If the file exists and is not empty, load its content. Otherwise, start with an empty list.
    if log_file_path.is_file() and os.path.getsize(log_file_path) > 0:
        with open(log_file_path, 'r') as file:
            try:
                log_data = json.load(file)
            except json.JSONDecodeError:
                log_data = []  # Reset if the file content is not valid JSON
    else:
        log_data = []

    # Extend the log data with the new entries
    log_data.extend(log_entries)

    # Write the updated log data back to the file
    with open(log_file_path, 'w') as file:
        json.dump(log_data, file, indent=4)
