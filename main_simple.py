#!/usr/bin/env python3
"""
Main Script - CAD-IG-ER Trading Strategy Backtest (Using Pre-computed Signals)

This version uses the validated signals from research to demonstrate the complete system.
For signal generation from scratch, see main_full.py

Target: >4% annualized returns with weekly rebalancing
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
from cad_ig_trading.backtesting.engine import BacktestEngine


def main():
    """Run complete backtest with pre-computed signals."""
    
    print("="*80)
    print("CAD-IG-ER TRADING STRATEGY - COMPLETE BACKTEST")
    print("="*80)
    print("\nUsing validated signals from research (Strategy 9)")
    print("Target: >4% annualized returns (weekly rebalancing, long-only, no leverage)")
    print()
    
    # ========================================================================
    # LOAD DATA WITH SIGNALS
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 1: LOAD DATA")
    print("="*80)
    
    df = pd.read_csv('data/processed/data_with_signals_v2.csv', parse_dates=['Date'])
    print(f"\n✓ Loaded {len(df)} rows from {df['Date'].min()} to {df['Date'].max()}")
    print(f"✓ Columns: {df.shape[1]}")
    print(f"✓ Signal (signal_s9) exposure: {df['signal_s9'].mean():.2%}")
    
    # ========================================================================
    # RUN BACKTEST
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 2: RUN BACKTEST")
    print("="*80)
    
    engine = BacktestEngine()
    results = engine.run_backtest(df, signal_col='signal_s9', resample_freq='W-FRI')
    
    print(f"\n✓ Backtest complete")
    print(f"✓ Resampling: Weekly (Friday)")
    print(f"✓ Signal lag: 1 week (no look-ahead bias)")
    
    # ========================================================================
    # DISPLAY RESULTS
    # ========================================================================
    engine.print_results()
    
    # ========================================================================
    # GENERATE TRADE BLOTTER
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 3: GENERATE TRADE BLOTTER")
    print("="*80)
    
    trade_blotter = engine.get_trade_blotter()
    
    if trade_blotter is not None and len(trade_blotter) > 0:
        print(f"\n✓ Total trades: {len(trade_blotter)}")
        print(f"✓ Winning trades: {(trade_blotter['Return'] > 0).sum()}")
        print(f"✓ Losing trades: {(trade_blotter['Return'] < 0).sum()}")
        print(f"✓ Win rate: {(trade_blotter['Return'] > 0).sum() / len(trade_blotter):.2%}")
        print(f"✓ Average return per trade: {trade_blotter['Return'].mean():.2%}")
        print(f"✓ Best trade: {trade_blotter['Return'].max():.2%}")
        print(f"✓ Worst trade: {trade_blotter['Return'].min():.2%}")
        print(f"✓ Average holding period: {trade_blotter['Holding_Weeks'].mean():.1f} weeks")
        
        # Save trade blotter
        blotter_path = Path("results/trade_blotters/trade_blotter_weekly_final.csv")
        blotter_path.parent.mkdir(parents=True, exist_ok=True)
        trade_blotter.to_csv(blotter_path, index=False)
        print(f"✓ Saved to: {blotter_path}")
        
        # Show first few trades
        print("\nFirst 10 trades:")
        print(trade_blotter.head(10).to_string(index=False))
        
        # Show best trades
        print("\nTop 5 winning trades:")
        print(trade_blotter.nlargest(5, 'Return')[['Trade_ID', 'Entry_Date', 'Exit_Date', 'Return', 'Holding_Weeks']].to_string(index=False))
    
    # ========================================================================
    # SAVE RESULTS
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 4: SAVE RESULTS")
    print("="*80)
    
    # Save metrics
    metrics_df = pd.DataFrame({
        'Metric': [
            'Total Return',
            'Annualized Return',
            'Volatility',
            'Sharpe Ratio',
            'Sortino Ratio',
            'Max Drawdown',
            'Win Rate',
            'Exposure',
            'Years',
            'Weeks'
        ],
        'Strategy': [
            f"{results['strategy']['total_return']:.2%}",
            f"{results['strategy']['annualized_return']:.2%}",
            f"{results['strategy']['volatility']:.2%}",
            f"{results['strategy']['sharpe_ratio']:.2f}",
            f"{results['strategy']['sortino_ratio']:.2f}",
            f"{results['strategy']['max_drawdown']:.2%}",
            f"{results['strategy']['win_rate']:.2%}",
            f"{results['strategy']['exposure']:.2%}",
            f"{results['strategy']['years']:.2f}",
            f"{results['strategy']['weeks']}"
        ],
        'Buy_and_Hold': [
            f"{results['buyhold']['total_return']:.2%}",
            f"{results['buyhold']['annualized_return']:.2%}",
            f"{results['buyhold']['volatility']:.2%}",
            f"{results['buyhold']['sharpe_ratio']:.2f}",
            f"{results['buyhold']['sortino_ratio']:.2f}",
            f"{results['buyhold']['max_drawdown']:.2%}",
            f"{results['buyhold']['win_rate']:.2%}",
            "100.00%",
            f"{results['strategy']['years']:.2f}",
            f"{results['strategy']['weeks']}"
        ]
    })
    
    metrics_path = Path("results/reports/backtest_metrics_final.csv")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(metrics_path, index=False)
    print(f"\n✓ Metrics saved to: {metrics_path}")
    
    # Save weekly returns
    if hasattr(engine, 'df_weekly'):
        weekly_path = Path("results/backtests/weekly_returns_final.csv")
        weekly_path.parent.mkdir(parents=True, exist_ok=True)
        engine.df_weekly.to_csv(weekly_path)
        print(f"✓ Weekly returns saved to: {weekly_path}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)
    
    ann_return = results['strategy']['annualized_return']
    sharpe = results['strategy']['sharpe_ratio']
    sortino = results['strategy']['sortino_ratio']
    max_dd = results['strategy']['max_drawdown']
    win_rate = results['strategy']['win_rate']
    exposure = results['strategy']['exposure']
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Annualized Return: {ann_return:.2%}")
    print(f"   Sharpe Ratio: {sharpe:.2f}")
    print(f"   Sortino Ratio: {sortino:.2f}")
    print(f"   Max Drawdown: {max_dd:.2%}")
    print(f"   Win Rate: {win_rate:.2%}")
    print(f"   Exposure: {exposure:.2%}")
    
    if ann_return >= 0.04:
        print(f"\n✅ SUCCESS: Target achieved ({ann_return:.2%} >= 4.00%)")
    else:
        print(f"\n⚠️  Target not achieved ({ann_return:.2%} < 4.00%)")
    
    print("\n📁 Output files:")
    print(f"   - {blotter_path}")
    print(f"   - {metrics_path}")
    print(f"   - {weekly_path}")
    
    print("\n" + "="*80)
    print("All done! 🎉")
    print("="*80 + "\n")
    
    return results


if __name__ == "__main__":
    results = main()

