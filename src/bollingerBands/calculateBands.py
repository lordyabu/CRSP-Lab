# This script introduces the BollingerBands class, designed to calculate and plot Bollinger Bands for stock trading data.
# It includes methods for calculating Bollinger Bands for a single stock, plotting these bands, and a concurrent processing
# feature to handle multiple stocks. The class can be used to analyze stock volatility and price trends,
# which are essential in identifying potential trading opportunities.


import numpy as np
import pandas as pd
import os
import math
from matplotlib import pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from src.config import DATA_DIR, BOLLINGER_DATA_DIR


class BollingerBands:
    def __init__(self, data_directory, Bperiods=19, name='Default'):
        """
        Initializes the BollingerBands instance.

        Args:
            data_directory (str): The directory where stock data is stored.
            Bperiods (int): The number of periods to use for calculating Bollinger Bands. Defaults to 19.
            name (str): The name of the Bollinger Bands instance. Defaults to 'Default'.
        """

        self.data_directory = data_directory
        self.Bperiods = Bperiods
        self.name = name
        self.save_dir = BOLLINGER_DATA_DIR

    def __str__(self):
        return self.name

    def calculate_bollinger_bands(self, df):
        """
        Calculates Bollinger Bands for a given DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing stock data with a 'Close' column.

        Returns:
            tuple: A tuple containing arrays for upper band, lower band, 3 standard deviation upper band,
                   3 standard deviation lower band, and middle band.
        """
        array_close = np.array(df['Close'])
        array_Middleband = [None] * self.Bperiods
        stndrd_deviation = [None] * self.Bperiods
        upper_band = [None] * self.Bperiods
        lower_band = [None] * self.Bperiods
        upper_band_3sd = [None] * self.Bperiods
        lower_band_3sd = [None] * self.Bperiods

        y = 0
        for x in range(array_close.size - self.Bperiods):
            sum_close = sum(array_close[y:y + self.Bperiods + 1])
            middleband_value = sum_close / (self.Bperiods + 1)
            array_Middleband.append(middleband_value)

            sum_squared_diff = sum([(middleband_value - array_close[i]) ** 2 for i in range(y, y + self.Bperiods + 1)])
            stdev = math.sqrt(sum_squared_diff / self.Bperiods)
            stndrd_deviation.append(stdev)

            upper_band.append(middleband_value + (1.96 * stdev))
            lower_band.append(middleband_value - (1.96 * stdev))
            upper_band_3sd.append(middleband_value + (2.96 * stdev))
            lower_band_3sd.append(middleband_value - (2.96 * stdev))

            y += 1

        return upper_band, lower_band, upper_band_3sd, lower_band_3sd, array_Middleband

    @staticmethod
    def plot_bollinger_bands(df, upper_band, lower_band, upper_band_3sd, lower_band_3sd, middle_band):
        """
        Plots Bollinger Bands for a given DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing stock data.
            upper_band (list): The calculated upper Bollinger Band.
            lower_band (list): The calculated lower Bollinger Band.
            upper_band_3sd (list): The calculated upper Bollinger Band with 3 standard deviations.
            lower_band_3sd (list): The calculated lower Bollinger Band with 3 standard deviations.
            middle_band (list): The calculated middle Bollinger Band.
        """
        start_index = 3000
        end_index = 3300

        df_sliced = df[start_index:end_index].reset_index(drop=True)

        plt.figure(figsize=(12, 6))
        plt.plot(df_sliced['Close'], color='blue', label='Close')
        plt.plot(upper_band[start_index:end_index], color='red', label='Upper Band (2 SD)')
        plt.plot(lower_band[start_index:end_index], color='green', label='Lower Band (2 SD)')
        plt.plot(upper_band_3sd[start_index:end_index], color='purple', linestyle='dashed', label='Upper Band (3 SD)')
        plt.plot(lower_band_3sd[start_index:end_index], color='brown', linestyle='dashed', label='Lower Band (3 SD)')
        plt.plot(middle_band[start_index:end_index], color='orange', label='Middle Band')

        plt.ylabel('Bollinger Bands')
        plt.xlabel(str(df_sliced.iloc[0]['date']) + "---" + str(df_sliced.iloc[-1]['date']))
        plt.legend()
        plt.tight_layout()
        plt.show()

    def calculate_individual_bands(self, stock_name, plot_band=False):
        """
        Calculates and optionally plots Bollinger Bands for an individual stock.

        Args:
            stock_name (str): The name of the stock file to process.
            plot_band (bool): If True, plots the Bollinger Bands. Defaults to False.
        """
        file_path = os.path.join(self.data_directory, f"{stock_name}")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            upper_band, lower_band, upper_band_3sd, lower_band_3sd, middle_band = self.calculate_bollinger_bands(df)
            if plot_band:
                BollingerBands.plot_bollinger_bands(df, upper_band, lower_band, upper_band_3sd, lower_band_3sd,
                                                    middle_band)

            # Add the bands to the DataFrame
            try:
                df[f'Lower_Band_{self.name}'] = lower_band
                df[f'Upper_Band_{self.name}'] = upper_band
                df[f'Lower_Band_3SD_{self.name}'] = lower_band_3sd
                df[f'Upper_Band_3SD_{self.name}'] = upper_band_3sd
                df[f'Middle_Band_{self.name}'] = middle_band
            except:
                return

            # Save the DataFrame back to CSV
            save_path = os.path.join(self.save_dir, f"{stock_name}")
            df.to_csv(save_path, index=False)
        else:
            print(f"The file for {stock_name} does not exist in the directory.")

    def calculate_all_bands(self):
        """
        Calculates Bollinger Bands for all stock files in the specified directory.
        Utilizes multithreading for concurrent processing.
        """
        filenames = [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]
        num_workers = 8
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(tqdm(executor.map(self.calculate_individual_bands, filenames), total=len(filenames)))
