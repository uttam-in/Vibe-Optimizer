"""
Test script to verify dashboard components
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✓ Streamlit imported")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import plotly
        print("✓ Plotly imported")
    except ImportError as e:
        print(f"✗ Plotly import failed: {e}")
        return False
    
    try:
        from src.ingestion.ingestion_service import CSVDataSource
        print("✓ Ingestion service imported")
    except ImportError as e:
        print(f"✗ Ingestion service import failed: {e}")
        return False
    
    try:
        from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer, VaderSentimentAnalyzer
        print("✓ Sentiment analyzers imported")
    except ImportError as e:
        print(f"✗ Sentiment analyzer import failed: {e}")
        return False
    
    try:
        from src.core.models import RawContent, SentimentLabel, SourceType
        print("✓ Core models imported")
    except ImportError as e:
        print(f"✗ Core models import failed: {e}")
        return False
    
    return True


def test_data_loading():
    """Test data loading functionality"""
    print("\nTesting data loading...")
    
    try:
        from src.ingestion.ingestion_service import CSVDataSource
        
        csv_path = "data/sentimentdataset.csv"
        
        if not os.path.exists(csv_path):
            print(f"✗ Data file not found: {csv_path}")
            return False
        
        csv_source = CSVDataSource(csv_path)
        content = csv_source.fetch_content(limit=10)
        
        if len(content) > 0:
            print(f"✓ Successfully loaded {len(content)} records")
            print(f"  Sample: {content[0].content[:50]}...")
            return True
        else:
            print("✗ No data loaded")
            return False
    
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False


def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("\nTesting sentiment analysis...")
    
    try:
        from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer, VaderSentimentAnalyzer
        
        # Try trained model first
        try:
            analyzer = TrainedSentimentAnalyzer()
            print("✓ Trained model loaded")
        except:
            print("⚠ Trained model not available, using VADER")
            analyzer = VaderSentimentAnalyzer()
            print("✓ VADER analyzer loaded")
        
        # Test analysis
        test_text = "This product is amazing! I love it!"
        result = analyzer.analyze(test_text)
        
        print(f"  Test text: {test_text}")
        print(f"  Sentiment: {result.label.value}")
        print(f"  Confidence: {result.score:.2%}")
        print(f"  Compound: {result.compound_score:.2f}")
        
        return True
    
    except Exception as e:
        print(f"✗ Sentiment analysis failed: {e}")
        return False


def test_dashboard_files():
    """Test that dashboard files exist"""
    print("\nTesting dashboard files...")
    
    files = [
        "src/dashboard/app.py",
        "src/dashboard/config.py",
        "src/dashboard/utils.py",
        "src/dashboard/pages/1_📊_Analytics.py",
        "src/dashboard/pages/2_🔍_Data_Explorer.py",
        "src/dashboard/pages/3_⚙️_Data_Ingestion.py",
        "src/dashboard/README.md"
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} not found")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests"""
    print("="*60)
    print("Dashboard Component Tests")
    print("="*60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Dashboard Files", test_dashboard_files()))
    results.append(("Data Loading", test_data_loading()))
    results.append(("Sentiment Analysis", test_sentiment_analysis()))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("All tests passed! ✓")
        print("\nTo start the dashboard, run:")
        print("  streamlit run src/dashboard/app.py")
        print("\nOr use the quick start script:")
        print("  python src/dashboard/run_dashboard.py")
    else:
        print("Some tests failed. Please fix the issues above.")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
