import pandas as pd
from config import DATA_DIR
import os
import json
from helperClasses.getTradeLogPath import get_full_tradelog_path


def extract_trades(identifier, sort_by='EndDate'):
    full_tradelog_path = get_full_tradelog_path()

    df = pd.read_csv(full_tradelog_path)

    # Convert 'StartDate' and 'EndDate' to datetime
    df['StartDate'] = pd.to_datetime(df['StartDate'].str.replace('Day_', ''), format='%Y%m%d')
    df['EndDate'] = pd.to_datetime(df['EndDate'].str.replace('Day_', ''), format='%Y%m%d')

    # Filter the DataFrame to only include rows where 'Identifier' matches the identifier
    df_filtered = df[df['Identifier'] == identifier]

    # Sort the filtered DataFrame based on the 'sort_by' column
    df_sorted = df_filtered.sort_values(by=sort_by)

    # Return the sorted DataFrame
    return df_sorted


# Usage example
# identifier_to_extract = 'test1'
# extracted_trades = extract_trades(identifier_to_extract, sort_by='EndDate')
# print(extracted_trades['EndDate'])
