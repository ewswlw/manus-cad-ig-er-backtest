#!/usr/bin/env python3
"""
Validate backtest engine using original research signals.

This loads the signal_s9 from research and runs backtest to verify engine works correctly.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
from cad_ig_trading.backtesting.engine import BacktestEngine

print("="*80)
print("VALIDATE BACKTEST ENGINE WITH RESEARCH SIGNALS")
print("="*80)

# Load original data with signals
df = pd.read_csv('/home/ubuntu/trading_strategy/data_with_signals_v2.csv', parse_dates=['Date'])
print(f"\nLoaded {len(df)} rows")
print(f"Signal (signal_s9) mean: {df['signal_s9'].mean():.2%}")
print(f"Signal sum: {df['signal_s9'].sum()}")

# Run backtest with original signal
engine = BacktestEngine()
results = engine.run_backtest(df, signal_col='signal_s9', resample_freq='W-FRI')

# Print results
engine.print_results()

# Get trade blotter
trade_blotter = engine.get_trade_blotter()
if trade_blotter is not None:
    print(f"\n✓ Total trades: {len(trade_blotter)}")
    print(f"✓ Average return per trade: {trade_blotter['Return'].mean():.2%}")
    
    # Save
    trade_blotter.to_csv('results/trade_blotters/trade_blotter_validation.csv', index=False)
    print(f"✓ Saved to: results/trade_blotters/trade_blotter_validation.csv")

print("\n" + "="*80)

