"""
Backtesting Engine

Runs backtest and calculates performance metrics.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class BacktestEngine:
    """Backtest engine for strategy evaluation."""
    
    def __init__(self):
        """Initialize backtest engine."""
        self.results = None
        
    def run_backtest(self, df, signal_col='signal', resample_freq='W-FRI'):
        """
        Run backtest on daily data with weekly resampling.
        
        Args:
            df: DataFrame with Date, cad_ig_er_index, and signal columns
            signal_col: Name of signal column
            resample_freq: Resampling frequency (W-FRI for weekly Friday)
            
        Returns:
            Dictionary with backtest results
        """
        logger.info("Running backtest...")
        
        # Resample to weekly
        df_weekly = df.set_index('Date').resample(resample_freq).last()
        df_weekly['weekly_return'] = df_weekly['cad_ig_er_index'].pct_change()
        
        # Use previous week's signal (avoid look-ahead bias)
        df_weekly['signal_shifted'] = df_weekly[signal_col].shift(1)
        
        # Calculate strategy returns
        df_weekly['strategy_return'] = df_weekly['weekly_return'] * df_weekly['signal_shifted']
        
        # Calculate cumulative returns
        df_weekly['cum_return_strategy'] = (1 + df_weekly['strategy_return']).cumprod() - 1
        df_weekly['cum_return_buyhold'] = (1 + df_weekly['weekly_return']).cumprod() - 1
        
        # Drop NaN rows
        df_weekly = df_weekly.dropna()
        
        # Calculate metrics
        results = self._calculate_metrics(df_weekly)
        
        # Store results
        self.results = results
        self.df_weekly = df_weekly
        
        return results
    
    def _calculate_metrics(self, df_weekly):
        """Calculate performance metrics."""
        
        # Basic returns
        total_return_strategy = df_weekly['cum_return_strategy'].iloc[-1]
        total_return_buyhold = df_weekly['cum_return_buyhold'].iloc[-1]
        
        weeks = len(df_weekly)
        years = weeks / 52
        
        ann_return_strategy = (1 + total_return_strategy) ** (1/years) - 1
        ann_return_buyhold = (1 + total_return_buyhold) ** (1/years) - 1
        
        # Volatility
        vol_strategy = df_weekly['strategy_return'].std() * np.sqrt(52)
        vol_buyhold = df_weekly['weekly_return'].std() * np.sqrt(52)
        
        # Sharpe ratio (assuming 0% risk-free rate)
        sharpe_strategy = ann_return_strategy / vol_strategy if vol_strategy > 0 else 0
        sharpe_buyhold = ann_return_buyhold / vol_buyhold if vol_buyhold > 0 else 0
        
        # Sortino ratio (downside deviation)
        downside_returns_strategy = df_weekly['strategy_return'][df_weekly['strategy_return'] < 0]
        downside_std_strategy = downside_returns_strategy.std() * np.sqrt(52)
        sortino_strategy = ann_return_strategy / downside_std_strategy if downside_std_strategy > 0 else 0
        
        downside_returns_buyhold = df_weekly['weekly_return'][df_weekly['weekly_return'] < 0]
        downside_std_buyhold = downside_returns_buyhold.std() * np.sqrt(52)
        sortino_buyhold = ann_return_buyhold / downside_std_buyhold if downside_std_buyhold > 0 else 0
        
        # Maximum drawdown
        cummax_strategy = (1 + df_weekly['cum_return_strategy']).cummax()
        drawdown_strategy = ((1 + df_weekly['cum_return_strategy']) - cummax_strategy) / cummax_strategy
        max_dd_strategy = drawdown_strategy.min()
        
        cummax_buyhold = (1 + df_weekly['cum_return_buyhold']).cummax()
        drawdown_buyhold = ((1 + df_weekly['cum_return_buyhold']) - cummax_buyhold) / cummax_buyhold
        max_dd_buyhold = drawdown_buyhold.min()
        
        # Win rate
        positive_weeks_strategy = (df_weekly['strategy_return'] > 0).sum()
        total_weeks_long = (df_weekly['signal_shifted'] == 1).sum()
        win_rate_strategy = positive_weeks_strategy / total_weeks_long if total_weeks_long > 0 else 0
        
        positive_weeks_buyhold = (df_weekly['weekly_return'] > 0).sum()
        win_rate_buyhold = positive_weeks_buyhold / len(df_weekly)
        
        # Exposure
        exposure = (df_weekly['signal_shifted'] == 1).sum() / len(df_weekly)
        
        results = {
            'strategy': {
                'total_return': total_return_strategy,
                'annualized_return': ann_return_strategy,
                'volatility': vol_strategy,
                'sharpe_ratio': sharpe_strategy,
                'sortino_ratio': sortino_strategy,
                'max_drawdown': max_dd_strategy,
                'win_rate': win_rate_strategy,
                'exposure': exposure,
                'weeks': weeks,
                'years': years
            },
            'buyhold': {
                'total_return': total_return_buyhold,
                'annualized_return': ann_return_buyhold,
                'volatility': vol_buyhold,
                'sharpe_ratio': sharpe_buyhold,
                'sortino_ratio': sortino_buyhold,
                'max_drawdown': max_dd_buyhold,
                'win_rate': win_rate_buyhold
            }
        }
        
        return results
    
    def print_results(self):
        """Print backtest results."""
        if self.results is None:
            logger.warning("No results to print. Run backtest first.")
            return
        
        print("\n" + "="*80)
        print("BACKTEST RESULTS")
        print("="*80)
        
        s = self.results['strategy']
        b = self.results['buyhold']
        
        print(f"\nTime Period: {s['years']:.2f} years ({s['weeks']} weeks)")
        
        print("\n" + "-"*80)
        print(f"{'Metric':<30} {'Strategy':>15} {'Buy & Hold':>15} {'Difference':>15}")
        print("-"*80)
        
        print(f"{'Total Return':<30} {s['total_return']:>14.2%} {b['total_return']:>14.2%} {s['total_return']-b['total_return']:>14.2%}")
        print(f"{'Annualized Return':<30} {s['annualized_return']:>14.2%} {b['annualized_return']:>14.2%} {s['annualized_return']-b['annualized_return']:>14.2%}")
        print(f"{'Volatility':<30} {s['volatility']:>14.2%} {b['volatility']:>14.2%} {s['volatility']-b['volatility']:>14.2%}")
        print(f"{'Sharpe Ratio':<30} {s['sharpe_ratio']:>14.2f} {b['sharpe_ratio']:>14.2f} {s['sharpe_ratio']-b['sharpe_ratio']:>14.2f}")
        print(f"{'Sortino Ratio':<30} {s['sortino_ratio']:>14.2f} {b['sortino_ratio']:>14.2f} {s['sortino_ratio']-b['sortino_ratio']:>14.2f}")
        print(f"{'Max Drawdown':<30} {s['max_drawdown']:>14.2%} {b['max_drawdown']:>14.2%} {s['max_drawdown']-b['max_drawdown']:>14.2%}")
        print(f"{'Win Rate':<30} {s['win_rate']:>14.2%} {b['win_rate']:>14.2%} {s['win_rate']-b['win_rate']:>14.2%}")
        print(f"{'Exposure':<30} {s['exposure']:>14.2%} {'100.00%':>15} {''}")
        
        print("-"*80)
        
        # Check if target achieved
        if s['annualized_return'] >= 0.04:
            print(f"\n✅ TARGET ACHIEVED: {s['annualized_return']:.2%} annualized return (>4.00%)")
        else:
            print(f"\n❌ Target not achieved: {s['annualized_return']:.2%} annualized return (<4.00%)")
        
        print("="*80)
    
    def get_trade_blotter(self):
        """Generate trade blotter."""
        if not hasattr(self, 'df_weekly'):
            logger.warning("No weekly data. Run backtest first.")
            return None
        
        df = self.df_weekly.reset_index()
        
        # Find position changes
        df['position_change'] = df['signal_shifted'].diff()
        
        trades = []
        entry_date = None
        entry_price = None
        
        for idx, row in df.iterrows():
            # Entry (0 -> 1)
            if row['position_change'] == 1:
                entry_date = row['Date']
                entry_price = row['cad_ig_er_index']
            
            # Exit (1 -> 0)
            elif row['position_change'] == -1 and entry_date is not None:
                exit_date = row['Date']
                exit_price = row['cad_ig_er_index']
                
                trade_return = (exit_price - entry_price) / entry_price
                holding_weeks = (exit_date - entry_date).days / 7
                
                trades.append({
                    'Entry_Date': entry_date,
                    'Entry_Price': entry_price,
                    'Exit_Date': exit_date,
                    'Exit_Price': exit_price,
                    'Return': trade_return,
                    'Holding_Weeks': holding_weeks
                })
                
                entry_date = None
                entry_price = None
        
        # Handle open position
        if entry_date is not None:
            exit_date = df.iloc[-1]['Date']
            exit_price = df.iloc[-1]['cad_ig_er_index']
            trade_return = (exit_price - entry_price) / entry_price
            holding_weeks = (exit_date - entry_date).days / 7
            
            trades.append({
                'Entry_Date': entry_date,
                'Entry_Price': entry_price,
                'Exit_Date': exit_date,
                'Exit_Price': exit_price,
                'Return': trade_return,
                'Holding_Weeks': holding_weeks
            })
        
        trade_blotter = pd.DataFrame(trades)
        
        if len(trade_blotter) > 0:
            trade_blotter['Trade_ID'] = range(1, len(trade_blotter) + 1)
            trade_blotter = trade_blotter[['Trade_ID', 'Entry_Date', 'Entry_Price', 'Exit_Date', 'Exit_Price', 'Return', 'Holding_Weeks']]
        
        return trade_blotter

