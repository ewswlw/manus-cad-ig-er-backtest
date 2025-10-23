"""
Setup script for CAD-IG Trading Strategy package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cad-ig-trading",
    version="1.0.0",
    author="Trading Strategy Team",
    author_email="trading@example.com",
    description="Modular trading strategy system for CAD-IG-ER index",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cad-ig-trading",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scikit-learn>=1.2.0",
        "lightgbm>=3.3.0",
        "xgboost>=1.7.0",
        "matplotlib>=3.6.0",
        "seaborn>=0.12.0",
        "pyyaml>=6.0",
        "joblib>=1.2.0",
        "scipy>=1.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "jupyter>=1.0.0",
            "ipython>=8.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cad-ig-train=scripts.train_models:main",
            "cad-ig-backtest=scripts.run_backtest:main",
            "cad-ig-signals=scripts.generate_signals:main",
        ],
    },
)

