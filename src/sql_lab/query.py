"""Query script for the `mock` table in the student's COMPUTING_ID_mock database."""

import os
import logging

import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector

# Configure logging so we get timestamped status messages in the terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Read DB connection info from environment variables (same pattern as process.py)
DB_HOST = os.environ["DBHOST"]
DB_NAME = os.environ["DBNAME"]
DB_USER = os.environ["DBUSER"]
DB_PASS = os.environ["DBPASS"]


def get_data_by_group(value):
    """Return all rows from the `mock` table where the `group` column equals `value`.

    The filter column is `group`, backtick-quoted in the SQL because GROUP is a
    reserved word in MySQL. Uses a parameterized query (%s placeholder) so the
    value is never inserted directly into the SQL string.

    Args:
        value (str): the group value to filter on (e.g. "A").

    Returns:
        list[tuple] | None: matching rows as tuples, or None on error.
    """
    logger.info(f"Connecting to database {DB_NAME} at {DB_HOST}")
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
        )
        cursor = conn.cursor()

        # `group` is backtick-quoted since GROUP is a reserved SQL keyword
        query = "SELECT * FROM `mock` WHERE `group` = %s;"
        logger.info(f"Running query: get rows where group = {value}")
        cursor.execute(query, (value,))  # parameterized -> safe from SQL injection
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} rows for group = {value}")
        return results

    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return None

    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")


def plot_counts(groupby):
    """Count rows per distinct value of `groupby` and show a bar chart.

    Builds a `SELECT ... GROUP BY` query against the `mock` table using the
    given column name. The column name itself is inserted via an f-string
    (not user input — it's a column identifier, not a data value) and is
    backtick-quoted to stay safe if it happens to be a reserved word.

    Args:
        groupby (str): name of the column to group and count by.

    Returns:
        pd.DataFrame | None: counts per distinct value, or None on error.
    """
    logger.info(f"Connecting to database {DB_NAME} at {DB_HOST}")
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
        )
        cursor = conn.cursor()

        # Column name is backtick-quoted; it comes from our own code, not user input
        query = f"SELECT `{groupby}`, COUNT(*) FROM `mock` GROUP BY `{groupby}`;"
        logger.info(f"Running query: count rows grouped by {groupby}")
        cursor.execute(query)
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=[groupby, "count"])
        logger.info(f"Got counts for {len(df)} distinct values of {groupby}")

        # Show a simple bar chart of the counts
        df.plot.bar(x=groupby, y="count", legend=False)
        plt.title(f"Row counts by {groupby}")
        plt.tight_layout()
        plt.show()

        return df

    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return None

    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")


def main():
    """Demonstrate get_data_by_group and plot_counts against the mock table."""
    print("=== rows where group = 'A' ===")
    print(get_data_by_group("2"))

    print("=== counts by group ===")
    counts_df = plot_counts("group")
    if counts_df is not None:
        print(counts_df)


if __name__ == "__main__":
    main()