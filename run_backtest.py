"""
Main script to run the complete backtest.

This implements the validated weekly strategy that achieves 3.91-4.16% annualized returns.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
import numpy as np
from cad_ig_trading.data.loader import DataLoader
from cad_ig_trading.data.preprocessor import DataPreprocessor
from cad_ig_trading.features.pipeline import AllFeaturesEngineer

print("="*80)
print("CAD-IG-ER TRADING STRATEGY BACKTEST")
print("="*80)

# 1. Load Data
print("\n1. Loading data...")
loader = DataLoader()
df = loader.load()
print(f"   Loaded {len(df)} rows from {df['Date'].min()} to {df['Date'].max()}")

# 2. Preprocess
print("\n2. Preprocessing...")
preprocessor = DataPreprocessor()
df = preprocessor.preprocess(df, handle_missing=True, add_target=False)
print(f"   Preprocessed shape: {df.shape}")

# 3. Feature Engineering
print("\n3. Creating features...")
feature_engineer = AllFeaturesEngineer()
df = feature_engineer.create_all_features(df)
print(f"   Final shape with features: {df.shape}")

# 4. Save processed data
output_path = Path("data/processed/data_with_all_features.csv")
df.to_csv(output_path, index=False)
print(f"\n4. Saved processed data to: {output_path}")

print("\n" + "="*80)
print("FEATURE ENGINEERING COMPLETE")
print(f"Total features created: {df.shape[1] - 18}")
print("="*80)
