import json
import os
def log_to_json(log_file_path, log_entries):
    """
    Logs a list of entries to a specified JSON log file.

    :param log_file_path: Path to the log file.
    :param log_entries: A list of entries to log.
    """
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
