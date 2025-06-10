"""
Database operations for the bank reviews application.
"""

import cx_Oracle
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
import json
import os
from .config import DB_CONFIG, CREATE_TABLES_SQL, REVIEWS_FILE, SENTIMENT_RESULTS_FILE

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Oracle client path
ORACLE_CLIENT_PATH = os.getenv('ORACLE_CLIENT_PATH', r'D:\instantclient_19_20\instantclient_23_8')
if os.path.exists(ORACLE_CLIENT_PATH):
    cx_Oracle.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
    logger.info(f"Oracle client initialized from {ORACLE_CLIENT_PATH}")
else:
    logger.warning(f"Oracle client path {ORACLE_CLIENT_PATH} not found. Please set ORACLE_CLIENT_PATH environment variable.")

class DatabaseManager:
    def __init__(self):
        """Initialize database connection."""
        try:
            self.connection = cx_Oracle.connect(**DB_CONFIG)
            logger.info("Successfully connected to Oracle database")
        except cx_Oracle.Error as error:
            logger.error(f"Error connecting to Oracle database: {error}")
            raise

    def create_tables(self):
        """Create database tables using the SQL script."""
        try:
            with open(CREATE_TABLES_SQL, 'r') as file:
                sql_script = file.read()
            
            cursor = self.connection.cursor()
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            self.connection.commit()
            logger.info("Successfully created database tables")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise

    def insert_banks(self, banks_df):
        """Insert unique banks into the banks table."""
        try:
            cursor = self.connection.cursor()
            
            # Get existing banks
            cursor.execute("SELECT bank_name FROM banks")
            existing_banks = {row[0] for row in cursor.fetchall()}
            
            # Insert new banks
            for bank_name in banks_df['bank'].unique():
                if bank_name not in existing_banks:
                    cursor.execute(
                        "INSERT INTO banks (bank_name) VALUES (:1)",
                        [bank_name]
                    )
            
            self.connection.commit()
            logger.info("Successfully inserted banks")
        except Exception as e:
            logger.error(f"Error inserting banks: {e}")
            raise

    def insert_reviews(self, reviews_df):
        """Insert reviews into the reviews table."""
        try:
            cursor = self.connection.cursor()
            
            # Get bank IDs
            cursor.execute("SELECT bank_id, bank_name FROM banks")
            bank_ids = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Prepare data for insertion
            for _, row in reviews_df.iterrows():
                bank_id = bank_ids[row['bank']]
                
                # Convert themes and keywords to strings
                themes = '|'.join(row['themes']) if isinstance(row['themes'], list) else row['themes']
                keywords = '|'.join(row['keywords']) if isinstance(row['keywords'], list) else row['keywords']
                
                cursor.execute("""
                    INSERT INTO reviews (
                        bank_id, review_text, rating, review_date, source,
                        sentiment_label, sentiment_score, vader_score, textblob_score,
                        themes, keywords
                    ) VALUES (
                        :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11
                    )
                """, [
                    bank_id,
                    row['review'],
                    float(row['rating']),
                    datetime.strptime(row['date'], '%Y-%m-%d').date(),
                    row['source'],
                    row['sentiment_label'],
                    float(row['sentiment_score']),
                    float(row['vader_score']),
                    float(row['textblob_score']),
                    themes,
                    keywords
                ])
            
            self.connection.commit()
            logger.info("Successfully inserted reviews")
        except Exception as e:
            logger.error(f"Error inserting reviews: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if hasattr(self, 'connection'):
            self.connection.close()
            logger.info("Database connection closed")

def main():
    """Main function to populate the database."""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Create tables
        db_manager.create_tables()
        
        # Load data
        reviews_df = pd.read_csv(REVIEWS_FILE)
        sentiment_df = pd.read_csv(SENTIMENT_RESULTS_FILE)
        
        # Merge data
        merged_df = pd.merge(
            reviews_df,
            sentiment_df[['review_id', 'sentiment_label', 'sentiment_score', 
                         'vader_score', 'textblob_score', 'themes', 'keywords']],
            left_index=True,
            right_on='review_id',
            how='left'
        )
        
        # Insert data
        db_manager.insert_banks(merged_df)
        db_manager.insert_reviews(merged_df)
        
        logger.info("Database population completed successfully")
    except Exception as e:
        logger.error(f"Error in database population: {e}")
        raise
    finally:
        if 'db_manager' in locals():
            db_manager.close()

if __name__ == "__main__":
    main() 