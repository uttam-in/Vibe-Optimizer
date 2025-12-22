"""
Application configuration.
Single Responsibility: Centralize configuration management.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    # Database
    database_url: str = "sqlite:///./vibe_optimizer.db"
    
    # API Keys
    twitter_api_key: str = ""
    twitter_api_secret: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    
    # Email
    sendgrid_api_key: str = ""
    report_email_from: str = ""
    report_email_to: List[str] = []
    
    # NLP Models
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    api_port: int = 8000
    dashboard_port: int = 8501
    
    # Scheduling
    ingestion_interval_minutes: int = 30
    report_schedule_cron: str = "0 9 * * 1"
    
    class Config:
        env_file = ".env"


settings = Settings()
