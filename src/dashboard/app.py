"""
Streamlit dashboard application.
Single Responsibility: Visualize data and insights.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


st.set_page_config(
    page_title="Vibe Optimizer Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Vibe Optimizer Dashboard")
st.markdown("Real-time brand sentiment and insights")

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=7), datetime.now())
)
source_filter = st.sidebar.multiselect(
    "Data Sources",
    ["Twitter", "Reddit", "Reviews"]
)

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Overall Sentiment", "Positive", "+5%")

with col2:
    st.metric("Total Mentions", "1,234", "+12%")

with col3:
    st.metric("Sentiment Score", "7.8/10", "+0.3")

# Sentiment over time chart
st.subheader("Sentiment Trend")
# Placeholder for chart

# Top topics
st.subheader("Top Topics")
# Placeholder for topics

# Recent insights
st.subheader("Recent Insights")
# Placeholder for insights
