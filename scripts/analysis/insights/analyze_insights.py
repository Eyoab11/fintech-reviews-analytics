"""
Generate insights and visualizations from sentiment and thematic analysis results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from wordcloud import WordCloud
from collections import Counter
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightsAnalyzer:
    def __init__(self):
        """Initialize the insights analyzer."""
        # Set up paths
        self.base_dir = Path(__file__).parent.parent.parent.parent
        self.data_dir = self.base_dir / "data"
        self.processed_dir = self.data_dir / "processed"
        self.analysis_dir = self.data_dir / "analysis"
        self.output_dir = self.analysis_dir / "insights"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load data
        self.reviews_df = pd.read_csv(self.processed_dir / "reviews_cleaned.csv")
        self.sentiment_df = pd.read_csv(
            self.analysis_dir / "sentiment_thematic" / "sentiment_thematic_results.csv"
        )
        
        # Merge data
        self.merged_df = pd.merge(
            self.reviews_df,
            self.sentiment_df[['review_id', 'sentiment_label', 'sentiment_score', 
                             'vader_score', 'textblob_score', 'themes', 'keywords']],
            left_index=True,
            right_on='review_id',
            how='left'
        )
        
        # Set up plotting style
        plt.style.use('seaborn')
        sns.set_palette("husl")

    def analyze_sentiment_distribution(self):
        """Analyze and visualize sentiment distribution by bank."""
        plt.figure(figsize=(12, 6))
        
        # Create sentiment distribution plot
        sentiment_counts = self.merged_df.groupby(['bank', 'sentiment_label']).size().unstack()
        sentiment_counts.plot(kind='bar', stacked=True)
        
        plt.title('Sentiment Distribution by Bank')
        plt.xlabel('Bank')
        plt.ylabel('Number of Reviews')
        plt.legend(title='Sentiment')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot
        plt.savefig(self.output_dir / 'sentiment_distribution.png')
        plt.close()

    def analyze_rating_distribution(self):
        """Analyze and visualize rating distribution by bank."""
        plt.figure(figsize=(12, 6))
        
        # Create rating distribution plot
        sns.boxplot(data=self.merged_df, x='bank', y='rating')
        
        plt.title('Rating Distribution by Bank')
        plt.xlabel('Bank')
        plt.ylabel('Rating')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot
        plt.savefig(self.output_dir / 'rating_distribution.png')
        plt.close()

    def generate_keyword_cloud(self):
        """Generate and save keyword cloud for each bank."""
        for bank in self.merged_df['bank'].unique():
            # Get keywords for the bank
            bank_keywords = self.merged_df[self.merged_df['bank'] == bank]['keywords']
            all_keywords = ' '.join([str(kw) for kw in bank_keywords if isinstance(kw, str)])
            
            # Generate word cloud
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                max_words=100
            ).generate(all_keywords)
            
            # Create and save plot
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Keyword Cloud - {bank}')
            plt.tight_layout()
            
            # Save plot
            plt.savefig(self.output_dir / f'keyword_cloud_{bank.lower().replace(" ", "_")}.png')
            plt.close()

    def analyze_themes(self):
        """Analyze theme distribution and generate insights."""
        # Convert themes string to list
        self.merged_df['themes_list'] = self.merged_df['themes'].apply(
            lambda x: x.split('|') if isinstance(x, str) else []
        )
        
        # Count themes by bank
        theme_counts = {}
        for bank in self.merged_df['bank'].unique():
            bank_themes = self.merged_df[self.merged_df['bank'] == bank]['themes_list']
            all_themes = [theme for themes in bank_themes for theme in themes]
            theme_counts[bank] = Counter(all_themes)
        
        # Create theme distribution plot
        plt.figure(figsize=(12, 6))
        
        # Prepare data for plotting
        theme_data = []
        for bank, counts in theme_counts.items():
            for theme, count in counts.items():
                theme_data.append({
                    'Bank': bank,
                    'Theme': theme,
                    'Count': count
                })
        
        theme_df = pd.DataFrame(theme_data)
        
        # Create plot
        sns.barplot(data=theme_df, x='Theme', y='Count', hue='Bank')
        
        plt.title('Theme Distribution by Bank')
        plt.xlabel('Theme')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.legend(title='Bank')
        plt.tight_layout()
        
        # Save plot
        plt.savefig(self.output_dir / 'theme_distribution.png')
        plt.close()
        
        return theme_counts

    def generate_insights(self):
        """Generate insights and recommendations."""
        insights = {
            'drivers': {},
            'pain_points': {},
            'recommendations': []
        }
        
        # Analyze sentiment and themes by bank
        for bank in self.merged_df['bank'].unique():
            bank_data = self.merged_df[self.merged_df['bank'] == bank]
            
            # Get top positive themes
            positive_reviews = bank_data[bank_data['sentiment_label'] == 'POSITIVE']
            positive_themes = Counter([
                theme for themes in positive_reviews['themes_list']
                for theme in themes
            ])
            
            # Get top negative themes
            negative_reviews = bank_data[bank_data['sentiment_label'] == 'NEGATIVE']
            negative_themes = Counter([
                theme for themes in negative_reviews['themes_list']
                for theme in themes
            ])
            
            # Store insights
            insights['drivers'][bank] = dict(positive_themes.most_common(2))
            insights['pain_points'][bank] = dict(negative_themes.most_common(2))
        
        # Generate recommendations based on insights
        all_pain_points = Counter()
        for pain_points in insights['pain_points'].values():
            all_pain_points.update(pain_points)
        
        # Add recommendations based on common pain points
        for theme, count in all_pain_points.most_common(3):
            if theme == 'User Interface & Experience':
                insights['recommendations'].append(
                    "Improve app UI/UX with modern design principles and better navigation"
                )
            elif theme == 'Transaction Performance':
                insights['recommendations'].append(
                    "Optimize transaction processing speed and reliability"
                )
            elif theme == 'Customer Support':
                insights['recommendations'].append(
                    "Enhance customer support with 24/7 availability and faster response times"
                )
        
        return insights

    def generate_report(self):
        """Generate the final analysis report."""
        # Create visualizations
        self.analyze_sentiment_distribution()
        self.analyze_rating_distribution()
        self.generate_keyword_cloud()
        theme_counts = self.analyze_themes()
        
        # Generate insights
        insights = self.generate_insights()
        
        # Save insights to JSON
        with open(self.output_dir / 'insights.json', 'w') as f:
            json.dump(insights, f, indent=4)
        
        logger.info("Analysis completed successfully!")
        logger.info(f"Results saved to {self.output_dir}")

def main():
    """Run the insights analysis."""
    analyzer = InsightsAnalyzer()
    analyzer.generate_report()

if __name__ == "__main__":
    main() 