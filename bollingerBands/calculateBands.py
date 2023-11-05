import numpy as np
import pandas as pd
import os
import math
from matplotlib import pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config import DATA_DIR

class BollingerBands:
    def __init__(self, data_directory, Bperiods=19, name='Default'):
        self.data_directory = data_directory
        self.Bperiods = Bperiods

        self.name = name

        self.save_dir = os.path.join(DATA_DIR, 'bollingerData')


    def __str__(self):
        return self.name

    def calculate_bollinger_bands(self, df):
        array_close = np.array(df['Close'])
        array_Middleband = [None] * self.Bperiods
        stndrd_deviation = [None] * self.Bperiods
        upper_band = [None] * self.Bperiods
        lower_band = [None] * self.Bperiods
        upper_band_3sd = [None] * self.Bperiods  # 3 standard deviations upper band
        lower_band_3sd = [None] * self.Bperiods  # 3 standard deviations lower band

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
            upper_band_3sd.append(middleband_value + (2.96 * stdev))  # 3 standard deviations upper band
            lower_band_3sd.append(middleband_value - (2.96 * stdev))  # 3 standard deviations lower band

            y += 1

        return upper_band, lower_band, upper_band_3sd, lower_band_3sd, array_Middleband

    @staticmethod
    def plot_bollinger_bands(df, upper_band, lower_band, upper_band_3sd, lower_band_3sd, middle_band):
        start_index = 3000
        end_index = 3300

        # Slice the relevant portion of the DataFrame
        df_sliced = df[start_index:end_index].reset_index(drop=True)

        print(df_sliced.iloc[0]['Day'], df_sliced.iloc[-1]['Day'])

        plt.figure(figsize=(12, 6))
        plt.plot(df_sliced['Close'], color='blue', label='Close')
        plt.plot(upper_band[start_index:end_index], color='red', label='Upper Band (2 SD)')
        plt.plot(lower_band[start_index:end_index], color='green', label='Lower Band (2 SD)')
        plt.plot(upper_band_3sd[start_index:end_index], color='purple', linestyle='dashed', label='Upper Band (3 SD)')
        plt.plot(lower_band_3sd[start_index:end_index], color='brown', linestyle='dashed', label='Lower Band (3 SD)')
        plt.plot(middle_band[start_index:end_index], color='orange', label='Middle Band')

        plt.ylabel('Bollinger Bands')
        plt.xlabel(df_sliced.iloc[0]['Day'] + "---" +  df_sliced.iloc[-1]['Day'])
        plt.legend()
        plt.tight_layout()
        plt.show()


    def calculate_individual_bands(self, stock_name):
        file_path = os.path.join(self.data_directory, f"{stock_name}")

        # print(file_path)

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            upper_band, lower_band, upper_band_3sd, lower_band_3sd, middle_band = self.calculate_bollinger_bands(df)
            # BollingerBands.plot_bollinger_bands(df, upper_band, lower_band, upper_band_3sd, lower_band_3sd, middle_band)

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

            # print(f"Bollinger Bands calculated, plotted, and saved for {stock_name}.")
        else:
            print(f"The file for {stock_name} does not exist in the directory.")



    def calculate_all_bands(self):
        filenames = [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]
        num_workers = 8

        # print(filenames)

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(tqdm(executor.map(self.calculate_individual_bands, filenames), total=len(filenames)))




# Usage:
# directory = os.path.join(DATA_DIR, 'dataDailyTwoCol')
# bollinger = BollingerBands(data_directory=directory)
# bollinger.calculate_individual_bands('AAPL')
# bollinger.calculate_all_bands()
