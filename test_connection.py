#!/usr/bin/env python3.11
"""Test Snowflake connection with private key authentication"""

import os
import sys
from snowflake.connector import connect

# Load environment variables
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT', 'GIJUXYU-ZV35737')
SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER', 'VINFANTE')
SNOWFLAKE_ROLE = os.environ.get('SNOWFLAKE_ROLE', 'ACCOUNTADMIN')
SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE', 'SNOWFLAKE_INTELLIGENCE')
SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA', 'AGENTS')

# Read private key in DER format
with open('/Users/vinfa/snowflake-mcp/keys/snowflake_private_key.p8', 'rb') as key_file:
    private_key = key_file.read()

try:
    print(f"Connecting to Snowflake...")
    print(f"  Account: {SNOWFLAKE_ACCOUNT}")
    print(f"  User: {SNOWFLAKE_USER}")
    print(f"  Role: {SNOWFLAKE_ROLE}")
    print(f"  Warehouse: {SNOWFLAKE_WAREHOUSE}")
    print(f"  Database: {SNOWFLAKE_DATABASE}")
    print(f"  Schema: {SNOWFLAKE_SCHEMA}")
    print()

    conn = connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        private_key=private_key,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

    print("✓ Connection successful!")
    print()

    # Test basic query
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
    result = cursor.fetchone()

    print("Current Context:")
    print(f"  User: {result[0]}")
    print(f"  Role: {result[1]}")
    print(f"  Warehouse: {result[2]}")
    print(f"  Database: {result[3]}")
    print(f"  Schema: {result[4]}")
    print()

    # Check available roles
    print("Checking available roles...")
    try:
        cursor.execute("SHOW GRANTS TO USER VINFANTE")
        grants = cursor.fetchall()
        roles = [g[1] for g in grants if g[0] == 'ROLE']
        print(f"  Available roles: {', '.join(roles) if roles else 'None'}")
    except Exception as e:
        print(f"  Error: {e}")
    print()

    # Check databases you have access to
    print("Checking databases...")
    try:
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"  Found {len(databases)} database(s):")
        for db in databases[:10]:
            print(f"    - {db[1]}")
    except Exception as e:
        print(f"  Error: {e}")
    print()

    # Check if SNOWFLAKE_INTELLIGENCE database exists
    print("Checking SNOWFLAKE_INTELLIGENCE database...")
    try:
        cursor.execute("USE DATABASE SNOWFLAKE_INTELLIGENCE")
        cursor.execute("SHOW SCHEMAS IN DATABASE SNOWFLAKE_INTELLIGENCE")
        schemas = cursor.fetchall()
        print(f"  Found {len(schemas)} schema(s) in SNOWFLAKE_INTELLIGENCE:")
        for schema in schemas:
            print(f"    - {schema[1]}")
    except Exception as e:
        print(f"  Error: {e}")
    print()

    # Check AGENTS schema
    print("Checking AGENTS schema contents...")
    try:
        cursor.execute("USE SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS")

        # Check tables
        cursor.execute("SHOW TABLES IN SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS")
        tables = cursor.fetchall()
        if tables:
            print(f"  Tables ({len(tables)}):")
            for table in tables:
                print(f"    - {table[1]}")

        # Check views
        cursor.execute("SHOW VIEWS IN SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS")
        views = cursor.fetchall()
        if views:
            print(f"  Views ({len(views)}):")
            for view in views:
                print(f"    - {view[1]}")

        # Try to query monthly_activity_analyst if it exists
        cursor.execute("SELECT * FROM MONTHLY_ACTIVITY_ANALYST LIMIT 1")
        result = cursor.fetchone()
        if result:
            print(f"  ✓ MONTHLY_ACTIVITY_ANALYST is accessible!")
            print(f"    Columns: {[col[0] for col in cursor.description]}")

    except Exception as e:
        print(f"  Note: {e}")

    cursor.close()
    conn.close()

    print()
    print("✓ All tests passed!")
    sys.exit(0)

except Exception as e:
    print(f"✗ Connection failed: {e}")
    sys.exit(1)
