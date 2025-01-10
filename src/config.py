import yaml
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self, path: str = "config.yaml"):
        cfg_path = Path(path)
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(cfg_path) as f:
            data = yaml.safe_load(f)
        # Exchange & API
        self.mode = data['exchange'].get('mode', 'paper')
        self.binance_api = {
            'apiKey': os.getenv('BINANCE_API_KEY', data['binance']['api_key']),
            'secret': os.getenv('BINANCE_SECRET_KEY', data['binance']['secret_key']),
            'enableRateLimit': True
        }
        # Market
        self.symbol = data.get('symbol', 'BTC/USDT')
        self.interval = data.get('interval', '1h')
        self.history_days = data.get('history_days', 60)
        # Model params
        m = data.get('model', {})
        self.model_params = {
            'num_leaves': m.get('num_leaves', 64),
            'learning_rate': m.get('learning_rate', 0.01),
            'n_estimators': m.get('n_estimators', 200)
        }
        # Strategy params
        s = data.get('strategy', {})
        self.profit_target = s.get('profit_target_pct', 1.0) / 100
        self.stop_loss = s.get('stop_loss_pct', 0.5) / 100
        self.risk_per_trade = s.get('risk_per_trade_pct', 1.0) / 100
        self.max_position = s.get('max_position_size', 0.1)
        # Logging
        self.log_level = data.get('logging', {}).get('level', 'INFO')
        # Backtest
        b = data.get('backtest', {})
        self.initial_balance = b.get('initial_balance', 10000)
        self.fee = b.get('fee_pct', 0.1) / 100