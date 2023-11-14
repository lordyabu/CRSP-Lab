# This script includes the 'graph_window_turtle' function, which provides a visualization tool for analyzing Turtle trading strategy
# applied to a specific stock over a selected time period. The function plots key elements of the strategy, including Rolling Maxes/Mins and
# trade entry and exit points, on a stock's price chart.

import matplotlib.pyplot as plt
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
import pandas as pd
import matplotlib.patches as mpatches

def graph_window_turtle(start_date, end_date, stock_name, strategy):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Load the Turtles  data
    df_turt = pd.read_csv(r'C:\Users\theal\Documents\CrspData\turtleData\{}.csv'.format(stock_name))

    # Convert 'date' to datetime and filter based on the window
    df_turt['date'] = pd.to_datetime(df_turt['date'], format='%Y%m%d')
    df_turt = df_turt[(df_turt['date'] >= start_date) & (df_turt['date'] <= end_date)]

    # Extract trades
    trades = extract_trades(strategy=f'{strategy}', stock_name=f'{stock_name}')

    # Filter trades based on the window
    trades = trades[(trades['StartDate'] >= start_date) & (trades['EndDate'] <= end_date)]

    # Plot Turtle specific data
    plt.figure(figsize=(12, 6))
    plt.plot(df_turt['date'], df_turt['Close'], color='blue', label='Close')
    plt.plot(df_turt['date'], df_turt['Rolling_Max_20'], color='#404040', label='Rolling Max 20')  # Dark gray
    plt.plot(df_turt['date'], df_turt['Rolling_Min_20'], color='#808080', label='Rolling Min 20')  # Medium gray
    plt.plot(df_turt['date'], df_turt['Rolling_Min_10'], color='#A0A0A0', linestyle='dashed',
             label='Rolling Min 10')  # Lighter gray
    plt.plot(df_turt['date'], df_turt['Rolling_Max_10'], color='#C0C0C0', linestyle='dashed',
             label='Rolling Max 10')  # Even lighter gray


    # Plot trades
    for _, trade in trades.iterrows():
        enter_date = trade['StartDate']
        exit_date = trade['EndDate']
        trade_type = trade['TradeType']
        pnl = trade['PnL%']  # Get the PnL value

        enter_price = df_turt.loc[df_turt['date'] == enter_date, 'Close'].values[0]
        exit_price = df_turt.loc[df_turt['date'] == exit_date, 'Close'].values[0]

        # Enter Long
        if trade_type == 'long':
            plt.scatter(enter_date, enter_price, color='green', zorder=5)
            plt.scatter(exit_date, exit_price, color='yellow', zorder=5)
        # Enter Short
        elif trade_type == 'short':
            plt.scatter(enter_date, enter_price, color='red', zorder=5)
            plt.scatter(exit_date, exit_price, color='orange', zorder=5)

        # Print trade information including PnL
        print(f"Trade Type: {trade_type}, Start Date: {enter_date}, End Date: {exit_date}, PnL%: {pnl}")

    # Create legend patches
    enter_long_patch = mpatches.Patch(color='green', label='Enter Long')
    exit_long_patch = mpatches.Patch(color='yellow', label='Exit Long')
    enter_short_patch = mpatches.Patch(color='red', label='Enter Short')
    exit_short_patch = mpatches.Patch(color='orange', label='Exit Short')

    # Get existing plot labels and handles
    handles, labels = plt.gca().get_legend_handles_labels()

    # Add custom patches
    handles.extend([enter_long_patch, exit_long_patch, enter_short_patch, exit_short_patch])

    # Create combined legend
    plt.legend(handles=handles, loc='upper left')

    plt.ylabel('Price Close')
    plt.xlabel('Date')
    plt.title(f'{stock_name} Turtle Trades')
    plt.tight_layout()
    plt.show()


