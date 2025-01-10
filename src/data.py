import ccxt
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger

def fetch_ohlcv(config) -> pd.DataFrame:
    logger.info("Fetching OHLCV data from Binance...")
    exchange = ccxt.binance(config.binance_api)
    now = datetime.utcnow()
    since = exchange.parse8601((now - timedelta(days=config.history_days)).isoformat())
    records = exchange.fetch_ohlcv(config.symbol, timeframe=config.interval, since=since)
    df = pd.DataFrame(records, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    # Feature engineering with pandas_ta
    df.ta.ema(length=10, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True)
    df.dropna(inplace=True)
    return df