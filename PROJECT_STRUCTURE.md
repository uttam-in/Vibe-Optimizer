# Vibe Optimizer - Project Structure

## Overview
NLP-powered brand intelligence platform built with SOLID principles in Python 3.x.

## Directory Structure

```
vibe-optimizer/
│
├── src/                           # Source code
│   ├── core/                      # Core domain layer (no dependencies)
│   │   ├── __init__.py
│   │   ├── models.py              # Domain models (RawContent, SentimentScore, etc.)
│   │   └── interfaces.py          # Abstract interfaces (IDataSource, ISentimentAnalyzer, etc.)
│   │
│   ├── ingestion/                 # Data ingestion layer
│   │   ├── __init__.py
│   │   ├── ingestion_service.py   # Orchestrates multi-source ingestion
│   │   └── sources/               # Data source adapters
│   │       ├── __init__.py
│   │       ├── twitter_source.py  # Twitter API adapter
│   │       ├── reddit_source.py   # Reddit API adapter
│   │       └── review_source.py   # Review platform adapter
│   │
│   ├── analysis/                  # NLP analysis layer
│   │   ├── __init__.py
│   │   ├── analysis_service.py    # Orchestrates analysis pipeline
│   │   ├── sentiment_analyzer.py  # Sentiment analysis implementations
│   │   └── topic_extractor.py     # Topic extraction/clustering
│   │
│   ├── storage/                   # Data persistence layer
│   │   ├── __init__.py
│   │   ├── database.py            # Database models and session management
│   │   └── repositories.py        # Repository pattern implementations
│   │
│   ├── insights/                  # Business insights layer
│   │   ├── __init__.py
│   │   └── insight_generator.py   # Generate actionable insights
│   │
│   ├── reporting/                 # Reporting layer
│   │   ├── __init__.py
│   │   ├── report_generator.py    # Report generation
│   │   └── email_service.py       # Email notifications
│   │
│   ├── api/                       # REST API layer
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI application
│   │   └── routes/                # API endpoints
│   │       ├── __init__.py
│   │       ├── sentiment.py       # Sentiment endpoints
│   │       ├── insights.py        # Insights endpoints
│   │       └── reports.py         # Reports endpoints
│   │
│   ├── dashboard/                 # Web dashboard
│   │   ├── __init__.py
│   │   └── app.py                 # Streamlit dashboard
│   │
│   └── scheduler/                 # Background jobs
│       ├── __init__.py
│       └── jobs.py                # Scheduled tasks
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_sentiment_analyzer.py
│   └── test_ingestion_service.py
│
├── config/                        # Configuration
│   ├── __init__.py
│   └── settings.py                # Application settings
│
├── scripts/                       # Utility scripts
│   ├── __init__.py
│   ├── setup_db.py                # Database initialization
│   └── run_ingestion.py           # Manual ingestion
│
├── docs/                          # Documentation
│   ├── SETUP.md                   # Setup guide
│   ├── ARCHITECTURE.md            # Architecture overview
│   └── API.md                     # API documentation
│
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── alembic.ini                    # Database migrations config
├── Makefile                       # Common commands
└── README.md                      # Project overview
```

## SOLID Principles Applied

### Single Responsibility Principle (SRP)
- Each class has one reason to change
- `SentimentAnalyzer`: Only sentiment analysis
- `TopicExtractor`: Only topic extraction
- `IngestionService`: Only orchestration
- `Repository`: Only data persistence

### Open/Closed Principle (OCP)
- Open for extension, closed for modification
- Add new sources by implementing `IDataSource`
- Add new analyzers by implementing `ISentimentAnalyzer`
- No need to modify existing code

### Liskov Substitution Principle (LSP)
- Implementations are interchangeable
- Any `IDataSource` can replace another
- Any `ISentimentAnalyzer` can be swapped
- Services depend on interfaces

### Interface Segregation Principle (ISP)
- Focused, specific interfaces
- `IDataSource`: Only data fetching
- `ISentimentAnalyzer`: Only sentiment analysis
- `ITopicExtractor`: Only topic operations

### Dependency Inversion Principle (DIP)
- Depend on abstractions, not concretions
- Services inject dependencies via interfaces
- Easy to test with mocks
- Flexible configuration

## Key Components

### Core Layer
- **models.py**: Domain entities (RawContent, AnalyzedContent, Insight, etc.)
- **interfaces.py**: Abstract interfaces for all major components

### Ingestion Layer
- **IngestionService**: Coordinates data collection from multiple sources
- **Source Adapters**: Twitter, Reddit, Reviews (implement IDataSource)

### Analysis Layer
- **AnalysisService**: Orchestrates NLP pipeline
- **SentimentAnalyzer**: Transformer-based or VADER sentiment analysis
- **TopicExtractor**: LDA or BERTopic for topic clustering

### Storage Layer
- **DatabaseManager**: SQLAlchemy session management
- **Repositories**: CRUD operations for each entity type

### Insights Layer
- **InsightGenerator**: Analyzes trends and generates actionable insights

### Reporting Layer
- **ReportGenerator**: Creates HTML/PDF reports
- **EmailService**: Sends automated reports via SendGrid

### API Layer
- **FastAPI**: REST endpoints for data access
- **Routes**: Sentiment, Insights, Reports endpoints

### Dashboard Layer
- **Streamlit**: Real-time visualization dashboard

### Scheduler Layer
- **APScheduler**: Background jobs for ingestion and reporting

## MVP Features Covered

✅ Ingest 2-3 sources (Twitter, Reddit, Reviews)
✅ Sentiment analysis with intensity
✅ Topic clustering
✅ Basic dashboard (sentiment over time + top topics)
✅ Weekly automated email reports
✅ SOLID principles throughout
✅ Extensible architecture
✅ Test structure
✅ Configuration management
