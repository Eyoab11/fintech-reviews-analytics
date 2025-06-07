# Fintech Reviews Analytics
Data analytics project to scrape, analyze, and visualize Google Play Store reviews for Ethiopian banks (CBE, BOA, Dashen).

## Setup
1. Clone the repository: `git clone https://github.com/Eyoab11/fintech-reviews-analytics.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Oracle XE or PostgreSQL (fallback) for database tasks.

## Methodology

### Task 1: Data Collection and Preprocessing
- **Scraping**: Used `google-play-scraper` to collect 1,200 reviews (400 per bank) from Google Play Store for CBE (`com.combanketh.mobilebanking`), BOA (`com.boa.boaMobileBanking`), and Dashen (`com.dashen.dashensuperapp`). Fields include review text, rating (1–5), date, bank name, and source ("Google Play"). Saved to `data/raw/reviews_raw.csv`.
- **Preprocessing**: Removed duplicates based on `review`, `rating`, `date`, and `bank`. Handled missing review text (if any) with "No review text". Normalized dates to `YYYY-MM-DD`. Saved cleaned data to `data/processed/reviews_cleaned.csv`.

## Folder Structure
- `data/`: Raw and processed datasets.
- `scripts/`: Python scripts for scraping, preprocessing, analysis, and visualization.
- `tests/`: Unit tests for scripts.
- `reports/`: Interim and final reports.
- `docs/`: Methodology documentation.
