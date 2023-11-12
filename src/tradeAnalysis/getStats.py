from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
import matplotlib.pyplot as plt
from src.helperFunctions.dataAnalysis.filterBadTrades import remove_naive
def get_trade_stats(trades):
    # Calculate durations
    trades['TradeDuration'] = trades['EndDate'] - trades['StartDate']

    # Calculate stats
    start_date = trades['StartDate'].min()
    end_date = trades['EndDate'].max()
    duration = end_date - start_date
    total_trades = len(trades)
    unique_stocks = trades['Symbol'].nunique()
    winning_trades = trades[trades['PnL%'] > 0]
    losing_trades = trades[trades['PnL%'] < 0]
    win_rate = (len(winning_trades) / total_trades) * 100
    avg_win = winning_trades['PnL%'].mean()
    avg_loss = losing_trades['PnL%'].mean()
    median_win = winning_trades['PnL%'].median()  # Median win
    median_loss = losing_trades['PnL%'].median()  # Median loss
    avg_trade = trades['PnL%'].mean()
    median_trade = trades['PnL%'].median()  # Median trade
    total_return = trades['PnL'].sum()
    total_return_percent = trades['PnL%'].sum()  # Total return percentage

    # Print stats
    print(f"Start: {start_date}")
    print(f"End: {end_date}")
    print(f"Duration: {duration}")
    print(f"# Trades: {total_trades}")
    print(f"# Different Stocks: {unique_stocks}")
    print(f"Win Rate [%]: {win_rate}")
    print(f"Avg. Trade [%]: {avg_trade}")
    print(f"Median Trade [%]: {median_trade}")
    print(f"Avg. Win [%]: {avg_win}")
    print(f"Median Win [%]: {median_win}")
    print(f"Avg. Loss [%]: {avg_loss}")
    print(f"Median Loss [%]: {median_loss}")
    print(f"Total Return [%] (Where every trade is weighted equally): {total_return_percent}")

def plot_wins_and_losses(trades):
    # Sample 100 random trades if the total number of trades is more than 100
    if len(trades) > 100:
        trades_sample = trades.sample(n=100)
    else:
        trades_sample = trades

    # Separate winning and losing trades
    winning_trades = trades_sample[trades_sample['PnL'] > 0]
    losing_trades = trades_sample[trades_sample['PnL'] < 0]

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plot winning trades in green ($ and %)
    plt.scatter(winning_trades['EndDate'], winning_trades['PnL%'], color='lightgreen', label='Winning Trades [%]', alpha=1)

    # Plot losing trades in red ($ and %)
    plt.scatter(losing_trades['EndDate'], losing_trades['PnL%'], color='pink', label='Losing Trades [%]', alpha=1)

    # Adding labels and title
    plt.xlabel('Time')
    plt.ylabel('Trade Wins/Losses ($ and %)')
    plt.title('Sample of 100 Trade Wins and Losses Over Time')
    plt.legend()

    # Display the plot
    plt.show()

# Usage
trades_df = extract_trades('test6turtle', 'EndDate')


# trades_df = remove_naive(trades_df)


get_trade_stats(trades_df)
# plot_wins_and_losses(trades_df)


# Find the index of the minimum and maximum values
min_exit_price_idx = trades_df['ExitPrice'].idxmin()
min_enter_price_idx = trades_df['EnterPrice'].idxmin()
min_pnl_percent_idx = trades_df['PnL%'].idxmin()
max_pnl_percent_idx = trades_df['PnL%'].idxmax()

# Print the minimum values and their corresponding indices
print(f"Minimum Exit Price: {trades_df['ExitPrice'].min()}, Index: {min_exit_price_idx}")
print(f"Minimum Enter Price: {trades_df['EnterPrice'].min()}, Index: {min_enter_price_idx}")
print(f"Minimum PnL%: {trades_df['PnL%'].min()}, Index: {min_pnl_percent_idx}")

# Print the maximum PnL% and its corresponding index
print(f"Maximum PnL%: {trades_df['PnL%'].max()}, Index: {max_pnl_percent_idx}")
