"""
Database models and session management.
Single Responsibility: Handle database connections and ORM models.
"""
from sqlalchemy import create_engine, Column, String, DateTime, Float, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class RawContentModel(Base):
    """ORM model for raw content."""
    __tablename__ = "raw_content"
    
    id = Column(String, primary_key=True)
    source_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String)
    timestamp = Column(DateTime, nullable=False)
    metadata = Column(JSON)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class AnalyzedContentModel(Base):
    """ORM model for analyzed content."""
    __tablename__ = "analyzed_content"
    
    id = Column(String, primary_key=True)
    raw_content_id = Column(String, nullable=False)
    sentiment_label = Column(String, nullable=False)
    sentiment_score = Column(Float, nullable=False)
    sentiment_intensity = Column(Float, nullable=False)
    topics = Column(JSON)
    entities = Column(JSON)
    processed_at = Column(DateTime, nullable=False)


class InsightModel(Base):
    """ORM model for insights."""
    __tablename__ = "insights"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    insight_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    supporting_data = Column(JSON)
    recommendations = Column(JSON)
    created_at = Column(DateTime, nullable=False)


class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a database session."""
        return self.SessionLocal()
