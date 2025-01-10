import click
from loguru import logger
from config import Config
from data import fetch_ohlcv
from model import TradingModel
from strategy import backtest, run_live
import asyncio

@click.group()
@click.pass_context
def cli(ctx):
    cfg = Config()
    logger.remove()
    logger.add(lambda msg: print(msg, end=''), level=cfg.log_level)
    ctx.obj = {'config': cfg}

@cli.command()
@click.pass_context
def train(ctx):
    """Train the ML model on historical data."""
    cfg = ctx.obj['config']
    df = fetch_ohlcv(cfg)
    tm = TradingModel(cfg.model_params)
    tm.train(df)

@cli.command()
@click.pass_context
def backtest_cmd(ctx):
    """Backtest the strategy over historical data."""
    cfg = ctx.obj['config']
    df = fetch_ohlcv(cfg)
    tm = TradingModel(cfg.model_params)
    tm.model = __import__('joblib').load('model.pkl')
    equity = backtest(df, cfg, tm)
    # TODO: plot equity curve or save to CSV
    logger.info(f"Backtest final equity: {equity[-1]:.2f}")

@cli.command()
@click.pass_context
def run(ctx):
    """Run live (or paper) trading loop."""
    cfg = ctx.obj['config']
    tm = TradingModel(cfg.model_params)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_live(cfg, tm, fetch_ohlcv))

if __name__ == '__main__':
    cli()