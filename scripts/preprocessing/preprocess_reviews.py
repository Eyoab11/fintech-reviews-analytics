# scripts/preprocessing/preprocess_reviews.py
import pandas as pd

# Load raw data
df = pd.read_csv("data/raw/reviews_raw.csv")

# Remove duplicates
df = df.drop_duplicates(subset=["review", "rating", "date", "bank"])

# Handle missing data
df["review"] = df["review"].fillna("No review text")  # Replace NaN with placeholder
# Check for other missing values
print(df.isna().sum())

# Normalize dates
df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

# Validate columns
expected_columns = ["review", "rating", "date", "bank", "source"]
assert all(col in df.columns for col in expected_columns), "Missing required columns"

# Save cleaned data
df.to_csv("data/processed/reviews_cleaned.csv", index=False)
print("Saved cleaned reviews to data/processed/reviews_cleaned.csv")