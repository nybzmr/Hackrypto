
**A production-grade algorithmic trading application** for crypto markets, featuring:

- **Robust feature engineering**: price returns, moving averages, RSI, MACD via `pandas_ta`.
- **LightGBM classifier**: optimized hyperparameters, model persistence.
- **Risk management**: configurable stop-loss, take-profit, position sizing, risk per trade.
- **Paper & live trading**: switch between simulation and real orders via `ccxt`.
- **Backtesting engine**: historical simulation with P&L, drawdown, Sharpe ratio metrics.
- **CLI & logging**: `click` interface, `loguru` logs with rotation and levels.
- **Containerized**: Dockerfile for easy deployment.

## Installation
```bash
git clone <repo-url>
cd ml-crypto-trading-bot-python
cp config_example.yaml config.yaml
# edit config.yaml with your API keys and parameters
pip install -r requirements.txt
```

## Usage
- **Train model** on historical data:
  ```bash
  python main.py train
  ```
- **Backtest strategy**:
  ```bash
  python main.py backtest
  ```
- **Run live/paper** trading:
  ```bash
  python main.py run
  ```

---