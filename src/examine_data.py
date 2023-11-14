# This script is designed to analyze and visualize trading strategies, focusing on 'bollinger_naive_dynamic_sl' and 'turtle_naive'.
# It utilizes various functions for extracting trades, plotting comprehensive analyses, and graphing specific trading windows.
# Key functionalities include extracting trade data, getting trade statistics, plotting wins and losses,
# and visualizing trade data for Bollinger Bands and Turtle trading strategies within specified time windows.

from src.tradeAnalysis.getGraphs import plot_everything
from src.tradeAnalysis.getStats import get_trade_stats, plot_wins_and_losses
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
from src.turtles.analysis.graphTurtleTrades import graph_window_turtle
from src.bollingerBands.analysis.graphBollingerTrades import graph_window_bollinger

import warnings
warnings.filterwarnings('ignore')

# Strategies: bollinger_naive_dynamic_sl, turtle_naive
trades_df = extract_trades(strategy='turtle_naive', sort_by='EndDate')
start_date = '2010-01-04'
end_date = '2020-12-31'

# Analysis and Visualization Section
# -----------------------------------

# Plot various graphs for the trading strategy
# Uncomment the line below to execute
# plot_everything(trades_df, start_date, end_date)

# Get and print trade statistics
# Uncomment the line below to execute
get_trade_stats(trades_df, start_date, end_date)

# Plot wins and losses
# Uncomment the line below to execute
# plot_wins_and_losses(trades_df, start_date, end_date)

# Bollinger Bands Analysis
# ------------------------

start_date_window_boll = '2010-10-11'
end_date_window_boll = '2011-12-31'
# Visualize Bollinger Bands trades for a specific window
# Uncomment the line below to execute
# graph_window_bollinger(start_date_window_boll, end_date_window_boll, 'AAPL', 'bollinger_naive_dynamic_sl')

# Turtle Trading Strategy Analysis
# ---------------------------------

start_date_window_turtle = '2018-10-11'
end_date_window_turtle = '2020-12-31'
# Visualize Turtle trades for a specific window
# Uncomment the line below to execute
# graph_window_turtle(start_date_window_turtle, end_date_window_turtle, 'AAPL', 'turtle_naive')
# ---------------------------------