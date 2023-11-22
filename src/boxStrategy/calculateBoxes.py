import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from src.config import BOX_DATA_DIR, OHLC_DATA_DIR
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class DarvasBoxCalculator:
    def __init__(self, data_directory, name='Default'):
        self.data_directory = data_directory
        self.name = name

        self.save_dir = BOX_DATA_DIR

    def __str__(self):
        return self.name

    def calculate_darvas_boxes(self, data):
        # Initialize columns for the Darvas boxes
        data['Box_Top'] = None
        data['Box_Bottom'] = None
        yearly_high = data['High'].rolling(window='250D').max()

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
                    for k in range(box_bottom_day + 1, len(data)):
                        if data['Close'].iloc[k] > box_top or data['Close'].iloc[k] < box_bottom:
                            data.at[data.index[k], 'Box_Top'] = box_top
                            data.at[data.index[k], 'Box_Bottom'] = box_bottom
                            break
                        data.at[data.index[k], 'Box_Top'] = box_top
                        data.at[data.index[k], 'Box_Bottom'] = box_bottom

                    data.at[data.index[k], 'Box_Top'] = box_top
                    data.at[data.index[k], 'Box_Bottom'] = box_bottom
                    i = k + 1
                else:
                    i += 1
            else:
                i += 1

        return data

    def plot_slice(self, df, start_date, end_date):
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

    def calculate_individual_stock_boxes(self, stock_name):
        file_path = os.path.join(self.data_directory, f"{stock_name}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = self.calculate_darvas_boxes(df)

            save_path = os.path.join(self.data_directory, f"{stock_name}_darvas.csv")
            df.to_csv(save_path, index=False)
        else:
            print(f"The file for {stock_name} does not exist in the directory.")

    def calculate_all_stock_boxes(self):
        filenames = [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]
        num_workers = 8
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(tqdm(executor.map(self.calculate_individual_stock_boxes, filenames), total=len(filenames)))



calculator = DarvasBoxCalculator(data_directory=OHLC_DATA_DIR)
path = os.path.join(calculator.data_directory, 'TSLA.csv')
data = pd.read_csv(path)
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
data["Date"] = data['date']
data.set_index('date', inplace=True)

print(data)
data = data.loc['2015-01-01': '2015-12-31']

updated_data = calculator.calculate_darvas_boxes(data)

count = 0
for i, row in updated_data.iterrows():
    print(i, row['Box_Top'], count)
    count += 1

calculator.plot_slice(updated_data, '2015-01-01', '2015-12-31')