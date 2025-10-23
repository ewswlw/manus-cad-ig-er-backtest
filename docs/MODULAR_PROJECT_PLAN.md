# Modular Trading Strategy Project Plan

**Date:** October 22, 2025  
**Objective:** Transform research scripts into production-ready modular system  
**Target:** CAD-IG-ER trading strategy with weekly/monthly rebalancing

---

## Project Overview

### Current State
- ✅ Research scripts (15 files)
- ✅ Validated strategies (weekly: 3.91-4.16%, monthly: 3.13%)
- ✅ Complete analysis and documentation
- ❌ Not modular or production-ready
- ❌ No separation of concerns
- ❌ Difficult to test and extend

### Target State
- ✅ Modular Python package
- ✅ Separated data, features, models, backtesting, execution
- ✅ Configuration-driven
- ✅ Fully tested
- ✅ Easy to extend and maintain
- ✅ Production-ready with monitoring

---

## Architecture Design

### High-Level Structure

```
cad_ig_trading/
├── config/                    # Configuration files
│   ├── __init__.py
│   ├── data_config.yaml      # Data sources and paths
│   ├── feature_config.yaml   # Feature engineering specs
│   ├── model_config.yaml     # Model hyperparameters
│   ├── strategy_config.yaml  # Strategy parameters
│   └── backtest_config.yaml  # Backtesting settings
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/                 # Data management
│   │   ├── __init__.py
│   │   ├── loader.py         # Load raw data
│   │   ├── validator.py      # Data quality checks
│   │   ├── preprocessor.py   # Clean and prepare data
│   │   └── resampler.py      # Weekly/monthly resampling
│   │
│   ├── features/             # Feature engineering
│   │   ├── __init__.py
│   │   ├── base.py           # Base feature class
│   │   ├── momentum.py       # Momentum features
│   │   ├── spreads.py        # Spread features
│   │   ├── macro.py          # Macro features
│   │   ├── regime.py         # Regime detection
│   │   ├── statistical.py    # Statistical features
│   │   └── pipeline.py       # Feature pipeline
│   │
│   ├── models/               # ML models
│   │   ├── __init__.py
│   │   ├── base.py           # Base model interface
│   │   ├── lgbm.py           # LightGBM wrapper
│   │   ├── xgboost.py        # XGBoost wrapper
│   │   ├── random_forest.py  # Random Forest wrapper
│   │   ├── ensemble.py       # Ensemble combiner
│   │   └── trainer.py        # Training logic
│   │
│   ├── strategies/           # Trading strategies
│   │   ├── __init__.py
│   │   ├── base.py           # Base strategy class
│   │   ├── weekly.py         # Weekly rebalancing
│   │   ├── monthly.py        # Monthly rebalancing
│   │   └── signals.py        # Signal generation
│   │
│   ├── backtesting/          # Backtesting engine
│   │   ├── __init__.py
│   │   ├── engine.py         # Backtest runner
│   │   ├── metrics.py        # Performance metrics
│   │   ├── validation.py     # Bias testing
│   │   └── reporting.py      # Report generation
│   │
│   ├── execution/            # Live execution (future)
│   │   ├── __init__.py
│   │   ├── broker.py         # Broker interface
│   │   ├── order_manager.py  # Order management
│   │   └── risk_manager.py   # Risk controls
│   │
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── logger.py         # Logging setup
│       ├── config_loader.py  # Config management
│       ├── metrics.py        # Common metrics
│       └── visualization.py  # Plotting utilities
│
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── test_data/
│   ├── test_features/
│   ├── test_models/
│   ├── test_strategies/
│   └── test_backtesting/
│
├── notebooks/                # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_analysis.ipynb
│   ├── 03_model_development.ipynb
│   └── 04_strategy_backtest.ipynb
│
├── scripts/                  # Executable scripts
│   ├── train_models.py       # Train and save models
│   ├── run_backtest.py       # Run backtests
│   ├── generate_signals.py   # Generate trading signals
│   └── validate_strategy.py  # Run validation tests
│
├── data/                     # Data directory
│   ├── raw/                  # Raw input data
│   ├── processed/            # Processed data
│   ├── features/             # Feature datasets
│   └── models/               # Saved models
│
├── results/                  # Output directory
│   ├── backtests/            # Backtest results
│   ├── reports/              # Generated reports
│   ├── trade_blotters/       # Trade logs
│   └── visualizations/       # Charts and plots
│
├── docs/                     # Documentation
│   ├── architecture.md       # System architecture
│   ├── features.md           # Feature documentation
│   ├── models.md             # Model documentation
│   ├── strategies.md         # Strategy documentation
│   └── api.md                # API reference
│
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── README.md                 # Project overview
├── .gitignore               # Git ignore rules
└── Makefile                 # Common commands
```

---

## Module Specifications

### 1. Data Module (`src/data/`)

**Purpose:** Handle all data loading, validation, and preprocessing

#### `loader.py`
```python
class DataLoader:
    def load_csv(path: str) -> pd.DataFrame
    def load_multiple(paths: List[str]) -> pd.DataFrame
    def validate_schema(df: pd.DataFrame) -> bool
```

#### `validator.py`
```python
class DataValidator:
    def check_missing_values(df: pd.DataFrame) -> Dict
    def check_date_continuity(df: pd.DataFrame) -> bool
    def check_outliers(df: pd.DataFrame) -> Dict
    def generate_quality_report(df: pd.DataFrame) -> str
```

#### `preprocessor.py`
```python
class DataPreprocessor:
    def handle_missing_values(df: pd.DataFrame, method: str) -> pd.DataFrame
    def remove_outliers(df: pd.DataFrame, threshold: float) -> pd.DataFrame
    def normalize_dates(df: pd.DataFrame) -> pd.DataFrame
```

#### `resampler.py`
```python
class DataResampler:
    def resample_weekly(df: pd.DataFrame) -> pd.DataFrame
    def resample_monthly(df: pd.DataFrame) -> pd.DataFrame
    def calculate_returns(df: pd.DataFrame, freq: str) -> pd.DataFrame
```

---

### 2. Features Module (`src/features/`)

**Purpose:** Feature engineering with modular, composable features

#### `base.py`
```python
class BaseFeature(ABC):
    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.Series
    
    @property
    @abstractmethod
    def name(self) -> str
    
    @property
    def dependencies(self) -> List[str]
```

#### `momentum.py`
```python
class MomentumFeatures:
    def compute_momentum(df: pd.DataFrame, periods: List[int]) -> pd.DataFrame
    def compute_rsi(df: pd.DataFrame, period: int) -> pd.Series
    def compute_acceleration(df: pd.DataFrame, period: int) -> pd.Series
```

#### `spreads.py`
```python
class SpreadFeatures:
    def compute_oas_changes(df: pd.DataFrame, periods: List[int]) -> pd.DataFrame
    def compute_spread_ratios(df: pd.DataFrame) -> pd.DataFrame
    def compute_spread_zscore(df: pd.DataFrame, window: int) -> pd.DataFrame
```

#### `pipeline.py`
```python
class FeaturePipeline:
    def __init__(self, config: Dict)
    def add_feature(self, feature: BaseFeature)
    def compute_all(self, df: pd.DataFrame) -> pd.DataFrame
    def get_feature_names(self) -> List[str]
    def save_pipeline(self, path: str)
    def load_pipeline(self, path: str)
```

---

### 3. Models Module (`src/models/`)

**Purpose:** ML model wrappers with consistent interface

#### `base.py`
```python
class BaseModel(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series)
    
    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray
    
    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray
    
    def save(self, path: str)
    def load(self, path: str)
```

#### `ensemble.py`
```python
class EnsembleModel:
    def __init__(self, models: List[BaseModel], weights: List[float])
    def fit(self, X: pd.DataFrame, y: pd.Series)
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray
    def get_feature_importance(self) -> pd.DataFrame
```

#### `trainer.py`
```python
class ModelTrainer:
    def __init__(self, config: Dict)
    def train_single_model(self, model: BaseModel, X, y) -> BaseModel
    def train_ensemble(self, models: List[BaseModel], X, y) -> EnsembleModel
    def walk_forward_train(self, model: BaseModel, df: pd.DataFrame) -> List[BaseModel]
    def optimize_hyperparameters(self, model: BaseModel, X, y) -> Dict
```

---

### 4. Strategies Module (`src/strategies/`)

**Purpose:** Trading strategy logic

#### `base.py`
```python
class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.Series
    
    @property
    @abstractmethod
    def rebalance_frequency(self) -> str
    
    def calculate_positions(self, signals: pd.Series) -> pd.Series
```

#### `weekly.py`
```python
class WeeklyStrategy(BaseStrategy):
    def __init__(self, model: EnsembleModel, threshold: float)
    def generate_signals(self, df: pd.DataFrame) -> pd.Series
    def rebalance_frequency(self) -> str
```

#### `signals.py`
```python
class SignalGenerator:
    def __init__(self, strategy: BaseStrategy)
    def generate(self, df: pd.DataFrame) -> pd.DataFrame
    def apply_filters(self, signals: pd.Series, filters: List) -> pd.Series
    def validate_signals(self, signals: pd.Series) -> bool
```

---

### 5. Backtesting Module (`src/backtesting/`)

**Purpose:** Backtest strategies with comprehensive metrics

#### `engine.py`
```python
class BacktestEngine:
    def __init__(self, config: Dict)
    def run(self, strategy: BaseStrategy, data: pd.DataFrame) -> BacktestResult
    def run_walk_forward(self, strategy: BaseStrategy, data: pd.DataFrame) -> BacktestResult
```

#### `metrics.py`
```python
class PerformanceMetrics:
    @staticmethod
    def calculate_returns(returns: pd.Series) -> Dict
    @staticmethod
    def calculate_sharpe(returns: pd.Series) -> float
    @staticmethod
    def calculate_max_drawdown(returns: pd.Series) -> float
    @staticmethod
    def calculate_win_rate(returns: pd.Series) -> float
    @staticmethod
    def generate_report(returns: pd.Series) -> pd.DataFrame
```

#### `validation.py`
```python
class StrategyValidator:
    def test_lookahead_bias(self, strategy: BaseStrategy, data: pd.DataFrame) -> bool
    def test_overfitting(self, strategy: BaseStrategy, data: pd.DataFrame) -> Dict
    def test_out_of_time(self, strategy: BaseStrategy, data: pd.DataFrame) -> Dict
    def run_all_tests(self, strategy: BaseStrategy, data: pd.DataFrame) -> Dict
```

---

## Configuration System

### Example: `config/strategy_config.yaml`

```yaml
strategy:
  name: "weekly_ensemble"
  type: "weekly"
  rebalance_frequency: "W-FRI"
  
  models:
    - type: "lightgbm"
      weight: 0.30
      params:
        n_estimators: 200
        max_depth: 5
        learning_rate: 0.02
    
    - type: "xgboost"
      weight: 0.25
      params:
        n_estimators: 200
        max_depth: 6
        learning_rate: 0.02
    
    - type: "random_forest"
      weight: 0.25
      params:
        n_estimators: 300
        max_depth: 10
  
  signal_generation:
    threshold: 0.48
    threshold_type: "fixed"  # or "adaptive"
    min_probability: 0.30
    max_probability: 0.70
  
  risk_management:
    max_position_size: 1.0
    max_drawdown: 0.05
    stop_loss: null
    take_profit: null
  
  features:
    - momentum
    - spreads
    - macro
    - regime
    - statistical
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1)
- ✅ Set up project structure
- ✅ Implement data module
- ✅ Implement configuration system
- ✅ Set up logging and utilities
- ✅ Write unit tests for data module

### Phase 2: Feature Engineering (Week 2)
- ✅ Implement base feature class
- ✅ Port all feature calculations to modules
- ✅ Create feature pipeline
- ✅ Add feature validation
- ✅ Write unit tests for features

### Phase 3: Model System (Week 3)
- ✅ Implement base model interface
- ✅ Create model wrappers (LightGBM, XGBoost, RF)
- ✅ Implement ensemble system
- ✅ Create model trainer
- ✅ Write unit tests for models

### Phase 4: Strategy System (Week 4)
- ✅ Implement base strategy class
- ✅ Port weekly and monthly strategies
- ✅ Create signal generator
- ✅ Add strategy validation
- ✅ Write unit tests for strategies

### Phase 5: Backtesting Engine (Week 5)
- ✅ Implement backtest engine
- ✅ Create metrics calculator
- ✅ Add validation tests
- ✅ Create reporting system
- ✅ Write unit tests for backtesting

### Phase 6: Integration & Testing (Week 6)
- ✅ Integration tests
- ✅ End-to-end testing
- ✅ Performance optimization
- ✅ Documentation
- ✅ Example notebooks

### Phase 7: Production Features (Week 7-8)
- ✅ Live data integration
- ✅ Model retraining pipeline
- ✅ Monitoring and alerting
- ✅ API for signal generation
- ✅ Deployment scripts

---

## Key Design Principles

### 1. Separation of Concerns
- Each module has single responsibility
- Clear interfaces between modules
- No circular dependencies

### 2. Configuration-Driven
- All parameters in config files
- Easy to experiment with different settings
- No hardcoded values

### 3. Testability
- Unit tests for all modules
- Integration tests for workflows
- Mock data for testing

### 4. Extensibility
- Easy to add new features
- Easy to add new models
- Easy to add new strategies

### 5. Reproducibility
- Random seeds in config
- Versioned data and models
- Logged experiments

### 6. Production-Ready
- Error handling
- Logging
- Monitoring
- Documentation

---

## Usage Examples

### Example 1: Run Backtest

```python
from cad_ig_trading import DataLoader, FeaturePipeline, WeeklyStrategy, BacktestEngine
from cad_ig_trading.utils import load_config

# Load configuration
config = load_config('config/strategy_config.yaml')

# Load and prepare data
loader = DataLoader(config['data'])
data = loader.load_csv('data/raw/with_er_daily.csv')

# Generate features
pipeline = FeaturePipeline(config['features'])
features = pipeline.compute_all(data)

# Create strategy
strategy = WeeklyStrategy(config['strategy'])

# Run backtest
engine = BacktestEngine(config['backtest'])
results = engine.run(strategy, features)

# Print results
print(results.summary())
results.plot()
```

### Example 2: Generate Live Signals

```python
from cad_ig_trading import DataLoader, FeaturePipeline, WeeklyStrategy
from cad_ig_trading.utils import load_config

# Load configuration
config = load_config('config/strategy_config.yaml')

# Load latest data
loader = DataLoader(config['data'])
data = loader.load_latest()

# Generate features
pipeline = FeaturePipeline.load('data/models/feature_pipeline.pkl')
features = pipeline.compute_all(data)

# Load trained strategy
strategy = WeeklyStrategy.load('data/models/weekly_strategy.pkl')

# Generate signal
signal = strategy.generate_signals(features)

print(f"Current signal: {'LONG' if signal[-1] == 1 else 'CASH'}")
print(f"Probability: {strategy.get_probability(features)[-1]:.2%}")
```

### Example 3: Train New Model

```python
from cad_ig_trading import DataLoader, FeaturePipeline, ModelTrainer
from cad_ig_trading.models import LightGBMModel, XGBoostModel, EnsembleModel
from cad_ig_trading.utils import load_config

# Load configuration
config = load_config('config/model_config.yaml')

# Prepare data
loader = DataLoader(config['data'])
data = loader.load_csv('data/raw/with_er_daily.csv')

pipeline = FeaturePipeline(config['features'])
features = pipeline.compute_all(data)

# Create models
lgbm = LightGBMModel(config['models']['lightgbm'])
xgb = XGBoostModel(config['models']['xgboost'])

# Train ensemble
trainer = ModelTrainer(config['training'])
ensemble = trainer.train_ensemble([lgbm, xgb], features, target)

# Save model
ensemble.save('data/models/ensemble_v2.pkl')

# Evaluate
metrics = trainer.evaluate(ensemble, features_test, target_test)
print(metrics)
```

---

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock external dependencies
- Cover edge cases

### Integration Tests
- Test module interactions
- Test full workflows
- Use sample data

### Validation Tests
- Lookahead bias
- Overfitting
- Out-of-time consistency
- Parameter sensitivity

### Performance Tests
- Execution speed
- Memory usage
- Scalability

---

## Documentation Requirements

### Code Documentation
- Docstrings for all classes and methods
- Type hints for all functions
- Inline comments for complex logic

### User Documentation
- README with quick start
- Architecture overview
- API reference
- Usage examples
- Configuration guide

### Developer Documentation
- Contributing guidelines
- Code style guide
- Testing guide
- Deployment guide

---

## Deployment Considerations

### Development Environment
- Local development with sample data
- Jupyter notebooks for exploration
- Unit tests run on commit

### Staging Environment
- Full historical data
- Automated backtesting
- Performance monitoring

### Production Environment
- Live data feeds
- Real-time signal generation
- Monitoring and alerting
- Automated retraining

---

## Success Metrics

### Code Quality
- ✅ 80%+ test coverage
- ✅ No circular dependencies
- ✅ All modules documented
- ✅ Passes linting (flake8, black)

### Performance
- ✅ Feature generation < 1 second
- ✅ Signal generation < 100ms
- ✅ Backtest full history < 10 seconds

### Usability
- ✅ Can run backtest with 5 lines of code
- ✅ Can add new feature in < 50 lines
- ✅ Can switch strategies via config

---

## Next Steps

1. **Review and approve architecture**
2. **Set up project structure**
3. **Begin Phase 1 implementation**
4. **Establish CI/CD pipeline**
5. **Create development roadmap**

---

**Document Version:** 1.0  
**Date:** October 22, 2025  
**Status:** Planning Phase  
**Next Review:** After Phase 1 completion

