from loguru import logger

def backtest(df, config, model):
    logger.info("Starting backtest...")
    balance = config.initial_balance
    position = 0
    entry_price = 0
    equity_curve = []
    for idx in range(len(df)-1):
        window = df.iloc[:idx+1]
        pred = model.predict(window)
        price = df['close'].iloc[idx]
        if position == 0 and pred == 1:
            # Determine size
            risk_amount = balance * config.risk_per_trade
            stop_price = price * (1 - config.stop_loss)
            position_size = min(risk_amount / (price - stop_price), balance * config.max_position / price)
            position = position_size
            entry_price = price
            balance -= position * price * (1 + config.fee)
            logger.debug(f"Enter long: size={position:.6f} @ {price}")
        elif position > 0:
            # Check exit
            high = df['high'].iloc[idx]
            low = df['low'].iloc[idx]
            exit = False
            if high >= entry_price * (1 + config.profit_target):
                exit_price = entry_price * (1 + config.profit_target)
                exit = True
            elif low <= entry_price * (1 - config.stop_loss):
                exit_price = entry_price * (1 - config.stop_loss)
                exit = True
            if exit:
                pnl = position * exit_price * (1 - config.fee)
                balance += pnl
                logger.debug(f"Exit long: size={position:.6f} @ {exit_price}, PnL={pnl - (position*entry_price):.2f}")
                position = 0
        equity_curve.append(balance + position * df['close'].iloc[idx])
    return equity_curve

async def run_live(config, model, data_fetch):
    from ccxt import binance
    import asyncio
    exchange = binance(config.binance_api)
    while True:
        df = data_fetch(config)
        pred = model.predict(df)
        price = df['close'].iloc[-1]
        if pred == 1:
            amount =  (await exchange.fetch_balance())[config.symbol.split('/')[1]] * config.max_position
            logger.info(f"LIVE BUY: {amount} @ {price}")
            if config.mode == 'live':
                order = await exchange.create_market_buy_order(config.symbol, amount)
                logger.info(f"Order executed: {order}")
        else:
            logger.info("LIVE: No signal")
        await asyncio.slee