import pandas as pd
from src.helperFunctions.getTradeLogPath import get_full_tradelog_path


def extract_trades(identifier=None, strategy=None, sort_by='EndDate', stock_name=None, trade_type=None):
    # Check that at least one of identifier or strategy is provided
    if identifier is None and strategy is None:
        raise ValueError("At least one of 'identifier' or 'strategy' must be provided")

    full_tradelog_path = get_full_tradelog_path()
    df = pd.read_csv(full_tradelog_path)

    # Convert 'StartDate' and 'EndDate' to datetime
    df['StartDate'] = pd.to_datetime(df['StartDate'], format='%Y%m%d')
    df['EndDate'] = pd.to_datetime(df['EndDate'], format='%Y%m%d')

    # Initialize the filter
    filter_condition = pd.Series([False] * len(df))

    # Apply identifier filter if provided
    if identifier:
        filter_condition |= (df['Identifier'] == identifier)

    # Apply strategy filter if provided
    if strategy:
        filter_condition |= (df['Strategy'] == strategy)

    # Apply the filter
    df_filtered = df[filter_condition]

    # Additional filters for stock name and trade type
    if stock_name:
        df_filtered = df_filtered[df_filtered['Symbol'] == stock_name]
    if trade_type:
        df_filtered = df_filtered[df_filtered['TradeType'] == trade_type]

    # Sort the filtered DataFrame
    df_sorted = df_filtered.sort_values(by=sort_by)

    # Return the sorted DataFrame
    return df_sorted


# Usage example
# identifier_to_extract = 'test1'
# extracted_trades = extract_trades(identifier_to_extract, sort_by='EndDate')
# print(extracted_trades['EndDate'])
