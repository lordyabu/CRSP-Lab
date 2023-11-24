from src.config import OHLC_DATA_DIR

# Suppressing warnings for cleaner output // Pandas DF slicing
import warnings
warnings.filterwarnings('ignore')

# ==========================
# Configuration and Settings (Make sure to configure the operations you turn to True below)
# ==========================

# Deciding which operations to run (set to True to execute)
do_major_ops = False
do_ohlc_calculations = False
select_date_range = False
do_band_calculation = False
run_bollinger_trades = False
do_window_calculation = False
run_turtle_trades = False
do_box_calculations = False
run_box_trades =False
create_non_trades = False


# ======================================================
# Directory Structure (Ensure this matches your setup) - (If you want to change names go to config.py(don't change helperData or tradeData))
# ======================================================

"""
CrspData
│
├── bollingerData       - Contains data for Bollinger Bands analysis
├── turtleData          - Contains data for Turtle strategy analysis
├── dataFiveMin         - Contains 5-minute interval data
├── helperData          - Contains helper files and data (valid stock names)
├── priceDataRAW        - Raw price data
├── priceDataMO         - Price data POST major op
├── priceDataOHLC       - Price data with Open-High-Low-Close (OHLC)
└── tradeData           - Trade-related data
"""

# =======================================
# Major Operations and Data Preprocessing
# =======================================

if do_major_ops:
    from src.helperFunctions.dataPreprocessing.majorOperations import major_operations

    # Configuration for major operations
    positive_major_op = False
    NaNs_major_op = True
    save_to_major_op_log = True

    # Performing major operations with progress tracking
    print("Performing major operations...")
    major_operations(positive=positive_major_op, NaNs=NaNs_major_op, save_to_log=save_to_major_op_log)


# ====================================
# Open-High-Low-Close (OHLC) Calculations
# ====================================

if do_ohlc_calculations:
    from src.helperFunctions.dataPreprocessing.getOHLCfrom5MinRet import get_ohlc
    print("Performing OHLC operations...")
    get_ohlc()

# =============================
# Date Range Selection for Data
# =============================

if select_date_range:
    from src.tests.test_price_calculations import TestMajorOp
    from src.helperFunctions.dataPreprocessing.findTimespanStocks import save_stock_filenames_in_timespan_daily

    start = '20100104'
    end = '20201231'
    exclude_nan = True
    exclude_negative = True
    print("Performing timespan operations...")
    save_stock_filenames_in_timespan_daily(start=start, end=end, exclude_nan=exclude_nan, exclude_negative=exclude_negative)

    # Test Data Set Validity Now
    test_major_op = TestMajorOp()
    test_major_op.set_test_flags(test_NaNs=exclude_nan, test_positives=exclude_negative)
    test_major_op.test_NaNs_major_op()
    test_major_op.test_positive_major_op()


# ==========================
# Bollinger Bands Calculation
# ==========================

if do_band_calculation:
    print("Running Bollinger Bands calculations...")
    from src.bollingerBands.calculateBands import BollingerBands

    directory = OHLC_DATA_DIR
    bollinger = BollingerBands(data_directory=directory)
    bollinger.calculate_all_bands()

# =======================
# Running Bollinger Trades
# =======================

if run_bollinger_trades:
    print("Running Bollinger Band trades...")
    from src.bollingerBands.runBands.runBollingerAll import run_all_bollinger_trades

    run_all_bollinger_trades('test1bollinger')

# ============================
# Turtle Strategy Calculations
# ============================

if do_window_calculation:
    from src.turtles.calculateWindows import TurtleWindows
    print("Running Turtle calculations...")
    directory = OHLC_DATA_DIR
    turtle_windows = TurtleWindows(data_directory=directory)
    turtle_windows.calculate_all_windows()

# ======================
# Running Turtle Trades
# ======================

if run_turtle_trades:
    print("Running Turtles trades...")
    from src.turtles.runTurtles.runTurtleAll import run_all_turtle_trades

    run_all_turtle_trades('test1turtles')


# ============================
# Box Strategy Calculations
# ============================

if do_box_calculations:
    from src.boxStrategy.calculateBoxes import DarvasBoxCalculator
    print("Running Box calculations...")
    directory = OHLC_DATA_DIR
    calculator = DarvasBoxCalculator(data_directory=directory)
    calculator.calculate_all_stock_boxes()

# ======================
# Running Box Trades
# ======================

if run_box_trades:
    print("Running Box trades...")
    from src.boxStrategy.runBoxes.runBoxAll import run_all_box_trades

    run_all_box_trades('test1box')

if run_bollinger_trades or run_turtle_trades or run_box_trades:
    from src.helperFunctions.tradeLog.getTradeLogPath import get_full_tradelog_path
    from src.helperFunctions.tradeLog.logInfo import update_trade_index
    full_tradelog_path = get_full_tradelog_path()
    update_trade_index(full_tradelog_path)

if create_non_trades:
    print("Creating Non Trades...")
    from src.nonTrades.nonTradePoints import get_non_trades
    from src.nonTrades.nonTradeLogFunctions import update_nontrade_index, get_full_nontradelog_path

    get_bollinger_non = False
    get_turtle_non = False
    get_box_non = True

    if get_bollinger_non:
        get_non_trades(strategy='bollinger_naive_dynamic_sl', identifier='test1bollinger', min_distance=3, short_distance=6,
                       medium_distance=9, long_distance=12, splits=[34, 33, 33])

    if get_turtle_non:
        get_non_trades(strategy='turtle_naive', identifier='test1turtle', min_distance=3, short_distance=6,
                       medium_distance=9, long_distance=12, splits=[34, 33, 33])

    if get_box_non:
        get_non_trades(strategy='box_naive', identifier='test1box', min_distance=3, short_distance=6,
                       medium_distance=9, long_distance=25, splits=[34, 33, 33])


    update_nontrade_index(get_full_nontradelog_path())


print("All operations completed.")