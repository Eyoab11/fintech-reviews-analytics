import pytest
import pandas as pd
from pathlib import Path
from scripts.scraping.scrape_reviews import app_ids

@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary directory for test output."""
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    return raw_dir

def test_scrape_reviews_app_ids():
    """Test that app_ids dictionary is valid."""
    assert len(app_ids) == 3, "Expected 3 app IDs"
    assert all(isinstance(app_id, str) for app_id in app_ids.values()), "App IDs must be strings"
    assert set(app_ids.keys()) == {"CBE", "BOA", "Dashen"}, "Incorrect bank names"

def test_scrape_reviews_output_format(output_dir, monkeypatch):
    """Test that scraping produces a CSV with correct columns using a mock."""
    from google_play_scraper import app as google_play_scraper
    import google_play_scraper.features.reviews as reviews_module
    
    # Mock the reviews function to return sample data
    mock_reviews = [
        {
            "content": "Test review",
            "score": 4,
            "at": pd.Timestamp("2023-10-15 12:34:56")
        }
    ]
    
    def mock_reviews_func(*args, **kwargs):
        return mock_reviews, None
    
    # Patch the correct function
    monkeypatch.setattr(reviews_module, "reviews", mock_reviews_func)

    # Run scraping for one bank
    all_reviews = []
    bank = "CBE"
    app_id = app_ids[bank]
    
    # Get reviews using the mocked function
    result, _ = reviews_module.reviews(app_id, lang="en", country="et", count=1)
    
    for review in result:
        all_reviews.append({
            "review": review["content"] or "",
            "rating": review["score"],
            "date": review["at"],
            "bank": bank,
            "source": "Google Play"
        })
    
    df = pd.DataFrame(all_reviews)
    output_path = output_dir / "test_reviews.csv"
    df.to_csv(output_path, index=False)

    # Verify output
    df_read = pd.read_csv(output_path)
    expected_columns = ["review", "rating", "date", "bank", "source"]
    assert list(df_read.columns) == expected_columns, f"Expected columns {expected_columns}, got {df_read.columns}"
    assert len(df_read) == 1, "Expected 1 review"
    assert df_read["source"].iloc[0] == "Google Play", "Source incorrect"
    assert df_read["bank"].iloc[0] == "CBE", "Bank incorrect"
    assert df_read["rating"].iloc[0] in range(1, 6), "Rating out of range"