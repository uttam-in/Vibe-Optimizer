# Setup Guide

## Prerequisites

- Python 3.9+
- PostgreSQL (or SQLite for development)
- API keys for data sources

## Installation

1. Clone repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download NLP models:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

6. Initialize database:
   ```bash
   python scripts/setup_db.py
   ```

## Running

### API Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

### Dashboard
```bash
streamlit run src/dashboard/app.py --server.port 8501
```

### Background Jobs
```bash
python -m src.scheduler.worker
```

### Manual Ingestion
```bash
python scripts/run_ingestion.py
```

## Testing

```bash
pytest tests/ -v --cov=src
```
