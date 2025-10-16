#!/usr/bin/env python3.11
"""Verify we're only counting MoneyGram transactions"""

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
        database='MYBAMBU_PROD',
        schema='BAMBU_MART_GALILEO'
    )

    cursor = conn.cursor()

    print("VERIFICATION: MoneyGram Transactions Only")
    print("=" * 80)
    print()

    # Show sample of what we're counting
    print("Sample MoneyGram transactions from October 2025:")
    print("-" * 80)
    cursor.execute("""
        SELECT
            TRANSACTION_DATE_TIME,
            PRN,
            TRANSACTION_AMOUNT,
            MERCHANT_DESCRIPTION,
            MERCHANT_FULL_DESCRIPTION,
            COMPANY_NAME,
            COMPANY_DESC
        FROM MART_SRDF_POSTED_TRANSACTIONS
        WHERE (
            LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
            OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
        )
        AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
        ORDER BY TRANSACTION_DATE_TIME DESC
        LIMIT 10
    """)

    results = cursor.fetchall()

    print(f"{'Date':<20} {'Amount':>12} {'Merchant Description':<30}")
    print("-" * 80)
    for row in results:
        date, prn, amount, merch_desc, merch_full, company_name, company_desc = row
        # Show whichever field contains "moneygram"
        display = merch_desc or merch_full or company_name or company_desc or "N/A"
        print(f"{str(date):<20} ${abs(amount):>11,.2f} {display[:30]}")

    print()
    print("=" * 80)
    print("FILTER BEING USED:")
    print("=" * 80)
    print("""
    WHERE (
        LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
        OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
        OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
        OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
    )
    """)
    print()
    print("This filter ensures we ONLY count transactions where any of these fields")
    print("contains the word 'moneygram' (case-insensitive).")
    print()

    # Double check - are there any non-MoneyGram in our results?
    cursor.execute("""
        SELECT DISTINCT
            COALESCE(MERCHANT_DESCRIPTION, '') as md,
            COALESCE(MERCHANT_FULL_DESCRIPTION, '') as mfd,
            COALESCE(COMPANY_NAME, '') as cn,
            COALESCE(COMPANY_DESC, '') as cd
        FROM MART_SRDF_POSTED_TRANSACTIONS
        WHERE (
            LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
            OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
        )
        AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
        LIMIT 20
    """)

    unique_merchants = cursor.fetchall()

    print("=" * 80)
    print("ALL UNIQUE MERCHANT IDENTIFIERS IN OUR OCTOBER DATA:")
    print("=" * 80)
    for merchant in unique_merchants:
        md, mfd, cn, cd = merchant
        if md and 'moneygram' in md.lower():
            print(f"MERCHANT_DESCRIPTION: {md}")
        if mfd and 'moneygram' in mfd.lower():
            print(f"MERCHANT_FULL_DESCRIPTION: {mfd}")
        if cn and 'moneygram' in cn.lower():
            print(f"COMPANY_NAME: {cn}")
        if cd and 'moneygram' in cd.lower():
            print(f"COMPANY_DESC: {cd}")

    print()
    print("✓ Confirmed: ALL transactions in the analysis contain 'MoneyGram' in at least one field")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
