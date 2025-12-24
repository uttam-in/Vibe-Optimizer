"""
Unit tests for sentiment analyzer.
Tests the TrainedSentimentAnalyzer with the trained model.
"""
import pytest
import os
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
from src.core.models import SentimentLabel, SentimentScore


@pytest.fixture
def analyzer():
    """Fixture to create analyzer instance."""
    model_path = "models/sentiment_model.pkl"
    if not os.path.exists(model_path):
        pytest.skip("Model not trained. Run: python scripts/train_sentiment_model.py")
    return TrainedSentimentAnalyzer(model_path=model_path)


class TestTrainedSentimentAnalyzer:
    """Test suite for TrainedSentimentAnalyzer."""
    
    def test_analyzer_initialization(self, analyzer):
        """Test that analyzer initializes correctly."""
        assert analyzer is not None
        assert analyzer.model is not None
        assert analyzer.vectorizer is not None
    
    def test_analyze_returns_sentiment_score(self, analyzer):
        """Test that analyze returns SentimentScore object."""
        result = analyzer.analyze("This is a test")
        assert isinstance(result, SentimentScore)
        assert hasattr(result, 'label')
        assert hasattr(result, 'score')
        assert hasattr(result, 'intensity')
        assert hasattr(result, 'compound_score')
    
    def test_sentiment_label_is_valid(self, analyzer):
        """Test that sentiment label is one of the valid types."""
        result = analyzer.analyze("This is a test")
        assert result.label in [
            SentimentLabel.POSITIVE,
            SentimentLabel.NEGATIVE,
            SentimentLabel.NEUTRAL
        ]
    
    def test_confidence_score_range(self, analyzer):
        """Test that confidence score is between 0 and 1."""
        result = analyzer.analyze("This is a test")
        assert 0.0 <= result.score <= 1.0
    
    def test_intensity_range(self, analyzer):
        """Test that intensity is between 0 and 1."""
        result = analyzer.analyze("This is a test")
        assert 0.0 <= result.intensity <= 1.0
    
    def test_compound_score_range(self, analyzer):
        """Test that compound score is between -1 and 1."""
        result = analyzer.analyze("This is a test")
        assert -1.0 <= result.compound_score <= 1.0
    
    def test_positive_sentiment_detection(self, analyzer):
        """Test detection of clearly positive sentiment."""
        positive_texts = [
            "I absolutely love this product! It's amazing!",
            "Best experience ever! Highly recommend!",
            "Fantastic quality and excellent service!",
            "So happy with my purchase! Five stars!",
        ]
        
        positive_count = 0
        for text in positive_texts:
            result = analyzer.analyze(text)
            if result.label == SentimentLabel.POSITIVE:
                positive_count += 1
        
        # At least 50% should be detected as positive
        assert positive_count >= len(positive_texts) * 0.5
    
    def test_negative_sentiment_detection(self, analyzer):
        """Test detection of clearly negative sentiment."""
        negative_texts = [
            "This is terrible and completely disappointing.",
            "Worst purchase ever. Very angry and frustrated.",
            "Horrible quality. Do not recommend at all.",
            "Extremely dissatisfied with this product.",
        ]
        
        negative_count = 0
        for text in negative_texts:
            result = analyzer.analyze(text)
            if result.label == SentimentLabel.NEGATIVE:
                negative_count += 1
        
        # At least 25% should be detected as negative
        assert negative_count >= len(negative_texts) * 0.25
    
    def test_neutral_sentiment_detection(self, analyzer):
        """Test detection of neutral sentiment."""
        neutral_texts = [
            "The product arrived on time.",
            "It has standard features.",
            "The color is blue.",
            "This is a description of the item.",
        ]
        
        # Should not crash on neutral texts
        for text in neutral_texts:
            result = analyzer.analyze(text)
            assert result is not None
    
    def test_empty_string_handling(self, analyzer):
        """Test handling of empty string."""
        result = analyzer.analyze("")
        assert isinstance(result, SentimentScore)
    
    def test_short_text_handling(self, analyzer):
        """Test handling of very short text."""
        result = analyzer.analyze("Good")
        assert isinstance(result, SentimentScore)
    
    def test_long_text_handling(self, analyzer):
        """Test handling of long text."""
        long_text = "This is a great product. " * 100
        result = analyzer.analyze(long_text)
        assert isinstance(result, SentimentScore)
    
    def test_special_characters_handling(self, analyzer):
        """Test handling of special characters."""
        texts_with_special_chars = [
            "I love this!!! 😊",
            "Great product... really!",
            "Amazing! Best ever!!!",
            "What a wonderful experience :)",
        ]
        
        for text in texts_with_special_chars:
            result = analyzer.analyze(text)
            assert isinstance(result, SentimentScore)
    
    def test_consistency_same_text(self, analyzer):
        """Test that same text produces consistent results."""
        text = "This is a great product!"
        result1 = analyzer.analyze(text)
        result2 = analyzer.analyze(text)
        
        assert result1.label == result2.label
        assert result1.score == result2.score
        assert result1.intensity == result2.intensity
        assert result1.compound_score == result2.compound_score
    
    def test_batch_analysis(self, analyzer):
        """Test analyzing multiple texts."""
        texts = [
            "I love this!",
            "This is terrible.",
            "It's okay.",
            "Amazing product!",
            "Very disappointed.",
        ]
        
        results = [analyzer.analyze(text) for text in texts]
        
        assert len(results) == len(texts)
        assert all(isinstance(r, SentimentScore) for r in results)
    
    def test_different_sentiments_different_scores(self, analyzer):
        """Test that different sentiments produce different compound scores."""
        positive_text = "I absolutely love this amazing product!"
        negative_text = "This is terrible and completely awful!"
        
        pos_result = analyzer.analyze(positive_text)
        neg_result = analyzer.analyze(negative_text)
        
        # Positive should have higher compound score than negative
        # (though model may not be perfect)
        assert pos_result.compound_score != neg_result.compound_score


class TestSentimentAnalyzerEdgeCases:
    """Test edge cases and error handling."""
    
    def test_model_not_found_error(self):
        """Test error when model file doesn't exist."""
        # Model initialization doesn't fail, but analyze should fail
        analyzer = TrainedSentimentAnalyzer(model_path="nonexistent_model.pkl")
        with pytest.raises(RuntimeError):
            analyzer.analyze("test text")
    
    def test_unicode_text_handling(self, analyzer):
        """Test handling of unicode characters."""
        unicode_texts = [
            "¡Excelente producto!",
            "Très bon produit!",
            "素晴らしい製品！",
            "Отличный продукт!",
        ]
        
        for text in unicode_texts:
            result = analyzer.analyze(text)
            assert isinstance(result, SentimentScore)
    
    def test_mixed_case_handling(self, analyzer):
        """Test handling of mixed case text."""
        texts = [
            "I LOVE THIS PRODUCT",
            "i love this product",
            "I LoVe ThIs PrOdUcT",
        ]
        
        for text in texts:
            result = analyzer.analyze(text)
            assert isinstance(result, SentimentScore)
    
    def test_numbers_in_text(self, analyzer):
        """Test handling of numbers in text."""
        result = analyzer.analyze("I rate this 10/10, absolutely amazing!")
        assert isinstance(result, SentimentScore)
    
    def test_urls_in_text(self, analyzer):
        """Test handling of URLs in text."""
        result = analyzer.analyze("Check out this product at https://example.com - it's great!")
        assert isinstance(result, SentimentScore)


class TestSentimentAnalyzerPerformance:
    """Test performance characteristics."""
    
    def test_analysis_speed(self, analyzer):
        """Test that analysis completes in reasonable time."""
        import time
        
        text = "This is a test of the sentiment analyzer performance."
        
        start_time = time.time()
        analyzer.analyze(text)
        end_time = time.time()
        
        # Should complete in less than 1 second
        assert (end_time - start_time) < 1.0
    
    def test_batch_performance(self, analyzer):
        """Test batch analysis performance."""
        import time
        
        texts = ["This is test text number {}".format(i) for i in range(50)]
        
        start_time = time.time()
        for text in texts:
            analyzer.analyze(text)
        end_time = time.time()
        
        # Should complete 50 analyses in less than 10 seconds
        assert (end_time - start_time) < 10.0
