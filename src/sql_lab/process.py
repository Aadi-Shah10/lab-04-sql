import os
import logging
import pandas as pd
import mysql.connector

# Configure logging so we get timestamped status messages in the terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Read DB connection info from environment variables (set via `export` in your shell)
DB_HOST = os.environ["DBHOST"]
DB_NAME = os.environ["DBNAME"]
DB_USER = os.environ["DBUSER"]
DB_PASS = os.environ["DBPASS"]


def read_data(filename):
    """Load a CSV file into a pandas DataFrame.

    Args:
        filename (str): path to the CSV file to read.

    Returns:
        pd.DataFrame: the loaded data.
    """
    logger.info(f"Reading data from {filename}")
    df = pd.read_csv(filename)  # no quotes around the variable!
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def clean_data(data):
    """Clean the DataFrame before upload: drop rows with missing values.

    Args:
        data (pd.DataFrame): the raw DataFrame to clean.

    Returns:
        pd.DataFrame: cleaned DataFrame with no missing values.
    """
    logger.info(f"Cleaning data: {len(data)} rows before dropping missing values")
    clean = data.dropna()
    logger.info(f"Cleaning data: {len(clean)} rows after dropping missing values")
    return clean


def load_data(data, table):
    """Create a MySQL table (if needed) and upload a DataFrame into it row-by-row.

    Args:
        data (pd.DataFrame): the cleaned DataFrame to upload.
        table (str): destination table name (always "mock" for this lab).
    """
    logger.info(f"Connecting to database {DB_NAME} at {DB_HOST}")
    conn = None
    try:
        # Open the connection
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
        )
        cursor = conn.cursor()

        # --- Build and run CREATE TABLE ---
        # Table/column names can't be parameterized with %s, so we build that
        # part as plain text (safe here because these come from our own code,
        # not user input) but every VALUE still goes through %s below.
        columns_sql = ", ".join([f"`{col}` VARCHAR(255)" for col in data.columns if col != "id"])
        create_stmt = f"CREATE TABLE IF NOT EXISTS `{table}` (id INT PRIMARY KEY, {columns_sql})"
        logger.info("Creating table if it does not already exist")
        cursor.execute(create_stmt)
        conn.commit()

        # --- Insert rows one at a time ---
        # Build the placeholder INSERT statement once, outside the loop.
        col_names = ", ".join([f"`{col}`" for col in data.columns])
        placeholders = ", ".join(["%s"] * len(data.columns))
        insert_stmt = f"INSERT INTO `{table}` ({col_names}) VALUES ({placeholders})"

        logger.info(f"Inserting {len(data)} rows into `{table}`")
        for _, row in data.iterrows():
            values = tuple(row)  # values as a tuple, matched to %s placeholders in order
            cursor.execute(insert_stmt, values)  # parameterized -> safe from SQL injection

        conn.commit()  # commit all inserts
        logger.info(f"Successfully uploaded {len(data)} rows to `{table}`")

    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")


def main():
    """Run the full pipeline: read, clean, and upload the mock data."""
    df = read_data("MOCK_DATA.csv")
    clean_df = clean_data(df)
    load_data(clean_df, "mock")  # always pass "mock" as the table name


if __name__ == "__main__":
    main()