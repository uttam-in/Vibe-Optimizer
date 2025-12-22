"""
Database setup script.
"""
from src.storage.database import DatabaseManager
from config.settings import settings


def main():
    """Initialize database tables."""
    db_manager = DatabaseManager(settings.database_url)
    db_manager.create_tables()
    print("Database tables created successfully!")


if __name__ == "__main__":
    main()
