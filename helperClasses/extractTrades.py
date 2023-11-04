import pandas as pd
from config import DATA_DIR
import os

full_tradelog_path = os.path.join(DATA_DIR, 'tradeData', 'allTrades.csv')


def extract_trades(identifier):
    df = pd.read_csv(full_tradelog_path)

    # Filter the DataFrame to only include rows where 'Identifier' matches the identifier
    df_filtered = df[df['Identifier'] == identifier]

    # Return the filtered DataFrame
    return df_filtered


# Usage example
# identifier_to_extract = 'test0'
# extracted_trades = extract_trades(identifier_to_extract)
# print(extracted_trades)
