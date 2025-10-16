#!/usr/bin/env python3.11
"""Find MoneyGram transaction data"""

from snowflake.connector import connect

# Read private key in DER format
with open('/Users/vinfa/snowflake-mcp/keys/snowflake_private_key.p8', 'rb') as key_file:
    private_key = key_file.read()

try:
    conn = connect(
        account='GIJUXYU-ZV35737',
        user='VINFANTE',
        private_key=private_key,
        role='ACCOUNTADMIN',
        warehouse='COMPUTE_WH'
    )

    cursor = conn.cursor()

    print("SEARCHING FOR MONEYGRAM TRANSACTION DATA")
    print("=" * 80)
    print()

    # Set a database context first
    cursor.execute("USE DATABASE MYBAMBU_PROD")

    # Search for relevant tables across all databases
    cursor.execute("""
        SELECT
            table_catalog,
            table_schema,
            table_name,
            row_count
        FROM INFORMATION_SCHEMA.TABLES
        WHERE (
            LOWER(table_name) LIKE '%transaction%'
            OR LOWER(table_name) LIKE '%moneygram%'
            OR LOWER(table_name) LIKE '%payment%'
            OR LOWER(table_name) LIKE '%money%gram%'
        )
        AND table_type = 'BASE TABLE'
        ORDER BY row_count DESC NULLS LAST
        LIMIT 20
    """)
    tables = cursor.fetchall()

    if tables:
        print(f"Found {len(tables)} potentially relevant table(s):")
        print()
        for table in tables:
            db, schema, name, rows = table
            row_str = f"{rows:,}" if rows else "Unknown"
            print(f"  {db}.{schema}.{name}")
            print(f"    Rows: {row_str}")
            print()
    else:
        print("No tables found with 'transaction', 'moneygram', or 'payment' in the name")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
