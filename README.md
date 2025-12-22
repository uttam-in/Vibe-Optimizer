# Vibe Optimizer

NLP-powered brand intelligence platform that analyzes sentiment and topics from multiple data sources.

## MVP Features

- Ingest data from 2-3 sources (social media, reviews, support tickets)
- Sentiment analysis with intensity scoring
- Topic clustering and trend detection
- Real-time dashboard with sentiment over time
- Weekly automated email reports

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

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
# Start ingestion workers
python -m src.ingestion.worker

# Start API server
python -m src.api.main

# Start dashboard
python -m src.dashboard.app
```
