import unittest
from src.config import DATA_DIR
import os
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades, extract_trades_auxillary
from src.nonTrades.nonTradeLogFunctions import extract_nontrades
from tqdm import tqdm
import json


class MyTestCase(unittest.TestCase):
    def test_date_overlap_aapl(self):
        print('AAPL')
        aapl_trades = extract_trades(strategy='bollinger_naive_dynamic_sl', stock_name='AAPL', identifier='test1bollinger')

        dates_trades = set(aapl_trades['StartDate'].values)

        non_trades_aapl = extract_nontrades(strategy='NonTradebollinger_naive_dynamic_sl', stock_name='AAPL')

        dates_non_trades = set(non_trades_aapl['StartDate'].values)
        print("Trade dates:", dates_trades)
        print("Non-trade dates:", dates_non_trades)
        assert len(aapl_trades) == len(non_trades_aapl)
        overlap = dates_trades.intersection(dates_non_trades)
        print("Overlapping dates:", overlap)
        assert len(overlap) == 0, "There should be no overlapping dates between trades and non-trades."


    def test_date_overlap_all_stocks(self):
        json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        valid_stocks = [stock.replace('.csv', '') for stock in data.get('valid_files')]

        for stock in tqdm(valid_stocks, desc='Processing stocks'):
            trades = extract_trades(strategy='bollinger_naive_dynamic_sl', stock_name=stock, identifier='test1bollinger')
            non_trades = extract_nontrades(strategy='NonTradebollinger_naive_dynamic_sl', stock_name=stock, identifier='NonTradetest1bollinger')

            # Convert StartDates to sets for comparison
            dates_trades = set(trades['StartDate'].values)
            dates_non_trades = set(non_trades['StartDate'].values)

            # Check for overlap and assert
            overlap = dates_trades.intersection(dates_non_trades)
            assert len(trades) == len(non_trades)
            self.assertEqual(len(overlap), 0, f"Overlap found in stock {stock}: {overlap}")

if __name__ == '__main__':
    unittest.main()
