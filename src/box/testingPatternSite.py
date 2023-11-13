import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from src.config import OHLC_DATA_DIR
# Assuming 'data' is a DataFrame with columns 'High', 'Low', and 'Close'
# Replace this with the actual loading of your data
path = os.path.join(OHLC_DATA_DIR, 'GOOG.csv')
data = pd.read_csv(path)  # Replace with your data file
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
data.set_index('date', inplace=True)


# Function to find Darvas boxes
def find_darvas_boxes(data):
    boxes = []
    yearly_high = data['High'].rolling(window='365D').max()

    i = 0
    while i < len(data):
        # Step 1: Find a new yearly high
        if data['High'].iloc[i] == yearly_high.iloc[i]:
            box_top_day = i
            box_top = data['High'].iloc[i]

            # Step 2: Find the box top (highest high of the next 3 days)
            for j in range(i + 1, min(i + 4, len(data))):
                if data['High'].iloc[j] > box_top:
                    box_top = None
                    break
                box_top_day = j

            if box_top is not None:
                # Step 3: Find the box bottom (lowest low of the next 3 days)
                box_bottom_day = box_top_day
                box_bottom = data['Low'].iloc[box_top_day]

                for j in range(box_top_day, min(box_top_day + 4, len(data))):
                    if data['Low'].iloc[j] < box_bottom:
                        box_bottom = data['Low'].iloc[j]
                        box_bottom_day = j

                boxes.append((box_top_day, box_top, box_bottom_day, box_bottom))
                i = box_bottom_day  # Continue from the bottom day
            else:
                i += 1  # Continue searching for a new high
        else:
            i += 1
    return boxes


# Function to plot a specific slice
def plot_slice(start_date, end_date):
    sliced_data = data.loc[start_date:end_date]
    darvas_boxes = find_darvas_boxes(sliced_data)

    plt.figure(figsize=(12, 6))
    plt.plot(sliced_data.index, sliced_data['High'], label='High')
    plt.plot(sliced_data.index, sliced_data['Low'], label='Low')

    for box in darvas_boxes:
        box_top_day, box_top, box_bottom_day, box_bottom = box
        plt.hlines(box_top, xmin=sliced_data.index[box_top_day], xmax=sliced_data.index[box_bottom_day], colors='g', label='Box Top' if box == darvas_boxes[0] else "")
        plt.hlines(box_bottom, xmin=sliced_data.index[box_top_day], xmax=sliced_data.index[box_bottom_day], colors='r', label='Box Bottom' if box == darvas_boxes[0] else "")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))  # Adjust interval as needed
    plt.gcf().autofmt_xdate()  # Rotate date labels
    plt.legend()
    plt.title('Darvas Boxes in Slice')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
    plt.show()

# Example usage
plot_slice('2010-01-01', '2010-12-31')  # Adjust these dates for your desired slice