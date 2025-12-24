"""
Sentiment analysis implementation using trained models.
Single Responsibility: Analyze sentiment of text.
"""
import os
import pickle
import numpy as np
from typing import Optional

from src.core.interfaces import ISentimentAnalyzer
from src.core.models import SentimentScore, SentimentLabel


class TrainedSentimentAnalyzer(ISentimentAnalyzer):
    """
    Sentiment analyzer using custom trained model.
    Uses scikit-learn model trained on domain-specific data.
    """
    
    def __init__(self, model_path: str = "models/sentiment_model.pkl"):
        """
        Initialize analyzer with trained model.
        
        Args:
            model_path: Path to trained model file (without extension)
        """
        self.model = None
        self.vectorizer = None
        self.model_path = model_path
        
        # Extract base path without extension
        if model_path.endswith('.pkl'):
            self.base_path = model_path[:-4]
        else:
            self.base_path = model_path
        
        # Load model if it exists
        if os.path.exists(f"{self.base_path}.pkl"):
            self._load_model()
    
    def _load_model(self):
        """Load trained model and vectorizer from disk."""
        try:
            # Load model
            with open(f"{self.base_path}.pkl", 'rb') as f:
                self.model = pickle.load(f)
            
            # Load vectorizer
            with open(f"{self.base_path}_vectorizer.pkl", 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            print(f"Model loaded successfully from {self.base_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def analyze(self, text: str) -> SentimentScore:
        """
        Analyze sentiment using trained model.
        
        Args:
            text: Input text to analyze
            
        Returns:
            SentimentScore with label, confidence, and intensity
        """
        if self.model is None or self.vectorizer is None:
            raise RuntimeError(
                "Model not loaded. Train a model first or provide valid model path."
            )
        
        # Vectorize text
        text_vec = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.model.predict(text_vec)[0]
        probabilities = self.model.predict_proba(text_vec)[0]
        
        # Get confidence (max probability)
        confidence = float(probabilities.max())
        
        # Map prediction to SentimentLabel
        label = SentimentLabel(prediction)
        
        # Calculate intensity based on probability distribution
        # Higher intensity means more extreme sentiment (further from neutral)
        intensity = self._calculate_intensity(probabilities, label)
        
        # Calculate compound score (-1 to 1)
        compound_score = self._calculate_compound_score(probabilities)
        
        return SentimentScore(
            label=label,
            score=confidence,
            intensity=intensity,
            compound_score=compound_score
        )
    
    def _calculate_intensity(
        self, 
        probabilities: np.ndarray, 
        label: SentimentLabel
    ) -> float:
        """
        Calculate sentiment intensity based on probability distribution.
        
        Args:
            probabilities: Class probabilities
            label: Predicted sentiment label
            
        Returns:
            Intensity score (0-1)
        """
        # Get class indices
        classes = list(self.model.classes_)
        
        # Find neutral probability
        try:
            neutral_idx = classes.index(SentimentLabel.NEUTRAL.value)
            neutral_prob = probabilities[neutral_idx]
        except (ValueError, IndexError):
            neutral_prob = 0.0
        
        # Intensity is inverse of neutral probability
        # High neutral prob = low intensity, low neutral prob = high intensity
        intensity = 1.0 - neutral_prob
        
        # Scale by confidence to avoid high intensity on uncertain predictions
        confidence = probabilities.max()
        intensity = intensity * confidence
        
        return float(np.clip(intensity, 0.0, 1.0))
    
    def _calculate_compound_score(self, probabilities: np.ndarray) -> float:
        """
        Calculate compound sentiment score from -1 (negative) to 1 (positive).
        
        Args:
            probabilities: Class probabilities
            
        Returns:
            Compound score (-1 to 1)
        """
        classes = list(self.model.classes_)
        
        # Get probabilities for each sentiment
        pos_prob = 0.0
        neg_prob = 0.0
        neu_prob = 0.0
        
        for idx, cls in enumerate(classes):
            if cls == SentimentLabel.POSITIVE.value:
                pos_prob = probabilities[idx]
            elif cls == SentimentLabel.NEGATIVE.value:
                neg_prob = probabilities[idx]
            elif cls == SentimentLabel.NEUTRAL.value:
                neu_prob = probabilities[idx]
        
        # Calculate compound: positive contribution minus negative contribution
        compound = pos_prob - neg_prob
        
        return float(np.clip(compound, -1.0, 1.0))


class TransformerSentimentAnalyzer(ISentimentAnalyzer):
    """Sentiment analyzer using Hugging Face transformers."""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        try:
            from transformers import pipeline
            self.pipeline = pipeline("sentiment-analysis", model=model_name)
        except ImportError:
            raise ImportError(
                "transformers library not installed. "
                "Install with: pip install transformers torch"
            )
    
    def analyze(self, text: str) -> SentimentScore:
        """
        Analyze sentiment using transformer model.
        
        Args:
            text: Input text to analyze
            
        Returns:
            SentimentScore with label, confidence, and intensity
        """
        # Run through pipeline
        result = self.pipeline(text[:512])[0]  # Limit to 512 chars
        
        # Map label
        label_map = {
            'POSITIVE': SentimentLabel.POSITIVE,
            'NEGATIVE': SentimentLabel.NEGATIVE,
            'NEUTRAL': SentimentLabel.NEUTRAL
        }
        label = label_map.get(result['label'].upper(), SentimentLabel.NEUTRAL)
        
        # Get confidence
        confidence = float(result['score'])
        
        # Calculate intensity (use confidence as proxy)
        intensity = confidence
        
        # Calculate compound score
        compound = confidence if label == SentimentLabel.POSITIVE else -confidence
        if label == SentimentLabel.NEUTRAL:
            compound = 0.0
        
        return SentimentScore(
            label=label,
            score=confidence,
            intensity=intensity,
            compound_score=compound
        )


class VaderSentimentAnalyzer(ISentimentAnalyzer):
    """Alternative sentiment analyzer using VADER (rule-based)."""
    
    def __init__(self):
        try:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            self.analyzer = SentimentIntensityAnalyzer()
        except ImportError:
            raise ImportError(
                "NLTK VADER not installed. "
                "Install with: pip install nltk && python -m nltk.downloader vader_lexicon"
            )
    
    def analyze(self, text: str) -> SentimentScore:
        """Analyze sentiment using VADER."""
        scores = self.analyzer.polarity_scores(text)
        
        # Determine label based on compound score
        compound = scores['compound']
        if compound >= 0.05:
            label = SentimentLabel.POSITIVE
        elif compound <= -0.05:
            label = SentimentLabel.NEGATIVE
        else:
            label = SentimentLabel.NEUTRAL
        
        # Get confidence (use the score for the predicted label)
        confidence = scores['pos'] if label == SentimentLabel.POSITIVE else \
                    scores['neg'] if label == SentimentLabel.NEGATIVE else \
                    scores['neu']
        
        # Intensity is absolute value of compound score
        intensity = abs(compound)
        
        return SentimentScore(
            label=label,
            score=float(confidence),
            intensity=float(intensity),
            compound_score=float(compound)
        )
