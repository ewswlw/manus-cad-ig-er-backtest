#!/bin/bash

echo "Creating production-ready folder structure..."

# Create environment-specific configs
mkdir -p config/environments/{dev,staging,prod}

# Create additional config directories
mkdir -p config/models
mkdir -p config/features
mkdir -p config/data

# Expand src structure with implementation files
mkdir -p src/cad_ig_trading/{data,features,models,strategies,backtesting,execution,utils}
touch src/cad_ig_trading/__init__.py

# Create specific feature subdirectories
mkdir -p src/cad_ig_trading/features/{momentum,spreads,macro,regime,statistical}

# Create model subdirectories
mkdir -p src/cad_ig_trading/models/{lgbm,xgboost,rf,ensemble}

# Create strategy subdirectories
mkdir -p src/cad_ig_trading/strategies/{weekly,monthly,common}

# Expand tests structure
mkdir -p tests/{unit,integration,e2e}
mkdir -p tests/unit/{data,features,models,strategies,backtesting}
mkdir -p tests/integration/{pipelines,workflows}
mkdir -p tests/fixtures

# Create deployment directories
mkdir -p deploy/{docker,kubernetes,scripts}
mkdir -p deploy/docker/{dev,prod}

# Create monitoring and logging
mkdir -p monitoring/{dashboards,alerts}
mkdir -p logs/{app,backtest,execution}

# Create API directory (for future REST API)
mkdir -p api/{routes,schemas,middleware}

# Create database migrations (for future)
mkdir -p db/migrations

# Create examples directory
mkdir -p examples/{notebooks,scripts}

# Create tools directory
mkdir -p tools/{data_processing,model_training,signal_generation}

# Create CI/CD
mkdir -p .github/workflows

# Create documentation structure
mkdir -p docs/{api,user_guide,developer_guide,architecture}
mkdir -p docs/images

# Create data versioning
mkdir -p data/versions

# Create model registry
mkdir -p models/registry/{weekly,monthly}
mkdir -p models/experiments

# Create results with more structure
mkdir -p results/{backtests,live_trading,analysis,reports}/{daily,weekly,monthly}

# Create cache directory
mkdir -p cache/{features,models}

# Create __init__.py files for proper package structure
touch src/cad_ig_trading/data/__init__.py
touch src/cad_ig_trading/features/__init__.py
touch src/cad_ig_trading/features/momentum/__init__.py
touch src/cad_ig_trading/features/spreads/__init__.py
touch src/cad_ig_trading/features/macro/__init__.py
touch src/cad_ig_trading/features/regime/__init__.py
touch src/cad_ig_trading/features/statistical/__init__.py
touch src/cad_ig_trading/models/__init__.py
touch src/cad_ig_trading/models/lgbm/__init__.py
touch src/cad_ig_trading/models/xgboost/__init__.py
touch src/cad_ig_trading/models/rf/__init__.py
touch src/cad_ig_trading/models/ensemble/__init__.py
touch src/cad_ig_trading/strategies/__init__.py
touch src/cad_ig_trading/strategies/weekly/__init__.py
touch src/cad_ig_trading/strategies/monthly/__init__.py
touch src/cad_ig_trading/strategies/common/__init__.py
touch src/cad_ig_trading/backtesting/__init__.py
touch src/cad_ig_trading/execution/__init__.py
touch src/cad_ig_trading/utils/__init__.py

# Create .gitkeep for empty directories
find . -type d -empty -exec touch {}/.gitkeep \;

echo "Production folder structure created!"
echo ""
echo "Directory count:"
find . -type d | wc -l
echo ""
echo "Structure overview:"
tree -L 3 -d -I '__pycache__|*.pyc|.git' | head -100

