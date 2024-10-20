import os
import requests
import pandas as pd
from decimal import Decimal
from django.utils import timezone
from .models import StockData
from datetime import datetime, timedelta
from django.http import JsonResponse



API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')


def fetch_stock_data(symbol, return_as_dataframe=False):
    """
    Fetch stock data from Alpha Vantage, store it in the database, and optionally return the data as a DataFrame.

    Args:
        symbol (str): The stock symbol to fetch data for.
        return_as_dataframe (bool): Whether to return the data as a DataFrame (for internal use) or not (for view use).

    Returns:
        pd.DataFrame: If return_as_dataframe is True, returns the DataFrame of stock data.
        JsonResponse: If return_as_dataframe is False, returns a JsonResponse for the view.
    """
    today = timezone.now().date()
    two_years_ago = today - timedelta(days=2 * 365)
    
    existing_data = StockData.objects.filter(symbol=symbol, timestamp__range=[two_years_ago, today]).order_by('timestamp')

    if existing_data.exists():
        stock_data_list = list(existing_data.values('timestamp', 'open_price', 'close_price', 'high_price', 'low_price', 'volume'))
        
        if return_as_dataframe:
            df = pd.DataFrame(stock_data_list)
            return df, None
        else:
            return JsonResponse({'status': 'success', 'message': f'Data for {symbol} fetched from the database.', 'data': stock_data_list})

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises exception for 4xx or 5xx errors
        data = response.json()

        if "Note" in data:
            error_message = data.get("Note", "Rate limit exceeded. Please try again later.")
            if return_as_dataframe:
                return None, error_message
            return JsonResponse({'status': 'error', 'message': error_message})

        if 'Time Series (Daily)' not in data:
            error_message = "No data available for this symbol."
            if return_as_dataframe:
                return None, error_message
            return JsonResponse({'status': 'error', 'message': error_message})

        time_series = data['Time Series (Daily)']

        stock_data_list = []

        for date, daily_data in time_series.items():
            stock_date = datetime.strptime(date, '%Y-%m-%d').date()

            if stock_date >= two_years_ago:
                timestamp = timezone.make_aware(datetime.combine(stock_date, datetime.min.time()))

                stock_entry = {
                    'timestamp': timestamp,
                    'open_price': Decimal(daily_data['1. open']),
                    'close_price': Decimal(daily_data['4. close']),
                    'high_price': Decimal(daily_data['2. high']),
                    'low_price': Decimal(daily_data['3. low']),
                    'volume': int(daily_data['5. volume']),
                }

                StockData.objects.update_or_create(
                    symbol=symbol,
                    timestamp=timestamp,
                    defaults=stock_entry
                )

                stock_data_list.append(stock_entry)

        if return_as_dataframe:
            df = pd.DataFrame(stock_data_list)
            return df, None

        return JsonResponse({'status': 'success', 'message': f'Data for {symbol} fetched and stored successfully.', 'data': stock_data_list})

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        if return_as_dataframe:
            return None, error_message
        return JsonResponse({'status': 'error', 'message': error_message})
