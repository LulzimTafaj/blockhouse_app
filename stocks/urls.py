from django.urls import path
from .views import fetch_data_view, backtest_view, predict_view, report_view

urlpatterns = [
    path('fetch/', fetch_data_view, name='fetch_data'),  # URL to fetch stock data
    path('backtest/', backtest_view, name='backtest'),   # URL to perform backtesting
    path('predict/', predict_view, name="predict_prices"),  # URL to predict stock prices
    path('report/', report_view, name='stock_report'),   # URL to generate stock report
]

handler404 = 'stocks.views.custom_404_view'