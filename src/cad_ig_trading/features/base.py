"""
Base Feature Engineering Module

Provides base class and utilities for feature engineering.
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class BaseFeature(ABC):
    """Abstract base class for feature engineering."""
    
    def __init__(self, name: str):
        """
        Initialize BaseFeature.
        
        Args:
            name: Name of the feature set
        """
        self.name = name
        self.feature_names = []
        
    @abstractmethod
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create features from input DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with new features added
        """
        pass
    
    def get_feature_names(self) -> List[str]:
        """
        Get list of feature names created by this feature set.
        
        Returns:
            List of feature names
        """
        return self.feature_names
    
    def _validate_columns(self, df: pd.DataFrame, required_columns: List[str]) -> None:
        """
        Validate that required columns exist in DataFrame.
        
        Args:
            df: Input DataFrame
            required_columns: List of required column names
            
        Raises:
            ValueError: If required columns are missing
        """
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")


class FeaturePipeline:
    """Pipeline for applying multiple feature engineering steps."""
    
    def __init__(self, features: Optional[List[BaseFeature]] = None):
        """
        Initialize FeaturePipeline.
        
        Args:
            features: List of BaseFeature instances to apply
        """
        self.features = features or []
        
    def add_feature(self, feature: BaseFeature) -> 'FeaturePipeline':
        """
        Add a feature engineering step to the pipeline.
        
        Args:
            feature: BaseFeature instance
            
        Returns:
            Self for method chaining
        """
        self.features.append(feature)
        return self
    
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all feature engineering steps to the DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with all features added
        """
        df = df.copy()
        
        logger.info(f"Applying {len(self.features)} feature engineering steps")
        logger.info(f"Starting shape: {df.shape}")
        
        for feature in self.features:
            logger.info(f"Applying {feature.name}...")
            df = feature.create_features(df)
            logger.info(f"  Added {len(feature.get_feature_names())} features")
        
        logger.info(f"Final shape: {df.shape}")
        logger.info(f"Total features added: {df.shape[1] - len(df.columns)}")
        
        return df
    
    def get_all_feature_names(self) -> List[str]:
        """
        Get all feature names from all feature engineering steps.
        
        Returns:
            List of all feature names
        """
        all_features = []
        for feature in self.features:
            all_features.extend(feature.get_feature_names())
        return all_features


# Utility functions for feature engineering

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        prices: Price series
        period: RSI period
        
    Returns:
        RSI series
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_bollinger_bands(prices: pd.Series, period: int = 20, 
                              num_std: float = 2.0) -> tuple:
    """
    Calculate Bollinger Bands.
    
    Args:
        prices: Price series
        period: Moving average period
        num_std: Number of standard deviations
        
    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    middle = prices.rolling(period).mean()
    std = prices.rolling(period).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    return upper, middle, lower


def calculate_drawdown(prices: pd.Series) -> pd.Series:
    """
    Calculate drawdown from peak.
    
    Args:
        prices: Price series
        
    Returns:
        Drawdown series
    """
    cummax = prices.cummax()
    drawdown = (prices - cummax) / cummax
    return drawdown


def calculate_zscore(series: pd.Series, window: int = 252) -> pd.Series:
    """
    Calculate rolling z-score.
    
    Args:
        series: Input series
        window: Rolling window size
        
    Returns:
        Z-score series
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    zscore = (series - mean) / std
    return zscore

