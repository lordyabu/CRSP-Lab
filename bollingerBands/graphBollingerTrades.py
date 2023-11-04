import matplotlib.pyplot as plt
from helperClasses.extractTrades import extract_trades
import pandas as pd
import matplotlib.patches as mpatches

def graph_window(start_day, end_day):
    # Load the Bollinger Bands data
    df_boll = pd.read_csv(r'C:\Users\theal\Documents\dataEnsembleLegends\bollingerData\AAPL.csv')

    # Convert 'Day' to datetime and filter based on the window
    df_boll['Day'] = pd.to_datetime(df_boll['Day'].str.replace('Day_', ''), format='%Y%m%d')
    df_boll = df_boll[(df_boll['Day'] >= start_day) & (df_boll['Day'] <= end_day)]

    # Extract trades
    trades = extract_trades('test1')
    trades['StartDate'] = pd.to_datetime(trades['StartDate'].str.replace('Day_', ''), format='%Y%m%d')
    trades['EndDate'] = pd.to_datetime(trades['EndDate'].str.replace('Day_', ''), format='%Y%m%d')

    # Filter trades based on the window
    trades = trades[(trades['StartDate'] >= start_day) & (trades['EndDate'] <= end_day)]

    # Plot Bollinger Bands
    plt.figure(figsize=(12, 6))
    plt.plot(df_boll['Day'], df_boll['Close'], color='blue', label='Close')
    plt.plot(df_boll['Day'], df_boll['Upper_Band_Default'], color='#404040', label='Upper Band (2 SD)')  # Dark gray
    plt.plot(df_boll['Day'], df_boll['Lower_Band_Default'], color='#808080', label='Lower Band (2 SD)')  # Medium gray
    plt.plot(df_boll['Day'], df_boll['Upper_Band_3SD_Default'], color='#A0A0A0', linestyle='dashed',
             label='Upper Band (3 SD)')  # Lighter gray
    plt.plot(df_boll['Day'], df_boll['Lower_Band_3SD_Default'], color='#C0C0C0', linestyle='dashed',
             label='Lower Band (3 SD)')  # Even lighter gray
    plt.plot(df_boll['Day'], df_boll['Middle_Band_Default'], color='#E0E0E0', label='Middle Band')  # Almost white

    # Plot trades
    for _, trade in trades.iterrows():
        enter_day = trade['StartDate']
        exit_day = trade['EndDate']
        trade_type = trade['TradeType']

        enter_price = df_boll.loc[df_boll['Day'] == enter_day, 'Close'].values[0]
        exit_price = df_boll.loc[df_boll['Day'] == exit_day, 'Close'].values[0]

        # Enter Long
        if trade_type == 'long':
            plt.scatter(enter_day, enter_price, color='green', zorder=5)
            plt.scatter(exit_day, exit_price, color='darkgreen', zorder=5)
        # Enter Short
        elif trade_type == 'short':
            plt.scatter(enter_day, enter_price, color='red', zorder=5)
            plt.scatter(exit_day, exit_price, color='darkred', zorder=5)

    # Create legend patches
    enter_long_patch = mpatches.Patch(color='green', label='Enter Long')
    exit_long_patch = mpatches.Patch(color='darkgreen', label='Exit Long')
    enter_short_patch = mpatches.Patch(color='red', label='Enter Short')
    exit_short_patch = mpatches.Patch(color='darkred', label='Exit Short')

    # Get existing plot labels and handles
    handles, labels = plt.gca().get_legend_handles_labels()

    # Add custom patches
    handles.extend([enter_long_patch, exit_long_patch, enter_short_patch, exit_short_patch])

    # Create combined legend
    plt.legend(handles=handles, loc='upper left')

    plt.ylabel('Return Close')
    plt.xlabel('Day')
    plt.title('AAPL Bollinger Bands and Trades')
    plt.tight_layout()
    plt.show()


# Usage example
start_day = pd.to_datetime('2011-05-11')
end_day = pd.to_datetime('2011-10-02')
graph_window(start_day, end_day)
