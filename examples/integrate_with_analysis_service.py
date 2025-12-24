"""
Example: Integrating TrainedSentimentAnalyzer with AnalysisService

This shows how to use the trained model with the existing analysis pipeline.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
from src.analysis.analysis_service import AnalysisService
from src.ingestion.ingestion_service import CSVDataSource
from src.core.models import SourceType, Topic


# Mock implementations for demonstration
class MockTopicExtractor:
    """Mock topic extractor for demonstration."""
    
    def extract_topics(self, texts, num_topics=5):
        """Mock topic extraction."""
        return [
            Topic(
                id="topic_1",
                name="Product Quality",
                keywords=["quality", "product", "great"],
                relevance_score=0.8
            ),
            Topic(
                id="topic_2",
                name="Customer Service",
                keywords=["service", "support", "help"],
                relevance_score=0.6
            )
        ]
    
    def assign_topics(self, text, topics):
        """Mock topic assignment."""
        # Simple keyword matching
        text_lower = text.lower()
        assigned = []
        for topic in topics:
            if any(keyword in text_lower for keyword in topic.keywords):
                assigned.append(topic)
        return assigned[:2]  # Return top 2


class MockRepository:
    """Mock repository for demonstration."""
    
    def __init__(self):
        self.storage = []
    
    def save(self, entity):
        """Save entity."""
        self.storage.append(entity)
        return f"id_{len(self.storage)}"
    
    def get_by_id(self, entity_id):
        """Get by ID."""
        return None
    
    def find(self, filters):
        """Find entities."""
        return self.storage
    
    def delete(self, entity_id):
        """Delete entity."""
        return True


def main():
    """Demonstrate integration with AnalysisService."""
    
    print("\n" + "=" * 70)
    print(" " * 15 + "ANALYSIS SERVICE INTEGRATION")
    print("=" * 70)
    
    # Step 1: Initialize components
    print("\n1. Initializing components...")
    
    sentiment_analyzer = TrainedSentimentAnalyzer(
        model_path="models/sentiment_model.pkl"
    )
    topic_extractor = MockTopicExtractor()
    repository = MockRepository()
    
    print("   ✓ Sentiment analyzer loaded")
    print("   ✓ Topic extractor initialized")
    print("   ✓ Repository initialized")
    
    # Step 2: Create AnalysisService
    print("\n2. Creating AnalysisService...")
    
    analysis_service = AnalysisService(
        sentiment_analyzer=sentiment_analyzer,
        topic_extractor=topic_extractor,
        repository=repository
    )
    
    print("   ✓ AnalysisService created")
    
    # Step 3: Load data
    print("\n3. Loading data from CSV...")
    
    csv_source = CSVDataSource("data/sentimentdataset.csv")
    raw_content = csv_source.fetch_content(query="", limit=10)
    
    print(f"   ✓ Loaded {len(raw_content)} items")
    
    # Step 4: Analyze content
    print("\n4. Analyzing content through pipeline...")
    
    analyzed_content = analysis_service.analyze_content(raw_content)
    
    print(f"   ✓ Analyzed {len(analyzed_content)} items")
    
    # Step 5: Display results
    print("\n5. Analysis Results:")
    print("-" * 70)
    
    for i, item in enumerate(analyzed_content[:5], 1):
        print(f"\n{i}. Text: {item.raw_content.content[:60]}...")
        print(f"   Sentiment: {item.sentiment.label.value.upper()}")
        print(f"   Confidence: {item.sentiment.score:.3f}")
        print(f"   Intensity: {item.sentiment.intensity:.3f}")
        print(f"   Compound: {item.sentiment.compound_score:.3f}")
        print(f"   Topics: {', '.join(t.name for t in item.topics) or 'None'}")
        print(f"   Processed: {item.processed_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 6: Summary statistics
    print("\n" + "-" * 70)
    print("6. Summary Statistics:")
    
    sentiment_counts = {}
    total_confidence = 0
    total_intensity = 0
    
    for item in analyzed_content:
        label = item.sentiment.label.value
        sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
        total_confidence += item.sentiment.score
        total_intensity += item.sentiment.intensity
    
    print(f"\n   Total analyzed: {len(analyzed_content)}")
    print(f"\n   Sentiment distribution:")
    for label, count in sentiment_counts.items():
        percentage = (count / len(analyzed_content)) * 100
        print(f"      {label.capitalize()}: {count} ({percentage:.1f}%)")
    
    print(f"\n   Average confidence: {total_confidence / len(analyzed_content):.3f}")
    print(f"   Average intensity: {total_intensity / len(analyzed_content):.3f}")
    
    # Step 7: Repository check
    print("\n7. Repository Status:")
    stored_items = repository.find({})
    print(f"   ✓ {len(stored_items)} items saved to repository")
    
    print("\n" + "=" * 70)
    print(" " * 20 + "INTEGRATION SUCCESSFUL!")
    print("=" * 70)
    
    print("\nThe trained sentiment analyzer is now integrated with:")
    print("  ✓ AnalysisService - Full NLP pipeline")
    print("  ✓ IngestionService - Data loading")
    print("  ✓ Repository - Data persistence")
    
    print("\nNext steps:")
    print("  1. Replace MockTopicExtractor with real implementation")
    print("  2. Replace MockRepository with database repository")
    print("  3. Add entity extraction (NER)")
    print("  4. Connect to API endpoints")
    print("  5. Build dashboard visualizations")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
