import streamlit as st
import requests
import json
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="SmartX AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        background: linear-gradient(90deg, #155dfc 0%, #9810fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .search-result {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 3px solid #155dfc;
    }
    .stButton>button {
        background: linear-gradient(135deg, #155dfc 0%, #9810fa 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'exa_results' not in st.session_state:
    st.session_state.exa_results = None

# Sidebar
with st.sidebar:
    st.image("https://www.figma.com/api/mcp/asset/fc4c77d4-b695-486f-8900-f9c169897790", width=80)
    st.title("SmartX AI Dashboard")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔍 AI Search", "📊 Analytics", "💡 Insights", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    st.metric("Active Projects", "12")
    st.metric("AI Queries Today", "47")
    st.metric("Success Rate", "94%")


# Main content area
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">Welcome to SmartX AI Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-Powered Intelligence Platform")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Searches", "1,234", "+12%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Code Contexts", "567", "+8%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("AI Insights", "89", "+15%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Users", "42", "+5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Recent Activity")
        activities = [
            {"time": "2 min ago", "action": "Web search completed", "query": "AI trends 2025"},
            {"time": "15 min ago", "action": "Code context retrieved", "query": "React hooks"},
            {"time": "1 hour ago", "action": "Analytics generated", "query": "User behavior"},
            {"time": "2 hours ago", "action": "Insight created", "query": "Market analysis"}
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div class="search-result">
                <strong>{activity['action']}</strong><br>
                <small>{activity['time']} • {activity['query']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Performance Overview")
        
        # Sample chart data
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range(start='2025-01-01', periods=7, freq='D')
        data = pd.DataFrame({
            'Date': dates,
            'Searches': np.random.randint(50, 150, 7),
            'Code Queries': np.random.randint(20, 80, 7)
        })
        
        st.line_chart(data.set_index('Date'))
        
        st.markdown("### 🎯 Top Categories")
        categories = {
            "AI & Machine Learning": 35,
            "Web Development": 28,
            "Data Science": 22,
            "Cloud Computing": 15
        }
        st.bar_chart(categories)


elif page == "🔍 AI Search":
    st.markdown('<h1 class="main-header">AI-Powered Search</h1>', unsafe_allow_html=True)
    st.markdown("### Search the web and get AI-enhanced results using Exa")
    
    # Search tabs
    tab1, tab2 = st.tabs(["🌐 Web Search", "💻 Code Context"])
    
    with tab1:
        st.markdown("#### Web Search with Exa")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input(
                "Enter your search query",
                placeholder="e.g., Latest AI trends in 2025",
                key="web_search"
            )
        with col2:
            num_results = st.number_input("Results", min_value=1, max_value=20, value=8)
        
        search_type = st.selectbox(
            "Search Type",
            ["auto", "fast", "deep"],
            help="auto: balanced, fast: quick results, deep: comprehensive"
        )
        
        if st.button("🔍 Search", key="search_btn"):
            if search_query:
                with st.spinner("Searching with Exa AI..."):
                    try:
                        # Note: In production, you'd call the Exa MCP tool here
                        # For demo purposes, showing the structure
                        st.session_state.search_history.append({
                            "query": search_query,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "web_search"
                        })
                        
                        # Simulated results structure
                        st.success(f"✅ Search completed for: '{search_query}'")
                        
                        st.markdown("### Search Results")
                        
                        # Demo results
                        demo_results = [
                            {
                                "title": "AI Trends 2025: What to Expect",
                                "url": "https://example.com/ai-trends-2025",
                                "snippet": "Explore the latest developments in artificial intelligence, including generative AI, autonomous systems, and ethical AI frameworks.",
                                "domain": "example.com"
                            },
                            {
                                "title": "The Future of Machine Learning",
                                "url": "https://example.com/ml-future",
                                "snippet": "Machine learning continues to evolve with new architectures, improved efficiency, and broader applications across industries.",
                                "domain": "example.com"
                            }
                        ]
                        
                        for i, result in enumerate(demo_results, 1):
                            st.markdown(f"""
                            <div class="search-result">
                                <h4>{i}. {result['title']}</h4>
                                <p>{result['snippet']}</p>
                                <small>🔗 <a href="{result['url']}" target="_blank">{result['domain']}</a></small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.info("💡 **Note**: This is a demo interface. In production, this would use the Exa MCP tool to fetch real-time search results.")
                        
                    except Exception as e:
                        st.error(f"Search failed: {str(e)}")
            else:
                st.warning("Please enter a search query")
    
    with tab2:
        st.markdown("#### Code Context Search with Exa")
        
        code_query = st.text_area(
            "Enter your code-related query",
            placeholder="e.g., React useState hook examples, Python pandas dataframe filtering",
            height=100
        )
        
        tokens = st.slider("Context Tokens", 1000, 50000, 5000, 1000)
        
        if st.button("🔍 Get Code Context", key="code_search_btn"):
            if code_query:
                with st.spinner("Fetching code context from Exa..."):
                    try:
                        st.session_state.search_history.append({
                            "query": code_query,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "code_context"
                        })
                        
                        st.success(f"✅ Code context retrieved for: '{code_query}'")
                        
                        st.markdown("### Code Context Results")
                        
                        # Demo code context
                        st.code("""
# Example: React useState Hook
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
        </div>
    );
}
                        """, language="javascript")
                        
                        st.markdown("""
                        **Context Summary:**
                        - useState is a React Hook for managing state in functional components
                        - Takes initial state as argument, returns [state, setState] array
                        - setState function triggers re-render when called
                        """)
                        
                        st.info("💡 **Note**: This is a demo. Production version would use Exa's code context API.")
                        
                    except Exception as e:
                        st.error(f"Code context retrieval failed: {str(e)}")
            else:
                st.warning("Please enter a code query")


elif page == "📊 Analytics":
    st.markdown('<h1 class="main-header">Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2025, 1, 1))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    st.markdown("---")
    
    # Analytics metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Search Volume")
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
        search_data = pd.DataFrame({
            'Date': dates,
            'Volume': np.random.randint(100, 300, 30)
        })
        st.line_chart(search_data.set_index('Date'))
    
    with col2:
        st.markdown("### Query Types")
        query_types = {
            "Web Search": 45,
            "Code Context": 30,
            "Documentation": 15,
            "Other": 10
        }
        st.bar_chart(query_types)
    
    with col3:
        st.markdown("### Response Times")
        response_data = pd.DataFrame({
            'Time': ['< 1s', '1-2s', '2-3s', '> 3s'],
            'Count': [120, 80, 30, 10]
        })
        st.bar_chart(response_data.set_index('Time'))
    
    st.markdown("---")
    
    st.markdown("### 📈 Detailed Analytics")
    
    # Sample detailed data
    analytics_data = pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=10, freq='D'),
        'Searches': np.random.randint(50, 150, 10),
        'Code Queries': np.random.randint(20, 80, 10),
        'Success Rate': np.random.uniform(0.85, 0.98, 10),
        'Avg Response Time (s)': np.random.uniform(0.5, 2.5, 10)
    })
    
    st.dataframe(analytics_data, use_container_width=True)

elif page == "💡 Insights":
    st.markdown('<h1 class="main-header">AI Insights</h1>', unsafe_allow_html=True)
    st.markdown("### Discover trends and patterns in your data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 Trending Topics")
        trends = [
            {"topic": "Generative AI", "growth": "+45%", "queries": 234},
            {"topic": "LLM Fine-tuning", "growth": "+38%", "queries": 189},
            {"topic": "AI Ethics", "growth": "+32%", "queries": 156},
            {"topic": "Edge AI", "growth": "+28%", "queries": 142},
            {"topic": "AI Agents", "growth": "+25%", "queries": 128}
        ]
        
        for trend in trends:
            st.markdown(f"""
            <div class="search-result">
                <strong>{trend['topic']}</strong>
                <span style="color: #155dfc; float: right;">{trend['growth']}</span><br>
                <small>{trend['queries']} queries this week</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💡 Key Insights")
        insights = [
            {
                "title": "Peak Usage Hours",
                "description": "Most searches occur between 9 AM - 11 AM and 2 PM - 4 PM",
                "impact": "High"
            },
            {
                "title": "Popular Frameworks",
                "description": "React, Next.js, and Python are the most searched technologies",
                "impact": "Medium"
            },
            {
                "title": "User Behavior",
                "description": "Users prefer deep search for technical queries",
                "impact": "Medium"
            }
        ]
        
        for insight in insights:
            impact_color = "#155dfc" if insight['impact'] == "High" else "#9810fa"
            st.markdown(f"""
            <div class="search-result">
                <strong>{insight['title']}</strong>
                <span style="background: {impact_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; float: right;">{insight['impact']}</span><br>
                <p style="margin-top: 0.5rem;">{insight['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Search History")
    if st.session_state.search_history:
        history_df = pd.DataFrame(st.session_state.search_history)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No search history yet. Try making some searches!")

elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
    
    st.markdown("### API Configuration")
    
    exa_api_key = st.text_input(
        "Exa API Key",
        type="password",
        help="Enter your Exa API key for search functionality"
    )
    
    st.markdown("### Search Preferences")
    
    default_search_type = st.selectbox(
        "Default Search Type",
        ["auto", "fast", "deep"]
    )
    
    default_results = st.slider("Default Number of Results", 1, 20, 8)
    
    enable_cache = st.checkbox("Enable Result Caching", value=True)
    
    st.markdown("### Display Settings")
    
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    
    show_timestamps = st.checkbox("Show Timestamps", value=True)
    
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>SmartX Technologies AI Dashboard • Powered by Exa AI</p>
    <p style="font-size: 0.9rem;">© 2025 SmartX Technologies. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
