# This script contains a function to remove specific trades from a trade log file based on an identifier.
# The function reads the trade log, filters out the rows with the specified identifier, and saves the updated data back to the file.


import pandas as pd
from getTradeLogPath import get_full_tradelog_path


def remove_trades(identifier):
    """
    Removes trades with a specific identifier from the trade log file.

    This function reads the trade log file, filters out all trades with the given identifier,
    and then saves the updated log back to the file. The function relies on 'get_full_tradelog_path'
    to determine the path of the trade log file.

    Args:
        identifier (str): The identifier used to filter out trades. Trades with this identifier will be removed from the log.
    """

    full_tradelog_path = get_full_tradelog_path()

    df = pd.read_csv(full_tradelog_path)

    # Filter out the rows where 'Identifier' column matches the identifier
    df_filtered = df[df['Identifier'] != identifier]

    # Save the filtered DataFrame back to the CSV
    df_filtered.to_csv(full_tradelog_path, index=False)
    print(f"Trades with identifier '{identifier}' have been removed.")


# Usage example
# identifier_to_remove = 'test3bollinger'
# remove_trades(identifier_to_remove)
