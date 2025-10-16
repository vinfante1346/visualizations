#!/usr/bin/env python3.11
"""Find tables related to Reg E and losses"""

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

    print("SEARCHING FOR REG E AND LOSS TABLES")
    print("=" * 100)
    print()

    # Set database context
    cursor.execute("USE DATABASE MYBAMBU_PROD")

    # Search for relevant tables
    cursor.execute("""
        SELECT
            table_catalog,
            table_schema,
            table_name,
            row_count
        FROM INFORMATION_SCHEMA.TABLES
        WHERE (
            LOWER(table_name) LIKE '%reg%e%'
            OR LOWER(table_name) LIKE '%dispute%'
            OR LOWER(table_name) LIKE '%chargeback%'
            OR LOWER(table_name) LIKE '%loss%'
            OR LOWER(table_name) LIKE '%fraud%'
            OR LOWER(table_name) LIKE '%claim%'
            OR LOWER(table_name) LIKE '%recovery%'
            OR LOWER(table_name) LIKE '%liability%'
            OR LOWER(table_name) LIKE '%charge%off%'
            OR LOWER(table_name) LIKE '%write%off%'
        )
        AND table_type = 'BASE TABLE'
        ORDER BY row_count DESC NULLS LAST
        LIMIT 30
    """)
    tables = cursor.fetchall()

    if tables:
        print(f"Found {len(tables)} potentially relevant table(s):")
        print()
        print(f"{'Database':<20} {'Schema':<30} {'Table Name':<50} {'Rows':>15}")
        print("-" * 115)
        for table in tables:
            db, schema, name, rows = table
            row_str = f"{rows:,}" if rows else "Unknown"
            print(f"{db:<20} {schema:<30} {name:<50} {row_str:>15}")
        print()
    else:
        print("No tables found. Let me search more broadly...")
        cursor.execute("""
            SELECT table_schema, table_name
            FROM INFORMATION_SCHEMA.TABLES
            WHERE table_catalog = 'MYBAMBU_PROD'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
            LIMIT 100
        """)
        all_tables = cursor.fetchall()
        print("Sample of available tables:")
        for schema, name in all_tables[:50]:
            print(f"  {schema}.{name}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
