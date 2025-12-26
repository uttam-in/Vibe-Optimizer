"""
Data Explorer Page
"""
import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.ingestion.ingestion_service import CSVDataSource
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer, VaderSentimentAnalyzer

st.set_page_config(page_title="Data Explorer", page_icon="🔍", layout="wide")

st.title("🔍 Data Explorer")
st.markdown("Explore and search through your data")

@st.cache_data
def load_data(csv_path: str, limit: int = 1000):
    try:
        csv_source = CSVDataSource(csv_path)
        return csv_source.fetch_content(limit=limit)
    except Exception as e:
        st.error(f"Error: {e}")
        return []

@st.cache_resource
def get_analyzer():
    try:
        return TrainedSentimentAnalyzer()
    except:
        try:
            return VaderSentimentAnalyzer()
        except:
            return None

# Sidebar
csv_path = st.sidebar.text_input("CSV Path", "data/sentimentdataset.csv")
limit = st.sidebar.slider("Data Limit", 100, 5000, 1000, 100)

# Load data
raw_content = load_data(csv_path, limit)
analyzer = get_analyzer()

if not raw_content or not analyzer:
    st.warning("Unable to load data or analyzer")
    st.stop()

# Search and filter
st.header("🔎 Search & Filter")

col1, col2, col3 = st.columns(3)

with col1:
    search_text = st.text_input("Search in content", "")

with col2:
    source_filter = st.multiselect(
        "Filter by source",
        options=list(set([c.source_type.value for c in raw_content])),
        default=[]
    )

with col3:
    date_filter = st.date_input(
        "Filter by date",
        value=[]
    )

# Apply filters
filtered = raw_content

if search_text:
    filtered = [c for c in filtered if search_text.lower() in c.content.lower()]

if source_filter:
    filtered = [c for c in filtered if c.source_type.value in source_filter]

if date_filter:
    if len(date_filter) == 2:
        start, end = date_filter
        filtered = [c for c in filtered if start <= c.timestamp.date() <= end]

st.info(f"Showing {len(filtered)} of {len(raw_content)} records")

# Analyze filtered data
with st.spinner("Analyzing..."):
    analyzed = []
    for content in filtered[:100]:  # Limit to 100 for performance
        try:
            sentiment = analyzer.analyze(content.content)
            analyzed.append({
                'Timestamp': content.timestamp,
                'Source': content.source_type.value,
                'Author': content.author or 'Unknown',
                'Content': content.content[:100] + '...' if len(content.content) > 100 else content.content,
                'Sentiment': sentiment.label.value,
                'Confidence': f"{sentiment.score:.2%}",
                'Compound': f"{sentiment.compound_score:.2f}" if sentiment.compound_score else "N/A",
                'Full_Content': content.content
            })
        except:
            continue

# Display as table
if analyzed:
    df = pd.DataFrame(analyzed)
    
    # Display table
    st.header("📋 Data Table")
    
    # Column selection
    display_cols = st.multiselect(
        "Select columns to display",
        options=['Timestamp', 'Source', 'Author', 'Content', 'Sentiment', 'Confidence', 'Compound'],
        default=['Timestamp', 'Source', 'Content', 'Sentiment', 'Confidence']
    )
    
    if display_cols:
        st.dataframe(df[display_cols], use_container_width=True, height=400)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"sentiment_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Detailed view
    st.header("🔍 Detailed View")
    
    selected_idx = st.selectbox(
        "Select a record to view details",
        options=range(len(analyzed)),
        format_func=lambda x: f"{analyzed[x]['Timestamp']} - {analyzed[x]['Content']}"
    )
    
    if selected_idx is not None:
        record = analyzed[selected_idx]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Content")
            st.write(record['Full_Content'])
        
        with col2:
            st.subheader("Metadata")
            st.write(f"**Timestamp:** {record['Timestamp']}")
            st.write(f"**Source:** {record['Source']}")
            st.write(f"**Author:** {record['Author']}")
            st.write("---")
            st.write(f"**Sentiment:** {record['Sentiment'].title()}")
            st.write(f"**Confidence:** {record['Confidence']}")
            st.write(f"**Compound Score:** {record['Compound']}")
else:
    st.warning("No data to display")
