"""
Example API endpoints for sentiment analysis.
Ready for FastAPI integration.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
from src.ingestion.ingestion_service import CSVDataSource
from src.core.models import SourceType


# Request/Response Models
class SentimentAnalysisRequest(BaseModel):
    """Request model for sentiment analysis."""
    text: str = Field(..., description="Text to analyze", min_length=1)
    include_metadata: bool = Field(default=True, description="Include analysis metadata")


class SentimentResult(BaseModel):
    """Sentiment analysis result."""
    label: str = Field(..., description="Sentiment label: positive, negative, or neutral")
    confidence: float = Field(..., description="Confidence score (0-1)")
    intensity: float = Field(..., description="Sentiment intensity (0-1)")
    compound_score: float = Field(..., description="Compound score (-1 to 1)")


class SentimentAnalysisResponse(BaseModel):
    """Response model for sentiment analysis."""
    success: bool
    data: dict
    error: Optional[str] = None


class BatchAnalysisRequest(BaseModel):
    """Request model for batch sentiment analysis."""
    texts: List[str] = Field(..., description="List of texts to analyze")
    include_metadata: bool = Field(default=False)


class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis."""
    success: bool
    data: dict
    error: Optional[str] = None


# Service Layer
class SentimentAnalysisAPI:
    """
    API service for sentiment analysis.
    Handles requests and coordinates with analyzer.
    """
    
    def __init__(self, model_path: str = "models/sentiment_model.pkl"):
        """
        Initialize API service.
        
        Args:
            model_path: Path to trained model
        """
        self.analyzer = TrainedSentimentAnalyzer(model_path=model_path)
        self.model_version = "1.0"
    
    def analyze_single(self, request: SentimentAnalysisRequest) -> SentimentAnalysisResponse:
        """
        Analyze sentiment of a single text.
        
        Args:
            request: Analysis request
            
        Returns:
            Analysis response
        """
        try:
            # Analyze sentiment
            sentiment = self.analyzer.analyze(request.text)
            
            # Build response
            response_data = {
                "text": request.text,
                "sentiment": {
                    "label": sentiment.label.value,
                    "confidence": round(sentiment.score, 4),
                    "intensity": round(sentiment.intensity, 4),
                    "compound_score": round(sentiment.compound_score, 4)
                }
            }
            
            # Add metadata if requested
            if request.include_metadata:
                response_data["metadata"] = {
                    "model": "trained_sentiment_model",
                    "version": self.model_version,
                    "analyzed_at": datetime.now().isoformat(),
                    "text_length": len(request.text)
                }
            
            return SentimentAnalysisResponse(
                success=True,
                data=response_data
            )
            
        except Exception as e:
            return SentimentAnalysisResponse(
                success=False,
                data={},
                error=str(e)
            )
    
    def analyze_batch(self, request: BatchAnalysisRequest) -> BatchAnalysisResponse:
        """
        Analyze sentiment of multiple texts.
        
        Args:
            request: Batch analysis request
            
        Returns:
            Batch analysis response
        """
        try:
            results = []
            sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
            
            for text in request.texts:
                sentiment = self.analyzer.analyze(text)
                
                result = {
                    "text": text,
                    "sentiment": {
                        "label": sentiment.label.value,
                        "confidence": round(sentiment.score, 4),
                        "intensity": round(sentiment.intensity, 4),
                        "compound_score": round(sentiment.compound_score, 4)
                    }
                }
                
                results.append(result)
                sentiment_counts[sentiment.label.value] += 1
            
            # Build response
            response_data = {
                "results": results,
                "summary": {
                    "total_analyzed": len(request.texts),
                    "sentiment_distribution": sentiment_counts,
                    "average_confidence": round(
                        sum(r["sentiment"]["confidence"] for r in results) / len(results), 4
                    )
                }
            }
            
            if request.include_metadata:
                response_data["metadata"] = {
                    "model": "trained_sentiment_model",
                    "version": self.model_version,
                    "analyzed_at": datetime.now().isoformat()
                }
            
            return BatchAnalysisResponse(
                success=True,
                data=response_data
            )
            
        except Exception as e:
            return BatchAnalysisResponse(
                success=False,
                data={},
                error=str(e)
            )
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Model information
        """
        return {
            "model_type": "trained_sentiment_model",
            "version": self.model_version,
            "supported_labels": ["positive", "negative", "neutral"],
            "features": [
                "confidence_score",
                "intensity_score",
                "compound_score"
            ]
        }


# FastAPI Integration Example
"""
To integrate with FastAPI, add this to your main.py:

from fastapi import FastAPI, HTTPException
from src.api.sentiment_api_example import (
    SentimentAnalysisAPI,
    SentimentAnalysisRequest,
    BatchAnalysisRequest
)

app = FastAPI(title="Sentiment Analysis API")

# Initialize service
sentiment_api = SentimentAnalysisAPI(model_path="models/sentiment_model.pkl")

@app.post("/api/sentiment/analyze")
async def analyze_sentiment(request: SentimentAnalysisRequest):
    response = sentiment_api.analyze_single(request)
    if not response.success:
        raise HTTPException(status_code=500, detail=response.error)
    return response

@app.post("/api/sentiment/batch")
async def analyze_batch(request: BatchAnalysisRequest):
    response = sentiment_api.analyze_batch(request)
    if not response.success:
        raise HTTPException(status_code=500, detail=response.error)
    return response

@app.get("/api/sentiment/model-info")
async def get_model_info():
    return sentiment_api.get_model_info()
"""
