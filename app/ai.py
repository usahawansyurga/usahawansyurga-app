import pandas as pd
import numpy as np


def generate_sample_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    data = {
        'date': np.tile(dates, 3),
        'symbol': ['AAA'] * 30 + ['BBB'] * 30 + ['CCC'] * 30,
        'close': np.random.uniform(1, 5, size=90)
    }
    return pd.DataFrame(data)


def scan_market():
    df = generate_sample_data()
    results = []
    for symbol, group in df.groupby('symbol'):
        group = group.sort_values('date')
        group['ma5'] = group['close'].rolling(window=5).mean()
        group['ma10'] = group['close'].rolling(window=10).mean()
        if group['ma5'].iloc[-1] > group['ma10'].iloc[-1]:
            results.append({'symbol': symbol, 'signal': 'BUY'})
    return results
