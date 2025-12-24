"""
Demo script showing complete sentiment analysis workflow.
Demonstrates training, analysis, and API-ready usage.

Usage: python scripts/demo_sentiment_analysis.py
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.model_trainer import SentimentModelTrainer
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
from src.ingestion.ingestion_service import CSVDataSource
from src.core.models import SourceType


def train_model_if_needed():
    """Train model if it doesn't exist."""
    model_path = "models/sentiment_model.pkl"
    
    if os.path.exists(model_path):
        print("✓ Model already exists, skipping training")
        return True
    
    print("\n" + "=" * 60)
    print("STEP 1: Training Sentiment Model")
    print("=" * 60)
    
    csv_path = "data/sentimentdataset.csv"
    if not os.path.exists(csv_path):
        print(f"✗ Error: Dataset not found at {csv_path}")
        return False
    
    # Initialize trainer
    trainer = SentimentModelTrainer(model_dir="models")
    
    # Load data
    print(f"\nLoading data from {csv_path}...")
    texts, labels = trainer.load_data_from_csv(csv_path)
    print(f"✓ Loaded {len(texts)} samples")
    
    # Train model
    print(f"\nTraining model...")
    metrics = trainer.train(
        texts=texts,
        labels=labels,
        algorithm='logistic_regression',
        test_size=0.2
    )
    
    print(f"✓ Training completed with accuracy: {metrics['accuracy']:.4f}")
    
    # Save model
    trainer.save_model(model_name='sentiment_model')
    print(f"✓ Model saved successfully")
    
    return True


def demo_sentiment_analysis():
    """Demonstrate sentiment analysis on sample texts."""
    print("\n" + "=" * 60)
    print("STEP 2: Sentiment Analysis Demo")
    print("=" * 60)
    
    # Initialize analyzer with trained model
    analyzer = TrainedSentimentAnalyzer(model_path="models/sentiment_model.pkl")
    
    # Test samples
    test_samples = [
        "I absolutely love this product! Best purchase ever!",
        "This is terrible. Worst experience of my life.",
        "It's okay, nothing special really.",
        "Amazing quality and fast shipping! Highly recommend!",
        "Disappointed with the service. Not worth the money.",
        "The weather is nice today.",
        "Feeling grateful for all the support!",
        "This makes me so angry and frustrated!",
    ]
    
    print("\nAnalyzing sample texts:\n")
    
    results = []
    for text in test_samples:
        sentiment = analyzer.analyze(text)
        results.append((text, sentiment))
        
        print(f"Text: '{text}'")
        print(f"  → Sentiment: {sentiment.label.value.upper()}")
        print(f"  → Confidence: {sentiment.score:.3f}")
        print(f"  → Intensity: {sentiment.intensity:.3f}")
        print(f"  → Compound: {sentiment.compound_score:.3f}")
        print()
    
    return results


def demo_csv_ingestion_and_analysis():
    """Demonstrate ingesting from CSV and analyzing."""
    print("\n" + "=" * 60)
    print("STEP 3: CSV Ingestion & Batch Analysis")
    print("=" * 60)
    
    csv_path = "data/sentimentdataset.csv"
    
    # Initialize CSV data source
    print(f"\nLoading data from {csv_path}...")
    csv_source = CSVDataSource(csv_path, source_type=SourceType.TWITTER)
    
    # Fetch sample content
    raw_content = csv_source.fetch_content(query="", limit=10)
    print(f"✓ Loaded {len(raw_content)} items")
    
    # Initialize analyzer
    analyzer = TrainedSentimentAnalyzer(model_path="models/sentiment_model.pkl")
    
    # Analyze each item
    print("\nAnalyzing content:\n")
    
    sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for item in raw_content:
        sentiment = analyzer.analyze(item.content)
        sentiment_counts[sentiment.label.value] += 1
        
        print(f"[{item.source_type.value}] {item.author or 'Unknown'}")
        print(f"  Text: {item.content[:80]}...")
        print(f"  Predicted: {sentiment.label.value.upper()} "
              f"(confidence: {sentiment.score:.2f})")
        print(f"  Original label: {item.metadata.get('sentiment', 'N/A')}")
        print()
    
    # Summary
    print("\n" + "-" * 60)
    print("Summary:")
    print(f"  Positive: {sentiment_counts['positive']}")
    print(f"  Negative: {sentiment_counts['negative']}")
    print(f"  Neutral: {sentiment_counts['neutral']}")
    print("-" * 60)


def demo_api_ready_usage():
    """Demonstrate API-ready usage pattern."""
    print("\n" + "=" * 60)
    print("STEP 4: API-Ready Usage Pattern")
    print("=" * 60)
    
    print("\nThis demonstrates how to use the analyzer in an API context:\n")
    
    # Initialize analyzer (would be done once at API startup)
    analyzer = TrainedSentimentAnalyzer(model_path="models/sentiment_model.pkl")
    
    # Simulate API request
    api_request = {
        "text": "This product exceeded my expectations! Absolutely wonderful!",
        "include_metadata": True
    }
    
    print(f"API Request:")
    print(f"  POST /api/sentiment/analyze")
    print(f"  Body: {api_request}")
    print()
    
    # Process request
    sentiment = analyzer.analyze(api_request["text"])
    
    # Format API response
    api_response = {
        "success": True,
        "data": {
            "text": api_request["text"],
            "sentiment": {
                "label": sentiment.label.value,
                "confidence": round(sentiment.score, 4),
                "intensity": round(sentiment.intensity, 4),
                "compound_score": round(sentiment.compound_score, 4)
            },
            "metadata": {
                "model": "trained_sentiment_model",
                "version": "1.0",
                "analyzed_at": datetime.now().isoformat()
            }
        }
    }
    
    print(f"API Response:")
    import json
    print(json.dumps(api_response, indent=2))


def main():
    """Run complete demo."""
    print("\n" + "=" * 70)
    print(" " * 15 + "SENTIMENT ANALYSIS DEMO")
    print("=" * 70)
    
    try:
        # Step 1: Train model if needed
        if not train_model_if_needed():
            print("\n✗ Failed to train model. Exiting.")
            return
        
        # Step 2: Demo sentiment analysis
        demo_sentiment_analysis()
        
        # Step 3: Demo CSV ingestion and batch analysis
        demo_csv_ingestion_and_analysis()
        
        # Step 4: Demo API-ready usage
        demo_api_ready_usage()
        
        print("\n" + "=" * 70)
        print(" " * 20 + "DEMO COMPLETED!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Use TrainedSentimentAnalyzer in your API endpoints")
        print("  2. Integrate with AnalysisService for full pipeline")
        print("  3. Build dashboard visualizations using the results")
        print("  4. Set up batch processing for large datasets")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
