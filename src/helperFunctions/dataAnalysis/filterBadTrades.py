# As data doesn't factor in share splits we need to void trades that occur during said splits
# We can check this by analyzing return % and if the change is price resembles a split e.x. (7 : 1) or (5:1)
import pandas as pd

# However, for now we will remove trades that are abs(chg) > 45



def remove_naive(trades):
    # Filter the trades DataFrame to keep rows where the absolute value of 'PnL%' is less than or equal to 0.45
    filtered_trades = trades[abs(trades['PnL%']) <= 100]
    return filtered_trades
