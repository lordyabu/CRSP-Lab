# As data doesn't factor in share splits we need to void trades that occur during said splits
# We can check this by analyzing return % and if the change is price resembles a split e.x. (7 : 1) or (5:1)
import pandas as pd

# However, for now we will remove trades that are abs(chg) > 45

from getTradeLogPath import get_full_tradelog_path


def remove_naive():
    # Read the trade log file into a DataFrame
    trade_log_path = get_full_tradelog_path()
    df = pd.read_csv(trade_log_path)

    # Calculate absolute percentage change
    df['abs_chg'] = abs((df['ExitPrice'] - df['EnterPrice']) / df['EnterPrice']) * 100

    # Remove rows where abs(chg) > 45%
    df = df[df['abs_chg'] <= 45]

    # Remove columns with the name "Unnamed: 0"
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Save the cleaned DataFrame back to the trade log file
    df.to_csv(trade_log_path, index=False)

# Call the function to remove rows with abs(chg) > 45% and save the cleaned DataFrame
remove_naive()