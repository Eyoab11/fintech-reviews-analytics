import pandas as pd

def preprocess_reviews(input_path, output_path):
    # Load raw data
    df = pd.read_csv(input_path)

    # Remove duplicates
    df = df.drop_duplicates(subset=["review", "rating", "date", "bank"])

    # Handle missing data
    df["review"] = df["review"].fillna("No review text")  # Replace NaN with placeholder
    print(df.isna().sum())  # Check for other missing values

    # Normalize dates
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # Validate columns
    expected_columns = ["review", "rating", "date", "bank", "source"]
    assert all(col in df.columns for col in expected_columns), "Missing required columns"

    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned reviews to {output_path}")
    return df

if __name__ == "__main__":
    preprocess_reviews("data/raw/reviews_raw.csv", "data/processed/reviews_cleaned.csv")