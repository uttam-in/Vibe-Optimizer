"""
Script to train sentiment analysis model using dataset.
Usage: python scripts/train_sentiment_model.py
"""
import os
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.model_trainer import SentimentModelTrainer


def main():
    """Train sentiment model using the sentiment dataset."""
    
    print("=" * 60)
    print("Sentiment Model Training")
    print("=" * 60)
    
    # Configuration
    csv_path = "data/sentimentdataset.csv"
    model_dir = "models"
    model_name = "sentiment_model"
    algorithm = "logistic_regression"  # or 'naive_bayes'
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        return
    
    # Initialize trainer
    print(f"\n1. Initializing trainer...")
    trainer = SentimentModelTrainer(model_dir=model_dir)
    
    # Load data
    print(f"\n2. Loading data from {csv_path}...")
    texts, labels = trainer.load_data_from_csv(csv_path)
    print(f"   Loaded {len(texts)} samples")
    print(f"   Label distribution:")
    print(labels.value_counts())
    
    # Train model
    print(f"\n3. Training {algorithm} model...")
    metrics = trainer.train(
        texts=texts,
        labels=labels,
        algorithm=algorithm,
        test_size=0.2,
        random_state=42,
        max_features=5000
    )
    
    # Display results
    print(f"\n4. Training Results:")
    print(f"   Algorithm: {metrics['algorithm']}")
    print(f"   Accuracy: {metrics['accuracy']:.4f}")
    print(f"   Training samples: {metrics['train_size']}")
    print(f"   Test samples: {metrics['test_size']}")
    print(f"   Features: {metrics['num_features']}")
    
    print(f"\n   Classification Report:")
    report = metrics['classification_report']
    for label, scores in report.items():
        if isinstance(scores, dict):
            print(f"   {label:12s}: precision={scores['precision']:.3f}, "
                  f"recall={scores['recall']:.3f}, f1={scores['f1-score']:.3f}")
    
    # Save model
    print(f"\n5. Saving model...")
    trainer.save_model(model_name=model_name)
    
    # Save metrics
    metrics_path = os.path.join(model_dir, f"{model_name}_metrics.json")
    with open(metrics_path, 'w') as f:
        # Convert numpy arrays to lists for JSON serialization
        metrics_json = {
            'algorithm': metrics['algorithm'],
            'accuracy': metrics['accuracy'],
            'train_size': metrics['train_size'],
            'test_size': metrics['test_size'],
            'num_features': metrics['num_features'],
            'trained_at': metrics['trained_at'],
            'confusion_matrix': metrics['confusion_matrix']
        }
        json.dump(metrics_json, f, indent=2)
    print(f"   Metrics saved to: {metrics_path}")
    
    # Test predictions
    print(f"\n6. Testing predictions:")
    test_texts = [
        "I love this product! It's amazing!",
        "This is terrible and disappointing.",
        "It's okay, nothing special.",
        "Absolutely fantastic experience!",
        "Worst purchase ever, very angry."
    ]
    
    for text in test_texts:
        prediction, confidence, probs = trainer.predict(text)
        print(f"   Text: '{text}'")
        print(f"   Prediction: {prediction} (confidence: {confidence:.3f})")
        print()
    
    # Feature importance
    print(f"\n7. Top features per sentiment:")
    importance = trainer.get_feature_importance(top_n=10)
    for label, features in importance.items():
        print(f"\n   {label}:")
        for feature, score in features[:5]:
            print(f"      {feature}: {score:.3f}")
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)
    print(f"\nModel files saved in '{model_dir}/' directory:")
    print(f"  - {model_name}.pkl")
    print(f"  - {model_name}_vectorizer.pkl")
    print(f"  - {model_name}_metrics.json")
    print("\nYou can now use TrainedSentimentAnalyzer in your application.")


if __name__ == "__main__":
    main()
