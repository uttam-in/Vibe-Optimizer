# Dashboard Quick Start

## 🚀 Start Dashboard

```bash
streamlit run src/dashboard/app.py
```

Or use the helper script:
```bash
python src/dashboard/run_dashboard.py
```

## 📋 Pages

| Page | Icon | Purpose |
|------|------|---------|
| Home | 📊 | Main dashboard with metrics and trends |
| Analytics | 📊 | Advanced analytics and patterns |
| Data Explorer | 🔍 | Search, filter, and export data |
| Data Ingestion | ⚙️ | Upload and process new data |

## ⚙️ Configuration

### Sidebar Settings
- **CSV Data Path**: Path to your data file
- **Data Limit**: Number of records to load (100-5000)
- **Date Range**: Filter by start/end dates
- **Data Sources**: Select platforms to include
- **Search Keywords**: Filter by text

## 🎯 Common Tasks

### View Overall Sentiment
1. Open dashboard
2. Check top metrics row
3. View sentiment distribution pie chart

### Analyze Trends
1. Scroll to "Sentiment Trend Over Time"
2. Hover over chart for details
3. Check compound score graph

### Search Content
1. Go to "🔍 Data Explorer" page
2. Enter search text
3. Apply filters
4. View results in table

### Export Data
1. Go to "🔍 Data Explorer"
2. Apply desired filters
3. Click "📥 Download as CSV"

### Upload New Data
1. Go to "⚙️ Data Ingestion"
2. Click "📁 CSV Upload" tab
3. Upload file
4. Configure options
5. Click "🚀 Start Ingestion"

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| No data loaded | Check CSV path in sidebar |
| Analyzer error | Run `python src/analysis/model_trainer.py` |
| Slow performance | Reduce data limit or apply filters |
| Import errors | Run `pip install -r requirements.txt` |

## 📊 Key Metrics

- **Overall Sentiment**: Dominant sentiment (Positive/Neutral/Negative)
- **Total Mentions**: Number of records analyzed
- **Avg Confidence**: Average prediction confidence
- **Positive Rate**: Percentage of positive mentions

## 🎨 Color Coding

- 🟢 **Green**: Positive sentiment
- 🟡 **Yellow**: Neutral sentiment
- 🔴 **Red**: Negative sentiment

## 💡 Tips

- Use date filters to focus on recent data
- Check hourly patterns in Analytics page
- Export filtered data for external analysis
- Monitor sentiment shifts in trend charts
- Use search to find specific topics

## 📚 More Info

- Full guide: `DASHBOARD_GUIDE.md`
- Dashboard README: `src/dashboard/README.md`
- Test components: `python test_dashboard.py`
