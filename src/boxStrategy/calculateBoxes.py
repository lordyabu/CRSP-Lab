# This class is designed for calculating and visualizing Darvas Boxes, a popular technique in stock trading based on price movements.


import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from src.config import BOX_DATA_DIR, OHLC_DATA_DIR
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades


class DarvasBoxCalculator:
    def __init__(self, data_directory, name='Default'):
        """
        Initializes the DarvasBoxCalculator instance.

        Args:
            data_directory (str): The directory where stock data files are stored.
            name (str): Optional; The name of the DarvasBoxCalculator instance. Defaults to 'Default'.
        """
        self.data_directory = data_directory
        self.name = name

        self.save_dir = BOX_DATA_DIR

    def __str__(self):
        return self.name

    def calculate_darvas_boxes(self, data):
        """
        Calculates Darvas Boxes for a given DataFrame.

        Args:
            data (pd.DataFrame): DataFrame containing stock data with 'High', 'Low', and 'Close' columns.

        Returns:
            pd.DataFrame: The DataFrame with added 'Box_Top' and 'Box_Bottom' columns indicating the Darvas Boxes.
        """
        # Initialize columns for the Darvas boxes
        data['Box_Top'] = None
        data['Box_Bottom'] = None
        data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
        data.set_index('date', inplace=True)
        yearly_high = data['High'].rolling(window='365D').max()

        i = 0
        while i < len(data):
            if data['High'].iloc[i] == yearly_high.iloc[i]:
                box_top_day = i
                box_top = data['High'].iloc[i]

                # Find the box top within the next 4 days
                for j in range(i + 1, min(i + 4, len(data))):
                    if data['High'].iloc[j] > box_top:
                        box_top = None
                        break
                    box_top_day = j

                if box_top is not None:
                    box_bottom_day = box_top_day
                    box_bottom = data['Low'].iloc[box_top_day]

                    # Find the box bottom within the next 4 days
                    for j in range(box_top_day, min(box_top_day + 4, len(data))):
                        if data['Low'].iloc[j] < box_bottom:
                            box_bottom = data['Low'].iloc[j]
                            box_bottom_day = j

                    # Mark the rows for this box until the close price breaks out of the box
                    for k in range(box_bottom_day, len(data)):
                        if data['Close'].iloc[k] > box_top or data['Close'].iloc[k] < box_bottom:
                            break
                        data.at[data.index[k], 'Box_Top'] = box_top
                        data.at[data.index[k], 'Box_Bottom'] = box_bottom
                        box_bottom_day = k

                    i = box_bottom_day
                    if i + 1 == len(data):
                        i += 1
                else:
                    i += 1
            else:
                i += 1

        return data

    def plot_slice(self, df, start_date, end_date):
        """
        Plots a section of the DataFrame with Darvas Boxes.

        Args:
            df (pd.DataFrame): DataFrame containing Darvas Boxes.
            start_date (str): The start date for the plot.
            end_date (str): The end date for the plot.
        """
        # Slicing the DataFrame to the specified date range
        sliced_data = df.loc[start_date:end_date]
        plt.figure(figsize=(12, 6))
        plt.plot(sliced_data.index, sliced_data['High'], label='High')
        plt.plot(sliced_data.index, sliced_data['Low'], label='Low')
        plt.plot(sliced_data.index, sliced_data['Close'], label='Close', linestyle='--')

        # Group by Box_Top and Box_Bottom to find continuous periods
        grouped = sliced_data.groupby(['Box_Top', 'Box_Bottom'])
        for (box_top, box_bottom), group in grouped:
            if pd.notna(box_top) and pd.notna(box_bottom):
                start = group.index[0]
                end = group.index[-1]
                plt.hlines(box_top, xmin=start, xmax=end, colors='g',
                           label='Box Top' if start == sliced_data.index[0] else "")
                plt.hlines(box_bottom, xmin=start, xmax=end, colors='r',
                           label='Box Bottom' if start == sliced_data.index[0] else "")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.title(f'Darvas Boxes from {start_date} to {end_date}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid()
        plt.show()

    def plot_slice_stock_old(self, stock_name, start_date, end_date):
        """
        An older version of the plotting method for a specific stock and date range.

        Args:
            stock_name (str): The name of the stock.
            start_date (str): The start date for the plot.
            end_date (str): The end date for the plot.
        """
        data_dir = os.path.join(self.save_dir, f"{stock_name}.csv")
        df = pd.read_csv(data_dir)
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df.set_index('date', inplace=True)

        # Slicing the DataFrame to the specified date range
        sliced_data = df.loc[start_date:end_date]
        plt.figure(figsize=(12, 6))
        plt.plot(sliced_data.index, sliced_data['High'], label='High')
        plt.plot(sliced_data.index, sliced_data['Low'], label='Low')
        plt.plot(sliced_data.index, sliced_data['Close'], label='Close', linestyle='--')

        # Group by Box_Top and Box_Bottom to find continuous periods
        grouped = sliced_data.groupby(['Box_Top', 'Box_Bottom'])
        for (box_top, box_bottom), group in grouped:
            if pd.notna(box_top) and pd.notna(box_bottom):
                start = group.index[0]
                end = group.index[-1]
                plt.hlines(box_top, xmin=start, xmax=end, colors='g',
                           label='Box Top' if start == sliced_data.index[0] else "")
                plt.hlines(box_bottom, xmin=start, xmax=end, colors='r',
                           label='Box Bottom' if start == sliced_data.index[0] else "")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.title(f'{stock_name} Darvas Boxes from {start_date} to {end_date}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid()
        plt.show()

    def plot_slice_stock(self, stock_name, start_date, end_date):
        """
        Updated version of the plotting method, including trade data.

        Args:
            stock_name (str): The name of the stock.
            start_date (str): The start date for the plot.
            end_date (str): The end date for the plot.
        """
        data_dir = os.path.join(self.save_dir, f"{stock_name}.csv")
        df = pd.read_csv(data_dir)
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df.set_index('date', inplace=True)

        # Slicing the DataFrame to the specified date range
        sliced_data = df.loc[start_date:end_date]

        # Plotting stock price data
        plt.figure(figsize=(12, 6))
        plt.plot(sliced_data.index, sliced_data['High'], label='High')
        plt.plot(sliced_data.index, sliced_data['Low'], label='Low')
        plt.plot(sliced_data.index, sliced_data['Close'], label='Close', linestyle='--')

        # Group by Box_Top and Box_Bottom to find continuous periods
        grouped = sliced_data.groupby(['Box_Top', 'Box_Bottom'])
        for (box_top, box_bottom), group in grouped:
            if pd.notna(box_top) and pd.notna(box_bottom):
                start = group.index[0]
                end = group.index[-1]
                plt.hlines(box_top, xmin=start, xmax=end, colors='g',
                           label='Box Top' if start == sliced_data.index[0] else "")
                plt.hlines(box_bottom, xmin=start, xmax=end, colors='r',
                           label='Box Bottom' if start == sliced_data.index[0] else "")

        # Extracting trade data
        trades_df = extract_trades(strategy='box_naive', sort_by='EndDate', stock_name=stock_name)

        # Converting trade dates to datetime for filtering
        trades_df['StartDate'] = pd.to_datetime(trades_df['StartDate'], format='%Y%m%d')
        trades_df['EndDate'] = pd.to_datetime(trades_df['EndDate'], format='%Y%m%d')

        # Filtering trades to the specified date range
        filtered_trades_df = trades_df[(trades_df['StartDate'] >= start_date) & (trades_df['EndDate'] <= end_date)]

        # Separating entry and exit points
        entry_points = filtered_trades_df[filtered_trades_df['TradeType'] == 'long'][['StartDate', 'EnterPrice']]
        exit_points = filtered_trades_df[filtered_trades_df['TradeType'] == 'long'][['EndDate', 'ExitPrice']]

        # Plotting trade entry and exit points
        plt.scatter(entry_points['StartDate'], entry_points['EnterPrice'], color='lime', label='Entry Points',
                    marker='o', s=100)
        plt.scatter(exit_points['EndDate'], exit_points['ExitPrice'], color='fuchsia', label='Exit Points', marker='o',
                    s=100)

        # Formatting and showing the plot
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.title(f'{stock_name} Darvas Boxes with Trades from {start_date} to {end_date}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid()
        plt.show()

    def calculate_individual_stock_boxes(self, stock_name):
        """
        Calculates Darvas Boxes for an individual stock and saves the result.

        Args:
            stock_name (str): The name of the stock file to process.
        """
        file_path = os.path.join(self.data_directory, f"{stock_name}")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            dates = df['date'].values
            df = self.calculate_darvas_boxes(df)

            df.insert(0, 'date', dates)

            save_path = os.path.join(self.save_dir, f"{stock_name}")
            df.to_csv(save_path, index=False)

            print(f"{stock_name} is done")
        else:
            print(f"The file for {stock_name} does not exist in the directory.")

    def calculate_all_stock_boxes(self):
        """
        Calculates Darvas Boxes for all stock files in the specified directory using multithreading.

        """
        filenames = [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]
        num_workers = 8
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(tqdm(executor.map(self.calculate_individual_stock_boxes, filenames), total=len(filenames)))

calculator = DarvasBoxCalculator(data_directory=OHLC_DATA_DIR)

# calculator.calculate_individual_stock_boxes('AAPL.csv')

# calculator.calculate_all_stock_boxes()

calculator.plot_slice_stock('AAPL', '2014-01-01', '2015-12-31')
