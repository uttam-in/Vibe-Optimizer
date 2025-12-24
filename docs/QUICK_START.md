# Quick Start Guide - Sentiment Analysis

## 🚀 Get Started in 3 Steps

### Step 1: Train the Model

```bash
python scripts/train_sentiment_model.py
```

This trains a sentiment analysis model using `data/sentimentdataset.csv` and saves it to the `models/` directory.

### Step 2: Test It

```python
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

# Initialize
analyzer = TrainedSentimentAnalyzer(model_path="models/sentiment_model.pkl")

# Analyze
sentiment = analyzer.analyze("I love this product!")

print(f"Sentiment: {sentiment.label.value}")
print(f"Confidence: {sentiment.score:.3f}")
```

### Step 3: Use It

Choose your integration:

#### Option A: API (FastAPI)

```python
from fastapi import FastAPI
from src.api.sentiment_api_example import SentimentAnalysisAPI, SentimentAnalysisRequest

app = FastAPI()
api = SentimentAnalysisAPI()

@app.post("/analyze")
async def analyze(request: SentimentAnalysisRequest):
    return api.analyze_single(request)
```

#### Option B: Dashboard (Streamlit)

```python
import streamlit as st
from src.dashboard.sentiment_dashboard_example import SentimentDashboardData

dashboard = SentimentDashboardData()
df = dashboard.analyze_dataset("data/sentimentdataset.csv", limit=100)

st.metric("Avg Confidence", f"{dashboard.get_average_metrics(df)['avg_confidence']:.3f}")
```

#### Option C: Batch Processing

```python
from src.ingestion.ingestion_service import CSVDataSource
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

# Load data
csv_source = CSVDataSource("data/sentimentdataset.csv")
content = csv_source.fetch_content(limit=100)

# Analyze
analyzer = TrainedSentimentAnalyzer()
for item in content:
    sentiment = analyzer.analyze(item.content)
    print(f"{item.content[:50]}... → {sentiment.label.value}")
```

## 📊 Complete Demo

Run the complete workflow demonstration:

```bash
python examples/complete_workflow.py
```

This shows:
- ✓ Model training
- ✓ Single text analysis
- ✓ Batch analysis
- ✓ API simulation
- ✓ Dashboard data preparation

## 🔧 Configuration

### Change Algorithm

```python
from src.analysis.model_trainer import SentimentModelTrainer

trainer = SentimentModelTrainer()
texts, labels = trainer.load_data_from_csv("data/sentimentdataset.csv")

# Use Naive Bayes instead of Logistic Regression
metrics = trainer.train(texts, labels, algorithm='naive_bayes')
trainer.save_model('nb_model')
```

### Adjust Features

```python
metrics = trainer.train(
    texts, 
    labels,
    max_features=10000,  # More features
    test_size=0.3        # Larger test set
)
```

## 📈 Model Output

```python
sentiment = analyzer.analyze("Great product!")

# Available attributes:
sentiment.label           # SentimentLabel.POSITIVE
sentiment.score          # 0.95 (confidence)
sentiment.intensity      # 0.87 (strength)
sentiment.compound_score # 0.92 (-1 to 1)
```

## 🎯 Use Cases

### 1. Real-time Analysis
```python
analyzer = TrainedSentimentAnalyzer()

def analyze_user_feedback(text: str):
    sentiment = analyzer.analyze(text)
    if sentiment.label.value == 'negative' and sentiment.intensity > 0.7:
        alert_support_team(text)
```

### 2. Trend Monitoring
```python
dashboard = SentimentDashboardData()
df = dashboard.analyze_dataset("data/sentimentdataset.csv")
trends = dashboard.get_sentiment_over_time(df, freq='D')
```

### 3. Batch Reports
```python
csv_source = CSVDataSource("data/sentimentdataset.csv")
content = csv_source.fetch_content(limit=1000)

results = []
for item in content:
    sentiment = analyzer.analyze(item.content)
    results.append({
        'date': item.timestamp,
        'sentiment': sentiment.label.value,
        'confidence': sentiment.score
    })

# Generate report
import pandas as pd
df = pd.DataFrame(results)
df.to_csv('sentiment_report.csv')
```

## 🐛 Troubleshooting

### Model not found?
```bash
# Train the model first
python scripts/train_sentiment_model.py
```

### Import errors?
```bash
# Install dependencies
pip install -r requirements.txt
```

### Low accuracy?
- Increase training data
- Try different algorithm
- Adjust max_features
- Clean text data better

## 📚 More Information

- **Full Documentation**: `docs/SENTIMENT_TRAINING.md`
- **API Examples**: `src/api/sentiment_api_example.py`
- **Dashboard Examples**: `src/dashboard/sentiment_dashboard_example.py`
- **Training Script**: `scripts/train_sentiment_model.py`
- **Complete Demo**: `examples/complete_workflow.py`

## 💡 Tips

1. **Cache the analyzer** - Don't reload for each request
2. **Monitor confidence** - Log low-confidence predictions
3. **Retrain regularly** - Update with new data
4. **Batch process** - More efficient for large datasets
5. **Version models** - Keep track of model versions

## 🎓 Next Steps

1. ✅ Train your model
2. ✅ Test with sample texts
3. ✅ Integrate into your application
4. ✅ Monitor performance
5. ✅ Iterate and improve

Happy analyzing! 🎉
