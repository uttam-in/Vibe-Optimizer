# Quick Reference - Sentiment Analysis

## 🚀 Model Status

✅ **TRAINED AND READY**
- Location: `models/sentiment_model.pkl`
- Accuracy: 72.1%
- Classes: Positive, Negative, Neutral

## 💻 Basic Usage

```python
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

analyzer = TrainedSentimentAnalyzer()
result = analyzer.analyze("I love this!")

print(result.label.value)      # 'positive'
print(result.score)            # 0.456 (confidence)
print(result.intensity)        # 0.359 (strength)
print(result.compound_score)   # 0.315 (-1 to 1)
```

## 📝 Common Tasks

### Analyze Single Text
```python
sentiment = analyzer.analyze("Your text here")
```

### Analyze from CSV
```python
from src.ingestion.ingestion_service import CSVDataSource

csv_source = CSVDataSource("data/sentimentdataset.csv")
content = csv_source.fetch_content(limit=100)

for item in content:
    sentiment = analyzer.analyze(item.content)
```

### Batch Analysis
```python
texts = ["Text 1", "Text 2", "Text 3"]
results = [analyzer.analyze(text) for text in texts]
```

## 🔧 Scripts

```bash
# Train model
python scripts/train_sentiment_model.py

# Run demo
python scripts/demo_sentiment_analysis.py

# Complete workflow
python examples/complete_workflow.py

# Verify model
python verify_model.py
```

## 📊 Model Output

```python
sentiment.label           # SentimentLabel enum
sentiment.score          # float (0-1) confidence
sentiment.intensity      # float (0-1) strength
sentiment.compound_score # float (-1 to 1) overall
```

## 🎯 Integration

### API (FastAPI)
```python
from src.api.sentiment_api_example import SentimentAnalysisAPI

api = SentimentAnalysisAPI()
response = api.analyze_single(request)
```

### Dashboard (Streamlit)
```python
from src.dashboard.sentiment_dashboard_example import SentimentDashboardData

dashboard = SentimentDashboardData()
df = dashboard.analyze_dataset("data.csv", limit=100)
```

## 📚 Documentation

- `docs/QUICK_START.md` - Get started in 3 steps
- `docs/SENTIMENT_TRAINING.md` - Full guide
- `MODEL_TRAINING_COMPLETE.md` - Training summary

## 🆘 Troubleshooting

**Model not found?**
```bash
python scripts/train_sentiment_model.py
```

**Import error?**
```bash
pip install -r requirements.txt
```

**Low accuracy?**
- Retrain with more data
- Try different algorithm
- Adjust parameters

## ✅ Checklist

- [x] Model trained (72.1% accuracy)
- [x] Model saved locally
- [x] Analyzer working
- [x] CSV ingestion working
- [x] API components ready
- [x] Dashboard components ready
- [x] Documentation complete

## 🎉 You're Ready!

Your sentiment analysis system is trained and ready for production use!
