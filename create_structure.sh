#!/bin/bash

# Create main directories
mkdir -p config
mkdir -p src/{data,features,models,strategies,backtesting,execution,utils}
mkdir -p tests/{test_data,test_features,test_models,test_strategies,test_backtesting}
mkdir -p notebooks
mkdir -p scripts
mkdir -p data/{raw,processed,features,models}
mkdir -p results/{backtests,reports,trade_blotters,visualizations}
mkdir -p docs

# Create __init__.py files
touch src/__init__.py
touch src/data/__init__.py
touch src/features/__init__.py
touch src/models/__init__.py
touch src/strategies/__init__.py
touch src/backtesting/__init__.py
touch src/execution/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

echo "Project structure created successfully!"
tree -L 3 -I '__pycache__|*.pyc'
