"""
Data Ingestion Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.ingestion.ingestion_service import CSVDataSource, IngestionService
from src.core.models import SourceType

st.set_page_config(page_title="Data Ingestion", page_icon="⚙️", layout="wide")

st.title("⚙️ Data Ingestion")
st.markdown("Ingest and process data from various sources")

# Tabs for different ingestion methods
tab1, tab2, tab3 = st.tabs(["📁 CSV Upload", "🔄 Batch Ingestion", "📊 Ingestion History"])

with tab1:
    st.header("Upload CSV File")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            temp_path = f"data/temp_{uploaded_file.name}"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Preview data
            st.subheader("Data Preview")
            df = pd.read_csv(temp_path)
            st.dataframe(df.head(10), use_container_width=True)
            
            st.write(f"**Total rows:** {len(df)}")
            st.write(f"**Columns:** {', '.join(df.columns)}")
            
            # Ingestion options
            st.subheader("Ingestion Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                limit = st.number_input("Number of records to ingest", min_value=1, max_value=len(df), value=min(1000, len(df)))
            
            with col2:
                source_type = st.selectbox("Source Type", ["Twitter", "Reddit", "Reviews"])
            
            search_query = st.text_input("Filter by keyword (optional)", "")
            
            if st.button("🚀 Start Ingestion", type="primary"):
                with st.spinner("Ingesting data..."):
                    try:
                        # Map source type
                        source_map = {
                            'Twitter': SourceType.TWITTER,
                            'Reddit': SourceType.REDDIT,
                            'Reviews': SourceType.REVIEWS
                        }
                        
                        # Create data source
                        csv_source = CSVDataSource(temp_path, source_map[source_type])
                        content = csv_source.fetch_content(query=search_query, limit=limit)
                        
                        st.success(f"✅ Successfully ingested {len(content)} records!")
                        
                        # Show sample
                        st.subheader("Sample Ingested Data")
                        for i, item in enumerate(content[:5]):
                            with st.expander(f"Record {i+1}: {item.content[:50]}..."):
                                st.write(f"**ID:** {item.id}")
                                st.write(f"**Source:** {item.source_type.value}")
                                st.write(f"**Content:** {item.content}")
                                st.write(f"**Author:** {item.author}")
                                st.write(f"**Timestamp:** {item.timestamp}")
                    
                    except Exception as e:
                        st.error(f"Error during ingestion: {e}")
        
        except Exception as e:
            st.error(f"Error processing file: {e}")

with tab2:
    st.header("Batch Ingestion from Existing Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_path = st.text_input("CSV File Path", "data/sentimentdataset.csv")
    
    with col2:
        batch_limit = st.number_input("Batch Size", min_value=10, max_value=10000, value=1000, step=100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        since_date = st.date_input("Ingest data since", value=datetime.now() - timedelta(days=30))
    
    with col2:
        batch_query = st.text_input("Search query", "")
    
    if st.button("🔄 Run Batch Ingestion", type="primary"):
        with st.spinner("Running batch ingestion..."):
            try:
                csv_source = CSVDataSource(csv_path)
                since_dt = datetime.combine(since_date, datetime.min.time())
                content = csv_source.fetch_content(query=batch_query, since=since_dt, limit=batch_limit)
                
                st.success(f"✅ Batch ingestion complete! Processed {len(content)} records")
                
                # Statistics
                st.subheader("Ingestion Statistics")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Records", len(content))
                
                with col2:
                    sources = set([c.source_type.value for c in content])
                    st.metric("Unique Sources", len(sources))
                
                with col3:
                    authors = set([c.author for c in content if c.author])
                    st.metric("Unique Authors", len(authors))
                
                # Timeline
                if content:
                    timestamps = [c.timestamp for c in content]
                    st.write(f"**Date Range:** {min(timestamps).date()} to {max(timestamps).date()}")
                    
                    # Distribution by source
                    source_counts = {}
                    for c in content:
                        source_counts[c.source_type.value] = source_counts.get(c.source_type.value, 0) + 1
                    
                    st.subheader("Distribution by Source")
                    for source, count in source_counts.items():
                        st.write(f"**{source.title()}:** {count} records")
            
            except Exception as e:
                st.error(f"Error during batch ingestion: {e}")

with tab3:
    st.header("Ingestion History")
    
    st.info("Ingestion history tracking coming soon!")
    
    # Placeholder for history
    st.subheader("Recent Ingestions")
    
    history_data = {
        'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(5)],
        'Source': ['CSV', 'Twitter API', 'Reddit API', 'CSV', 'Reviews'],
        'Records': [1000, 250, 180, 500, 320],
        'Status': ['✅ Success', '✅ Success', '⚠️ Partial', '✅ Success', '✅ Success']
    }
    
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, use_container_width=True)
    
    # Stats
    st.subheader("Overall Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Ingestions", "47")
    
    with col2:
        st.metric("Total Records", "23,450")
    
    with col3:
        st.metric("Success Rate", "94.5%")
    
    with col4:
        st.metric("Avg Batch Size", "498")

# Footer
st.markdown("---")
st.markdown("*Configure data sources and ingestion schedules in the settings*")
