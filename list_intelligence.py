#!/usr/bin/env python3.11
"""List all objects in SNOWFLAKE_INTELLIGENCE database"""

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
        warehouse='COMPUTE_WH',
        database='SNOWFLAKE_INTELLIGENCE'
    )

    cursor = conn.cursor()

    print("SNOWFLAKE_INTELLIGENCE DATABASE")
    print("=" * 80)
    print()

    # List all schemas
    cursor.execute("SHOW SCHEMAS IN DATABASE SNOWFLAKE_INTELLIGENCE")
    schemas = cursor.fetchall()

    for schema in schemas:
        schema_name = schema[1]
        if schema_name == 'INFORMATION_SCHEMA':
            continue

        print(f"Schema: {schema_name}")
        print("-" * 80)

        try:
            cursor.execute(f"USE SCHEMA SNOWFLAKE_INTELLIGENCE.{schema_name}")

            # Tables
            cursor.execute(f"SHOW TABLES IN SCHEMA SNOWFLAKE_INTELLIGENCE.{schema_name}")
            tables = cursor.fetchall()
            if tables:
                print(f"  Tables ({len(tables)}):")
                for table in tables:
                    print(f"    - {table[1]}")

            # Views
            cursor.execute(f"SHOW VIEWS IN SCHEMA SNOWFLAKE_INTELLIGENCE.{schema_name}")
            views = cursor.fetchall()
            if views:
                print(f"  Views ({len(views)}):")
                for view in views:
                    print(f"    - {view[1]}")

            # File Formats
            cursor.execute(f"SHOW FILE FORMATS IN SCHEMA SNOWFLAKE_INTELLIGENCE.{schema_name}")
            formats = cursor.fetchall()
            if formats:
                print(f"  File Formats ({len(formats)}):")
                for fmt in formats:
                    print(f"    - {fmt[1]}")

            # Stages
            cursor.execute(f"SHOW STAGES IN SCHEMA SNOWFLAKE_INTELLIGENCE.{schema_name}")
            stages = cursor.fetchall()
            if stages:
                print(f"  Stages ({len(stages)}):")
                for stage in stages:
                    print(f"    - {stage[1]}")

        except Exception as e:
            print(f"  Error: {e}")

        print()

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
