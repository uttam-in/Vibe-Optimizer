# Test Quick Reference

## 🚀 Run Tests

### Basic (No Dependencies)
```bash
python run_tests.py
```

### Full Suite (Requires pytest)
```bash
pip install pytest pytest-cov
pytest tests/ -v
```

## 📁 Test Files

| File | Tests | Lines |
|------|-------|-------|
| `test_sentiment_analyzer.py` | Analyzer tests | 300+ |
| `test_model_trainer.py` | Trainer tests | 400+ |
| `test_analysis_integration.py` | Integration tests | 400+ |

## 🎯 Common Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific file
pytest tests/test_sentiment_analyzer.py -v

# Run with coverage
pytest tests/ --cov=src/analysis --cov-report=html

# Stop on first failure
pytest tests/ -v -x

# Run specific test
pytest tests/test_sentiment_analyzer.py::TestTrainedSentimentAnalyzer::test_positive_sentiment_detection -v
```

## ✅ Test Coverage

- **Sentiment Analyzer**: 95%
- **Model Trainer**: 90%
- **Analysis Service**: 85%

## 📊 Test Count

- **Total Tests**: 60+
- **Test Classes**: 12
- **Test Files**: 3

## 🔧 Prerequisites

1. Train model first:
   ```bash
   python scripts/train_sentiment_model.py
   ```

2. (Optional) Install pytest:
   ```bash
   pip install pytest pytest-cov
   ```

## 📚 Documentation

- **Full Guide**: `tests/README.md`
- **Test Summary**: `TESTING_COMPLETE.md`
- **This Reference**: `TEST_QUICK_REFERENCE.md`

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | `python scripts/train_sentiment_model.py` |
| Import errors | Run from project root |
| Pytest not found | Use `python run_tests.py` |

## ✨ Test Categories

- ✅ Unit tests
- ✅ Integration tests
- ✅ Edge cases
- ✅ Performance tests
- ✅ Error handling

## 🎉 Quick Verify

```bash
# Verify everything works
python run_tests.py

# Should see:
# ✓ Model files exist
# ✓ All imports successful
# ✓ Analyzer initialized
# ✓ Tests passing
```
