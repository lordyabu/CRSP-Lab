# This script contains a function to process CSV files in a given directory, ensuring that certain numeric values are positive.
# It reads each file, converts negative values in specific columns to their absolute values, and saves the modified data to an output directory.
# It also tracks processed files and returns a log entry with details of the operation.

import os
import pandas as pd
from datetime import datetime


def force_positives(directory, output_directory):
    """
    Processes CSV files in a directory to ensure specific numeric columns only contain positive values.

    This function iterates over all CSV files in the given directory, modifies any negative values in 'OPENPRC' and 'PRC' columns
    to their absolute values, and saves the updated files to a specified output directory. It also keeps track of the files processed
    and returns a log entry with the details of this operation.

    Args:
        directory (str): Path to the directory containing the CSV files to be processed.
        output_directory (str): Path to the directory where the processed files will be saved.

    Returns:
        dict: A log entry containing details of the operation, including the operation name, processed files,
              output directory, and a timestamp.
    """
    processed_files = []  # Keep track of processed files

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)

            # Check and replace negative values in 'OPENPRC' and 'PRC' with their absolute values
            data['OPENPRC'] = data['OPENPRC'].apply(lambda x: abs(x) if x < 0 else x)
            data['PRC'] = data['PRC'].apply(lambda x: abs(x) if x < 0 else x)

            # After operations, save the DataFrame
            output_file_path = os.path.join(output_directory, filename)
            data.to_csv(output_file_path, index=False)
            processed_files.append(filename)  # Add the filename to the list of processed files

    # Log entry at the end of processing
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "operation": "Force Positive Values",
        "details": f"Processed files with forced positive values in {output_directory}",
        "files_processed": processed_files,
        "timestamp": current_datetime

    }
    return log_entry
