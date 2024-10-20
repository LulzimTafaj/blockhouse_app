from django.test import TestCase
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from unittest.mock import patch
from .models import StockData
from .backtests import backtest_strategy
from .tasks import fetch_stock_data

class BacktestTestCase(TestCase):
    """
    TestCase class for testing backtesting functionality.
    """

    def setUp(self):
        """
        Set up test data for the tests.
        """
        StockData.objects.create(
            symbol='AAPL',
            timestamp=timezone.now(),
            open_price=Decimal('150.00'),
            close_price=Decimal('155.00'),
            high_price=Decimal('156.00'),
            low_price=Decimal('149.50'),
            volume=1000000
        )
        
    def test_backtest_valid_symbol(self):
        """
        Test backtesting with a valid stock symbol.
        """
        result = backtest_strategy('AAPL', 10000)
        self.assertIn('Total Return (%)', result)
        self.assertIn('Max Drawdown (%)', result)
        self.assertIn('Number of Trades', result)
        self.assertGreaterEqual(result['Number of Trades'], 0)

    def test_backtest_invalid_symbol(self):
        """
        Test backtesting with an invalid stock symbol.
        """
        result = backtest_strategy('INVALID', 10000)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error')
        self.assertIn('message', result)

    def test_fetch_data_and_backtest(self):
        """
        Test fetching data and backtesting for a symbol not in the database.
        """
        StockData.objects.all().delete()
        df, error_message = fetch_stock_data('IBM', return_as_dataframe=True)
        self.assertIsNotNone(df)
        self.assertIsNone(error_message)
        result = backtest_strategy('IBM', 10000)
        self.assertIn('Total Return (%)', result)
        self.assertGreaterEqual(result['Number of Trades'], 0)

    def test_backtest_with_custom_moving_averages(self):
        """
        Test backtesting with custom moving average windows.
        """
        result = backtest_strategy('AAPL', 10000, short_window=10, long_window=30)
        self.assertIn('Total Return (%)', result)
        self.assertIn('Max Drawdown (%)', result)
        self.assertGreaterEqual(result['Number of Trades'], 0)

    def test_backtest_empty_database(self):
        """
        Test backtesting when the database is empty.
        """
        StockData.objects.all().delete()
        result = backtest_strategy('AAPL', 10000)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error')

    @patch('stocks.tasks.requests.get')
    def test_fetch_data_and_backtest_with_api_mock(self, mock_get):
        """
        Test fetching data and backtesting using a mocked API response.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Time Series (Daily)": {
                "2024-10-17": {
                    "1. open": "150.00",
                    "2. high": "155.00",
                    "3. low": "145.00",
                    "4. close": "152.00",
                    "5. volume": "1000000"
                },
            }
        }

        StockData.objects.all().delete()
        df, error_message = fetch_stock_data('MSFT', return_as_dataframe=True)
        self.assertIsNotNone(df)
        self.assertIsNone(error_message)
        result = backtest_strategy('MSFT', 10000)
        self.assertIn('Total Return (%)', result)
        self.assertGreaterEqual(result['Number of Trades'], 0)
