# Vibe Optimizer Dashboard - Complete Guide

## Overview

The Vibe Optimizer Dashboard is a comprehensive Streamlit-based web application for real-time sentiment analysis and brand monitoring. It integrates with the ingestion and analysis services to provide interactive visualizations and insights.

## Features Implemented

### ✅ Main Dashboard (Home Page)
- **Real-time Metrics Display**
  - Overall sentiment with visual indicators
  - Total mentions count
  - Average confidence scores
  - Positive rate percentage

- **Sentiment Distribution**
  - Interactive pie chart
  - Detailed breakdown with percentages
  - Color-coded visualization

- **Trend Analysis**
  - Daily sentiment counts over time
  - Compound score tracking
  - Time-series line charts

- **Source Analysis**
  - Mentions by platform (Twitter, Reddit, Reviews)
  - Sentiment breakdown by source
  - Comparative bar charts

- **Keyword Analysis**
  - Top 10 hashtags visualization
  - Frequency counts
  - Horizontal bar chart

- **Recent Mentions Browser**
  - Expandable mention cards
  - Sentiment filtering
  - Full metadata display
  - Adjustable display count

### ✅ Analytics Page
- **Hourly Patterns**
  - Sentiment distribution by hour of day
  - Identify peak engagement times
  - Multi-line time series

- **Score Distribution**
  - Histogram of compound scores
  - Box plots by sentiment
  - Statistical analysis

- **Confidence vs Intensity**
  - Scatter plot analysis
  - Correlation visualization
  - Quality assessment

- **Source Comparison**
  - Average metrics by platform
  - Grouped bar charts
  - Performance comparison

- **Daily Trends**
  - Sentiment trend with volume overlay
  - Dual-axis visualization
  - Moving averages

- **Statistical Summary**
  - Mean, median, standard deviation
  - Comprehensive metrics
  - Three-column layout

### ✅ Data Explorer Page
- **Advanced Search & Filtering**
  - Text search in content
  - Source filtering
  - Date range filtering
  - Real-time results

- **Interactive Data Table**
  - Customizable columns
  - Sortable and searchable
  - Responsive design
  - Pagination support

- **Export Functionality**
  - CSV download
  - Filtered data export
  - Timestamped filenames

- **Detailed Record View**
  - Full content display
  - Complete metadata
  - Sentiment analysis results
  - Two-column layout

### ✅ Data Ingestion Page
- **CSV Upload**
  - Drag-and-drop file upload
  - Data preview
  - Column validation
  - Configurable ingestion options

- **Batch Ingestion**
  - Process existing datasets
  - Date filtering
  - Keyword search
  - Progress tracking

- **Ingestion Statistics**
  - Record counts
  - Source distribution
  - Date range analysis
  - Success metrics

- **Ingestion History**
  - Recent ingestion jobs
  - Status tracking
  - Overall statistics

## Architecture

### Integration with Services

```
Dashboard (Streamlit)
    ├── Ingestion Service
    │   ├── CSVDataSource
    │   └── fetch_content()
    │
    ├── Analysis Service
    │   ├── TrainedSentimentAnalyzer
    │   ├── VaderSentimentAnalyzer (fallback)
    │   └── analyze()
    │
    └── Core Models
        ├── RawContent
        ├── SentimentScore
        └── SentimentLabel
```

### File Structure

```
src/dashboard/
├── app.py                          # Main dashboard (Home)
├── config.py                       # Configuration settings
├── utils.py                        # Utility functions
├── run_dashboard.py                # Quick start script
├── __init__.py                     # Module init
├── README.md                       # Dashboard documentation
└── pages/
    ├── 1_📊_Analytics.py          # Advanced analytics
    ├── 2_🔍_Data_Explorer.py      # Data exploration
    └── 3_⚙️_Data_Ingestion.py     # Data ingestion
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- streamlit==1.29.0
- plotly==5.18.0
- pandas==2.1.4
- numpy==1.26.2

### 2. Verify Data

Ensure the data file exists:
```bash
ls data/sentimentdataset.csv
```

### 3. Train Model (Optional)

For best results, train the sentiment model:
```bash
python src/analysis/model_trainer.py
```

The dashboard will fallback to VADER if the trained model is unavailable.

### 4. Test Components

Run the test script:
```bash
python test_dashboard.py
```

## Running the Dashboard

### Method 1: Direct Streamlit Command

```bash
streamlit run src/dashboard/app.py
```

### Method 2: Quick Start Script

```bash
python src/dashboard/run_dashboard.py
```

### Method 3: Custom Configuration

```bash
streamlit run src/dashboard/app.py --server.port 8502 --server.address localhost
```

The dashboard will open at `http://localhost:8501` (or your specified port).

## Usage Guide

### Main Dashboard

1. **Configure Data Source**
   - Open sidebar
   - Set CSV path (default: `data/sentimentdataset.csv`)
   - Adjust data limit (100-5000 records)

2. **Apply Filters**
   - Select date range
   - Choose data sources (Twitter, Reddit, Reviews)
   - Enter search keywords

3. **View Metrics**
   - Overall sentiment at the top
   - Scroll for detailed visualizations
   - Hover over charts for details

4. **Browse Mentions**
   - Scroll to "Recent Mentions"
   - Filter by sentiment
   - Expand cards for full details

### Analytics Page

1. Navigate to "📊 Analytics" in sidebar
2. Explore hourly patterns for optimal posting times
3. Analyze score distributions for data quality
4. Compare sources to identify best platforms
5. Review statistical summaries

### Data Explorer

1. Navigate to "🔍 Data Explorer"
2. Use search box to find specific content
3. Apply filters (source, date)
4. Select columns to display
5. Download filtered results as CSV
6. Click records for detailed view

### Data Ingestion

1. Navigate to "⚙️ Data Ingestion"
2. **CSV Upload Tab:**
   - Upload new CSV file
   - Preview data
   - Configure options
   - Start ingestion
3. **Batch Ingestion Tab:**
   - Set file path
   - Configure filters
   - Run batch process
4. **History Tab:**
   - View recent ingestions
   - Check statistics

## Configuration

### Dashboard Settings (config.py)

```python
DEFAULT_CSV_PATH = "data/sentimentdataset.csv"
DEFAULT_DATA_LIMIT = 1000
MAX_DATA_LIMIT = 5000
MODEL_PATH = "models/sentiment_model.pkl"
FALLBACK_TO_VADER = True
```

### Color Scheme

```python
SENTIMENT_COLORS = {
    'positive': '#00CC96',  # Green
    'neutral': '#FFA15A',   # Orange
    'negative': '#EF553B'   # Red
}
```

### Performance Settings

```python
CACHE_TTL = 3600  # 1 hour cache
MAX_DISPLAY_RECORDS = 100
```

## Utility Functions

The `utils.py` module provides:

- `calculate_sentiment_distribution()` - Aggregate sentiment counts
- `create_time_series_df()` - Convert to time series DataFrame
- `extract_hashtags()` - Extract and count hashtags
- `get_sentiment_emoji()` - Get emoji for sentiment
- `export_to_csv()` - Export data to CSV
- `detect_sentiment_shift()` - Detect significant changes
- `format_large_number()` - Format with K/M suffixes

## Troubleshooting

### Issue: "Could not initialize sentiment analyzer"

**Solution:**
1. Train the model: `python src/analysis/model_trainer.py`
2. Verify model file: `models/sentiment_model.pkl`
3. Dashboard will use VADER as fallback

### Issue: "No data loaded"

**Solution:**
1. Check CSV path in sidebar
2. Verify file exists: `ls data/sentimentdataset.csv`
3. Check file format matches expected structure
4. Try reducing data limit

### Issue: Slow performance

**Solution:**
1. Reduce data limit in sidebar
2. Apply date range filters
3. Filter by specific sources
4. Clear Streamlit cache: `Ctrl+C` and restart

### Issue: Charts not displaying

**Solution:**
1. Check browser console for errors
2. Verify plotly is installed: `pip install plotly`
3. Try different browser
4. Clear browser cache

### Issue: Import errors

**Solution:**
1. Verify all dependencies: `pip install -r requirements.txt`
2. Check Python version (3.8+)
3. Ensure src is in Python path

## Data Format

Expected CSV columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| Timestamp | datetime | Yes | Format: YYYY-MM-DD HH:MM:SS |
| Text | string | Yes | Content text |
| Platform | string | Yes | twitter, reddit, etc. |
| User | string | No | Author username |
| Hashtags | string | No | Comma-separated |
| Sentiment | string | No | Original label |
| Retweets | float | No | Engagement metric |
| Likes | float | No | Engagement metric |
| Country | string | No | Location |

## Customization

### Adding New Visualizations

Edit `app.py`:

```python
import plotly.express as px

# Create your chart
fig = px.scatter(df, x='x_col', y='y_col', color='category')

# Display
st.plotly_chart(fig, use_container_width=True)
```

### Creating New Pages

Add file to `pages/`:

```python
# src/dashboard/pages/4_🎯_My_Page.py
import streamlit as st

st.set_page_config(page_title="My Page", page_icon="🎯")
st.title("🎯 My Custom Page")

# Your code here
```

### Custom Styling

Add CSS in `app.py`:

```python
st.markdown("""
<style>
    .custom-class {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
```

## Performance Optimization

### Caching

Use Streamlit caching decorators:

```python
@st.cache_data(ttl=3600)
def load_data(path):
    # Expensive operation
    return data

@st.cache_resource
def get_analyzer():
    # Resource initialization
    return analyzer
```

### Data Limits

- Default: 1000 records
- Maximum: 5000 records
- Adjust based on performance

### Filtering

Apply filters early to reduce data processing:
1. Date range first
2. Source filter second
3. Text search last

## Future Enhancements

Potential additions:

- [ ] Real-time data streaming with WebSocket
- [ ] Alert system for sentiment changes
- [ ] Topic modeling visualization
- [ ] Multi-brand comparison
- [ ] PDF report generation
- [ ] User authentication
- [ ] Database integration (PostgreSQL)
- [ ] Scheduled data refresh
- [ ] Email notifications
- [ ] API endpoint integration
- [ ] Custom dashboard layouts
- [ ] Advanced filtering options
- [ ] Sentiment prediction
- [ ] Anomaly detection

## API Integration

To add live API sources:

1. Configure credentials in `.env`:
```env
TWITTER_API_KEY=your_key
REDDIT_CLIENT_ID=your_id
```

2. Update ingestion service:
```python
from src.ingestion.sources.twitter_source import TwitterSource

twitter = TwitterSource(api_key=os.getenv('TWITTER_API_KEY'))
content = twitter.fetch_content(query="brand", limit=100)
```

3. Add refresh button in dashboard:
```python
if st.button("🔄 Refresh Data"):
    # Fetch new data
    new_data = fetch_from_api()
    st.success(f"Loaded {len(new_data)} new records")
```

## Testing

Run comprehensive tests:

```bash
# Test dashboard components
python test_dashboard.py

# Test with pytest
pytest tests/test_dashboard.py -v

# Test specific page
streamlit run src/dashboard/pages/1_📊_Analytics.py
```

## Deployment

### Local Network

```bash
streamlit run src/dashboard/app.py --server.address 0.0.0.0
```

Access from other devices: `http://your-ip:8501`

### Streamlit Cloud

1. Push to GitHub
2. Connect at share.streamlit.io
3. Deploy from repository

### Docker

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "src/dashboard/app.py"]
```

## Support

For issues:
1. Check this guide
2. Review error messages in terminal
3. Check Streamlit logs
4. Verify data format
5. Test with smaller dataset

## Summary

The dashboard is fully functional with:
- ✅ 4 pages (Home, Analytics, Explorer, Ingestion)
- ✅ 15+ interactive visualizations
- ✅ Real-time sentiment analysis
- ✅ Advanced filtering and search
- ✅ Data export capabilities
- ✅ Comprehensive documentation
- ✅ Utility functions
- ✅ Configuration management
- ✅ Error handling
- ✅ Performance optimization

Ready to use with: `streamlit run src/dashboard/app.py`
