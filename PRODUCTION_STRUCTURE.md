# Production Folder Structure

**Date:** October 22, 2025  
**Version:** 2.0 - Production Ready  
**Total Directories:** 123

---

## Overview

This document describes the production-ready folder structure for the CAD-IG Trading Strategy system. The structure follows enterprise best practices for modular, scalable, and maintainable Python applications.

---

## Root Structure

```
cad_ig_trading/
├── src/                    # Source code (main package)
├── config/                 # Configuration files
├── tests/                  # Test suite
├── deploy/                 # Deployment configurations
├── api/                    # REST API (future)
├── tools/                  # Utility tools
├── examples/               # Usage examples
├── docs/                   # Documentation
├── data/                   # Data storage
├── models/                 # Model registry
├── results/                # Output results
├── logs/                   # Application logs
├── monitoring/             # Monitoring configs
├── cache/                  # Cached data
├── db/                     # Database migrations
└── .github/                # CI/CD workflows
```

---

## Detailed Structure

### 1. Source Code (`src/`)

Main application code organized as a proper Python package.

```
src/
└── cad_ig_trading/                    # Main package
    ├── __init__.py
    ├── data/                          # Data management
    │   ├── __init__.py
    │   ├── loader.py                  # Data loading
    │   ├── validator.py               # Data validation
    │   ├── preprocessor.py            # Data preprocessing
    │   └── resampler.py               # Time resampling
    │
    ├── features/                      # Feature engineering
    │   ├── __init__.py
    │   ├── base.py                    # Base feature class
    │   ├── pipeline.py                # Feature pipeline
    │   ├── momentum/                  # Momentum features
    │   │   ├── __init__.py
    │   │   ├── returns.py
    │   │   ├── rsi.py
    │   │   └── acceleration.py
    │   ├── spreads/                   # Spread features
    │   │   ├── __init__.py
    │   │   ├── oas.py
    │   │   ├── ratios.py
    │   │   └── zscore.py
    │   ├── macro/                     # Macro features
    │   │   ├── __init__.py
    │   │   ├── surprises.py
    │   │   └── indicators.py
    │   ├── regime/                    # Regime detection
    │   │   ├── __init__.py
    │   │   ├── volatility.py
    │   │   └── economic.py
    │   └── statistical/               # Statistical features
    │       ├── __init__.py
    │       ├── rolling.py
    │       └── distributions.py
    │
    ├── models/                        # ML models
    │   ├── __init__.py
    │   ├── base.py                    # Base model interface
    │   ├── trainer.py                 # Training logic
    │   ├── lgbm/                      # LightGBM
    │   │   ├── __init__.py
    │   │   └── model.py
    │   ├── xgboost/                   # XGBoost
    │   │   ├── __init__.py
    │   │   └── model.py
    │   ├── rf/                        # Random Forest
    │   │   ├── __init__.py
    │   │   └── model.py
    │   └── ensemble/                  # Ensemble
    │       ├── __init__.py
    │       ├── weighted.py
    │       └── stacking.py
    │
    ├── strategies/                    # Trading strategies
    │   ├── __init__.py
    │   ├── base.py                    # Base strategy
    │   ├── signals.py                 # Signal generation
    │   ├── weekly/                    # Weekly strategy
    │   │   ├── __init__.py
    │   │   └── strategy.py
    │   ├── monthly/                   # Monthly strategy
    │   │   ├── __init__.py
    │   │   └── strategy.py
    │   └── common/                    # Shared utilities
    │       ├── __init__.py
    │       ├── filters.py
    │       └── thresholds.py
    │
    ├── backtesting/                   # Backtesting engine
    │   ├── __init__.py
    │   ├── engine.py                  # Backtest runner
    │   ├── metrics.py                 # Performance metrics
    │   ├── validation.py              # Bias testing
    │   └── reporting.py               # Report generation
    │
    ├── execution/                     # Live execution
    │   ├── __init__.py
    │   ├── broker.py                  # Broker interface
    │   ├── order_manager.py           # Order management
    │   └── risk_manager.py            # Risk controls
    │
    └── utils/                         # Utilities
        ├── __init__.py
        ├── config_loader.py           # Config management
        ├── logger.py                  # Logging setup
        ├── metrics.py                 # Common metrics
        └── visualization.py           # Plotting
```

**Key Points:**
- Proper Python package with `__init__.py` files
- Subdirectories for feature types, models, strategies
- Clear separation of concerns
- Easy to navigate and extend

---

### 2. Configuration (`config/`)

Environment-specific and component-specific configurations.

```
config/
├── strategy_config.yaml               # Main strategy config
├── environments/                      # Environment-specific
│   ├── dev/
│   │   ├── config.yaml               # Dev settings
│   │   └── secrets.yaml              # Dev secrets (gitignored)
│   ├── staging/
│   │   ├── config.yaml               # Staging settings
│   │   └── secrets.yaml              # Staging secrets
│   └── prod/
│       ├── config.yaml               # Production settings
│       └── secrets.yaml              # Prod secrets (gitignored)
├── models/                           # Model configurations
│   ├── lightgbm.yaml
│   ├── xgboost.yaml
│   └── ensemble.yaml
├── features/                         # Feature configurations
│   ├── momentum.yaml
│   ├── spreads.yaml
│   └── macro.yaml
└── data/                             # Data configurations
    ├── sources.yaml
    └── validation.yaml
```

**Key Points:**
- Separate configs for dev/staging/prod
- Component-specific configs
- Secrets managed separately (not in git)

---

### 3. Tests (`tests/`)

Comprehensive test suite with unit, integration, and E2E tests.

```
tests/
├── __init__.py
├── conftest.py                       # Pytest configuration
├── fixtures/                         # Test fixtures
│   ├── sample_data.csv
│   ├── mock_models.pkl
│   └── test_configs.yaml
├── unit/                             # Unit tests
│   ├── data/
│   │   ├── test_loader.py
│   │   ├── test_validator.py
│   │   └── test_preprocessor.py
│   ├── features/
│   │   ├── test_momentum.py
│   │   ├── test_spreads.py
│   │   └── test_pipeline.py
│   ├── models/
│   │   ├── test_lgbm.py
│   │   ├── test_ensemble.py
│   │   └── test_trainer.py
│   ├── strategies/
│   │   ├── test_weekly.py
│   │   └── test_signals.py
│   └── backtesting/
│       ├── test_engine.py
│       └── test_metrics.py
├── integration/                      # Integration tests
│   ├── pipelines/
│   │   ├── test_feature_pipeline.py
│   │   └── test_training_pipeline.py
│   └── workflows/
│       ├── test_backtest_workflow.py
│       └── test_signal_workflow.py
└── e2e/                              # End-to-end tests
    ├── test_full_backtest.py
    └── test_live_signal.py
```

**Key Points:**
- Separated unit, integration, E2E tests
- Fixtures for reusable test data
- Comprehensive coverage

---

### 4. Deployment (`deploy/`)

Deployment configurations for different environments.

```
deploy/
├── docker/                           # Docker configs
│   ├── dev/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── prod/
│       ├── Dockerfile
│       ├── docker-compose.yml
│       └── .dockerignore
├── kubernetes/                       # K8s manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secrets.yaml
└── scripts/                          # Deployment scripts
    ├── deploy_dev.sh
    ├── deploy_staging.sh
    └── deploy_prod.sh
```

**Key Points:**
- Docker for containerization
- Kubernetes for orchestration
- Environment-specific deployments

---

### 5. API (`api/`)

REST API for signal generation and monitoring (future).

```
api/
├── __init__.py
├── main.py                           # FastAPI app
├── routes/                           # API endpoints
│   ├── __init__.py
│   ├── signals.py                    # Signal endpoints
│   ├── backtest.py                   # Backtest endpoints
│   └── health.py                     # Health checks
├── schemas/                          # Pydantic schemas
│   ├── __init__.py
│   ├── signal.py
│   └── backtest.py
└── middleware/                       # API middleware
    ├── __init__.py
    ├── auth.py
    └── logging.py
```

**Key Points:**
- FastAPI for REST API
- Pydantic for validation
- Authentication and logging middleware

---

### 6. Tools (`tools/`)

Utility scripts for common tasks.

```
tools/
├── data_processing/                  # Data tools
│   ├── download_data.py
│   ├── clean_data.py
│   └── validate_data.py
├── model_training/                   # Training tools
│   ├── train_weekly.py
│   ├── train_monthly.py
│   └── optimize_hyperparams.py
└── signal_generation/                # Signal tools
    ├── generate_signals.py
    └── backtest_signals.py
```

**Key Points:**
- Standalone utility scripts
- Common operational tasks
- Easy to run from command line

---

### 7. Examples (`examples/`)

Usage examples and tutorials.

```
examples/
├── notebooks/                        # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_strategy_backtest.ipynb
└── scripts/                          # Example scripts
    ├── simple_backtest.py
    ├── generate_report.py
    └── live_signals.py
```

**Key Points:**
- Interactive notebooks for exploration
- Example scripts for common use cases
- Educational and onboarding

---

### 8. Documentation (`docs/`)

Comprehensive documentation.

```
docs/
├── MODULAR_PROJECT_PLAN.md           # Architecture
├── VALIDATION_REPORT.md              # Validation results
├── WEEKLY_VS_MONTHLY_COMPARISON.md   # Strategy comparison
├── api/                              # API docs
│   ├── endpoints.md
│   └── schemas.md
├── user_guide/                       # User documentation
│   ├── installation.md
│   ├── quickstart.md
│   └── configuration.md
├── developer_guide/                  # Developer docs
│   ├── contributing.md
│   ├── testing.md
│   └── deployment.md
├── architecture/                     # Architecture docs
│   ├── overview.md
│   ├── data_flow.md
│   └── design_patterns.md
└── images/                           # Documentation images
    ├── architecture.png
    └── workflow.png
```

**Key Points:**
- Separate user and developer docs
- Architecture documentation
- Visual diagrams

---

### 9. Data (`data/`)

Data storage with versioning.

```
data/
├── raw/                              # Raw input data
│   ├── with_er_daily.csv
│   └── .gitkeep
├── processed/                        # Processed data
│   ├── data_with_all_features.csv
│   └── .gitkeep
├── features/                         # Feature datasets
│   └── .gitkeep
├── models/                           # Saved models (deprecated, use models/)
│   └── .gitkeep
└── versions/                         # Data versioning
    ├── v1.0/
    ├── v1.1/
    └── .gitkeep
```

**Key Points:**
- Separate raw and processed data
- Data versioning for reproducibility
- .gitkeep to track empty directories

---

### 10. Models (`models/`)

Model registry and experiments.

```
models/
├── registry/                         # Production models
│   ├── weekly/
│   │   ├── v1.0/
│   │   │   ├── model.pkl
│   │   │   ├── metadata.json
│   │   │   └── performance.json
│   │   └── v1.1/
│   └── monthly/
│       └── v1.0/
└── experiments/                      # Experimental models
    ├── exp_001/
    ├── exp_002/
    └── .gitkeep
```

**Key Points:**
- Versioned production models
- Separate experiments directory
- Metadata and performance tracking

---

### 11. Results (`results/`)

Output results organized by type and frequency.

```
results/
├── backtests/                        # Backtest results
│   ├── daily/
│   ├── weekly/
│   └── monthly/
├── live_trading/                     # Live trading results
│   ├── daily/
│   ├── weekly/
│   └── monthly/
├── analysis/                         # Analysis reports
│   ├── daily/
│   ├── weekly/
│   └── monthly/
├── reports/                          # Generated reports
│   ├── daily/
│   ├── weekly/
│   └── monthly/
├── trade_blotters/                   # Trade logs
│   └── .gitkeep
└── visualizations/                   # Charts and plots
    └── .gitkeep
```

**Key Points:**
- Organized by result type
- Frequency-based subdirectories
- Separate live and backtest results

---

### 12. Logs (`logs/`)

Application logs organized by component.

```
logs/
├── app/                              # Application logs
│   ├── app.log
│   └── error.log
├── backtest/                         # Backtest logs
│   └── backtest.log
└── execution/                        # Execution logs
    └── execution.log
```

**Key Points:**
- Separate logs by component
- Rotation and archiving
- Error logs separate

---

### 13. Monitoring (`monitoring/`)

Monitoring and alerting configurations.

```
monitoring/
├── dashboards/                       # Dashboard configs
│   ├── grafana/
│   │   └── strategy_dashboard.json
│   └── prometheus/
│       └── alerts.yml
└── alerts/                           # Alert rules
    ├── performance_alerts.yaml
    └── system_alerts.yaml
```

**Key Points:**
- Grafana dashboards
- Prometheus alerts
- Performance monitoring

---

### 14. Cache (`cache/`)

Cached data for performance.

```
cache/
├── features/                         # Cached features
│   └── .gitkeep
└── models/                           # Cached model predictions
    └── .gitkeep
```

**Key Points:**
- Speed up repeated computations
- Gitignored (not in version control)
- Automatic cleanup

---

### 15. Database (`db/`)

Database migrations (for future use).

```
db/
└── migrations/                       # DB migrations
    ├── 001_initial_schema.sql
    └── .gitkeep
```

**Key Points:**
- Version-controlled migrations
- Future: store signals, results in DB

---

### 16. CI/CD (`.github/`)

GitHub Actions workflows.

```
.github/
└── workflows/
    ├── test.yml                      # Run tests on PR
    ├── lint.yml                      # Linting checks
    ├── deploy_staging.yml            # Deploy to staging
    └── deploy_prod.yml               # Deploy to production
```

**Key Points:**
- Automated testing
- Automated deployment
- Code quality checks

---

## Environment Variables

Create `.env` files for each environment (gitignored):

```bash
# .env.dev
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DATA_PATH=/path/to/data
MODEL_PATH=/path/to/models

# .env.prod
ENVIRONMENT=production
LOG_LEVEL=INFO
DATA_PATH=/prod/data
MODEL_PATH=/prod/models
```

---

## Package Installation

The package can be installed in development or production mode:

```bash
# Development installation (editable)
pip install -e ".[dev]"

# Production installation
pip install .

# With specific extras
pip install ".[api,monitoring]"
```

---

## Key Improvements Over Initial Structure

### 1. **Environment Separation**
- Dev/Staging/Prod configs
- Environment-specific secrets
- Easy environment switching

### 2. **Modular Package Structure**
- Proper Python package (`src/cad_ig_trading/`)
- Subdirectories for feature types
- Clear module boundaries

### 3. **Comprehensive Testing**
- Unit, integration, E2E tests
- Test fixtures
- High coverage achievable

### 4. **Production Features**
- Docker and Kubernetes support
- Monitoring and alerting
- API for signal generation
- CI/CD pipelines

### 5. **Better Organization**
- Model registry with versioning
- Results organized by type/frequency
- Separate logs by component
- Caching for performance

### 6. **Scalability**
- Easy to add new features/models
- Supports multiple strategies
- Handles multiple environments
- Ready for team collaboration

---

## Migration from Research Code

To migrate research code to this structure:

1. **Move feature code** → `src/cad_ig_trading/features/`
2. **Move model code** → `src/cad_ig_trading/models/`
3. **Move strategy code** → `src/cad_ig_trading/strategies/`
4. **Create tests** → `tests/unit/` and `tests/integration/`
5. **Update configs** → `config/environments/`
6. **Add documentation** → `docs/`

---

## Next Steps

1. **Implement core modules** (Phase 1-6 from roadmap)
2. **Write unit tests** for each module
3. **Create Docker images** for deployment
4. **Set up CI/CD** pipelines
5. **Add monitoring** dashboards
6. **Deploy to staging** for testing
7. **Deploy to production** when validated

---

**Document Version:** 2.0  
**Last Updated:** October 22, 2025  
**Total Directories:** 123  
**Status:** Production-Ready Structure

