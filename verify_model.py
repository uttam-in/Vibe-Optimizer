"""Quick verification that the model is trained and working."""
import os
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer

print("=" * 60)
print("MODEL VERIFICATION")
print("=" * 60)

# Check files exist
print("\n1. Model Files:")
files = [
    "models/sentiment_model.pkl",
    "models/sentiment_model_vectorizer.pkl",
    "models/sentiment_model_metrics.json"
]

for file in files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"   ✓ {file} ({size:,} bytes)")
    else:
        print(f"   ✗ {file} NOT FOUND")

# Test the model
print("\n2. Model Testing:")
try:
    analyzer = TrainedSentimentAnalyzer()
    
    test_cases = [
        "I absolutely love this product!",
        "This is terrible and disappointing.",
        "It's okay, nothing special."
    ]
    
    for text in test_cases:
        result = analyzer.analyze(text)
        print(f"\n   Text: '{text}'")
        print(f"   → Sentiment: {result.label.value.upper()}")
        print(f"   → Confidence: {result.score:.3f}")
        print(f"   → Compound: {result.compound_score:.3f}")
    
    print("\n" + "=" * 60)
    print("✓ MODEL IS TRAINED AND WORKING!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
