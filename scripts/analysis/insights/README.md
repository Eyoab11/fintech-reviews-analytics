# Insights & Visualization README

This module generates insights and visualizations from the sentiment and thematic analysis of fintech app reviews.

## Overview
- **Script:** `analyze_insights.py`
- **Input Data:**
  - `data/processed/reviews_cleaned.csv` (cleaned reviews)
  - `data/analysis/sentiment_thematic/sentiment_thematic_results.csv` (sentiment & theme results)
- **Outputs:**
  - Visualizations (PNG files)
  - Insights summary (`insights.json`)

## How to Run
1. Ensure you have the required dependencies:
   ```bash
   pip install -r requirements-viz.txt
   ```
2. Run the analysis script:
   ```bash
   python -m scripts.analysis.insights.analyze_insights
   ```
3. Outputs will be saved in `data/analysis/insights/`.

## Visualizations Generated
1. **Sentiment Distribution by Bank** (`sentiment_distribution.png`)
   - **Type:** Stacked Bar Chart
   - **Description:** Shows the count of positive, neutral, and negative reviews for each bank.

2. **Rating Distribution by Bank** (`rating_distribution.png`)
   - **Type:** Boxplot
   - **Description:** Visualizes the spread and median of review ratings for each bank.

3. **Theme Distribution by Bank** (`theme_distribution.png`)
   - **Type:** Grouped Bar Chart
   - **Description:** Shows the frequency of each identified theme (e.g., Customer Support, Transaction Performance) for each bank.

4. **Keyword Cloud per Bank** (`keyword_cloud_<bank>.png`)
   - **Type:** Word Cloud
   - **Description:** Visualizes the most common keywords in reviews for each bank.

## Insights Output
- **File:** `insights.json`
- **Contents:**
  - Top drivers (positive themes) and pain points (negative themes) per bank
  - Practical recommendations based on the most common pain points

## Customization
- You can modify or extend the script to generate additional plots or insights as needed.
- The script is modular and can be adapted for other types of review analytics.

## Example Usage
After running the script, check the `data/analysis/insights/` directory for all generated plots and the `insights.json` file. Use these outputs for your final report and presentations. 