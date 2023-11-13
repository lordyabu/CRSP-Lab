import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from src.config import OHLC_DATA_DIR

# Function to create and plot the box within a specified range
def plot_box_slice(start_index, end_index):
    path = os.path.join(OHLC_DATA_DIR, 'GOOG.csv')
    goog = pd.read_csv(path)

    class box(object):
        high = []
        low = []
        date_high = []
        date_low = []

    box1 = box()
    idx = 0

    for i in range(1, len(goog)):
        if goog.High[i] <= goog.High[i - 1]:
            idx += 1
        else:
            idx = 0

        if idx == 3 and start_index <= i <= end_index:
            high_vals = goog.High[i - 3:i]
            low_vals = goog.Low[i - 3:i]
            box1.high.append(high_vals.max())
            box1.low.append(low_vals.min())
            box1.date_high.append(goog.index[i - 3])
            box1.date_low.append(goog.index[i - 3 + np.argmin(low_vals)])

    # Slicing the main data for plotting
    goog_sliced = goog.loc[start_index:end_index]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(goog_sliced.index, goog_sliced.High, label='GOOG High')
    plt.plot(goog_sliced.index, goog_sliced.Low, label='GOOG Low')

    # Drawing boxes
    for i in range(len(box1.high)):
        rect = Rectangle((box1.date_low[i], box1.low[i]), box1.date_high[i] - box1.date_low[i], box1.high[i] - box1.low[i],
                         fill=False, edgecolor='green', linewidth=2)
        plt.gca().add_patch(rect)

    plt.grid()
    plt.legend()
    plt.show()

# Example usage
plot_box_slice(start_index=100, end_index=200)
