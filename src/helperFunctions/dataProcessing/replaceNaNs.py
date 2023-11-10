import pandas as pd
import os
from datetime import datetime

def fill_nan_according_to_rules(directory, output_directory):
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
