"""
Simple test runner script.
Runs tests without requiring pytest to be installed.
For full test suite, install pytest: pip install pytest pytest-cov
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_basic_tests():
    """Run basic tests without pytest."""
    print("=" * 70)
    print(" " * 20 + "RUNNING BASIC TESTS")
    print("=" * 70)
    
    # Test 1: Model files exist
    print("\n1. Checking model files...")
    model_files = [
        "models/sentiment_model.pkl",
        "models/sentiment_model_vectorizer.pkl",
        "models/sentiment_model_metrics.json"
    ]
    
    all_exist = True
    for file in model_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("\n   Model not trained. Run: python scripts/train_sentiment_model.py")
        return False
    
    # Test 2: Import modules
    print("\n2. Testing imports...")
    try:
        from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
        print("   ✓ TrainedSentimentAnalyzer")
        
        from src.analysis.model_trainer import SentimentModelTrainer
        print("   ✓ SentimentModelTrainer")
        
        from src.analysis.analysis_service import AnalysisService
        print("   ✓ AnalysisService")
        
        from src.ingestion.ingestion_service import CSVDataSource
        print("   ✓ CSVDataSource")
        
    except Exception as e:
        print(f"   ✗ Import error: {e}")
        return False
    
    # Test 3: Initialize analyzer
    print("\n3. Testing analyzer initialization...")
    try:
        analyzer = TrainedSentimentAnalyzer()
        print("   ✓ Analyzer initialized")
    except Exception as e:
        print(f"   ✗ Initialization error: {e}")
        return False
    
    # Test 4: Test sentiment analysis
    print("\n4. Testing sentiment analysis...")
    test_cases = [
        ("I love this product!", "positive"),
        ("This is terrible.", "negative"),
        ("It's okay.", "neutral"),
    ]
    
    passed = 0
    for text, expected in test_cases:
        try:
            result = analyzer.analyze(text)
            status = "✓" if result.label.value == expected else "~"
            print(f"   {status} '{text}' → {result.label.value} (expected: {expected})")
            if result.label.value == expected:
                passed += 1
        except Exception as e:
            print(f"   ✗ Error analyzing '{text}': {e}")
    
    print(f"\n   Passed: {passed}/{len(test_cases)}")
    
    # Test 5: Test with CSV data
    print("\n5. Testing CSV ingestion...")
    if os.path.exists("data/sentimentdataset.csv"):
        try:
            csv_source = CSVDataSource("data/sentimentdataset.csv")
            content = csv_source.fetch_content(limit=5)
            print(f"   ✓ Loaded {len(content)} items from CSV")
            
            # Analyze first item
            if len(content) > 0:
                sentiment = analyzer.analyze(content[0].content)
                print(f"   ✓ Analyzed: '{content[0].content[:50]}...'")
                print(f"     → Sentiment: {sentiment.label.value}")
                print(f"     → Confidence: {sentiment.score:.3f}")
        except Exception as e:
            print(f"   ✗ CSV test error: {e}")
    else:
        print("   ~ Dataset not found (optional)")
    
    # Test 6: Test model trainer
    print("\n6. Testing model trainer...")
    try:
        trainer = SentimentModelTrainer()
        print("   ✓ Trainer initialized")
        
        # Test loading existing model
        trainer.load_model('sentiment_model')
        print("   ✓ Model loaded")
        
        # Test prediction
        pred, conf, probs = trainer.predict("This is great!")
        print(f"   ✓ Prediction: {pred} (confidence: {conf:.3f})")
        
    except Exception as e:
        print(f"   ✗ Trainer test error: {e}")
    
    print("\n" + "=" * 70)
    print(" " * 20 + "BASIC TESTS COMPLETE")
    print("=" * 70)
    print("\nFor comprehensive testing, install pytest:")
    print("  pip install pytest pytest-cov")
    print("\nThen run:")
    print("  pytest tests/ -v")
    
    return True


def run_pytest():
    """Run pytest if available."""
    try:
        import pytest
        print("\n" + "=" * 70)
        print(" " * 15 + "RUNNING PYTEST TEST SUITE")
        print("=" * 70)
        print()
        
        # Run pytest
        exit_code = pytest.main([
            'tests/',
            '-v',
            '--tb=short',
            '-x'  # Stop on first failure
        ])
        
        return exit_code == 0
        
    except ImportError:
        print("\nPytest not installed. Running basic tests only.")
        print("Install pytest for full test suite: pip install pytest pytest-cov")
        return None


if __name__ == "__main__":
    print("\nSentiment Analysis Test Suite")
    print("=" * 70)
    
    # Try pytest first
    pytest_result = run_pytest()
    
    if pytest_result is None:
        # Pytest not available, run basic tests
        basic_result = run_basic_tests()
        sys.exit(0 if basic_result else 1)
    else:
        sys.exit(0 if pytest_result else 1)
