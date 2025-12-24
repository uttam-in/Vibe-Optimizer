# Vibe Optimizer

NLP-powered brand intelligence platform that analyzes sentiment and topics from multiple data sources.

## MVP Features

- ✅ Ingest data from CSV and multiple sources (social media, reviews, support tickets)
- ✅ **Trained sentiment analysis model** with intensity scoring
- ✅ Sentiment classification (Positive, Negative, Neutral)
- ✅ Confidence and compound scoring
- Topic clustering and trend detection
- Real-time dashboard with sentiment over time
- Weekly automated email reports
- ✅ **API-ready sentiment analysis endpoints**
- ✅ **Dashboard-ready data components**

## Architecture

Built with SOLID principles:
- **Single Responsibility**: Each module handles one concern
- **Open/Closed**: Extensible via interfaces/abstract classes
- **Liskov Substitution**: Source adapters are interchangeable
- **Interface Segregation**: Focused interfaces per component
- **Dependency Inversion**: Depends on abstractions, not concrete implementations

## Tech Stack

- Python 3.x
- NLP: spaCy, transformers, scikit-learn
- Data: pandas, numpy
- Storage: SQLAlchemy (PostgreSQL/SQLite)
- API: FastAPI
- Dashboard: Plotly/Dash or Streamlit
- Scheduling: APScheduler
- Email: SMTP/SendGrid

## Project Structure

```
vibe-optimizer/
├── src/
│   ├── core/              # Domain models and business logic
│   ├── ingestion/         # Data source adapters
│   ├── analysis/          # NLP processing
│   ├── storage/           # Data persistence
│   ├── insights/          # Insight generation
│   ├── reporting/         # Report generation
│   ├── api/               # REST API
│   └── dashboard/         # Web dashboard
├── tests/                 # Unit and integration tests
├── config/                # Configuration files
├── scripts/               # Utility scripts
└── docs/                  # Documentation
```

## Quick Start

### 1. Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Train Sentiment Model

```bash
# Train the sentiment analysis model using the dataset
python scripts/train_sentiment_model.py
```

This will create trained model files in the `models/` directory.

### 3. Test the System

```bash
# Run complete workflow demo
python examples/complete_workflow.py
```

### 4. Use the Analyzer

```python
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

# Initialize analyzer
analyzer = TrainedSentimentAnalyzer()

# Analyze text
sentiment = analyzer.analyze("I love this product!")
print(f"Sentiment: {sentiment.label.value}")
print(f"Confidence: {sentiment.score:.3f}")
```

## Testing

### Run Tests

```bash
# Basic tests (no dependencies)
python run_tests.py

# Full test suite (requires pytest)
pip install pytest pytest-cov
pytest tests/ -v
```

### Test Coverage
- 60+ test cases
- 85-95% code coverage
- Unit, integration, and performance tests

See [TEST_QUICK_REFERENCE.md](TEST_QUICK_REFERENCE.md) for more details.

## Documentation

- **Quick Start**: [docs/QUICK_START.md](docs/QUICK_START.md)
- **Training Guide**: [docs/SENTIMENT_TRAINING.md](docs/SENTIMENT_TRAINING.md)
- **Implementation Summary**: [SENTIMENT_ANALYSIS_IMPLEMENTATION.md](SENTIMENT_ANALYSIS_IMPLEMENTATION.md)
- **Testing Guide**: [tests/README.md](tests/README.md)
- **Test Quick Reference**: [TEST_QUICK_REFERENCE.md](TEST_QUICK_REFERENCE.md)

## Running

```bash
# Start ingestion workers
python -m src.ingestion.worker

# Start API server
python -m src.api.main

# Start dashboard
python -m src.dashboard.app
```
