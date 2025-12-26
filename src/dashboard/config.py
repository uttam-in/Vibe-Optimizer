"""
Dashboard configuration settings
"""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DashboardConfig:
    """Dashboard configuration"""
    
    # Data settings
    DEFAULT_CSV_PATH: str = "data/sentimentdataset.csv"
    DEFAULT_DATA_LIMIT: int = 1000
    MAX_DATA_LIMIT: int = 5000
    
    # Model settings
    MODEL_PATH: str = "models/sentiment_model.pkl"
    FALLBACK_TO_VADER: bool = True
    
    # Display settings
    PAGE_TITLE: str = "Vibe Optimizer Dashboard"
    PAGE_ICON: str = "📊"
    LAYOUT: str = "wide"
    
    # Chart colors
    SENTIMENT_COLORS: Dict[str, str] = None
    
    # Filter defaults
    DEFAULT_DATE_RANGE_DAYS: int = 30
    DEFAULT_SOURCES: List[str] = None
    
    # Performance settings
    CACHE_TTL: int = 3600  # 1 hour
    MAX_DISPLAY_RECORDS: int = 100
    
    def __post_init__(self):
        if self.SENTIMENT_COLORS is None:
            self.SENTIMENT_COLORS = {
                'positive': '#00CC96',
                'neutral': '#FFA15A',
                'negative': '#EF553B'
            }
        
        if self.DEFAULT_SOURCES is None:
            self.DEFAULT_SOURCES = ['Twitter', 'Reddit']


# Global config instance
config = DashboardConfig()


# Theme settings
THEME = {
    'primary_color': '#636EFA',
    'background_color': '#FFFFFF',
    'secondary_background_color': '#F0F2F6',
    'text_color': '#262730',
    'font': 'sans-serif'
}


# Chart templates
CHART_TEMPLATE = 'plotly_white'


# Metric display formats
METRIC_FORMATS = {
    'percentage': '{:.1f}%',
    'decimal': '{:.2f}',
    'integer': '{:,}',
    'currency': '${:,.2f}'
}
