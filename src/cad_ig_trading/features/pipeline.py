"""
Complete Feature Engineering Pipeline

Implements all 140+ features from the research phase.
"""

import pandas as pd
import numpy as np
from .base import BaseFeature, FeaturePipeline, calculate_rsi, calculate_zscore
import logging

logger = logging.getLogger(__name__)


class AllFeaturesEngineer:
    """Complete feature engineering pipeline with all 140+ features."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.feature_names = []
        
    def create_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create all features at once.
        
        Args:
            df: Input DataFrame with raw data
            
        Returns:
            DataFrame with all features added
        """
        df = df.copy()
        
        logger.info("Creating all features...")
        logger.info(f"Starting shape: {df.shape}")
        
        # 1. Regime Detection Features
        df = self._create_regime_features(df)
        
        # 2. Momentum & Mean Reversion Features
        df = self._create_momentum_features(df)
        
        # 3. Spread Dynamics Features
        df = self._create_spread_features(df)
        
        # 4. Yield Curve Features
        df = self._create_yield_curve_features(df)
        
        # 5. Macro Surprise Features
        df = self._create_macro_features(df)
        
        # 6. Equity Market Features
        df = self._create_equity_features(df)
        
        # 7. Cross-Asset Features
        df = self._create_cross_asset_features(df)
        
        # 8. Statistical Features
        df = self._create_statistical_features(df)
        
        # 9. Interaction Features
        df = self._create_interaction_features(df)
        
        # 10. Lag Features
        df = self._create_lag_features(df)
        
        # 11. Rolling Statistics
        df = self._create_rolling_stats(df)
        
        # Handle infinite values
        df = df.replace([np.inf, -np.inf], np.nan)
        
        logger.info(f"Final shape: {df.shape}")
        logger.info(f"Total features created: {df.shape[1] - 18}")  # Subtract original columns
        
        return df
    
    def _create_regime_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create regime detection features."""
        logger.info("  Creating regime features...")
        
        # Volatility regimes
        df['volatility_20d'] = df['cad_ig_er_index'].pct_change().rolling(20).std()
        df['volatility_60d'] = df['cad_ig_er_index'].pct_change().rolling(60).std()
        df['volatility_ratio'] = df['volatility_20d'] / df['volatility_60d']
        df['high_vol_regime'] = (df['volatility_20d'] > df['volatility_20d'].rolling(252).quantile(0.75)).astype(int)
        
        # VIX regimes
        df['vix_ma_20'] = df['vix'].rolling(20).mean()
        df['vix_ma_60'] = df['vix'].rolling(60).mean()
        df['vix_regime'] = (df['vix'] > df['vix_ma_60']).astype(int)
        df['vix_zscore'] = calculate_zscore(df['vix'], 252)
        
        # Economic regime
        df['economic_regime_change'] = df['us_economic_regime'].diff()
        
        # Spread regimes
        df['cad_oas_zscore'] = calculate_zscore(df['cad_oas'], 252)
        df['us_hy_oas_zscore'] = calculate_zscore(df['us_hy_oas'], 252)
        df['us_ig_oas_zscore'] = calculate_zscore(df['us_ig_oas'], 252)
        
        # Credit spread widening regime
        df['spread_widening'] = (df['cad_oas'].diff(5) > 0).astype(int)
        
        return df
    
    def _create_momentum_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create momentum and mean reversion features."""
        logger.info("  Creating momentum features...")
        
        # Multi-timeframe momentum
        for period in [5, 10, 20, 40, 60, 120]:
            df[f'momentum_{period}d'] = df['cad_ig_er_index'].pct_change(period)
            df[f'momentum_{period}d_rank'] = df[f'momentum_{period}d'].rolling(252).rank(pct=True)
        
        # RSI indicators
        df['rsi_14'] = calculate_rsi(df['cad_ig_er_index'], 14)
        df['rsi_28'] = calculate_rsi(df['cad_ig_er_index'], 28)
        
        # Mean reversion signals
        df['distance_from_ma_20'] = (df['cad_ig_er_index'] - df['cad_ig_er_index'].rolling(20).mean()) / df['cad_ig_er_index'].rolling(20).std()
        df['distance_from_ma_60'] = (df['cad_ig_er_index'] - df['cad_ig_er_index'].rolling(60).mean()) / df['cad_ig_er_index'].rolling(60).std()
        
        # Bollinger Band position
        bb_middle = df['cad_ig_er_index'].rolling(20).mean()
        bb_std = df['cad_ig_er_index'].rolling(20).std()
        df['bb_upper'] = bb_middle + 2 * bb_std
        df['bb_lower'] = bb_middle - 2 * bb_std
        df['bb_position'] = (df['cad_ig_er_index'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        return df
    
    def _create_spread_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create spread dynamics features."""
        logger.info("  Creating spread features...")
        
        # Spread changes
        for col in ['cad_oas', 'us_hy_oas', 'us_ig_oas']:
            for period in [1, 5, 10, 20]:
                df[f'{col}_change_{period}d'] = df[col].diff(period)
                df[f'{col}_pct_change_{period}d'] = df[col].pct_change(period)
        
        # Spread ratios
        df['cad_us_ig_spread_ratio'] = df['cad_oas'] / df['us_ig_oas']
        df['hy_ig_spread_ratio'] = df['us_hy_oas'] / df['us_ig_oas']
        
        # Spread momentum
        df['cad_oas_momentum_10d'] = df['cad_oas'].diff(10)
        df['us_hy_oas_momentum_10d'] = df['us_hy_oas'].diff(10)
        
        return df
    
    def _create_yield_curve_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create yield curve features."""
        logger.info("  Creating yield curve features...")
        
        # Yield curve changes
        df['us_3m_10y_change_5d'] = df['us_3m_10y'].diff(5)
        df['us_3m_10y_change_20d'] = df['us_3m_10y'].diff(20)
        
        # Yield curve steepening/flattening
        df['curve_steepening'] = (df['us_3m_10y'].diff(5) > 0).astype(int)
        
        return df
    
    def _create_macro_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create macro surprise features."""
        logger.info("  Creating macro features...")
        
        # Cumulative surprises
        for col in ['us_growth_surprises', 'us_inflation_surprises', 'us_hard_data_surprises']:
            df[f'{col}_cumsum_20d'] = df[col].rolling(20).sum()
            df[f'{col}_cumsum_60d'] = df[col].rolling(60).sum()
            df[f'{col}_ma_20d'] = df[col].rolling(20).mean()
        
        # Surprise momentum
        df['growth_surprise_momentum'] = df['us_growth_surprises'].diff(5)
        df['inflation_surprise_momentum'] = df['us_inflation_surprises'].diff(5)
        
        # Combined surprise index
        df['combined_surprise_index'] = (
            df['us_growth_surprises'] + 
            df['us_hard_data_surprises'] - 
            df['us_inflation_surprises']
        )
        
        return df
    
    def _create_equity_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create equity market features."""
        logger.info("  Creating equity features...")
        
        # Equity revisions momentum
        df['us_equity_revisions_change_5d'] = df['us_equity_revisions'].diff(5)
        df['us_equity_revisions_change_20d'] = df['us_equity_revisions'].diff(20)
        
        # TSX momentum
        df['tsx_momentum_20d'] = df['tsx'].pct_change(20)
        df['tsx_momentum_60d'] = df['tsx'].pct_change(60)
        
        # SPX earnings features
        df['spx_eps_change_20d'] = df['spx_1bf_eps'].pct_change(20)
        df['spx_sales_change_20d'] = df['spx_1bf_sales'].pct_change(20)
        
        # TSX earnings features
        df['tsx_eps_change_20d'] = df['tsx_1bf_eps'].pct_change(20)
        df['tsx_sales_change_20d'] = df['tsx_1bf_sales'].pct_change(20)
        
        return df
    
    def _create_cross_asset_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create cross-asset relationship features."""
        logger.info("  Creating cross-asset features...")
        
        # US IG vs CAD IG relative performance
        df['us_ig_er_momentum_20d'] = df['us_ig_er_index'].pct_change(20)
        df['cad_ig_er_momentum_20d'] = df['cad_ig_er_index'].pct_change(20)
        df['cad_us_ig_relative_momentum'] = df['cad_ig_er_momentum_20d'] - df['us_ig_er_momentum_20d']
        
        # US HY performance
        df['us_hy_er_momentum_20d'] = df['us_hy_er_index'].pct_change(20)
        
        # Correlation features
        df['cad_us_ig_corr_60d'] = df['cad_ig_er_index'].pct_change().rolling(60).corr(df['us_ig_er_index'].pct_change())
        
        return df
    
    def _create_statistical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create statistical features."""
        logger.info("  Creating statistical features...")
        
        # Skewness and kurtosis
        returns = df['cad_ig_er_index'].pct_change()
        df['returns_skew_60d'] = returns.rolling(60).skew()
        df['returns_kurt_60d'] = returns.rolling(60).kurt()
        
        # Drawdown
        cummax = df['cad_ig_er_index'].cummax()
        df['drawdown'] = (df['cad_ig_er_index'] - cummax) / cummax
        df['drawdown_duration'] = (df['drawdown'] < 0).astype(int).groupby((df['drawdown'] >= 0).cumsum()).cumsum()
        
        # Up/down day streaks
        df['up_day'] = (df['cad_ig_er_index'].diff() > 0).astype(int)
        df['up_streak'] = df['up_day'].groupby((df['up_day'] != df['up_day'].shift()).cumsum()).cumsum()
        df['down_streak'] = (1 - df['up_day']).groupby((df['up_day'] != df['up_day'].shift()).cumsum()).cumsum()
        
        return df
    
    def _create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features."""
        logger.info("  Creating interaction features...")
        
        # VIX * Spread interactions
        df['vix_x_cad_oas'] = df['vix'] * df['cad_oas']
        df['vix_x_spread_change'] = df['vix'] * df['cad_oas_change_5d']
        
        # Momentum * Volatility
        df['momentum_20d_x_vol'] = df['momentum_20d'] * df['volatility_20d']
        
        # Regime * Momentum
        df['high_vol_x_momentum'] = df['high_vol_regime'] * df['momentum_20d']
        df['vix_regime_x_momentum'] = df['vix_regime'] * df['momentum_20d']
        
        # Economic regime * Spreads
        df['econ_regime_x_cad_oas'] = df['us_economic_regime'] * df['cad_oas']
        
        # Surprise interactions
        df['growth_x_inflation_surprise'] = df['us_growth_surprises'] * df['us_inflation_surprises']
        
        return df
    
    def _create_lag_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create lag features."""
        logger.info("  Creating lag features...")
        
        # Key features with lags
        key_features = ['vix', 'cad_oas', 'us_hy_oas', 'momentum_20d', 'volatility_20d']
        for feat in key_features:
            if feat in df.columns:
                for lag in [1, 5, 10]:
                    df[f'{feat}_lag_{lag}'] = df[feat].shift(lag)
        
        return df
    
    def _create_rolling_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create rolling statistics features."""
        logger.info("  Creating rolling statistics...")
        
        # Rolling min/max
        df['cad_oas_min_60d'] = df['cad_oas'].rolling(60).min()
        df['cad_oas_max_60d'] = df['cad_oas'].rolling(60).max()
        df['cad_oas_range_position'] = (df['cad_oas'] - df['cad_oas_min_60d']) / (df['cad_oas_max_60d'] - df['cad_oas_min_60d'])
        
        # Rolling rank
        df['vix_rank_252d'] = df['vix'].rolling(252).rank(pct=True)
        df['cad_oas_rank_252d'] = df['cad_oas'].rolling(252).rank(pct=True)
        
        return df

