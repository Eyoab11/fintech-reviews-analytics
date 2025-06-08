import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def mock_input_csv(tmp_path):
    """Create a mock input CSV for testing preprocessing."""
    data = [
        {"review": "Love the app", "rating": 5, "date": "2023-10-15 12:34:56", "bank": "CBE", "source": "Google Play"},
        {"review": "App crashes often", "rating": 2, "date": "2023-10-16 09:00:00", "bank": "BOA", "source": "Google Play"},
        {"review": None, "rating": 3, "date": "2023-10-17 14:22:33", "bank": "Dashen", "source": "Google Play"},
        {"review": "Love the app", "rating": 5, "date": "2023-10-15 12:34:56", "bank": "CBE", "source": "Google Play"}
    ]
    df = pd.DataFrame(data)
    input_path = tmp_path / "data" / "raw" / "mock_reviews.csv"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(input_path, index=False)
    return input_path

@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary directory for test output."""
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)
    return processed_dir

def test_preprocess_reviews_columns(mock_input_csv, output_dir):
    """Test that preprocessing produces a CSV with correct columns."""
    from scripts.preprocessing.preprocess_reviews import preprocess_reviews
    output_path = output_dir / "reviews_cleaned.csv"
    preprocess_reviews(mock_input_csv, output_path)

    df = pd.read_csv(output_path)
    expected_columns = ["review", "rating", "date", "bank", "source"]
    assert list(df.columns) == expected_columns, f"Expected columns {expected_columns}, got {df.columns}"

def test_preprocess_reviews_duplicates(mock_input_csv, output_dir):
    """Test that duplicates are removed."""
    from scripts.preprocessing.preprocess_reviews import preprocess_reviews
    output_path = output_dir / "reviews_cleaned.csv"
    preprocess_reviews(mock_input_csv, output_path)

    df = pd.read_csv(output_path)
    assert len(df) == 3, f"Expected 3 rows after removing duplicates, got {len(df)}"

def test_preprocess_reviews_date_format(mock_input_csv, output_dir):
    """Test that dates are normalized to YYYY-MM-DD."""
    from scripts.preprocessing.preprocess_reviews import preprocess_reviews
    output_path = output_dir / "reviews_cleaned.csv"
    preprocess_reviews(mock_input_csv, output_path)

    df = pd.read_csv(output_path)
    for date in df["date"]:
        try:
            pd.to_datetime(date, format="%Y-%m-%d")
        except ValueError:
            pytest.fail(f"Date {date} not in YYYY-MM-DD format")

def test_preprocess_reviews_missing_reviews(mock_input_csv, output_dir):
    """Test that missing reviews are handled."""
    from scripts.preprocessing.preprocess_reviews import preprocess_reviews
    output_path = output_dir / "reviews_cleaned.csv"
    preprocess_reviews(mock_input_csv, output_path)

    df = pd.read_csv(output_path)
    assert not df["review"].isna().any(), "Missing reviews not handled"
    assert all(df["review"] != ""), "Empty reviews not handled"
    assert "No review text" in df["review"].values, "Missing reviews not replaced with 'No review text'"