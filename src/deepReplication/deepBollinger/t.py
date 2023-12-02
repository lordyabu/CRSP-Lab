import numpy as np

# Create a simple time series as a NumPy array
time_series = np.arange(1, 21)  # 1 to 20

# Define the number of splits you want (e.g., 3)
num_splits = 3

# Calculate the size of each split
split_size = len(time_series) // num_splits

# Initialize lists to store the split data
train_splits, test_splits = [], []

# Create the splits
for i in range(num_splits):
    start = i * split_size
    end = (i + 1) * split_size
    test_split = time_series[start:end]
    train_split = np.concatenate((time_series[:start], time_series[end:]), axis=None)
    train_splits.append(train_split)
    test_splits.append(test_split)

# Visualize the splits
for i, (train, test) in enumerate(zip(train_splits, test_splits)):
    print(f"Split {i + 1}:")
    print(f"Train Set: {train}")
    print(f"Test Set: {test}")
    print("=" * 20)
