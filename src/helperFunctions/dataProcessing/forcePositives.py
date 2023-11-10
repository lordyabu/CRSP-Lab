import os
import pandas as pd
from datetime import datetime
def force_positives(directory, output_directory):
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
