import matplotlib.pyplot as plt
import pandas as pd
import ast
def plot_rolling_stats(df, start_index=0, end_index=None):
    # If end_index is not provided, use the last index of the DataFrame
    if end_index is None:
        end_index = len(df)

    df_subset = df.iloc[start_index:end_index]
    df_subset['date'] = pd.to_datetime(df_subset['date'], format='%Y%m%d')

    plt.figure(figsize=(14, 7))
    plt.plot(df_subset['date'], df_subset['Close'], label='Price', color='blue')

    if 'Rolling_Max_10' in df_subset.columns:
        plt.plot(df_subset['date'], df_subset['Rolling_Max_10'], label='Rolling Max 10', color='red', linestyle='--', alpha=.7)
    if 'Rolling_Min_10' in df_subset.columns:
        plt.plot(df_subset['date'], df_subset['Rolling_Min_10'], label='Rolling Min 10', color='green', linestyle='--', alpha=.7)
    if 'Rolling_Max_20' in df_subset.columns:
        plt.plot(df_subset['date'], df_subset['Rolling_Max_20'], label='Rolling Max 20', color='purple', linestyle='--', alpha=.7)
    if 'Rolling_Min_20' in df_subset.columns:
        plt.plot(df_subset['date'], df_subset['Rolling_Min_20'], label='Rolling Min 20', color='orange', linestyle='--', alpha=.7)

    plt.scatter([], [], color='green', marker='^', s=100, label='Enter Long')
    plt.scatter([], [], color='red', marker='v', s=100, label='Enter Short')
    plt.scatter([], [], color='lightgreen', marker='>', s=100, label='Exit Long')
    plt.scatter([], [], color='pink', marker='<', s=100, label='Exit Short')

    if 'Actions' in df_subset.columns:
        for idx, row in df_subset.iterrows():
            # Convert the string representation of the list to an actual list
            action_list = ast.literal_eval(row['Actions'])
            for action in action_list:
                if action == 'EnterLong':
                    plt.scatter(row['date'], row['Close'], color='green', marker='^', s=100)
                    print(f"{row['date']}: Enter Long at {row['Close']}, Rolling Max 20: {row['Rolling_Max_20']}")
                elif action == 'EnterShort':
                    plt.scatter(row['date'], row['Close'], color='red', marker='v', s=100)
                    print(f"{row['date']}: Enter Short at {row['Close']}, Rolling Min 20: {row['Rolling_Min_20']}")
                elif action == 'ExitLong':
                    plt.scatter(row['date'], row['Close'], color='lightgreen', marker='>', s=100)
                    print(f"{row['date']}: Exit Long at {row['Close']}, Rolling Min 10: {row['Rolling_Min_10']}")
                elif action == 'ExitShort':
                    plt.scatter(row['date'], row['Close'], color='pink', marker='<', s=100)
                    print(f"{row['date']}: Exit Short at {row['Close']}, Rolling Max 10: {row['Rolling_Max_10']}")

    plt.title('Rolling Min/Max and Price with Action Points')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


df = pd.read_csv('AAPLTurtleTrades.csv')


plot_rolling_stats(df, 2000,2400)
