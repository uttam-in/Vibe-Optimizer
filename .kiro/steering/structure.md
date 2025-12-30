# Project Structure & Architecture

## Design Principles
Built with SOLID principles throughout:
- **SRP**: Each module handles one concern
- **OCP**: Extensible via interfaces (add sources/analyzers without modifying existing code)
- **LSP**: Source adapters and analyzers are interchangeable
- **ISP**: Focused interfaces per component
- **DIP**: Services depend on abstractions in `src/core/interfaces.py`

## Directory Layout

```
src/
├── core/           # Domain models & interfaces (no external deps)
│   ├── models.py       # RawContent, SentimentScore, Topic, Insight, etc.
│   └── interfaces.py   # IDataSource, ISentimentAnalyzer, IRepository, etc.
├── ingestion/      # Data collection
│   ├── ingestion_service.py  # Orchestration + CSVDataSource
│   └── sources/              # Platform adapters (twitter, reddit, reviews)
├── analysis/       # NLP processing
│   ├── sentiment_analyzer.py # TrainedSentimentAnalyzer, VADERAnalyzer
│   ├── topic_extractor.py    # Topic clustering
│   ├── model_trainer.py      # Model training utilities
│   └── analysis_service.py   # Pipeline orchestration
├── storage/        # Persistence layer
│   ├── database.py       # SQLAlchemy models & session management
│   └── repositories.py   # Repository pattern implementations
├── insights/       # Business intelligence
│   └── insight_generator.py  # Trend analysis, actionable insights
├── reporting/      # Report generation
│   ├── report_generator.py   # HTML/PDF reports
│   └── email_service.py      # SendGrid integration
├── api/            # REST API (FastAPI)
│   ├── main.py           # App entry point
│   └── routes/           # Endpoint modules (sentiment, insights, reports)
├── dashboard/      # Web UI (Streamlit)
│   └── app.py            # Dashboard entry point
└── scheduler/      # Background jobs (APScheduler)
    └── jobs.py           # Scheduled ingestion & reporting

config/             # Application settings (pydantic-settings)
scripts/            # Utility scripts (setup_db, train_model, run_ingestion)
tests/              # pytest test suite
models/             # Trained ML models (.pkl files)
data/               # Dataset files (CSV)
docs/               # Documentation
examples/           # Usage examples
```

## Key Patterns

### Adding a New Data Source
1. Create adapter in `src/ingestion/sources/`
2. Implement `IDataSource` interface
3. Register in ingestion service

### Adding a New Analyzer
1. Create class implementing `ISentimentAnalyzer`
2. Inject via dependency inversion

### Repository Pattern
- All persistence goes through `src/storage/repositories.py`
- Implements `IRepository` interface

## Entry Points
- API: `src/api/main.py` → `uvicorn src.api.main:app`
- Dashboard: `src/dashboard/app.py` → `streamlit run`
- Workers: `src/ingestion/worker` (module)
- Scheduler: `src/scheduler/jobs.py`
