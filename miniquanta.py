import requests
import numpy as np
from datetime import datetime

APIKEY = 'CN3DS0UHCVZ46DA5'

def get_forex_data(fx_pair: str, time_frame: str = "daily", output: str = "compact"):
    tf = time_frame.upper()
    from_currency = fx_pair.upper()[:3]
    to_currency = fx_pair.upper()[-3:]
    api_params = f"function=FX_{tf}&from_symbol={from_currency}&to_symbol={to_currency}&outputsize={output}&apikey=" + APIKEY
    url = f"https://www.alphavantage.co/query?"
    response = requests.get(url + api_params)
    data = []
    for date, values in response.json()[f"Time Series FX ({tf[0]+tf[1:].lower()})"].items():
        data.append({
            'date': datetime.strptime(date, '%Y-%m-%d'),
            'open': float(values['1. open']),
            'high': float(values['2. high']),
            'low': float(values['3. low']),
            'close': float(values['4. close'])
        })
    return data

def calculate_moving_std(prices, window_size):
    prices = np.array(prices)
    return np.lib.stride_tricks.sliding_window_view(prices, window_size).std(axis=-1)

def identify_high_volatility(data, window_size, threshold):
    # extrair os preços de fechamento da lista de dicionários
    prices = [day['close'] for day in data]
    dates = [day['date'] for day in data]
    
    # calcular o desvio padrão móvel dos preços
    moving_std = np.concatenate(([np.nan] * (window_size - 1), calculate_moving_std(prices, window_size)))
    
    # identificar as datas com alta volatilidade
    high_volatility_dates = [dates[i] for i, std in enumerate(moving_std) if std > threshold]
    return high_volatility_dates



