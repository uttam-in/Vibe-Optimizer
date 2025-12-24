"""
Unit tests for sentiment model trainer.
Tests the SentimentModelTrainer class.
"""
import pytest
import os
import tempfile
import shutil
import pandas as pd
from src.analysis.model_trainer import SentimentModelTrainer
from src.core.models import SentimentLabel


@pytest.fixture
def temp_model_dir():
    """Create temporary directory for model files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_csv_data(tmp_path):
    """Create sample CSV data for testing."""
    csv_file = tmp_path / "test_data.csv"
    data = {
        'Text': [
            'I love this product!',
            'This is terrible.',
            'It is okay.',
            'Amazing quality!',
            'Very disappointed.',
            'Great experience!',
            'Not good at all.',
            'Pretty average.',
            'Excellent service!',
            'Worst ever.',
        ],
        'Sentiment': [
            'Positive',
            'Negative',
            'Neutral',
            'Positive',
            'Negative',
            'Positive',
            'Negative',
            'Neutral',
            'Positive',
            'Negative',
        ]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    return str(csv_file)


class TestSentimentModelTrainer:
    """Test suite for SentimentModelTrainer."""
    
    def test_trainer_initialization(self, temp_model_dir):
        """Test trainer initializes correctly."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        assert trainer.model_dir == temp_model_dir
        assert os.path.exists(temp_model_dir)
        assert trainer.vectorizer is None
        assert trainer.model is None
    
    def test_load_data_from_csv(self, sample_csv_data, temp_model_dir):
        """Test loading data from CSV file."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        
        assert len(texts) == 10
        assert len(labels) == 10
        assert isinstance(texts, pd.Series)
        assert isinstance(labels, pd.Series)
    
    def test_load_data_file_not_found(self, temp_model_dir):
        """Test error when CSV file doesn't exist."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        with pytest.raises(FileNotFoundError):
            trainer.load_data_from_csv("nonexistent.csv")
    
    def test_load_data_missing_columns(self, tmp_path, temp_model_dir):
        """Test error when CSV is missing required columns."""
        csv_file = tmp_path / "bad_data.csv"
        df = pd.DataFrame({'WrongColumn': ['test']})
        df.to_csv(csv_file, index=False)
        
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        with pytest.raises(ValueError):
            trainer.load_data_from_csv(str(csv_file))
    
    def test_preprocess_labels(self, temp_model_dir):
        """Test label preprocessing and normalization."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        labels = pd.Series(['Positive', 'negative', 'NEUTRAL', 'Joy', 'Anger'])
        normalized = trainer.preprocess_labels(labels)
        
        assert len(normalized) == 5
        assert all(label in ['positive', 'negative', 'neutral'] for label in normalized)
    
    def test_label_mapping(self, temp_model_dir):
        """Test that emotion labels are mapped correctly."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        # Test positive emotions
        assert trainer.label_mapping['Joy'] == SentimentLabel.POSITIVE
        assert trainer.label_mapping['Happiness'] == SentimentLabel.POSITIVE
        assert trainer.label_mapping['Love'] == SentimentLabel.POSITIVE
        
        # Test negative emotions
        assert trainer.label_mapping['Anger'] == SentimentLabel.NEGATIVE
        assert trainer.label_mapping['Sadness'] == SentimentLabel.NEGATIVE
        assert trainer.label_mapping['Fear'] == SentimentLabel.NEGATIVE
        
        # Test neutral
        assert trainer.label_mapping['Neutral'] == SentimentLabel.NEUTRAL
    
    def test_train_logistic_regression(self, sample_csv_data, temp_model_dir):
        """Test training with logistic regression."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        
        metrics = trainer.train(
            texts=texts,
            labels=labels,
            algorithm='logistic_regression',
            test_size=0.3,  # Increased to ensure at least 3 samples in test set
            random_state=42
        )
        
        assert metrics is not None
        assert 'accuracy' in metrics
        assert 'algorithm' in metrics
        assert metrics['algorithm'] == 'logistic_regression'
        assert 0.0 <= metrics['accuracy'] <= 1.0
        assert trainer.model is not None
        assert trainer.vectorizer is not None
    
    def test_train_naive_bayes(self, sample_csv_data, temp_model_dir):
        """Test training with naive bayes."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        
        metrics = trainer.train(
            texts=texts,
            labels=labels,
            algorithm='naive_bayes',
            test_size=0.3,  # Increased to ensure at least 3 samples in test set
            random_state=42
        )
        
        assert metrics is not None
        assert metrics['algorithm'] == 'naive_bayes'
        assert trainer.model is not None
    
    def test_train_invalid_algorithm(self, sample_csv_data, temp_model_dir):
        """Test error with invalid algorithm."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        
        with pytest.raises(ValueError):
            trainer.train(texts, labels, algorithm='invalid_algorithm')
    
    def test_train_metrics_structure(self, sample_csv_data, temp_model_dir):
        """Test that training metrics have correct structure."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        
        metrics = trainer.train(texts, labels, test_size=0.3)
        
        assert 'algorithm' in metrics
        assert 'accuracy' in metrics
        assert 'classification_report' in metrics
        assert 'confusion_matrix' in metrics
        assert 'train_size' in metrics
        assert 'test_size' in metrics
        assert 'num_features' in metrics
        assert 'trained_at' in metrics
    
    def test_save_model(self, sample_csv_data, temp_model_dir):
        """Test saving trained model."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        trainer.train(texts, labels, test_size=0.3)
        
        trainer.save_model(model_name='test_model')
        
        model_path = os.path.join(temp_model_dir, 'test_model.pkl')
        vectorizer_path = os.path.join(temp_model_dir, 'test_model_vectorizer.pkl')
        
        assert os.path.exists(model_path)
        assert os.path.exists(vectorizer_path)
        assert os.path.getsize(model_path) > 0
        assert os.path.getsize(vectorizer_path) > 0
    
    def test_save_model_without_training(self, temp_model_dir):
        """Test error when saving without training."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        with pytest.raises(ValueError):
            trainer.save_model()
    
    def test_load_model(self, sample_csv_data, temp_model_dir):
        """Test loading saved model."""
        # Train and save
        trainer1 = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer1.load_data_from_csv(sample_csv_data)
        trainer1.train(texts, labels, test_size=0.3)
        trainer1.save_model(model_name='test_model')
        
        # Load in new instance
        trainer2 = SentimentModelTrainer(model_dir=temp_model_dir)
        trainer2.load_model(model_name='test_model')
        
        assert trainer2.model is not None
        assert trainer2.vectorizer is not None
    
    def test_load_model_not_found(self, temp_model_dir):
        """Test error when loading non-existent model."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        with pytest.raises(FileNotFoundError):
            trainer.load_model(model_name='nonexistent_model')
    
    def test_predict(self, sample_csv_data, temp_model_dir):
        """Test prediction on new text."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        trainer.train(texts, labels, test_size=0.3)
        
        prediction, confidence, probabilities = trainer.predict("I love this!")
        
        assert prediction in ['positive', 'negative', 'neutral']
        assert 0.0 <= confidence <= 1.0
        assert len(probabilities) == 3  # Three classes
        assert sum(probabilities) == pytest.approx(1.0, rel=1e-5)
    
    def test_predict_without_training(self, temp_model_dir):
        """Test error when predicting without training."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        with pytest.raises(ValueError):
            trainer.predict("test text")
    
    def test_get_feature_importance(self, sample_csv_data, temp_model_dir):
        """Test getting feature importance."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        trainer.train(texts, labels, algorithm='logistic_regression', test_size=0.3)
        
        importance = trainer.get_feature_importance(top_n=5)
        
        assert isinstance(importance, dict)
        # Should have entries for each class
        assert len(importance) > 0
    
    def test_train_with_custom_parameters(self, sample_csv_data, temp_model_dir):
        """Test training with custom parameters."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        
        metrics = trainer.train(
            texts=texts,
            labels=labels,
            algorithm='logistic_regression',
            test_size=0.3,
            random_state=123,
            max_features=100
        )
        
        assert metrics is not None
        assert metrics['test_size'] == 3  # 30% of 10 samples
        assert metrics['num_features'] <= 100


class TestModelTrainerIntegration:
    """Integration tests for model trainer."""
    
    def test_full_training_pipeline(self, sample_csv_data, temp_model_dir):
        """Test complete training pipeline."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        # Load data
        texts, labels = trainer.load_data_from_csv(sample_csv_data)
        assert len(texts) > 0
        
        # Train
        metrics = trainer.train(texts, labels, test_size=0.3)
        assert metrics['accuracy'] >= 0.0
        
        # Save
        trainer.save_model(model_name='pipeline_test')
        assert os.path.exists(os.path.join(temp_model_dir, 'pipeline_test.pkl'))
        
        # Load
        new_trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        new_trainer.load_model(model_name='pipeline_test')
        
        # Predict
        prediction, confidence, _ = new_trainer.predict("This is great!")
        assert prediction in ['positive', 'negative', 'neutral']
        assert confidence > 0.0
    
    def test_model_persistence(self, sample_csv_data, temp_model_dir):
        """Test that saved model produces same predictions."""
        # Train and save
        trainer1 = SentimentModelTrainer(model_dir=temp_model_dir)
        texts, labels = trainer1.load_data_from_csv(sample_csv_data)
        trainer1.train(texts, labels, test_size=0.3, random_state=42)
        trainer1.save_model(model_name='persist_test')
        
        pred1, conf1, _ = trainer1.predict("I love this product!")
        
        # Load and predict
        trainer2 = SentimentModelTrainer(model_dir=temp_model_dir)
        trainer2.load_model(model_name='persist_test')
        pred2, conf2, _ = trainer2.predict("I love this product!")
        
        # Should produce same results
        assert pred1 == pred2
        assert conf1 == conf2


class TestModelTrainerWithRealData:
    """Tests using the actual dataset if available."""
    
    @pytest.mark.skipif(
        not os.path.exists("data/sentimentdataset.csv"),
        reason="Dataset not available"
    )
    def test_train_on_real_dataset(self, temp_model_dir):
        """Test training on the actual sentiment dataset."""
        trainer = SentimentModelTrainer(model_dir=temp_model_dir)
        
        texts, labels = trainer.load_data_from_csv("data/sentimentdataset.csv")
        
        assert len(texts) > 100  # Should have substantial data
        
        metrics = trainer.train(
            texts=texts,
            labels=labels,
            algorithm='logistic_regression',
            test_size=0.2
        )
        
        # Should achieve reasonable accuracy
        assert metrics['accuracy'] > 0.5
        assert metrics['train_size'] > 0
        assert metrics['test_size'] > 0
