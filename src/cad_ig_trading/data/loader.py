"""
Data Loader Module

Handles loading and basic preprocessing of raw data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and preprocess raw CAD-IG-ER index data."""
    
    def __init__(self, data_path: Optional[Union[str, Path]] = None):
        """
        Initialize DataLoader.
        
        Args:
            data_path: Path to the raw data file. If None, uses default path.
        """
        if data_path is None:
            # Default to project data directory
            project_root = Path(__file__).parents[4]
            data_path = project_root / "cad_ig_trading" / "data" / "raw" / "with_er_daily.csv"
        
        self.data_path = Path(data_path)
        self.df = None
        
    def load(self) -> pd.DataFrame:
        """
        Load raw data from CSV.
        
        Returns:
            DataFrame with loaded data
        """
        logger.info(f"Loading data from {self.data_path}")
        
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self.df = pd.read_csv(self.data_path, parse_dates=['Date'])
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        
        logger.info(f"Loaded {len(self.df)} rows, {self.df.shape[1]} columns")
        logger.info(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        
        return self.df
    
    def get_data(self) -> pd.DataFrame:
        """
        Get loaded data. Loads if not already loaded.
        
        Returns:
            DataFrame with data
        """
        if self.df is None:
            self.load()
        return self.df.copy()
    
    def get_column_info(self) -> pd.DataFrame:
        """
        Get information about columns in the dataset.
        
        Returns:
            DataFrame with column information
        """
        if self.df is None:
            self.load()
        
        info = pd.DataFrame({
            'column': self.df.columns,
            'dtype': self.df.dtypes.values,
            'null_count': self.df.isnull().sum().values,
            'null_pct': (self.df.isnull().sum() / len(self.df) * 100).values,
            'unique_values': [self.df[col].nunique() for col in self.df.columns]
        })
        
        return info
    
    def get_date_range(self) -> tuple:
        """
        Get the date range of the dataset.
        
        Returns:
            Tuple of (start_date, end_date)
        """
        if self.df is None:
            self.load()
        
        return (self.df['Date'].min(), self.df['Date'].max())
    
    def filter_by_date(self, start_date: Optional[str] = None, 
                       end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Filter data by date range.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            self.load()
        
        df_filtered = self.df.copy()
        
        if start_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] >= pd.to_datetime(start_date)]
        
        if end_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] <= pd.to_datetime(end_date)]
        
        logger.info(f"Filtered to {len(df_filtered)} rows")
        
        return df_filtered

