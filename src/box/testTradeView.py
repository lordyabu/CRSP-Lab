import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from src.config import OHLC_DATA_DIR
from matplotlib.patches import Rectangle

# Load data
path = os.path.join(OHLC_DATA_DIR, 'GOOG.csv')
data = pd.read_csv(path)
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
data.set_index('date', inplace=True)

# Darvas Box Parameters
boxp = 5  # Box length


# Calculate the Darvas Box
def calculate_darvas_box(data, boxp):
    data['TopBox'] = 0.0
    data['BottomBox'] = 0.0

    for i in range(boxp, len(data)):
        highest_high = data['High'].iloc[i-boxp:i].max()
        if data['High'].iloc[i] > highest_high:
            new_high = data['High'].iloc[i]
            lowest_low = data['Low'].iloc[i-boxp:i].min()

            # Updating the Top and Bottom Box values
            data['TopBox'].iloc[i] = new_high
            data['BottomBox'].iloc[i] = lowest_low

    return data

def plot_slice_with_connected_highs_lows(start_date, end_date, boxp):
    sliced_data = data.loc[start_date:end_date]
    sliced_data = calculate_darvas_box(sliced_data, boxp)

    plt.figure(figsize=(12, 6))
    plt.plot(sliced_data.index, sliced_data['High'], label='High')
    plt.plot(sliced_data.index, sliced_data['Low'], label='Low')
    plt.plot(sliced_data.index, sliced_data['Close'], label='Close', color='black', linewidth=1)

    # Connect highs and lows of Darvas Boxes
    plt.plot(sliced_data.index, sliced_data['TopBox'], label='Top Box', color='green', linewidth=2)
    plt.plot(sliced_data.index, sliced_data['BottomBox'], label='Bottom Box', color='red', linewidth=2)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))  # Adjust interval as needed
    plt.gcf().autofmt_xdate()  # Rotate date labels
    plt.legend()
    plt.title('Darvas Boxes (Connected Highs and Lows)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
    plt.show()

# Example usage
plot_slice_with_connected_highs_lows('2020-01-01', '2020-03-05', boxp)
