from tqdm import tqdm
import os
from src.config import DATA_DIR
# 0. Decide what operations to run. If this is fresh run, I suggest having all set to True
do_major_ops = False
select_date_range = False
do_ohlc_calculations = True
do_band_calculation = False
run_bollinger_trades = False
# 1. Assuming you have ran the provided MatLab scripts, Have data directory in your Documents Folder Structured like this.
# Only dataDailyTwoCol and dataFiveMin need to have data in currently.

"""
CrspData
│
├── bollingerData       - Description of 'bollingerData' contents
├── dataDailyTwoCol     - Description of 'dataDailyTwoCol' contents
├── dataFiveMin         - Description of 'dataFiveMin' contents
├── helperData          - Contains helper files and data
├── priceData           - Raw price data
├── priceDataOHLC       - Price data with Open-High-Low-Close (OHLC)
├── priceDataTest       - Test data for price information
├── testData            - General test data used across the project
└── tradeData           - Trade-related data

Note: Replace the descriptions with more specific information about what each directory contains.
"""

# 1. Apply your major operations to the dataset. For more what details on what a major op is go to ./notes/DataPreprocessing.txt.txt
if do_major_ops:
    from src.tests.test_price_calculations import TestMajorOp
    from src.helperFunctions.dataProcessing.majorOperations import major_operations

    positive_major_op = False
    NaNs_major_op = True
    save_to_major_op_log = True

    # Major Operations with Progress Bar
    print("Performing major operations...")
    with tqdm(total=2, desc="Major Operations") as pbar:
        major_operations(positive=positive_major_op, NaNs=NaNs_major_op, save_to_log=save_to_major_op_log)
        pbar.update(1)

        test_major_op = TestMajorOp()
        test_major_op.set_test_flags(NaNs_major_op, positive_major_op)

        test_major_op.test_NaNs_major_op()
        pbar.update(1)
        test_major_op.test_positive_major_op()


if select_date_range:
    from src.tests.test_price_calculations import TestMajorOp
    from helperFunctions.findTimespanStocks import save_stock_filenames_in_timespan_daily

    start = '20100104'
    end = '20201231'
    exclude_nan = True
    exclude_positive = True
    print("Performing timespan operations...")
    save_stock_filenames_in_timespan_daily(start=start, end=end, exclude_nan=exclude_nan, exclude_positive=exclude_positive)

    test_major_op = TestMajorOp()
    test_major_op.set_test_flags(True, True)

    test_major_op.test_NaNs_major_op()
    test_major_op.test_positive_major_op()


if do_ohlc_calculations:
    from src.helperFunctions.dataProcessing.getOHLCfrom5MinRet import get_ohlc
    print("Performing OHLC operations...")
    get_ohlc()


if do_band_calculation:
    from src.bollingerBands.calculateBands import BollingerBands

    directory = os.path.join(DATA_DIR, 'priceDataOHLCSplitTest')
    bollinger = BollingerBands(data_directory=directory)
    bollinger.calculate_all_bands()


if run_bollinger_trades:
    pass

print("All operations completed.")