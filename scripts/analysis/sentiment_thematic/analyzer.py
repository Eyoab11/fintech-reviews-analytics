"""
Sentiment and Thematic Analysis implementation for fintech reviews.
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import json
from pathlib import Path
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentThematicAnalyzer:
    def __init__(self):
        """Initialize the sentiment and thematic analyzer."""
        # Initialize sentiment analyzers
        self.vader = SentimentIntensityAnalyzer()
        
        # Define theme categories and their keywords
        self.theme_keywords = {
            'Account Access Issues': ['login', 'password', 'access', 'account', 'security', 'verify', 'authentication'],
            'Transaction Performance': ['transfer', 'transaction', 'payment', 'money', 'send', 'receive', 'deposit', 'withdraw'],
            'User Interface & Experience': ['interface', 'ui', 'ux', 'design', 'app', 'screen', 'button', 'layout', 'navigation'],
            'Customer Support': ['support', 'help', 'service', 'contact', 'response', 'assist', 'customer service'],
            'Feature Requests': ['feature', 'function', 'option', 'ability', 'should', 'could', 'would like', 'wish']
        }

    def analyze_sentiment(self, text):
        """
        Analyze sentiment of a given text using VADER and TextBlob.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Dictionary containing sentiment label and score
        """
        try:
            # VADER sentiment analysis
            vader_scores = self.vader.polarity_scores(text)
            
            # TextBlob sentiment analysis
            blob = TextBlob(text)
            textblob_score = blob.sentiment.polarity
            
            # Combine scores (weighted average)
            combined_score = (vader_scores['compound'] + textblob_score) / 2
            
            # Determine label
            if combined_score >= 0.05:
                label = 'POSITIVE'
            elif combined_score <= -0.05:
                label = 'NEGATIVE'
            else:
                label = 'NEUTRAL'
            
            return {
                'label': label,
                'score': abs(combined_score),  # Use absolute value for confidence
                'vader_score': vader_scores['compound'],
                'textblob_score': textblob_score
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {'label': 'ERROR', 'score': 0.0, 'vader_score': 0.0, 'textblob_score': 0.0}

    def extract_keywords(self, text):
        """
        Extract keywords from text using simple regex and word frequency.
        
        Args:
            text (str): The text to extract keywords from
            
        Returns:
            list: List of extracted keywords
        """
        # Convert to lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words and remove common words
        words = text.split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'as'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords

    def identify_themes(self, text):
        """
        Identify themes in text based on keyword matching.
        
        Args:
            text (str): The text to identify themes in
            
        Returns:
            list: List of identified themes
        """
        # Convert text to lowercase for matching
        text = text.lower()
        
        theme_scores = defaultdict(int)
        for theme, keywords in self.theme_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    theme_scores[theme] += 1
        
        # Return themes with scores above threshold
        return [theme for theme, score in theme_scores.items() if score > 0]

    def process_reviews(self, reviews_df):
        """
        Process all reviews and return analysis results.
        
        Args:
            reviews_df (pd.DataFrame): DataFrame containing reviews
            
        Returns:
            pd.DataFrame: DataFrame containing analysis results
        """
        results = []
        
        for _, row in reviews_df.iterrows():
            review_text = row['review']
            
            # Analyze sentiment
            sentiment_result = self.analyze_sentiment(review_text)
            
            # Extract keywords
            keywords = self.extract_keywords(review_text)
            
            # Identify themes
            themes = self.identify_themes(review_text)
            
            results.append({
                'review_id': row.name,
                'bank': row['bank'],
                'rating': row['rating'],
                'review_text': review_text,
                'date': row['date'],
                'source': row['source'],
                'sentiment_label': sentiment_result['label'],
                'sentiment_score': sentiment_result['score'],
                'vader_score': sentiment_result['vader_score'],
                'textblob_score': sentiment_result['textblob_score'],
                'keywords': keywords,
                'themes': themes
            })
        
        return pd.DataFrame(results)

    def save_results(self, results_df, output_path):
        """
        Save analysis results to CSV.
        
        Args:
            results_df (pd.DataFrame): DataFrame containing results
            output_path (str or Path): Path to save results
        """
        results_df.to_csv(output_path, index=False)
        logger.info(f"Results saved to {output_path}")

    def generate_summary(self, results_df):
        """
        Generate summary statistics from results.
        
        Args:
            results_df (pd.DataFrame): DataFrame containing results
            
        Returns:
            dict: Dictionary containing summary statistics
        """
        # Convert themes list to string for proper grouping
        results_df['themes_str'] = results_df['themes'].apply(lambda x: '|'.join(x) if x else 'No Theme')
        
        # Calculate theme distribution by bank
        themes_by_bank = {}
        for bank in results_df['bank'].unique():
            bank_themes = results_df[results_df['bank'] == bank]['themes_str'].value_counts().to_dict()
            themes_by_bank[bank] = bank_themes
        
        return {
            'total_reviews': len(results_df),
            'sentiment_distribution': results_df['sentiment_label'].value_counts().to_dict(),
            'themes_by_bank': themes_by_bank,
            'average_sentiment_by_bank': results_df.groupby('bank')['sentiment_score'].mean().to_dict()
        } 