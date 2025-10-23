# GitHub Actions Setup Instructions

**Last Updated:** October 23, 2025  
**Status:** Optional - CI/CD configuration guide

The GitHub Actions workflow files couldn't be pushed automatically due to permission restrictions. Follow these steps to add them manually:

## Option 1: Add via GitHub Web Interface

1. Go to your repository: https://github.com/ewswlw/manus-cad-ig-er-backtest
2. Click on "Actions" tab
3. Click "New workflow"
4. Click "set up a workflow yourself"
5. Copy the content from the workflow file below
6. Save and commit

## Option 2: Add via Git (Recommended)

```bash
# Clone the repository (if not already cloned)
git clone https://github.com/ewswlw/manus-cad-ig-er-backtest.git
cd manus-cad-ig-er-backtest

# Create .github/workflows directory
mkdir -p .github/workflows

# Create the workflow file
cat > .github/workflows/test.yml << 'EOF'
[CONTENT BELOW]
EOF

# Commit and push
git add .github/workflows/test.yml
git commit -m "Add GitHub Actions workflow for automated testing"
git push origin main
```

## Workflow File: `.github/workflows/test.yml`

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    - name: Type check with mypy
      run: |
        mypy src/ --ignore-missing-imports

    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=term

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black isort flake8

    - name: Check formatting with black
      run: |
        black --check src/ tests/

    - name: Check import sorting with isort
      run: |
        isort --check-only src/ tests/

    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --count --show-source --statistics
```

## Additional Workflow Files (Optional)

### Linting Only: `.github/workflows/lint.yml`

```yaml
name: Lint

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install black isort flake8 mypy
    - name: Run black
      run: black --check src/ tests/
    - name: Run isort
      run: isort --check-only src/ tests/
    - name: Run flake8
      run: flake8 src/ tests/
    - name: Run mypy
      run: mypy src/ --ignore-missing-imports
```

### Deploy to Staging: `.github/workflows/deploy_staging.yml`

```yaml
name: Deploy to Staging

on:
  push:
    branches: [ develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to staging
      run: |
        echo "Deploy to staging environment"
        # Add your deployment commands here
```

### Deploy to Production: `.github/workflows/deploy_prod.yml`

```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: |
        echo "Deploy to production environment"
        # Add your deployment commands here
```

## Why This Happened

GitHub Apps (like the one used by Manus) require explicit `workflows` permission to create or modify files in `.github/workflows/`. This is a security feature to prevent unauthorized workflow modifications.

## Next Steps

1. Add the workflow files manually using one of the options above
2. The workflows will automatically run on:
   - Every push to `main` or `develop` branches
   - Every pull request to `main` or `develop` branches
3. You can view workflow runs in the "Actions" tab of your repository

## Verification

After adding the workflows, verify they work by:
1. Making a small change to README.md
2. Committing and pushing
3. Checking the "Actions" tab to see the workflow run

---

**Note:** The workflows are configured but won't run until you have actual test files. You can disable them temporarily by adding `if: false` to the job definition.

