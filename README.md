# Fintech Reviews Analytics
Data analytics project to scrape, analyze, and visualize Google Play Store reviews for Ethiopian banks (CBE, BOA, Dashen).

## Setup
1. Clone the repository: `git clone https://github.com/Eyoab11/fintech-reviews-analytics.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Oracle XE or PostgreSQL (fallback) for database tasks.

## Methodology
- **Task 1**: Scrape 400+ reviews per bank using `google-play-scraper`.
- **Task 2**: Perform sentiment analysis with DistilBERT and thematic analysis with spaCy/TF-IDF.
- **Task 3**: Store cleaned data in Oracle database.
- **Task 4**: Generate insights, visualizations, and recommendations.

## Folder Structure
- `data/`: Raw and processed datasets.
- `scripts/`: Python scripts for scraping, preprocessing, analysis, and visualization.
- `tests/`: Unit tests for scripts.
- `reports/`: Interim and final reports.
- `docs/`: Methodology documentation.
