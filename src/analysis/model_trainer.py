"""
Model training module for sentiment analysis.
Single Responsibility: Train and save sentiment analysis models.
"""
import os
import pickle
import pandas as pd
from typing import Tuple, Optional, Dict, Any
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np

from src.core.models import SentimentLabel


class SentimentModelTrainer:
    """
    Trains sentiment analysis models using labeled data.
    Supports multiple algorithms and saves trained models for production use.
    """
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize the model trainer.
        
        Args:
            model_dir: Directory to save trained models
        """
        self.model_dir = model_dir
        self.vectorizer = None
        self.model = None
        
        # Map various emotion labels to sentiment categories
        self.label_mapping = {
            # Positive sentiments
            'Positive': SentimentLabel.POSITIVE,
            'Joy': SentimentLabel.POSITIVE,
            'Happiness': SentimentLabel.POSITIVE,
            'Happy': SentimentLabel.POSITIVE,
            'Love': SentimentLabel.POSITIVE,
            'Excitement': SentimentLabel.POSITIVE,
            'Elation': SentimentLabel.POSITIVE,
            'Euphoria': SentimentLabel.POSITIVE,
            'Contentment': SentimentLabel.POSITIVE,
            'Serenity': SentimentLabel.POSITIVE,
            'Gratitude': SentimentLabel.POSITIVE,
            'Hope': SentimentLabel.POSITIVE,
            'Empowerment': SentimentLabel.POSITIVE,
            'Compassion': SentimentLabel.POSITIVE,
            'Tenderness': SentimentLabel.POSITIVE,
            'Arousal': SentimentLabel.POSITIVE,
            'Enthusiasm': SentimentLabel.POSITIVE,
            'Fulfillment': SentimentLabel.POSITIVE,
            'Reverence': SentimentLabel.POSITIVE,
            'Amusement': SentimentLabel.POSITIVE,
            'Enjoyment': SentimentLabel.POSITIVE,
            'Admiration': SentimentLabel.POSITIVE,
            'Affection': SentimentLabel.POSITIVE,
            'Awe': SentimentLabel.POSITIVE,
            'Surprise': SentimentLabel.POSITIVE,
            'Adoration': SentimentLabel.POSITIVE,
            'Anticipation': SentimentLabel.POSITIVE,
            'Kind': SentimentLabel.POSITIVE,
            'Kindness': SentimentLabel.POSITIVE,
            'Pride': SentimentLabel.POSITIVE,
            
            # Negative sentiments
            'Negative': SentimentLabel.NEGATIVE,
            'Anger': SentimentLabel.NEGATIVE,
            'Fear': SentimentLabel.NEGATIVE,
            'Sadness': SentimentLabel.NEGATIVE,
            'Disgust': SentimentLabel.NEGATIVE,
            'Disappointed': SentimentLabel.NEGATIVE,
            'Bitter': SentimentLabel.NEGATIVE,
            'Shame': SentimentLabel.NEGATIVE,
            'Confusion': SentimentLabel.NEGATIVE,
            
            # Neutral sentiments
            'Neutral': SentimentLabel.NEUTRAL,
            'Acceptance': SentimentLabel.NEUTRAL,
            'Calmness': SentimentLabel.NEUTRAL,
        }
        
        # Create model directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
    
    def load_data_from_csv(
        self, 
        csv_path: str,
        text_column: str = 'Text',
        label_column: str = 'Sentiment'
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Load training data from CSV file.
        
        Args:
            csv_path: Path to CSV file
            text_column: Name of text column
            label_column: Name of sentiment label column
            
        Returns:
            Tuple of (texts, labels)
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Validate columns
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in CSV")
        if label_column not in df.columns:
            raise ValueError(f"Column '{label_column}' not found in CSV")
        
        # Clean data
        df = df[[text_column, label_column]].copy()
        df = df.dropna()
        df[text_column] = df[text_column].str.strip()
        df[label_column] = df[label_column].str.strip()
        
        # Filter out rows with empty text
        df = df[df[text_column].str.len() > 0]
        
        return df[text_column], df[label_column]
    
    def preprocess_labels(self, labels: pd.Series) -> np.ndarray:
        """
        Normalize sentiment labels to standard format.
        
        Args:
            labels: Raw sentiment labels
            
        Returns:
            Normalized labels array
        """
        # Normalize to standard labels
        normalized = labels.apply(lambda x: x.strip().title())
        
        # Map to SentimentLabel enum values
        normalized = normalized.map(
            lambda x: self.label_mapping.get(x, SentimentLabel.NEUTRAL).value
        )
        
        return normalized.values
    
    def train(
        self,
        texts: pd.Series,
        labels: pd.Series,
        algorithm: str = 'logistic_regression',
        test_size: float = 0.2,
        random_state: int = 42,
        max_features: int = 5000
    ) -> Dict[str, Any]:
        """
        Train sentiment analysis model.
        
        Args:
            texts: Training texts
            labels: Training labels
            algorithm: 'naive_bayes' or 'logistic_regression'
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
            max_features: Maximum number of features for TF-IDF
            
        Returns:
            Dictionary with training metrics
        """
        # Preprocess labels
        labels_normalized = self.preprocess_labels(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels_normalized,
            test_size=test_size,
            random_state=random_state,
            stratify=labels_normalized
        )
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            strip_accents='unicode',
            lowercase=True
        )
        
        # Fit vectorizer and transform training data
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train model
        if algorithm == 'naive_bayes':
            self.model = MultinomialNB(alpha=0.1)
        elif algorithm == 'logistic_regression':
            self.model = LogisticRegression(
                max_iter=1000,
                random_state=random_state,
                C=1.0,
                class_weight='balanced'
            )
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        # Fit model
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        # Prepare metrics
        metrics = {
            'algorithm': algorithm,
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': conf_matrix.tolist(),
            'train_size': len(X_train),
            'test_size': len(X_test),
            'num_features': len(self.vectorizer.get_feature_names_out()),
            'trained_at': datetime.now().isoformat()
        }
        
        return metrics
    
    def save_model(self, model_name: str = 'sentiment_model'):
        """
        Save trained model and vectorizer to disk.
        
        Args:
            model_name: Base name for saved files
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("No trained model to save. Train a model first.")
        
        # Save model
        model_path = os.path.join(self.model_dir, f'{model_name}.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        # Save vectorizer
        vectorizer_path = os.path.join(self.model_dir, f'{model_name}_vectorizer.pkl')
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        print(f"Model saved to: {model_path}")
        print(f"Vectorizer saved to: {vectorizer_path}")
    
    def load_model(self, model_name: str = 'sentiment_model'):
        """
        Load trained model and vectorizer from disk.
        
        Args:
            model_name: Base name of saved files
        """
        # Load model
        model_path = os.path.join(self.model_dir, f'{model_name}.pkl')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        # Load vectorizer
        vectorizer_path = os.path.join(self.model_dir, f'{model_name}_vectorizer.pkl')
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
        
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        print(f"Model loaded from: {model_path}")
    
    def predict(self, text: str) -> Tuple[str, float, np.ndarray]:
        """
        Predict sentiment for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (predicted_label, confidence, probabilities)
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("No trained model available. Train or load a model first.")
        
        # Vectorize text
        text_vec = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.model.predict(text_vec)[0]
        probabilities = self.model.predict_proba(text_vec)[0]
        confidence = probabilities.max()
        
        return prediction, confidence, probabilities
    
    def get_feature_importance(self, top_n: int = 20) -> Dict[str, list]:
        """
        Get most important features for each sentiment class.
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            Dictionary mapping sentiment labels to top features
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("No trained model available.")
        
        feature_names = self.vectorizer.get_feature_names_out()
        
        # For logistic regression
        if hasattr(self.model, 'coef_'):
            importance_dict = {}
            for idx, label in enumerate(self.model.classes_):
                # Get coefficients for this class
                coef = self.model.coef_[idx]
                # Get top positive features
                top_indices = coef.argsort()[-top_n:][::-1]
                top_features = [(feature_names[i], coef[i]) for i in top_indices]
                importance_dict[label] = top_features
            
            return importance_dict
        
        return {}
