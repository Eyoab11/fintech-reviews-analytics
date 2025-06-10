"""
Main script to run sentiment and thematic analysis on fintech reviews.
"""

import json
from pathlib import Path
import logging
import pandas as pd
import sys
import os

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.analysis.sentiment_thematic.analyzer import SentimentThematicAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the sentiment and thematic analysis."""
    # Initialize analyzer
    analyzer = SentimentThematicAnalyzer()
    
    # Load reviews data
    data_path = Path("../../../data/processed/reviews_cleaned.csv")
    if not data_path.exists():
        raise FileNotFoundError(f"Reviews file not found at {data_path}")
    
    reviews_df = pd.read_csv(data_path)
    
    # Debug: Print column names
    logger.info("Available columns in the DataFrame:")
    logger.info(reviews_df.columns.tolist())
    
    # Process reviews
    logger.info("Starting sentiment and thematic analysis...")
    results_df = analyzer.process_reviews(reviews_df)
    
    # Create output directories
    output_dir = Path("reports/sentiment_thematic")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save detailed results
    results_path = output_dir / "analysis_results.csv"
    analyzer.save_results(results_df, results_path)
    
    # Generate and save summary
    summary = analyzer.generate_summary(results_df)
    summary_path = output_dir / "analysis_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=4)
    
    logger.info("Analysis completed successfully!")
    logger.info(f"Results saved to {results_path}")
    logger.info(f"Summary saved to {summary_path}")

if __name__ == "__main__":
    main() 