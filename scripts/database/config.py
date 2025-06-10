"""
Database configuration settings.
"""

import os
from pathlib import Path

# Database configuration
DB_CONFIG = {
    'user': os.getenv('ORACLE_USER', 'system'),
    'password': os.getenv('ORACLE_PASSWORD', 'your_password'),
    'dsn': os.getenv('ORACLE_DSN', 'localhost:1521/XEPDB1'),
    'encoding': 'UTF-8'
}

# SQL file paths
SQL_DIR = Path(__file__).parent
CREATE_TABLES_SQL = SQL_DIR / 'create_tables.sql'

# Data file paths
DATA_DIR = Path(__file__).parent.parent.parent / 'data'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
ANALYSIS_DATA_DIR = DATA_DIR / 'analysis'

# Input files
REVIEWS_FILE = PROCESSED_DATA_DIR / 'reviews_cleaned.csv'
SENTIMENT_RESULTS_FILE = ANALYSIS_DATA_DIR / 'sentiment_thematic' / 'sentiment_thematic_results.csv' 