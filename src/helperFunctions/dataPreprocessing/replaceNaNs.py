# This script contains a function for processing CSV files to fill NaN values according to specific rules.
# It targets columns like 'OPENPRC' and 'PRC', replacing NaNs with appropriate values based on the data's context.
# The function also tracks and logs the files processed, saving the modified data to a specified output directory.

import pandas as pd
import os
from datetime import datetime

def fill_nan_according_to_rules(directory, output_directory):
    """
    Processes CSV files to fill NaN values according to predefined rules and saves the updated files.

    This function iterates through each CSV file in the given directory, fills NaN values in specific columns ('OPENPRC' and 'PRC'),
    and saves the processed files to the output directory. It skips files where the 'date' column contains NaN. The function
    also keeps track of files processed and returns a log entry summarizing the operation.

    Args:
        directory (str): The path to the directory containing the CSV files to be processed.
        output_directory (str): The path to the directory where the processed files will be saved.

    Returns:
        dict: A log entry containing details of the operation, including the operation name, processed files,
              output directory, and a timestamp.
    """
    processed_files = []  # Keep track of processed files

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)

            # Skip files where 'date' contains NaN
            if data['date'].isna().any():
                continue

            # Create a column to mark where NaNs were replaced
            data['NaN_Replaced'] = 0

            # Mark where 'OPENPRC' NaNs will be replaced
            data.loc[data['OPENPRC'].isna(), 'NaN_Replaced'] = 1

            # Fill 'OPENPRC' NaNs using the previous row's 'PRC'
            data['OPENPRC'] = data['OPENPRC'].fillna(data['PRC'].shift())

            # Mark where 'PRC' NaNs will be replaced
            data.loc[data['PRC'].isna(), 'NaN_Replaced'] = 1

            # Fill 'PRC' NaNs using 'OPENPRC' where possible, otherwise use the previous row's 'PRC'
            data['PRC'] = data['PRC'].fillna(data['OPENPRC']).fillna(data['PRC'].shift())

            # After operations, save the DataFrame
            output_file_path = os.path.join(output_directory, filename)
            data.to_csv(output_file_path, index=False)
            processed_files.append(filename)  # Add the filename to the list of processed files

    # Write a single log entry at the end of processing
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "operation": "NaN replacement",
        "details": f"Processed files with NaN replacement in {output_directory}",
        "files_processed": processed_files,
        "timestamp": current_datetime
    }

    return log_entry
