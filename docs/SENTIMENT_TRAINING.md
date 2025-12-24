# Sentiment Analysis Training Module

## Overview

This module provides a complete training pipeline for sentiment analysis models using the dataset in `data/sentimentdataset.csv`. The trained models can be used in APIs, dashboards, and batch processing workflows.

## Architecture

### Components

1. **Model Trainer** (`src/analysis/model_trainer.py`)
   - Loads and preprocesses training data
   - Trains scikit-learn models (Logistic Regression, Naive Bayes)
   - Evaluates model performance
   - Saves trained models for production use

2. **Sentiment Analyzer** (`src/analysis/sentiment_analyzer.py`)
   - `TrainedSentimentAnalyzer`: Uses custom trained models
   - `TransformerSentimentAnalyzer`: Uses Hugging Face transformers
   - `VaderSentimentAnalyzer`: Uses VADER rule-based analysis

3. **API Integration** (`src/api/sentiment_api_example.py`)
   - FastAPI-ready endpoints
   - Single and batch analysis
   - Pydantic models for request/response validation

4. **Dashboard Integration** (`src/dashboard/sentiment_dashboard_example.py`)
   - Streamlit-ready components
   - Data visualization helpers
   - Performance metrics

## Quick Start

### 1. Train the Model

```bash
# Train sentiment model using the dataset
python scripts/train_sentiment_model.py
```

This will:
- Load data from `data/sentimentdataset.csv`
- Train a Logistic Regression model
- Save model files to `models/` directory:
  - `sentiment_model.pkl` (trained model)
  - `sentiment_model_vectorizer.pkl` (TF-IDF vectorizer)
  - `sentiment_model_metrics.json` (performance metrics)

### 2. Run the Demo

```bash
# Complete workflow demonstration
python scripts/demo_sentiment_analysis.py
```

This demonstrates:
- Model training (if needed)
- Single text analysis
- Batch analysis from CSV
- API-ready usage patterns

### 3. Use in Your Code

```python
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

# Initialize analyzer
analyzer = TrainedSentimentAnalyzer(model_path="models/sentiment_model.pkl")

# Analyze text
sentiment = analyzer.analyze("I love this product!")

print(f"Label: {sentiment.label.value}")
print(f"Confidence: {sentiment.score:.3f}")
print(f"Intensity: {sentiment.intensity:.3f}")
print(f"Compound: {sentiment.compound_score:.3f}")
```

## Training Details

### Dataset Format

The training expects CSV with these columns:
- `Text`: The text content to analyze
- `Sentiment`: Label (Positive, Negative, Neutral)
- `Timestamp`: When the content was created
- Other metadata columns (optional)

### Model Configuration

Default settings in `SentimentModelTrainer`:
- **Algorithm**: Logistic Regression (configurable)
- **Features**: TF-IDF with 5000 max features
- **N-grams**: Unigrams and bigrams (1-2)
- **Test Split**: 20% for evaluation
- **Class Balancing**: Enabled

### Performance Metrics

After training, you'll see:
- **Accuracy**: Overall classification accuracy
- **Precision/Recall/F1**: Per-class metrics
- **Confusion Matrix**: Detailed error analysis
- **Feature Importance**: Top words per sentiment

## API Integration

### FastAPI Example

```python
from fastapi import FastAPI
from src.api.sentiment_api_example import (
    SentimentAnalysisAPI,
    SentimentAnalysisRequest
)

app = FastAPI()
sentiment_api = SentimentAnalysisAPI(model_path="models/sentiment_model.pkl")

@app.post("/api/sentiment/analyze")
async def analyze(request: SentimentAnalysisRequest):
    return sentiment_api.analyze_single(request)
```

### API Endpoints

1. **Single Analysis**: `POST /api/sentiment/analyze`
   ```json
   {
     "text": "I love this!",
     "include_metadata": true
   }
   ```

2. **Batch Analysis**: `POST /api/sentiment/batch`
   ```json
   {
     "texts": ["Great!", "Terrible!", "Okay."],
     "include_metadata": false
   }
   ```

3. **Model Info**: `GET /api/sentiment/model-info`

## Dashboard Integration

### Streamlit Example

```python
import streamlit as st
from src.dashboard.sentiment_dashboard_example import SentimentDashboardData

# Initialize
dashboard = SentimentDashboardData(model_path="models/sentiment_model.pkl")

# Analyze dataset
df = dashboard.analyze_dataset("data/sentimentdataset.csv", limit=100)

# Display metrics
metrics = dashboard.get_average_metrics(df)
st.metric("Avg Confidence", f"{metrics['avg_confidence']:.3f}")

# Show distribution
dist = dashboard.get_sentiment_distribution(df)
st.bar_chart(dist)
```

### Dashboard Features

- Sentiment distribution pie charts
- Sentiment trends over time
- Top positive/negative texts
- Platform-wise sentiment breakdown
- Model accuracy metrics

## Advanced Usage

### Custom Training

```python
from src.analysis.model_trainer import SentimentModelTrainer

# Initialize trainer
trainer = SentimentModelTrainer(model_dir="models")

# Load data
texts, labels = trainer.load_data_from_csv("data/sentimentdataset.csv")

# Train with custom parameters
metrics = trainer.train(
    texts=texts,
    labels=labels,
    algorithm='logistic_regression',  # or 'naive_bayes'
    test_size=0.2,
    max_features=10000,  # More features
    random_state=42
)

# Save model
trainer.save_model(model_name='custom_model')
```

### Batch Processing

```python
from src.ingestion.ingestion_service import CSVDataSource
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

# Load data
csv_source = CSVDataSource("data/sentimentdataset.csv")
raw_content = csv_source.fetch_content(limit=1000)

# Analyze in batch
analyzer = TrainedSentimentAnalyzer()
results = []

for item in raw_content:
    sentiment = analyzer.analyze(item.content)
    results.append({
        'text': item.content,
        'sentiment': sentiment.label.value,
        'confidence': sentiment.score
    })
```

### Integration with Analysis Service

```python
from src.analysis.analysis_service import AnalysisService
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
from src.analysis.topic_extractor import TopicExtractor  # When implemented
from src.storage.repositories import Repository  # When implemented

# Initialize components
sentiment_analyzer = TrainedSentimentAnalyzer()
topic_extractor = TopicExtractor()
repository = Repository()

# Create analysis service
analysis_service = AnalysisService(
    sentiment_analyzer=sentiment_analyzer,
    topic_extractor=topic_extractor,
    repository=repository
)

# Analyze content
analyzed = analysis_service.analyze_content(raw_content)
```

## Model Output

### SentimentScore Object

```python
@dataclass
class SentimentScore:
    label: SentimentLabel          # POSITIVE, NEGATIVE, or NEUTRAL
    score: float                   # Confidence (0-1)
    intensity: float               # Sentiment strength (0-1)
    compound_score: float          # Overall score (-1 to 1)
```

### Interpretation

- **Label**: The predicted sentiment category
- **Score**: How confident the model is (higher = more confident)
- **Intensity**: How strong the sentiment is (0 = weak, 1 = strong)
- **Compound**: Overall sentiment (-1 = very negative, 0 = neutral, 1 = very positive)

## Best Practices

### For Production

1. **Model Versioning**: Save models with version numbers
   ```python
   trainer.save_model(model_name='sentiment_model_v1.0')
   ```

2. **Model Monitoring**: Track prediction confidence over time
   ```python
   if sentiment.score < 0.6:
       # Log low-confidence predictions for review
       logger.warning(f"Low confidence: {sentiment.score}")
   ```

3. **Batch Processing**: Process large datasets in chunks
   ```python
   chunk_size = 1000
   for i in range(0, len(texts), chunk_size):
       chunk = texts[i:i+chunk_size]
       # Process chunk
   ```

4. **Caching**: Cache analyzer instance (don't reload for each request)
   ```python
   # In FastAPI
   @lru_cache()
   def get_analyzer():
       return TrainedSentimentAnalyzer()
   ```

### For Accuracy

1. **Regular Retraining**: Retrain with new data periodically
2. **Domain-Specific Data**: Use data from your specific domain
3. **Label Quality**: Ensure training labels are accurate
4. **Feature Engineering**: Experiment with different TF-IDF parameters

## Troubleshooting

### Model Not Found

```
FileNotFoundError: Model file not found
```
**Solution**: Run `python scripts/train_sentiment_model.py` first

### Low Accuracy

**Solutions**:
- Increase training data size
- Try different algorithms (naive_bayes vs logistic_regression)
- Adjust max_features parameter
- Clean and preprocess text better

### Memory Issues

**Solutions**:
- Reduce max_features in TF-IDF
- Process data in smaller batches
- Use sparse matrices (already implemented)

## Dependencies

Required packages:
```
scikit-learn>=1.0.0
pandas>=1.3.0
numpy>=1.21.0
```

Optional for other analyzers:
```
transformers>=4.0.0  # For TransformerSentimentAnalyzer
torch>=1.9.0         # For transformers
nltk>=3.6.0          # For VaderSentimentAnalyzer
```

## Future Enhancements

- [ ] Support for fine-tuning transformer models
- [ ] Multi-label sentiment classification
- [ ] Emotion detection (joy, anger, fear, etc.)
- [ ] Aspect-based sentiment analysis
- [ ] Real-time model updates
- [ ] A/B testing framework for models

## Support

For issues or questions:
1. Check the demo script: `python scripts/demo_sentiment_analysis.py`
2. Review training logs in `models/sentiment_model_metrics.json`
3. Verify dataset format matches expected structure
