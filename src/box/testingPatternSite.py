import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from src.config import OHLC_DATA_DIR
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from IPython.display import display, HTML
import json
import plotly
from IPython.display import display, Javascript


# Assuming 'data' is a DataFrame with columns 'High', 'Low', and 'Close'
# Replace this with the actual loading of your data
path = os.path.join(OHLC_DATA_DIR, 'TSLA.csv')
data = pd.read_csv(path)  # Replace with your data file
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
data.set_index('date', inplace=True)


# Function to find Darvas boxes
def find_darvas_boxes(data):
    boxes = []
    yearly_high = data['High'].rolling(window='365D').max()

    i = 0
    while i < len(data):
        if data['High'].iloc[i] == yearly_high.iloc[i]:
            box_top_day = i
            box_top = data['High'].iloc[i]

            for j in range(i + 1, min(i + 4, len(data))):
                if data['High'].iloc[j] > box_top:
                    box_top = None
                    break
                box_top_day = j

            if box_top is not None:
                box_bottom_day = box_top_day
                box_bottom = data['Low'].iloc[box_top_day]

                for j in range(box_top_day, min(box_top_day + 4, len(data))):
                    if data['Low'].iloc[j] < box_bottom:
                        box_bottom = data['Low'].iloc[j]
                        box_bottom_day = j

                # Extend the box until the Close price breaks out
                for k in range(box_bottom_day + 1, len(data)):
                    if data['Close'].iloc[k] > box_top or data['Close'].iloc[k] < box_bottom:
                        break
                    box_bottom_day = k

                boxes.append((box_top_day, box_top, box_bottom_day, box_bottom))
                i = box_bottom_day
            else:
                i += 1
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
    plt.plot(sliced_data.index, sliced_data['Close'], label='Close', linestyle='--')  # Added line for Close price

    for box in darvas_boxes:
        box_top_day, box_top, box_bottom_day, box_bottom = box
        plt.hlines(box_top, xmin=sliced_data.index[box_top_day], xmax=sliced_data.index[box_bottom_day], colors='g', label='Box Top' if box == darvas_boxes[0] else "")
        plt.hlines(box_bottom, xmin=sliced_data.index[box_top_day], xmax=sliced_data.index[box_bottom_day], colors='r', label='Box Bottom' if box == darvas_boxes[0] else "")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))  # Adjust interval as needed
    plt.gcf().autofmt_xdate()  # Rotate date labels
    plt.legend()
    plt.title('Darvas Boxes in Slice with Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
    plt.show()


def plot_slice_plotly(start_date, end_date):
    sliced_data = data.loc[start_date:end_date]
    darvas_boxes = find_darvas_boxes(sliced_data)

    # Calculate y-axis limits based on the selected slice
    y_max = max(sliced_data['High'].max(), sliced_data['Close'].max())
    y_min = min(sliced_data['Low'].min(), sliced_data['Close'].min())

    # Creating figure with dynamic y-axis
    fig = go.Figure()

    # Add High, Low, and Close prices
    fig.add_trace(go.Scatter(x=sliced_data.index, y=sliced_data['High'], mode='lines', name='High'))
    fig.add_trace(go.Scatter(x=sliced_data.index, y=sliced_data['Low'], mode='lines', name='Low'))
    fig.add_trace(go.Scatter(x=sliced_data.index, y=sliced_data['Close'], mode='lines', name='Close'))

    # Add Darvas boxes
    for box in darvas_boxes:
        box_top_day, box_top, box_bottom_day, box_bottom = box
        fig.add_trace(go.Scatter(x=[sliced_data.index[box_top_day], sliced_data.index[box_bottom_day]],
                                 y=[box_top, box_top], mode='lines', line=dict(color='green', dash='dot'), name='Box Top'))
        fig.add_trace(go.Scatter(x=[sliced_data.index[box_top_day], sliced_data.index[box_bottom_day]],
                                 y=[box_bottom, box_bottom], mode='lines', line=dict(color='red', dash='dot'), name='Box Bottom'))

    # Update layout for a better view with dynamic y-axis
    fig.update_layout(title='Darvas Boxes with Interactive Plot',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      yaxis=dict(range=[y_min, y_max], autorange=False),
                      xaxis_rangeslider_visible=True)

    fig.show()





# Example usage
# plot_slice('2015-01-01', '2015-12-31')  # Adjust these dates for your desired slice
plot_slice_plotly('2010-01-01', '2020-12-31')