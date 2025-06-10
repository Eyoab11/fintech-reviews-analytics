import pytest
import pandas as pd
from scripts.sentiment_thematic_analysis import SentimentThematicAnalyzer

@pytest.fixture
def analyzer():
    return SentimentThematicAnalyzer()

@pytest.fixture
def sample_reviews():
    return pd.DataFrame({
        'review_id': [1, 2, 3],
        'bank': ['Bank A', 'Bank B', 'Bank A'],
        'rating': [5, 1, 4],
        'review_text': [
            "Great app! The interface is very user-friendly and transfers are quick.",
            "Terrible experience. Can't login and customer support is unresponsive.",
            "Good features but the app crashes sometimes during transactions."
        ]
    })


def test_sentiment_analysis(analyzer):
    # Test positive sentiment
    result = analyzer.analyze_sentiment("Great app with excellent features!")
    assert result['label'] in ['POSITIVE', 'NEGATIVE']
    assert 0 <= result['score'] <= 1

    # Test negative sentiment
    result = analyzer.analyze_sentiment("Terrible experience, app keeps crashing")
    assert result['label'] in ['POSITIVE', 'NEGATIVE']
    assert 0 <= result['score'] <= 1

def test_keyword_extraction(analyzer):
    text = "The app interface is user-friendly and transfers are quick"
    keywords = analyzer.extract_keywords(text)
    assert len(keywords) > 0
    assert all(isinstance(k, str) for k in keywords)

def test_theme_identification(analyzer):
    # Test UI theme
    text = "The interface is very user-friendly and easy to navigate"
    themes = analyzer.identify_themes(text)
    assert 'User Interface & Experience' in themes

    # Test transaction theme
    text = "Transfers are quick and payments process instantly"
    themes = analyzer.identify_themes(text)
    assert 'Transaction Performance' in themes

def test_process_reviews(analyzer, sample_reviews):
    results = analyzer.process_reviews(sample_reviews)
    
    # Check if all required columns are present
    required_columns = ['review_id', 'bank', 'rating', 'review_text', 
                       'sentiment_label', 'sentiment_score', 'keywords', 'themes']
    assert all(col in results.columns for col in required_columns)
    
    # Check if results have the same number of rows as input
    assert len(results) == len(sample_reviews)
    
    # Check if sentiment scores are within valid range
    assert all(0 <= score <= 1 for score in results['sentiment_score'])
    
    # Check if themes are lists
    assert all(isinstance(themes, list) for themes in results['themes']) 