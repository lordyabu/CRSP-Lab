import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv("C:/Users/theal/Documents/dataEnsembleLegends/bollingerData/AAPL.csv")

# Calculate rolling high, low, and close returns
df['Rolling_Max_20'] = df['High'].rolling(window=20).max()
df['Rolling_Min_20'] = df['Low'].rolling(window=20).min()
df['Rolling_Max_55'] = df['High'].rolling(window=55).max()
df['Rolling_Min_55'] = df['Low'].rolling(window=55).min()

# Initialize position and portfolio value
position = 0
portfolio_value = 100000  # Starting with $100,000

for index, row in df.iterrows():

    print(row['Close'], row['Rolling_Max_20'])

    # Entry Signals for System 1 (20-day breakout)
    if row['Close'] > row['Rolling_Max_20']:
        # Buy signal
        if position <= 0:
            position += 1
            print(f"Buy 1 Unit at day {index + 1} with return {row['Close']}")
    elif row['Close'] < row['Rolling_Min_20']:
        # Sell signal
        if position >= 0:
            position -= 1
            print(f"Sell 1 Unit at day {index + 1} with return {row['Close']}")

    # Exit Signals for System 1 (10-day breakout)
    if position > 0 and row['Close'] < df['Low'].rolling(window=10).min()[index]:
        # Exit long position
        position = 0
        print(f"Exit long position at day {index + 1} with return {row['Close']}")
    elif position < 0 and row['Close'] > df['High'].rolling(window=10).max()[index]:
        # Exit short position
        position = 0
        print(f"Exit short position at day {index + 1} with return {row['Close']}")

    # Portfolio value update based on position and daily return
    if position != 0:
        # Assuming buying 1 unit involves investing a fixed fraction of the portfolio
        # and returns are compounded
        investment_fraction = 0.01  # 1% of the portfolio value
        portfolio_change = (row['Return'] + 1) ** position - 1  # Compound return
        portfolio_value *= (1 + investment_fraction * portfolio_change)

print(f"Final portfolio value: {portfolio_value}")
