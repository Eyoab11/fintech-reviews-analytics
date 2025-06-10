# Database Setup Instructions

This directory contains the database setup and operations for the bank reviews application.

## Prerequisites

1. Oracle Database XE (Express Edition) installed
2. Python 3.9 or higher
3. Oracle Instant Client installed and configured

## Oracle Instant Client Setup

1. Download Oracle Instant Client:
   - Go to [Oracle Instant Client Downloads](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
   - Download "Basic Package" (ZIP) for Windows x64
   - Create an Oracle account if you don't have one

2. Install Oracle Instant Client:
   - Extract downloaded ZIP to `D:\instantclient_19_20\instantclient_23_8`
   - You should see files like `oci.dll`, `oraociei19.dll`, etc.

3. Configure System PATH:
   - Open Windows System Properties (Win + Pause/Break)
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit"
   - Click "New"
   - Add: `D:\instantclient_19_20\instantclient_23_8`
   - Click "OK" on all windows

4. Set Oracle Client Path:
   - Create or edit `.env` file in project root
   - Add: `ORACLE_CLIENT_PATH=D:\instantclient_19_20\instantclient_23_8`

## Database Setup

1. Install Oracle Database XE:
   - Download from [Oracle's website](https://www.oracle.com/database/technologies/xe-downloads.html)
   - Follow the installation instructions for your operating system

2. Install Python dependencies:
   ```bash
   pip install -r requirements-db.txt
   ```

3. Set up environment variables in `.env`:
   ```
   ORACLE_USER=your_username
   ORACLE_PASSWORD=your_password
   ORACLE_DSN=localhost:1521/XEPDB1
   ORACLE_CLIENT_PATH=D:\instantclient_19_20\instantclient_23_8
   ```

## Database Structure

The database consists of two main tables:

1. `banks` - Stores information about the banks
   - bank_id (PRIMARY KEY)
   - bank_name
   - created_at
   - updated_at

2. `reviews` - Stores the review data
   - review_id (PRIMARY KEY)
   - bank_id (FOREIGN KEY)
   - review_text
   - rating
   - review_date
   - source
   - sentiment_label
   - sentiment_score
   - vader_score
   - textblob_score
   - themes
   - keywords
   - created_at
   - updated_at

## Usage

To create tables and populate the database:

```bash
python -m scripts.database.db_operations
```

## Troubleshooting

1. If you get "Cannot locate Oracle Client library" error:
   - Verify Oracle Instant Client is installed correctly at `D:\instantclient_19_20\instantclient_23_8`
   - Check if the PATH environment variable includes the Instant Client directory
   - Verify the ORACLE_CLIENT_PATH in .env points to the correct directory

2. If you get connection errors:
   - Verify Oracle XE is running
   - Check if the credentials in .env are correct
   - Verify the DSN format is correct

## Notes

- Make sure Oracle XE is running before executing the script
- The script will create tables if they don't exist
- Data is loaded from the processed CSV files in the data directory
- All database operations are logged for debugging purposes 