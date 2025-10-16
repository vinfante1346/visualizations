#!/usr/bin/env python3.11
"""Query for MoneyGram transaction customers"""

from snowflake.connector import connect
from datetime import datetime, timedelta

# Read private key in DER format
with open('/Users/vinfa/snowflake-mcp/keys/snowflake_private_key.p8', 'rb') as key_file:
    private_key = key_file.read()

try:
    conn = connect(
        account='GIJUXYU-ZV35737',
        user='VINFANTE',
        private_key=private_key,
        role='ACCOUNTADMIN',
        warehouse='COMPUTE_WH',
        database='SNOWFLAKE_INTELLIGENCE',
        schema='AGENTS'
    )

    cursor = conn.cursor()

    print("MONEYGRAM TRANSACTION ANALYSIS")
    print("=" * 80)
    print()

    # First, let's see what's in the monthly activity table
    print("Checking available data in MONTHLY_ACTIVITY_COHORT_SUMMARY...")
    cursor.execute("SELECT * FROM MONTHLY_ACTIVITY_COHORT_SUMMARY LIMIT 5")
    sample_data = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    print(f"Columns: {', '.join(columns)}")
    print()

    if sample_data:
        print("Sample data:")
        for row in sample_data:
            print(f"  {row}")
    print()

    # Try to find MoneyGram related data
    print("Searching for MoneyGram transaction data...")

    # Check if we have transaction type or product information
    cursor.execute("""
        SELECT COUNT(DISTINCT column_name) as col_count
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'AGENTS'
        AND table_name = 'MONTHLY_ACTIVITY_COHORT_SUMMARY'
    """)
    col_count = cursor.fetchone()[0]
    print(f"Table has {col_count} columns")
    print()

    # List all columns
    cursor.execute("""
        SELECT column_name, data_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'AGENTS'
        AND table_name = 'MONTHLY_ACTIVITY_COHORT_SUMMARY'
        ORDER BY ordinal_position
    """)
    all_columns = cursor.fetchall()
    print("All columns:")
    for col in all_columns:
        print(f"  - {col[0]} ({col[1]})")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
