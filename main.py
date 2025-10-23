#!/usr/bin/env python3
"""
Main Script - Complete CAD-IG-ER Trading Strategy Backtest

This script runs the complete end-to-end backtest:
1. Load data
2. Preprocess
3. Engineer features
4. Train models
5. Generate signals
6. Run backtest
7. Generate reports

Target: >4% annualized returns with weekly rebalancing
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
import numpy as np
from cad_ig_trading.data.loader import DataLoader
from cad_ig_trading.data.preprocessor import DataPreprocessor
from cad_ig_trading.features.pipeline import AllFeaturesEngineer
from cad_ig_trading.models.ensemble import WeeklyEnsembleStrategy
from cad_ig_trading.backtesting.engine import BacktestEngine


def main():
    """Run complete backtest pipeline."""
    
    print("="*80)
    print("CAD-IG-ER TRADING STRATEGY - COMPLETE BACKTEST")
    print("="*80)
    print("\nTarget: >4% annualized returns (weekly rebalancing, long-only, no leverage)")
    print()
    
    # ========================================================================
    # STEP 1: LOAD DATA
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 1: LOAD DATA")
    print("="*80)
    
    loader = DataLoader()
    df = loader.load()
    print(f"\n✓ Loaded {len(df)} rows from {df['Date'].min()} to {df['Date'].max()}")
    print(f"✓ Columns: {df.shape[1]}")
    
    # ========================================================================
    # STEP 2: PREPROCESS
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 2: PREPROCESS DATA")
    print("="*80)
    
    preprocessor = DataPreprocessor()
    df = preprocessor.preprocess(df, handle_missing=True, add_target=False)
    print(f"\n✓ Preprocessed shape: {df.shape}")
    print(f"✓ Missing values handled")
    print(f"✓ Infinite values replaced")
    
    # ========================================================================
    # STEP 3: FEATURE ENGINEERING
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 3: FEATURE ENGINEERING")
    print("="*80)
    
    feature_engineer = AllFeaturesEngineer()
    df = feature_engineer.create_all_features(df)
    print(f"\n✓ Final shape: {df.shape}")
    print(f"✓ Total features created: {df.shape[1] - 18}")
    
    # Save processed data
    output_path = Path("data/processed/data_with_all_features.csv")
    df.to_csv(output_path, index=False)
    print(f"✓ Saved to: {output_path}")
    
    # ========================================================================
    # STEP 4: TRAIN MODELS & GENERATE SIGNALS
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 4: TRAIN MODELS & GENERATE SIGNALS")
    print("="*80)
    
    strategy = WeeklyEnsembleStrategy(n_features=60, threshold=0.45)
    df = strategy.generate_signals(df, train_size=0.6)
    
    print(f"\n✓ Models trained (LightGBM, XGBoost, Random Forest)")
    print(f"✓ Ensemble weights: LGBM=40%, XGB=35%, RF=25%")
    print(f"✓ Feature selection: Top 60 features")
    print(f"✓ Probability threshold: 0.45")
    print(f"✓ Filters applied: Momentum & Volatility")
    
    # ========================================================================
    # STEP 5: RUN BACKTEST
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 5: RUN BACKTEST")
    print("="*80)
    
    engine = BacktestEngine()
    results = engine.run_backtest(df, signal_col='signal', resample_freq='W-FRI')
    
    print(f"\n✓ Backtest complete")
    print(f"✓ Resampling: Weekly (Friday)")
    print(f"✓ Signal lag: 1 week (no look-ahead bias)")
    
    # ========================================================================
    # STEP 6: DISPLAY RESULTS
    # ========================================================================
    engine.print_results()
    
    # ========================================================================
    # STEP 7: GENERATE TRADE BLOTTER
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 7: GENERATE TRADE BLOTTER")
    print("="*80)
    
    trade_blotter = engine.get_trade_blotter()
    
    if trade_blotter is not None and len(trade_blotter) > 0:
        print(f"\n✓ Total trades: {len(trade_blotter)}")
        print(f"✓ Winning trades: {(trade_blotter['Return'] > 0).sum()}")
        print(f"✓ Losing trades: {(trade_blotter['Return'] < 0).sum()}")
        print(f"✓ Average return per trade: {trade_blotter['Return'].mean():.2%}")
        print(f"✓ Average holding period: {trade_blotter['Holding_Weeks'].mean():.1f} weeks")
        
        # Save trade blotter
        blotter_path = Path("results/trade_blotters/trade_blotter_weekly.csv")
        blotter_path.parent.mkdir(parents=True, exist_ok=True)
        trade_blotter.to_csv(blotter_path, index=False)
        print(f"✓ Saved to: {blotter_path}")
        
        # Show first few trades
        print("\nFirst 10 trades:")
        print(trade_blotter.head(10).to_string(index=False))
    
    # ========================================================================
    # STEP 8: SAVE RESULTS
    # ========================================================================
    print("\n" + "="*80)
    print("STEP 8: SAVE RESULTS")
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
            f"{results['buyhold'].get('years', results['strategy']['years']):.2f}",
            f"{results['strategy']['weeks']}"
        ]
    })
    
    metrics_path = Path("results/reports/backtest_metrics.csv")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(metrics_path, index=False)
    print(f"\n✓ Metrics saved to: {metrics_path}")
    
    # Save weekly returns
    if hasattr(engine, 'df_weekly'):
        weekly_path = Path("results/backtests/weekly_returns.csv")
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
    max_dd = results['strategy']['max_drawdown']
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Annualized Return: {ann_return:.2%}")
    print(f"   Sharpe Ratio: {sharpe:.2f}")
    print(f"   Max Drawdown: {max_dd:.2%}")
    
    if ann_return >= 0.04:
        print(f"\n✅ SUCCESS: Target achieved ({ann_return:.2%} >= 4.00%)")
    else:
        print(f"\n⚠️  Target not achieved ({ann_return:.2%} < 4.00%)")
    
    print("\n📁 Output files:")
    print(f"   - {output_path}")
    print(f"   - {blotter_path}")
    print(f"   - {metrics_path}")
    print(f"   - {weekly_path}")
    
    print("\n" + "="*80)
    print("All done! 🎉")
    print("="*80 + "\n")
    
    return results


if __name__ == "__main__":
    results = main()

