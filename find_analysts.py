#!/usr/bin/env python3.11
"""Find all Cortex Analyst semantic models and services"""

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

    print("=" * 80)
    print("SEARCHING FOR CORTEX ANALYST RESOURCES")
    print("=" * 80)
    print()

    # Search all databases for potential analyst resources
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

    for db in databases:
        db_name = db[1]
        print(f"Checking database: {db_name}")

        try:
            cursor.execute(f"USE DATABASE {db_name}")
            cursor.execute(f"SHOW SCHEMAS IN DATABASE {db_name}")
            schemas = cursor.fetchall()

            for schema in schemas:
                schema_name = schema[1]
                if schema_name in ['INFORMATION_SCHEMA']:
                    continue

                try:
                    # Look for views (semantic models are often views)
                    cursor.execute(f"SHOW VIEWS IN SCHEMA {db_name}.{schema_name}")
                    views = cursor.fetchall()

                    for view in views:
                        view_name = view[1]
                        if 'ANALYST' in view_name.upper() or 'SEMANTIC' in view_name.upper():
                            print(f"  ✓ Found view: {db_name}.{schema_name}.{view_name}")

                    # Look for tables that might be semantic models
                    cursor.execute(f"SHOW TABLES IN SCHEMA {db_name}.{schema_name}")
                    tables = cursor.fetchall()

                    for table in tables:
                        table_name = table[1]
                        if 'ANALYST' in table_name.upper() or 'SEMANTIC' in table_name.upper() or 'ACTIVITY' in table_name.upper():
                            print(f"  ✓ Found table: {db_name}.{schema_name}.{table_name}")

                except Exception as e:
                    pass  # Skip schemas we can't access

        except Exception as e:
            pass  # Skip databases we can't access

    print()
    print("=" * 80)
    print("CHECKING FOR CORTEX SERVICES")
    print("=" * 80)
    print()

    # Try to find Cortex services in SNOWFLAKE_INTELLIGENCE
    try:
        cursor.execute("USE DATABASE SNOWFLAKE_INTELLIGENCE")
        cursor.execute("SHOW SCHEMAS")
        schemas = cursor.fetchall()

        print("Schemas in SNOWFLAKE_INTELLIGENCE:")
        for schema in schemas:
            print(f"  - {schema[1]}")
        print()

        # Check each schema for objects
        for schema in schemas:
            schema_name = schema[1]
            if schema_name == 'INFORMATION_SCHEMA':
                continue

            print(f"Objects in SNOWFLAKE_INTELLIGENCE.{schema_name}:")
            try:
                cursor.execute(f"USE SCHEMA SNOWFLAKE_INTELLIGENCE.{schema_name}")

                # Show all objects
                cursor.execute(f"SHOW OBJECTS IN SCHEMA SNOWFLAKE_INTELLIGENCE.{schema_name}")
                objects = cursor.fetchall()

                if objects:
                    for obj in objects:
                        obj_name = obj[1]
                        obj_type = obj[2]
                        print(f"  - {obj_name} ({obj_type})")
                else:
                    print("  (empty)")

            except Exception as e:
                print(f"  Error: {e}")
            print()

    except Exception as e:
        print(f"Error checking SNOWFLAKE_INTELLIGENCE: {e}")

    cursor.close()
    conn.close()

    print()
    print("✓ Search complete!")

except Exception as e:
    print(f"✗ Error: {e}")
