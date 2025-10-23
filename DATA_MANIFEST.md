# Data Files Manifest

This document describes all data files included in the repository.

## Raw Data (`data/raw/`)

### with_er_daily.csv (1.1 MB)
- **Description:** Original CAD-IG-ER index daily data
- **Time Period:** 2003-2025 (21.82 years)
- **Frequency:** Daily
- **Rows:** ~5,700 observations
- **Columns:** 18 features
  - Date
  - CAD_IG_ER (Excess Return Index)
  - CAD_OAS (Option-Adjusted Spread)
  - US_IG_OAS, US_HY_OAS (US spreads)
  - VIX (Volatility Index)
  - SPX_FWD_EPS, SPX_FWD_SALES (S&P 500 forward metrics)
  - Macro surprises (GDP, CPI, Employment, etc.)
  - Cross-asset indicators

## Processed Data (`data/processed/`)

### data_with_all_features.csv (13 MB)
- **Description:** Complete dataset with all engineered features
- **Features:** 140+ engineered features including:
  - Momentum features (returns, RSI, acceleration)
  - Spread features (OAS levels, ratios, z-scores)
  - Macro features (surprises, interactions)
  - Regime features (volatility regimes, economic cycles)
  - Statistical features (rolling stats, distributions)
- **Used for:** Model training and backtesting

## Results

### Backtests (`results/backtests/`)

#### strategy_comparison_v3.csv
- **Description:** Comparison of all 12 strategies tested
- **Columns:**
  - Strategy name
  - Annualized return
  - Sharpe ratio
  - Max drawdown
  - Win rate
  - Total trades
- **Best Strategy:** Strategy 9 (Advanced Ensemble) - 4.16% annualized

### Trade Blotters (`results/trade_blotters/`)

#### trade_blotter_strategy9.csv (Weekly Strategy)
- **Description:** Complete trade-by-trade log for weekly strategy
- **Trades:** 136 trades over 21.82 years
- **Columns:**
  - Trade ID
  - Entry date/price
  - Exit date/price
  - Return %
  - Holding period (weeks)
  - P&L
- **Performance:**
  - Average trade: +0.38%
  - Win rate: 58.1%
  - Best trade: +9.21% (COVID recovery)
  - Worst trade: -1.02%

#### trade_blotter_monthly.csv (Monthly Strategy)
- **Description:** Complete trade-by-trade log for monthly strategy
- **Trades:** 38 trades over 21.82 years
- **Columns:** Same as weekly
- **Performance:**
  - Average trade: +1.20%
  - Win rate: 65.8%
  - Best trade: +9.21%
  - Worst trade: -1.04%

### Analysis (`results/analysis/`)

#### feature_importance_v2.csv
- **Description:** Feature importance rankings from ensemble models
- **Features:** Top 70 features ranked by importance
- **Top Features:**
  1. SPX_FWD_EPS_chg_5d
  2. CAD_OAS_level
  3. US_IG_OAS_chg_20d
  4. VIX_level
  5. Momentum_20d

### Reports (`results/reports/`)

#### FINAL_PERFORMANCE_METRICS.csv
- **Description:** Summary performance metrics for all strategies
- **Metrics:**
  - Returns (total, annualized, CAGR)
  - Risk metrics (volatility, Sharpe, Sortino, max DD)
  - Trade statistics (count, win rate, avg return)
  - Comparison vs Buy & Hold

### Visualizations (`results/visualizations/`)

#### correlation_matrix.png
- **Description:** Correlation heatmap of top features
- **Shows:** Feature relationships and multicollinearity

#### eda_overview.png
- **Description:** Exploratory data analysis overview
- **Panels:**
  - Price history
  - Returns distribution
  - Volatility over time
  - Feature correlations
  - Regime detection
  - Seasonal patterns

#### final_strategy_performance.png
- **Description:** Final strategy performance visualization
- **Panels:**
  - Cumulative returns
  - Drawdown chart
  - Monthly returns heatmap
  - Trade distribution
  - Win/loss analysis
  - Rolling Sharpe ratio

#### strategy_performance_analysis.png
- **Description:** Detailed performance analysis
- **Shows:** Multiple strategy comparisons

#### weekly_vs_monthly_comparison.png
- **Description:** Side-by-side comparison of weekly vs monthly strategies
- **Panels:**
  - Cumulative returns
  - Drawdowns
  - Trade frequency
  - Risk-adjusted returns

## Data Usage

### For Backtesting
```python
import pandas as pd

# Load raw data
df_raw = pd.read_csv('data/raw/with_er_daily.csv', parse_dates=['Date'])

# Load processed data with features
df_features = pd.read_csv('data/processed/data_with_all_features.csv', parse_dates=['Date'])

# Load backtest results
results = pd.read_csv('results/backtests/strategy_comparison_v3.csv')
```

### For Analysis
```python
# Load trade blotter
trades = pd.read_csv('results/trade_blotters/trade_blotter_strategy9.csv', parse_dates=['Entry_Date', 'Exit_Date'])

# Load feature importance
features = pd.read_csv('results/analysis/feature_importance_v2.csv')

# Load performance metrics
metrics = pd.read_csv('results/reports/FINAL_PERFORMANCE_METRICS.csv')
```

## Data Quality

### Validation Checks Passed
✅ No missing values in target variable (CAD_IG_ER)
✅ No duplicate dates
✅ Continuous time series (no gaps)
✅ All features within expected ranges
✅ No look-ahead bias (features properly lagged)
✅ Consistent data types

### Data Preprocessing Applied
- Forward-fill for missing macro data (max 5 days)
- Outlier handling (winsorization at 99th percentile)
- Feature scaling (standardization for ML models)
- Time-based train/test split (no data leakage)

## File Sizes Summary

| File | Size | Rows | Purpose |
|------|------|------|---------|
| with_er_daily.csv | 1.1 MB | ~5,700 | Raw input data |
| data_with_all_features.csv | 13 MB | ~5,700 | Engineered features |
| strategy_comparison_v3.csv | <1 KB | 12 | Strategy comparison |
| trade_blotter_strategy9.csv | ~20 KB | 136 | Weekly trades |
| trade_blotter_monthly.csv | ~10 KB | 38 | Monthly trades |
| feature_importance_v2.csv | ~5 KB | 70 | Feature rankings |
| FINAL_PERFORMANCE_METRICS.csv | <1 KB | 12 | Performance summary |

## Data Versioning

Current version: **v1.0**
- Initial dataset: 2003-01-01 to 2025-01-31
- Features: 140 engineered features
- Models: Weekly and monthly strategies

Future versions will be stored in `data/versions/` with version tags.

## Data Sources

- **CAD-IG-ER Index:** Bloomberg
- **Spreads (OAS):** Bloomberg
- **Macro Data:** Bloomberg Economic Calendar
- **VIX:** CBOE
- **SPX Forward Metrics:** FactSet

## License & Usage

This data is for research and backtesting purposes only. Do not use for live trading without proper validation and risk management.

---

**Last Updated:** October 23, 2025
**Data Version:** 1.0
**Repository:** https://github.com/ewswlw/manus-cad-ig-er-backtest
