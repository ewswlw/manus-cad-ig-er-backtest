.PHONY: help install test lint format clean docs backtest

help:
	@echo "Available commands:"
	@echo "  make install     - Install package and dependencies"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black and isort"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make docs        - Build documentation"
	@echo "  make backtest    - Run full backtest"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	cd docs && make html

backtest:
	python scripts/run_backtest.py --config config/strategy_config.yaml

train:
	python scripts/train_models.py --config config/model_config.yaml

signals:
	python scripts/generate_signals.py --config config/strategy_config.yaml

