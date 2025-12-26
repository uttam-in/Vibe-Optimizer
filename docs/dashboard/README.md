# Vibe Optimizer Dashboard

A comprehensive Streamlit dashboard for sentiment analysis and brand monitoring.

## Features

### Main Dashboard (Home)
- **Real-time Metrics**: Overall sentiment, total mentions, confidence scores
- **Sentiment Distribution**: Visual breakdown with pie charts
- **Trend Analysis**: Time-series sentiment tracking
- **Source Analysis**: Compare sentiment across different platforms
- **Top Keywords**: Identify trending hashtags and topics
- **Recent Mentions**: Browse and filter recent content

### Analytics Page
- **Hourly Patterns**: Discover sentiment trends by time of day
- **Score Distribution**: Statistical analysis of sentiment scores
- **Confidence vs Intensity**: Correlation analysis
- **Source Comparison**: Compare metrics across data sources
- **Daily Trends**: Track sentiment changes over time
- **Statistical Summary**: Comprehensive statistics

### Data Explorer
- **Advanced Search**: Filter by text, source, and date
- **Data Table**: Interactive table with customizable columns
- **Export**: Download filtered data as CSV
- **Detailed View**: Inspect individual records

### Data Ingestion
- **CSV Upload**: Upload and process new data files
- **Batch Ingestion**: Process existing datasets
- **Ingestion History**: Track ingestion jobs (coming soon)

## Installation

1. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Verify the sentiment model is trained:
```bash
python src/analysis/model_trainer.py
```

## Running the Dashboard

### Start the dashboard:
```bash
streamlit run src/dashboard/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Alternative: Run with custom port
```bash
streamlit run src/dashboard/app.py --server.port 8502
```

## Configuration

### Data Source
By default, the dashboard loads data from `data/sentimentdataset.csv`. You can change this in the sidebar:
- Navigate to the sidebar
- Update the "CSV Data Path" field
- Adjust the "Data Limit" slider

### Filters
- **Date Range**: Filter data by start and end dates
- **Data Sources**: Select specific platforms (Twitter, Reddit, Reviews)
- **Search Keywords**: Filter content by text search

## Usage Guide

### 1. Main Dashboard
- View overall sentiment metrics at the top
- Scroll down to see sentiment distribution and trends
- Use filters in the sidebar to focus on specific data
- Expand recent mentions to see full details

### 2. Analytics
- Navigate to "📊 Analytics" in the sidebar
- Explore hourly patterns to find optimal posting times
- Analyze score distributions for data quality insights
- Compare sources to identify best-performing platforms

### 3. Data Explorer
- Navigate to "🔍 Data Explorer"
- Use search and filters to find specific content
- Select columns to display in the table
- Download filtered results as CSV
- Click on records for detailed view

### 4. Data Ingestion
- Navigate to "⚙️ Data Ingestion"
- Upload new CSV files in the "CSV Upload" tab
- Run batch ingestion from existing files
- Monitor ingestion history

## Data Format

The dashboard expects CSV files with the following columns:
- `Timestamp`: Date and time (format: YYYY-MM-DD HH:MM:SS)
- `Text`: Content text
- `Platform`: Source platform (twitter, reddit, etc.)
- `User`: Author username (optional)
- `Hashtags`: Comma-separated hashtags (optional)
- `Sentiment`: Original sentiment label (optional)
- `Retweets`, `Likes`: Engagement metrics (optional)

## Troubleshooting

### Model Not Found
If you see "Could not initialize sentiment analyzer":
1. Train the model: `python src/analysis/model_trainer.py`
2. Verify model file exists: `models/sentiment_model.pkl`
3. The dashboard will fallback to VADER if trained model is unavailable

### Data Loading Issues
- Verify CSV file path is correct
- Check CSV format matches expected structure
- Ensure timestamps are in correct format
- Try reducing the data limit

### Performance Issues
- Reduce the data limit in sidebar
- Filter by date range to load less data
- Close unused browser tabs
- Restart the Streamlit server

## Architecture

The dashboard integrates with:
- **Ingestion Service** (`src/ingestion/`): Loads data from CSV and APIs
- **Analysis Service** (`src/analysis/`): Performs sentiment analysis
- **Core Models** (`src/core/`): Data structures and interfaces

## Customization

### Adding New Visualizations
Edit `src/dashboard/app.py` and add new Plotly charts:
```python
import plotly.express as px

fig = px.bar(data, x='category', y='value')
st.plotly_chart(fig, use_container_width=True)
```

### Creating New Pages
Add new files to `src/dashboard/pages/`:
```python
# src/dashboard/pages/4_🎯_My_Page.py
import streamlit as st

st.title("My Custom Page")
# Your code here
```

### Styling
Modify the CSS in `app.py`:
```python
st.markdown("""
<style>
    .custom-class {
        /* Your styles */
    }
</style>
""", unsafe_allow_html=True)
```

## API Integration

To integrate with live APIs (Twitter, Reddit):
1. Configure API credentials in `.env`
2. Update ingestion service to use API sources
3. Implement real-time data refresh in dashboard

## Future Enhancements

- [ ] Real-time data streaming
- [ ] Alert notifications for sentiment changes
- [ ] Topic modeling visualization
- [ ] Comparative brand analysis
- [ ] Export reports as PDF
- [ ] User authentication
- [ ] Database integration
- [ ] Scheduled data refresh

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main project README
3. Check logs in the terminal running Streamlit
