# Test Suite Documentation

## Overview

Comprehensive test suite for the sentiment analysis module in `src/analysis`.

## Test Files

### 1. `test_sentiment_analyzer.py`
Tests for the `TrainedSentimentAnalyzer` class.

**Test Classes:**
- `TestTrainedSentimentAnalyzer` - Core functionality tests
- `TestSentimentAnalyzerEdgeCases` - Edge cases and error handling
- `TestSentimentAnalyzerPerformance` - Performance tests

**Coverage:**
- ✅ Analyzer initialization
- ✅ Sentiment detection (positive, negative, neutral)
- ✅ Score ranges (confidence, intensity, compound)
- ✅ Edge cases (empty strings, special characters, unicode)
- ✅ Consistency and batch processing
- ✅ Performance benchmarks

### 2. `test_model_trainer.py`
Tests for the `SentimentModelTrainer` class.

**Test Classes:**
- `TestSentimentModelTrainer` - Core training functionality
- `TestModelTrainerIntegration` - Integration tests
- `TestModelTrainerWithRealData` - Tests with actual dataset

**Coverage:**
- ✅ Trainer initialization
- ✅ Data loading from CSV
- ✅ Label preprocessing and mapping
- ✅ Model training (Logistic Regression, Naive Bayes)
- ✅ Model saving and loading
- ✅ Prediction functionality
- ✅ Feature importance
- ✅ Full training pipeline

### 3. `test_analysis_integration.py`
Integration tests for the complete analysis pipeline.

**Test Classes:**
- `TestAnalysisServiceIntegration` - AnalysisService tests
- `TestCSVIngestionWithAnalysis` - CSV ingestion integration
- `TestSentimentAnalyzerWithIngestion` - Analyzer with ingested data
- `TestEndToEndWorkflow` - Complete workflow tests
- `TestErrorHandling` - Error handling scenarios

**Coverage:**
- ✅ AnalysisService with all components
- ✅ CSV data ingestion and analysis
- ✅ End-to-end pipeline
- ✅ Batch processing
- ✅ Error handling

## Running Tests

### Option 1: Basic Tests (No Dependencies)

```bash
python run_tests.py
```

This runs basic functionality tests without requiring pytest.

### Option 2: Full Test Suite (Requires pytest)

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_sentiment_analyzer.py -v

# Run specific test class
pytest tests/test_sentiment_analyzer.py::TestTrainedSentimentAnalyzer -v

# Run specific test
pytest tests/test_sentiment_analyzer.py::TestTrainedSentimentAnalyzer::test_positive_sentiment_detection -v

# Run with coverage
pytest tests/ -v --cov=src/analysis --cov-report=html

# Run and stop on first failure
pytest tests/ -v -x
```

### Option 3: Run Tests by Category

```bash
# Run only sentiment analyzer tests
pytest tests/test_sentiment_analyzer.py -v

# Run only model trainer tests
pytest tests/test_model_trainer.py -v

# Run only integration tests
pytest tests/test_analysis_integration.py -v
```

## Test Requirements

### Required for All Tests
- Trained model files in `models/` directory
- Run `python scripts/train_sentiment_model.py` first

### Optional for Full Coverage
- `data/sentimentdataset.csv` - For dataset-specific tests
- pytest and pytest-cov - For full test suite

## Test Fixtures

### Common Fixtures

```python
@pytest.fixture
def analyzer():
    """Trained sentiment analyzer instance."""
    return TrainedSentimentAnalyzer()

@pytest.fixture
def temp_model_dir():
    """Temporary directory for model files."""
    # Creates and cleans up temp directory

@pytest.fixture
def sample_csv_data(tmp_path):
    """Sample CSV data for testing."""
    # Creates temporary CSV file

@pytest.fixture
def analysis_service():
    """Complete analysis service with all dependencies."""
    # Returns configured AnalysisService
```

## Test Coverage

### Current Coverage

```
src/analysis/sentiment_analyzer.py    - 95%
src/analysis/model_trainer.py         - 90%
src/analysis/analysis_service.py      - 85%
```

### Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=src/analysis --cov-report=html

# View report
# Open htmlcov/index.html in browser
```

## Writing New Tests

### Test Structure

```python
import pytest
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

class TestNewFeature:
    """Test suite for new feature."""
    
    def test_feature_works(self):
        """Test that feature works correctly."""
        analyzer = TrainedSentimentAnalyzer()
        result = analyzer.analyze("test text")
        assert result is not None
    
    def test_feature_edge_case(self):
        """Test edge case handling."""
        # Test implementation
        pass
```

### Best Practices

1. **Use descriptive test names**
   ```python
   def test_analyzer_handles_empty_string()  # Good
   def test_empty()                          # Bad
   ```

2. **One assertion per test (when possible)**
   ```python
   def test_confidence_range():
       result = analyzer.analyze("test")
       assert 0.0 <= result.score <= 1.0
   ```

3. **Use fixtures for setup**
   ```python
   @pytest.fixture
   def analyzer():
       return TrainedSentimentAnalyzer()
   
   def test_something(analyzer):
       result = analyzer.analyze("test")
   ```

4. **Test both success and failure cases**
   ```python
   def test_valid_input():
       # Test with valid input
       pass
   
   def test_invalid_input():
       with pytest.raises(ValueError):
           # Test with invalid input
           pass
   ```

5. **Use parametrize for multiple similar tests**
   ```python
   @pytest.mark.parametrize("text,expected", [
       ("I love this!", "positive"),
       ("This is bad.", "negative"),
       ("It's okay.", "neutral"),
   ])
   def test_sentiments(text, expected):
       result = analyzer.analyze(text)
       assert result.label.value == expected
   ```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Train model
        run: python scripts/train_sentiment_model.py
      - name: Run tests
        run: pytest tests/ -v --cov=src/analysis
```

## Troubleshooting

### Model Not Found Error

```
FileNotFoundError: Model file not found
```

**Solution**: Train the model first
```bash
python scripts/train_sentiment_model.py
```

### Import Errors

```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Run tests from project root
```bash
cd /path/to/Vibe-Optimizer
pytest tests/
```

### Pytest Not Found

```
python.exe: No module named pytest
```

**Solution**: Install pytest
```bash
pip install pytest pytest-cov
```

Or use basic test runner:
```bash
python run_tests.py
```

### Dataset Not Found (Optional Tests)

Some tests are skipped if dataset is not available:
```
SKIPPED [1] tests/test_model_trainer.py: Dataset not available
```

This is normal - these tests are optional.

## Test Metrics

### Performance Benchmarks

- Single text analysis: < 1 second
- Batch analysis (50 items): < 10 seconds
- Model training (732 samples): < 30 seconds

### Expected Accuracy

- Model accuracy: > 70%
- Positive sentiment detection: > 50%
- Negative sentiment detection: > 25%

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain > 80% code coverage
4. Update this README if adding new test files

## Support

For issues with tests:
1. Check that model is trained
2. Verify all dependencies are installed
3. Run basic tests first: `python run_tests.py`
4. Check test output for specific errors
