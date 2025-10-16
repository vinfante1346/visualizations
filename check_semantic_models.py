#!/usr/bin/env python3.11
"""Check for semantic models in the stage"""

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
        database='SNOWFLAKE_INTELLIGENCE',
        schema='AGENTS'
    )

    cursor = conn.cursor()

    print("Checking STAGE_SEMANTIC_MODELS")
    print("=" * 80)
    print()

    # List files in the stage
    cursor.execute("LIST @STAGE_SEMANTIC_MODELS")
    files = cursor.fetchall()

    if files:
        print(f"Found {len(files)} file(s) in stage:")
        for file in files:
            print(f"  - {file[0]}")
    else:
        print("No files found in STAGE_SEMANTIC_MODELS")

    print()
    print("-" * 80)
    print()

    # Check for any Cortex Analyst related objects
    print("Looking for Cortex Analyst services...")
    try:
        # Try different commands to find analyst services
        commands = [
            "SHOW FUNCTIONS LIKE '%ANALYST%'",
            "SHOW PROCEDURES LIKE '%ANALYST%'",
            "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%ANALYST%'",
        ]

        for cmd in commands:
            try:
                cursor.execute(cmd)
                results = cursor.fetchall()
                if results:
                    print(f"\n{cmd}:")
                    for row in results[:5]:  # Show first 5
                        print(f"  {row}")
            except Exception as e:
                pass

    except Exception as e:
        print(f"  Error: {e}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
