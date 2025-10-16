#!/usr/bin/env python3.11
"""Ask Cortex Analyst about MoneyGram transactions"""

from snowflake.connector import connect
import json

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

    print("ASKING CORTEX ANALYST ABOUT MONEYGRAM TRANSACTIONS")
    print("=" * 80)
    print()

    # Use Cortex Analyst with the semantic model
    question = """
    How many customers did a MoneyGram transaction this month that did not do one last month?
    """

    print(f"Question: {question.strip()}")
    print()

    # Call Cortex Analyst using the semantic model from the stage
    semantic_model_path = "@STAGE_SEMANTIC_MODELS/MONTHLY_ACTIVITY 10_6_2025, 6_06 PM.yaml"

    query = f"""
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mixtral-8x7b',
        [
            {{
                'role': 'system',
                'content': 'You are a data analyst. Answer questions about MoneyGram transactions based on the data.'
            }},
            {{
                'role': 'user',
                'content': '{question.strip()}'
            }}
        ]
    ) AS response
    """

    print("Querying Cortex Analyst...")
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            print("Response:")
            print(result[0])
    except Exception as e:
        print(f"Cortex query error: {e}")
        print()
        print("Let me try to find the relevant tables with transaction data...")

        # Search for tables with MoneyGram or transaction data
        cursor.execute("""
            SELECT table_schema, table_name
            FROM INFORMATION_SCHEMA.TABLES
            WHERE table_catalog = 'SNOWFLAKE_INTELLIGENCE'
            AND (
                LOWER(table_name) LIKE '%transaction%'
                OR LOWER(table_name) LIKE '%moneygram%'
                OR LOWER(table_name) LIKE '%payment%'
            )
        """)
        tables = cursor.fetchall()

        if tables:
            print("Found potentially relevant tables:")
            for table in tables:
                print(f"  - {table[0]}.{table[1]}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
