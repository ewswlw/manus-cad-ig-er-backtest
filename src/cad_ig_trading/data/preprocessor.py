"""
Data Preprocessor Module

Handles data cleaning, missing value treatment, and basic transformations.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocess and clean data."""
    
    def __init__(self):
        """Initialize DataPreprocessor."""
        self.fill_methods = {}
        
    def handle_missing_values(self, df: pd.DataFrame, 
                             method: str = 'forward_fill',
                             max_fill: int = 5) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            df: Input DataFrame
            method: Method to handle missing values ('forward_fill', 'backward_fill', 'drop')
            max_fill: Maximum number of consecutive values to fill
            
        Returns:
            DataFrame with missing values handled
        """
        df = df.copy()
        
        logger.info(f"Handling missing values using method: {method}")
        logger.info(f"Missing values before: {df.isnull().sum().sum()}")
        
        if method == 'forward_fill':
            # Forward fill with limit
            df = df.fillna(method='ffill', limit=max_fill)
        elif method == 'backward_fill':
            df = df.fillna(method='bfill', limit=max_fill)
        elif method == 'drop':
            df = df.dropna()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        logger.info(f"Missing values after: {df.isnull().sum().sum()}")
        
        return df
    
    def handle_outliers(self, df: pd.DataFrame, 
                       columns: list,
                       method: str = 'winsorize',
                       lower_quantile: float = 0.01,
                       upper_quantile: float = 0.99) -> pd.DataFrame:
        """
        Handle outliers in specified columns.
        
        Args:
            df: Input DataFrame
            columns: List of columns to process
            method: Method to handle outliers ('winsorize', 'clip')
            lower_quantile: Lower quantile for winsorization
            upper_quantile: Upper quantile for winsorization
            
        Returns:
            DataFrame with outliers handled
        """
        df = df.copy()
        
        logger.info(f"Handling outliers in {len(columns)} columns using method: {method}")
        
        for col in columns:
            if col not in df.columns:
                logger.warning(f"Column {col} not found, skipping")
                continue
            
            if method == 'winsorize':
                lower = df[col].quantile(lower_quantile)
                upper = df[col].quantile(upper_quantile)
                df[col] = df[col].clip(lower=lower, upper=upper)
            elif method == 'clip':
                # Clip to +/- 3 standard deviations
                mean = df[col].mean()
                std = df[col].std()
                lower = mean - 3 * std
                upper = mean + 3 * std
                df[col] = df[col].clip(lower=lower, upper=upper)
        
        return df
    
    def handle_infinite_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Replace infinite values with NaN.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with infinite values replaced
        """
        df = df.copy()
        
        inf_count = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
        
        if inf_count > 0:
            logger.info(f"Replacing {inf_count} infinite values with NaN")
            df = df.replace([np.inf, -np.inf], np.nan)
        
        return df
    
    def add_target_variable(self, df: pd.DataFrame, 
                           target_col: str = 'cad_ig_er_index',
                           horizon: int = 1) -> pd.DataFrame:
        """
        Add target return variable.
        
        Args:
            df: Input DataFrame
            target_col: Column to calculate returns from
            horizon: Number of periods ahead for target
            
        Returns:
            DataFrame with target variable added
        """
        df = df.copy()
        
        df['target_return'] = df[target_col].pct_change(horizon).shift(-horizon)
        
        logger.info(f"Added target_return with {horizon}-period horizon")
        
        return df
    
    def preprocess(self, df: pd.DataFrame, 
                  handle_missing: bool = True,
                  handle_outliers_flag: bool = False,
                  add_target: bool = True) -> pd.DataFrame:
        """
        Run full preprocessing pipeline.
        
        Args:
            df: Input DataFrame
            handle_missing: Whether to handle missing values
            handle_outliers_flag: Whether to handle outliers
            add_target: Whether to add target variable
            
        Returns:
            Preprocessed DataFrame
        """
        logger.info("Starting preprocessing pipeline")
        
        df = df.copy()
        
        # Handle infinite values first
        df = self.handle_infinite_values(df)
        
        # Handle missing values
        if handle_missing:
            df = self.handle_missing_values(df, method='forward_fill', max_fill=5)
        
        # Handle outliers (optional, usually done after feature engineering)
        if handle_outliers_flag:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Exclude Date and index columns
            numeric_cols = [col for col in numeric_cols if col not in ['Date']]
            df = self.handle_outliers(df, numeric_cols, method='winsorize')
        
        # Add target variable
        if add_target:
            df = self.add_target_variable(df)
        
        logger.info(f"Preprocessing complete. Shape: {df.shape}")
        
        return df

