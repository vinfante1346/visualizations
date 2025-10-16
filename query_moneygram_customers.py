#!/usr/bin/env python3.11
"""Query MoneyGram customers - this month vs last month"""

from snowflake.connector import connect
from datetime import datetime

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
        database='MYBAMBU_PROD',
        schema='BAMBU_MART_GALILEO'
    )

    cursor = conn.cursor()

    print("MONEYGRAM CUSTOMER ANALYSIS")
    print("=" * 80)
    print()

    # First, let's see the structure of the posted transactions table
    print("Checking table structure...")
    cursor.execute("""
        SELECT column_name, data_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'BAMBU_MART_GALILEO'
        AND table_name = 'MART_SRDF_POSTED_TRANSACTIONS'
        AND (
            LOWER(column_name) LIKE '%merchant%'
            OR LOWER(column_name) LIKE '%desc%'
            OR LOWER(column_name) LIKE '%name%'
            OR LOWER(column_name) LIKE '%type%'
            OR LOWER(column_name) LIKE '%date%'
            OR LOWER(column_name) LIKE '%prn%'
            OR LOWER(column_name) LIKE '%customer%'
            OR LOWER(column_name) LIKE '%user%'
        )
        ORDER BY ordinal_position
    """)
    columns = cursor.fetchall()

    print("Relevant columns:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    print()

    # Sample some data to see MoneyGram transactions
    print("Sampling MoneyGram transactions...")
    cursor.execute("""
        SELECT *
        FROM MART_SRDF_POSTED_TRANSACTIONS
        WHERE (
            LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
            OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
        )
        LIMIT 5
    """)
    sample = cursor.fetchall()

    if sample:
        print(f"Found MoneyGram transactions! Sample:")
        print(f"Columns: {[col[0] for col in cursor.description]}")
        for row in sample[:2]:
            print(f"  {row[:10]}...")  # Show first 10 fields
        print()

        # Now run the actual analysis
        print("Analyzing MoneyGram customers...")
        print()

        query = """
        WITH this_month AS (
            SELECT DISTINCT PRN
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
        ),
        last_month AS (
            SELECT DISTINCT PRN
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATEADD('MONTH', -1, DATE_TRUNC('MONTH', CURRENT_DATE()))
        )
        SELECT
            COUNT(DISTINCT this_month.PRN) AS new_moneygram_customers
        FROM this_month
        LEFT JOIN last_month ON this_month.PRN = last_month.PRN
        WHERE last_month.PRN IS NULL
        """

        cursor.execute(query)
        result = cursor.fetchone()

        print("RESULT:")
        print("=" * 80)
        print(f"Customers who did a MoneyGram transaction this month")
        print(f"but did NOT do one last month: {result[0]:,}")
        print()

    else:
        print("No MoneyGram transactions found. Let me check what merchant descriptions are available...")
        cursor.execute("""
            SELECT DISTINCT MERCHANT_DESCRIPTION
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE MERCHANT_DESCRIPTION IS NOT NULL
            LIMIT 50
        """)
        merchants = cursor.fetchall()
        print("Sample merchant descriptions:")
        for merchant in merchants[:20]:
            print(f"  - {merchant[0]}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
