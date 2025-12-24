"""
Complete workflow example: Training → Analysis → API → Dashboard

This example demonstrates the full pipeline from training a model
to using it in production-ready applications.
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def step1_train_model():
    """Step 1: Train the sentiment analysis model."""
    print("\n" + "=" * 70)
    print("STEP 1: Training Sentiment Model")
    print("=" * 70)
    
    from src.analysis.model_trainer import SentimentModelTrainer
    
    # Check if model already exists
    if os.path.exists("models/sentiment_model.pkl"):
        print("✓ Model already exists. Skipping training.")
        print("  (Delete models/sentiment_model.pkl to retrain)")
        return True
    
    try:
        # Initialize trainer
        trainer = SentimentModelTrainer(model_dir="models")
        
        # Load data
        print("\nLoading training data...")
        texts, labels = trainer.load_data_from_csv("data/sentimentdataset.csv")
        print(f"✓ Loaded {len(texts)} samples")
        
        # Train model
        print("\nTraining model (this may take a minute)...")
        metrics = trainer.train(
            texts=texts,
            labels=labels,
            algorithm='logistic_regression',
            test_size=0.2
        )
        
        print(f"✓ Training completed!")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        
        # Save model
        trainer.save_model(model_name='sentiment_model')
        print("✓ Model saved successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Error training model: {e}")
        return False


def step2_test_analyzer():
    """Step 2: Test the trained analyzer."""
    print("\n" + "=" * 70)
    print("STEP 2: Testing Sentiment Analyzer")
    print("=" * 70)
    
    from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
    
    try:
        # Initialize analyzer
        analyzer = TrainedSentimentAnalyzer(model_path="models/sentiment_model.pkl")
        print("✓ Analyzer loaded successfully")
        
        # Test samples
        test_cases = [
            ("I absolutely love this! Best ever!", "positive"),
            ("This is terrible and disappointing.", "negative"),
            ("It's okay, nothing special.", "neutral"),
            ("Amazing quality! Highly recommend!", "positive"),
            ("Worst experience. Very frustrated.", "negative"),
        ]
        
        print("\nTesting predictions:\n")
        correct = 0
        
        for text, expected in test_cases:
            sentiment = analyzer.analyze(text)
            is_correct = sentiment.label.value == expected
            correct += is_correct
            
            status = "✓" if is_correct else "✗"
            print(f"{status} Text: '{text}'")
            print(f"  Expected: {expected}, Got: {sentiment.label.value}")
            print(f"  Confidence: {sentiment.score:.3f}, "
                  f"Intensity: {sentiment.intensity:.3f}")
            print()
        
        accuracy = correct / len(test_cases)
        print(f"Test Accuracy: {accuracy:.1%} ({correct}/{len(test_cases)})")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing analyzer: {e}")
        return False


def step3_batch_analysis():
    """Step 3: Perform batch analysis on CSV data."""
    print("\n" + "=" * 70)
    print("STEP 3: Batch Analysis from CSV")
    print("=" * 70)
    
    from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
    from src.ingestion.ingestion_service import CSVDataSource
    from src.core.models import SourceType
    
    try:
        # Initialize components
        analyzer = TrainedSentimentAnalyzer(model_path="models/sentiment_model.pkl")
        csv_source = CSVDataSource("data/sentimentdataset.csv")
        
        # Fetch data
        print("\nFetching data from CSV...")
        raw_content = csv_source.fetch_content(query="", limit=20)
        print(f"✓ Loaded {len(raw_content)} items")
        
        # Analyze
        print("\nAnalyzing content...")
        results = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for item in raw_content:
            sentiment = analyzer.analyze(item.content)
            sentiment_counts[sentiment.label.value] += 1
            
            results.append({
                'text': item.content,
                'predicted': sentiment.label.value,
                'original': item.metadata.get('sentiment', '').strip().lower(),
                'confidence': sentiment.score
            })
        
        # Display summary
        print(f"\n✓ Analysis completed!")
        print(f"\nSentiment Distribution:")
        for label, count in sentiment_counts.items():
            percentage = (count / len(results)) * 100
            print(f"  {label.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Calculate accuracy
        matches = sum(1 for r in results 
                     if r['predicted'] == r['original'] 
                     and r['original'] in ['positive', 'negative', 'neutral'])
        valid = sum(1 for r in results 
                   if r['original'] in ['positive', 'negative', 'neutral'])
        
        if valid > 0:
            accuracy = matches / valid
            print(f"\nModel Accuracy: {accuracy:.1%} ({matches}/{valid} correct)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in batch analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


def step4_api_simulation():
    """Step 4: Simulate API usage."""
    print("\n" + "=" * 70)
    print("STEP 4: API Usage Simulation")
    print("=" * 70)
    
    from src.api.sentiment_api_example import (
        SentimentAnalysisAPI,
        SentimentAnalysisRequest,
        BatchAnalysisRequest
    )
    
    try:
        # Initialize API
        api = SentimentAnalysisAPI(model_path="models/sentiment_model.pkl")
        print("✓ API service initialized")
        
        # Test single analysis
        print("\n1. Single Text Analysis:")
        request = SentimentAnalysisRequest(
            text="This product is absolutely amazing! Love it!",
            include_metadata=True
        )
        
        response = api.analyze_single(request)
        
        if response.success:
            print("✓ Request successful")
            print(f"  Sentiment: {response.data['sentiment']['label']}")
            print(f"  Confidence: {response.data['sentiment']['confidence']}")
        else:
            print(f"✗ Request failed: {response.error}")
        
        # Test batch analysis
        print("\n2. Batch Analysis:")
        batch_request = BatchAnalysisRequest(
            texts=[
                "Great product!",
                "Terrible service.",
                "It's okay.",
                "Best purchase ever!",
                "Very disappointed."
            ],
            include_metadata=False
        )
        
        batch_response = api.analyze_batch(batch_request)
        
        if batch_response.success:
            print("✓ Batch request successful")
            summary = batch_response.data['summary']
            print(f"  Total analyzed: {summary['total_analyzed']}")
            print(f"  Distribution: {summary['sentiment_distribution']}")
            print(f"  Avg confidence: {summary['average_confidence']}")
        else:
            print(f"✗ Batch request failed: {batch_response.error}")
        
        # Get model info
        print("\n3. Model Information:")
        info = api.get_model_info()
        print(f"  Model type: {info['model_type']}")
        print(f"  Version: {info['version']}")
        print(f"  Supported labels: {', '.join(info['supported_labels'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in API simulation: {e}")
        import traceback
        traceback.print_exc()
        return False


def step5_dashboard_data():
    """Step 5: Prepare dashboard data."""
    print("\n" + "=" * 70)
    print("STEP 5: Dashboard Data Preparation")
    print("=" * 70)
    
    from src.dashboard.sentiment_dashboard_example import SentimentDashboardData
    
    try:
        # Initialize dashboard
        dashboard = SentimentDashboardData(model_path="models/sentiment_model.pkl")
        print("✓ Dashboard data provider initialized")
        
        # Analyze dataset
        print("\nAnalyzing dataset for dashboard...")
        df = dashboard.analyze_dataset("data/sentimentdataset.csv", limit=50)
        print(f"✓ Analyzed {len(df)} samples")
        
        # Get metrics
        print("\nDashboard Metrics:")
        
        # 1. Distribution
        dist = dashboard.get_sentiment_distribution(df)
        print(f"\n1. Sentiment Distribution:")
        for label, count in dist.items():
            print(f"   {label.capitalize()}: {count}")
        
        # 2. Average metrics
        metrics = dashboard.get_average_metrics(df)
        print(f"\n2. Average Metrics:")
        print(f"   Confidence: {metrics['avg_confidence']:.3f}")
        print(f"   Intensity: {metrics['avg_intensity']:.3f}")
        print(f"   Compound: {metrics['avg_compound_score']:.3f}")
        
        # 3. Top positive
        print(f"\n3. Top Positive Text:")
        top_pos = dashboard.get_top_positive_texts(df, n=1)
        if len(top_pos) > 0:
            text = top_pos.iloc[0]['text']
            score = top_pos.iloc[0]['compound_score']
            print(f"   '{text[:60]}...'")
            print(f"   Score: {score:.3f}")
        
        # 4. Top negative
        print(f"\n4. Top Negative Text:")
        top_neg = dashboard.get_top_negative_texts(df, n=1)
        if len(top_neg) > 0:
            text = top_neg.iloc[0]['text']
            score = top_neg.iloc[0]['compound_score']
            print(f"   '{text[:60]}...'")
            print(f"   Score: {score:.3f}")
        
        # 5. Accuracy
        accuracy = dashboard.get_model_accuracy(df)
        print(f"\n5. Model Accuracy:")
        print(f"   Accuracy: {accuracy['accuracy']:.1%}")
        print(f"   Samples compared: {accuracy['total_compared']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error preparing dashboard data: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run complete workflow."""
    print("\n" + "=" * 70)
    print(" " * 15 + "COMPLETE WORKFLOW DEMONSTRATION")
    print("=" * 70)
    print("\nThis demonstrates the full pipeline:")
    print("  1. Train sentiment model")
    print("  2. Test the analyzer")
    print("  3. Batch analysis from CSV")
    print("  4. API usage simulation")
    print("  5. Dashboard data preparation")
    
    steps = [
        ("Training Model", step1_train_model),
        ("Testing Analyzer", step2_test_analyzer),
        ("Batch Analysis", step3_batch_analysis),
        ("API Simulation", step4_api_simulation),
        ("Dashboard Data", step5_dashboard_data),
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            success = step_func()
            results.append((step_name, success))
        except Exception as e:
            print(f"\n✗ Unexpected error in {step_name}: {e}")
            results.append((step_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print(" " * 25 + "SUMMARY")
    print("=" * 70)
    
    for step_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {step_name}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n" + "=" * 70)
        print(" " * 15 + "🎉 ALL STEPS COMPLETED SUCCESSFULLY! 🎉")
        print("=" * 70)
        print("\nYour sentiment analysis system is ready!")
        print("\nNext steps:")
        print("  • Integrate TrainedSentimentAnalyzer into your API")
        print("  • Build a Streamlit dashboard using dashboard components")
        print("  • Set up batch processing for large datasets")
        print("  • Monitor model performance and retrain periodically")
    else:
        print("\n" + "=" * 70)
        print(" " * 20 + "⚠ SOME STEPS FAILED ⚠")
        print("=" * 70)
        print("\nPlease review the errors above and:")
        print("  • Ensure data/sentimentdataset.csv exists")
        print("  • Check that all dependencies are installed")
        print("  • Verify file permissions for models/ directory")


if __name__ == "__main__":
    main()
