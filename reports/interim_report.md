# Interim Report: Bank App Reviews Analysis  
**Date**: June 8, 2024  
**Author**: Eyoab Amare  

## Project Overview  
This project analyzes customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:  
- Commercial Bank of Ethiopia (CBE)  
- Bank of Abyssinia (BOA)  
- Dashen Bank  

## Task 1: Data Collection and Preprocessing  

### 1. Implementation Summary  

**Data Collection:**  
- Collected 400+ reviews per bank using the google-play-scraper library  
- Implemented continuation tokens for pagination  
- Added 1-second delay between requests to avoid rate limiting  
- Handled empty responses and exceptions gracefully  

**Preprocessing Pipeline:**  
- Removed 32 duplicate reviews  
- Filled 27 empty reviews with "No review text" placeholder  
- Standardized all dates to YYYY-MM-DD format  
- Validated required columns: ["review", "rating", "date", "bank", "source"]  

### 2. Key Metrics  

| Metric                | Value          |
|-----------------------|----------------|
| Total reviews collected | 1200+         |
| Duplicates removed    | 32             |
| Empty reviews handled | 27             |
| Missing data rate     | 2.3%           |

### 3. Outputs  
- **Raw data**: `data/raw/reviews_raw.csv`  
- **Processed data**: `data/processed/reviews_cleaned.csv`  
- Folder structure:  
# Interim Report: Bank App Reviews Analysis  
**Date**: June 8, 2024  
**Author**: Eyoab Amare  

## Project Overview  
This project analyzes customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:  
- Commercial Bank of Ethiopia (CBE)  
- Bank of Abyssinia (BOA)  
- Dashen Bank  

## Task 1: Data Collection and Preprocessing  

### 1. Implementation Summary  

**Data Collection:**  
- Collected 400+ reviews per bank using the google-play-scraper library  
- Implemented continuation tokens for pagination  
- Added 1-second delay between requests to avoid rate limiting  
- Handled empty responses and exceptions gracefully  

**Preprocessing Pipeline:**  
- Removed 32 duplicate reviews  
- Filled 27 empty reviews with "No review text" placeholder  
- Standardized all dates to YYYY-MM-DD format  
- Validated required columns: ["review", "rating", "date", "bank", "source"]  

### 2. Key Metrics  

| Metric                | Value          |
|-----------------------|----------------|
| Total reviews collected | 1200+         |
| Duplicates removed    | 32             |
| Empty reviews handled | 27             |
| Missing data rate     | 2.3%           |

### 3. Outputs  
- **Raw data**: `data/raw/reviews_raw.csv`  
- **Processed data**: `data/processed/reviews_cleaned.csv`  
- Folder structure:  

- data/
  - raw/
  - processed/

  
### 4. Challenges & Solutions  

| Challenge               | Solution                          |
|-------------------------|-----------------------------------|
| Google Play rate limiting | Implemented 1s delay between requests |
| Mixed date formats      | Standardized using pd.to_datetime |
| Empty reviews           | Filled with placeholder text      |

## Next Steps  
1. Implement HuggingFace transformer for advanced sentiment analysis  
2. Develop thematic clustering (3-5 themes per bank)  
3. Create visualization dashboard for insights  

**Tools Used**: Python 3.13, Pandas, google-play-scraper, Git/GitHub  