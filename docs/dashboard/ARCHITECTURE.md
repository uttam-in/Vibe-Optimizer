# Dashboard Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Vibe Optimizer Dashboard                     │
│                         (Streamlit UI)                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  Ingestion   │ │   Analysis   │ │    Core      │
        │   Service    │ │   Service    │ │   Models     │
        └──────────────┘ └──────────────┘ └──────────────┘
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Dashboard Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     Home     │  │  Analytics   │  │    Data      │          │
│  │   Dashboard  │  │     Page     │  │   Explorer   │          │
│  │   (app.py)   │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     Data     │  │    Utils     │  │    Config    │          │
│  │  Ingestion   │  │   Module     │  │   Settings   │          │
│  │              │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Ingestion Service  │ │ Analysis Service│ │   Core Models   │
├─────────────────────┤ ├─────────────────┤ ├─────────────────┤
│                     │ │                 │ │                 │
│ • CSVDataSource     │ │ • Trained Model │ │ • RawContent    │
│ • IngestionService  │ │ • VADER Model   │ │ • SentimentScore│
│ • fetch_content()   │ │ • analyze()     │ │ • SentimentLabel│
│                     │ │                 │ │ • SourceType    │
└─────────────────────┘ └─────────────────┘ └─────────────────┘
```

## Data Flow

```
┌──────────────┐
│  CSV File    │
│  (Data)      │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│   CSVDataSource      │
│   • Read CSV         │
│   • Parse rows       │
│   • Create objects   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   RawContent[]       │
│   • id               │
│   • source_type      │
│   • content          │
│   • timestamp        │
│   • metadata         │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  SentimentAnalyzer   │
│  • Vectorize text    │
│  • Predict sentiment │
│  • Calculate scores  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  SentimentScore[]    │
│  • label             │
│  • score             │
│  • intensity         │
│  • compound_score    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Dashboard Views     │
│  • Metrics           │
│  • Charts            │
│  • Tables            │
└──────────────────────┘
```

## Page Structure

```
Dashboard Application
│
├── Home Page (app.py)
│   ├── Metrics Row
│   │   ├── Overall Sentiment
│   │   ├── Total Mentions
│   │   ├── Avg Confidence
│   │   └── Positive Rate
│   │
│   ├── Sentiment Distribution
│   │   ├── Pie Chart
│   │   └── Breakdown Table
│   │
│   ├── Trend Analysis
│   │   ├── Daily Sentiment Counts
│   │   └── Compound Score Over Time
│   │
│   ├── Source Analysis
│   │   ├── Mentions by Source
│   │   └── Sentiment by Source
│   │
│   ├── Keyword Analysis
│   │   └── Top Hashtags
│   │
│   └── Recent Mentions
│       └── Expandable Cards
│
├── Analytics Page
│   ├── Hourly Patterns
│   ├── Score Distribution
│   ├── Confidence vs Intensity
│   ├── Source Comparison
│   ├── Daily Trends
│   └── Statistical Summary
│
├── Data Explorer Page
│   ├── Search & Filter
│   ├── Data Table
│   ├── Export Button
│   └── Detailed View
│
└── Data Ingestion Page
    ├── CSV Upload Tab
    ├── Batch Ingestion Tab
    └── History Tab
```

## Class Diagram

```
┌─────────────────────────┐
│   CSVDataSource         │
├─────────────────────────┤
│ - csv_path: str         │
│ - source_type: SourceType│
├─────────────────────────┤
│ + fetch_content()       │
│ + get_source_type()     │
└───────────┬─────────────┘
            │ creates
            ▼
┌─────────────────────────┐
│   RawContent            │
├─────────────────────────┤
│ - id: str               │
│ - source_type: SourceType│
│ - content: str          │
│ - author: str           │
│ - timestamp: datetime   │
│ - metadata: dict        │
└───────────┬─────────────┘
            │ analyzed by
            ▼
┌─────────────────────────┐
│ SentimentAnalyzer       │
├─────────────────────────┤
│ - model                 │
│ - vectorizer            │
├─────────────────────────┤
│ + analyze(text)         │
└───────────┬─────────────┘
            │ produces
            ▼
┌─────────────────────────┐
│   SentimentScore        │
├─────────────────────────┤
│ - label: SentimentLabel │
│ - score: float          │
│ - intensity: float      │
│ - compound_score: float │
└─────────────────────────┘
```

## Interaction Flow

```
User Action → Dashboard → Service → Model → Result → Visualization

Example: View Sentiment Trend
│
├─ User selects date range
│  └─> Dashboard filters data
│      └─> CSVDataSource.fetch_content(since=date)
│          └─> Returns RawContent[]
│              └─> SentimentAnalyzer.analyze(content)
│                  └─> Returns SentimentScore[]
│                      └─> Dashboard creates time series
│                          └─> Plotly renders chart
│                              └─> User sees visualization
```

## State Management

```
┌─────────────────────────────────────────┐
│         Streamlit Session State         │
├─────────────────────────────────────────┤
│                                         │
│  Cached Data (@st.cache_data)          │
│  ├── raw_content: List[RawContent]     │
│  ├── analyzed_data: List[Dict]         │
│  └── filtered_data: List[Dict]         │
│                                         │
│  Cached Resources (@st.cache_resource) │
│  ├── sentiment_analyzer                │
│  └── csv_source                        │
│                                         │
│  User Inputs (Widgets)                 │
│  ├── date_range: Tuple[date, date]    │
│  ├── source_filter: List[str]         │
│  ├── search_query: str                │
│  └── data_limit: int                  │
│                                         │
└─────────────────────────────────────────┘
```

## Performance Optimization

```
┌─────────────────────────────────────────┐
│         Optimization Strategy           │
├─────────────────────────────────────────┤
│                                         │
│  1. Data Loading                       │
│     └─> @st.cache_data(ttl=3600)      │
│         • Cache for 1 hour             │
│         • Invalidate on param change   │
│                                         │
│  2. Model Loading                      │
│     └─> @st.cache_resource             │
│         • Load once per session        │
│         • Reuse across requests        │
│                                         │
│  3. Data Filtering                     │
│     └─> Apply filters early            │
│         • Date range first             │
│         • Source filter second         │
│         • Text search last             │
│                                         │
│  4. Visualization                      │
│     └─> Limit data points              │
│         • Max 5000 records             │
│         • Aggregate when needed        │
│         • Use efficient chart types    │
│                                         │
└─────────────────────────────────────────┘
```

## Error Handling

```
┌─────────────────────────────────────────┐
│          Error Handling Flow            │
├─────────────────────────────────────────┤
│                                         │
│  Data Loading Errors                   │
│  ├── File not found                    │
│  │   └─> Display error message         │
│  │       └─> Suggest valid path        │
│  │                                      │
│  ├── Invalid format                    │
│  │   └─> Show format requirements      │
│  │       └─> Provide example           │
│  │                                      │
│  └── Empty dataset                     │
│      └─> Display warning               │
│          └─> Suggest alternatives      │
│                                         │
│  Model Errors                          │
│  ├── Model not found                   │
│  │   └─> Fallback to VADER             │
│  │       └─> Show warning              │
│  │                                      │
│  └── Analysis failure                  │
│      └─> Skip record                   │
│          └─> Continue processing       │
│                                         │
│  UI Errors                             │
│  ├── Invalid input                     │
│  │   └─> Validate and show message    │
│  │                                      │
│  └── Chart rendering                   │
│      └─> Show placeholder              │
│          └─> Log error                 │
│                                         │
└─────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Development Environment         │
├─────────────────────────────────────────┤
│                                         │
│  Local Machine                         │
│  ├── Python 3.10+                      │
│  ├── Streamlit                         │
│  ├── Dependencies                      │
│  └── Data files                        │
│                                         │
│  Run: streamlit run app.py            │
│  Access: http://localhost:8501         │
│                                         │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Production Environment           │
├─────────────────────────────────────────┤
│                                         │
│  Option 1: Streamlit Cloud             │
│  ├── GitHub integration                │
│  ├── Auto deployment                   │
│  └── Free hosting                      │
│                                         │
│  Option 2: Docker Container            │
│  ├── Dockerfile                        │
│  ├── Docker Compose                    │
│  └── Cloud deployment                  │
│                                         │
│  Option 3: Traditional Server          │
│  ├── Nginx reverse proxy               │
│  ├── Systemd service                   │
│  └── SSL certificate                   │
│                                         │
└─────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────┐
│          Technology Stack               │
├─────────────────────────────────────────┤
│                                         │
│  Frontend                              │
│  ├── Streamlit 1.29.0                 │
│  ├── Plotly 5.18.0                    │
│  └── Custom CSS                        │
│                                         │
│  Backend                               │
│  ├── Python 3.10+                      │
│  ├── Pandas 2.1.4                      │
│  └── NumPy 1.26.2                      │
│                                         │
│  ML/NLP                                │
│  ├── Scikit-learn 1.7.2               │
│  ├── NLTK 3.8.1                        │
│  └── Custom trained models             │
│                                         │
│  Data Processing                       │
│  ├── CSV parsing                       │
│  ├── Date/time handling                │
│  └── Text processing                   │
│                                         │
└─────────────────────────────────────────┘
```

## Security Considerations

```
┌─────────────────────────────────────────┐
│          Security Measures              │
├─────────────────────────────────────────┤
│                                         │
│  Input Validation                      │
│  ├── File path validation              │
│  ├── Data limit constraints            │
│  └── Query sanitization                │
│                                         │
│  Data Protection                       │
│  ├── No sensitive data in logs         │
│  ├── Secure file handling              │
│  └── Memory cleanup                    │
│                                         │
│  Access Control (Future)               │
│  ├── User authentication               │
│  ├── Role-based access                 │
│  └── API key management                │
│                                         │
└─────────────────────────────────────────┘
```

## Scalability

```
Current Capacity:
├── Data: Up to 5,000 records per load
├── Users: Single user (local)
├── Refresh: Manual
└── Storage: In-memory

Future Scaling:
├── Data: Database integration (PostgreSQL)
├── Users: Multi-user with authentication
├── Refresh: Real-time streaming
└── Storage: Persistent with caching layer
```
