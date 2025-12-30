# Tech Stack & Build System

## Language & Runtime
- Python 3.10+
- Conda environment (`.conda/`)

## Core Dependencies
| Category | Libraries |
|----------|-----------|
| NLP/ML | spaCy, transformers, scikit-learn, torch, nltk |
| Data | pandas, numpy |
| Database | SQLAlchemy, Alembic (PostgreSQL/SQLite) |
| API | FastAPI, uvicorn, pydantic |
| Dashboard | Streamlit, Plotly |
| Scheduling | APScheduler, Celery, Redis |
| Email | SendGrid |
| Social APIs | tweepy (Twitter), praw (Reddit) |
| Testing | pytest, pytest-cov, pytest-asyncio |

## Configuration
- Environment variables via `.env` (see `.env.example`)
- Settings managed in `config/settings.py` using pydantic-settings
- Database migrations via Alembic (`alembic.ini`)

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Setup
cp .env.example .env
python scripts/setup_db.py

# Train sentiment model
python scripts/train_sentiment_model.py

# Run tests
pytest tests/ -v --cov=src

# Run API server
uvicorn src.api.main:app --reload --port 8000

# Run dashboard
streamlit run src/dashboard/app.py --server.port 8501

# Run ingestion
python scripts/run_ingestion.py

# Demo/verification
python examples/complete_workflow.py
python verify_model.py
```

## Makefile Targets
- `make install` - Install deps + spaCy model
- `make setup` - Create .env and init DB
- `make test` - Run pytest with coverage
- `make run-api` - Start FastAPI server
- `make run-dashboard` - Start Streamlit dashboard
- `make clean` - Remove cache files
