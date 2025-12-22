"""
FastAPI application entry point.
Single Responsibility: API routing and configuration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import sentiment, insights, reports


app = FastAPI(
    title="Vibe Optimizer API",
    description="Brand intelligence and sentiment analysis platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sentiment.router, prefix="/api/v1/sentiment", tags=["sentiment"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["insights"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])


@app.get("/")
def root():
    return {"message": "Vibe Optimizer API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
