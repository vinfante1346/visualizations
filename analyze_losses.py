#!/usr/bin/env python3.11
"""Analyze Reg E and total losses by month"""

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

    print("=" * 120)
    print("REG E AND LOSS ANALYSIS")
    print("=" * 120)
    print()

    # First, explore the Reg E table structure
    print("Exploring MART_SRDF_CHARGEBACK_DISPUTES_REGE table structure...")
    cursor.execute("""
        SELECT column_name, data_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'BAMBU_MART_GALILEO'
        AND table_name = 'MART_SRDF_CHARGEBACK_DISPUTES_REGE'
        AND (
            LOWER(column_name) LIKE '%amount%'
            OR LOWER(column_name) LIKE '%date%'
            OR LOWER(column_name) LIKE '%status%'
            OR LOWER(column_name) LIKE '%type%'
            OR LOWER(column_name) LIKE '%loss%'
            OR LOWER(column_name) LIKE '%dispute%'
            OR LOWER(column_name) LIKE '%reason%'
        )
        ORDER BY ordinal_position
    """)
    columns = cursor.fetchall()

    print("Key columns:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    print()

    # Sample data
    print("Sample Reg E records:")
    cursor.execute("""
        SELECT *
        FROM MART_SRDF_CHARGEBACK_DISPUTES_REGE
        LIMIT 3
    """)
    sample = cursor.fetchall()
    col_names = [col[0] for col in cursor.description]
    print(f"Columns: {col_names[:15]}...")
    for row in sample[:2]:
        print(f"Sample: {row[:10]}...")
    print()

    # Now let's get monthly Reg E losses
    print("=" * 120)
    print("REG E MONTHLY LOSS ANALYSIS")
    print("=" * 120)
    print()

    cursor.execute("""
        SELECT
            DATE_TRUNC('MONTH', DATE_LOGGED) as month,
            COUNT(*) as total_disputes,
            COUNT(DISTINCT ACCOUNT_ID) as unique_customers,
            SUM(ABS(DISPUTE_AMOUNT)) as total_dispute_amount,
            AVG(ABS(DISPUTE_AMOUNT)) as avg_dispute_amount,
            SUM(ABS(FINAL_RESOLUTION_AMOUNT)) as total_resolution_amount,
            SUM(CASE WHEN ENDING_STATUS LIKE '%Loss%' OR ENDING_STATUS LIKE '%Denied%'
                OR DISPUTE_STATUS LIKE '%Loss%' OR DISPUTE_STATUS LIKE '%Denied%'
                THEN ABS(COALESCE(FINAL_RESOLUTION_AMOUNT, DISPUTE_AMOUNT)) ELSE 0 END) as estimated_loss_amount,
            COUNT(CASE WHEN ENDING_STATUS LIKE '%Loss%' OR ENDING_STATUS LIKE '%Denied%'
                OR DISPUTE_STATUS LIKE '%Loss%' OR DISPUTE_STATUS LIKE '%Denied%' THEN 1 END) as loss_count
        FROM MART_SRDF_CHARGEBACK_DISPUTES_REGE
        WHERE DATE_LOGGED >= DATEADD('MONTH', -12, CURRENT_DATE())
        GROUP BY DATE_TRUNC('MONTH', DATE_LOGGED)
        ORDER BY month DESC
    """)

    monthly_rege = cursor.fetchall()

    if monthly_rege:
        print(f"{'Month':<15} {'Disputes':>10} {'Customers':>10} {'Disputed $':>18} {'Resolved $':>18} {'Losses':>18} {'Loss Count':>12}")
        print("-" * 120)

        total_disputes = 0
        total_amount = 0
        total_resolved = 0
        total_losses = 0

        for row in monthly_rege:
            month, disputes, customers, amount, avg_amt, resolved, loss_amt, loss_cnt = row
            total_disputes += disputes
            total_amount += amount if amount else 0
            total_resolved += resolved if resolved else 0
            total_losses += loss_amt if loss_amt else 0

            month_str = str(month)[:7]
            print(f"{month_str:<15} {disputes:>10,} {customers:>10,} ${amount:>17,.2f} ${resolved:>17,.2f} ${loss_amt:>17,.2f} {loss_cnt:>12,}")

        print("-" * 120)
        print(f"{'TOTAL':<15} {total_disputes:>10,} {'':<10} ${total_amount:>17,.2f} ${total_resolved:>17,.2f} ${total_losses:>17,.2f}")
        print()
        print(f"Average Monthly Loss: ${total_losses / len(monthly_rege):,.2f}")
        print()

    # Check chargeback table as well
    print("=" * 120)
    print("CHARGEBACK AND DISPUTE ANALYSIS (CDF)")
    print("=" * 120)
    print()

    cursor.execute("""
        SELECT column_name, data_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'BAMBU_MART_GALILEO'
        AND table_name = 'MART_CDF_CHARGEBACK_AND_DISPUTE'
        AND (
            LOWER(column_name) LIKE '%amount%'
            OR LOWER(column_name) LIKE '%date%'
            OR LOWER(column_name) LIKE '%status%'
            OR LOWER(column_name) LIKE '%loss%'
        )
        ORDER BY ordinal_position
    """)
    cb_columns = cursor.fetchall()

    print("Chargeback table key columns:")
    for col in cb_columns:
        print(f"  - {col[0]} ({col[1]})")
    print()

    # Monthly chargeback analysis
    cursor.execute("""
        SELECT
            DATE_TRUNC('MONTH', DISPUTE_DATE) as month,
            COUNT(*) as total_chargebacks,
            COUNT(DISTINCT PRN) as unique_customers,
            SUM(ABS(BILLING_AMOUNT)) as total_amount,
            AVG(ABS(BILLING_AMOUNT)) as avg_amount
        FROM MART_CDF_CHARGEBACK_AND_DISPUTE
        WHERE DISPUTE_DATE >= DATEADD('MONTH', -6, CURRENT_DATE())
        GROUP BY DATE_TRUNC('MONTH', DISPUTE_DATE)
        ORDER BY month DESC
    """)

    monthly_cb = cursor.fetchall()

    if monthly_cb:
        print(f"{'Month':<15} {'Chargebacks':>12} {'Customers':>10} {'Total Amount':>18} {'Avg Amount':>15}")
        print("-" * 120)

        total_cb = 0
        total_cb_amount = 0

        for row in monthly_cb:
            month, cb_count, customers, amount, avg_amt = row
            total_cb += cb_count
            total_cb_amount += amount if amount else 0

            month_str = str(month)[:7]
            print(f"{month_str:<15} {cb_count:>12,} {customers:>10,} ${amount:>17,.2f} ${avg_amt:>14,.2f}")

        print("-" * 120)
        print(f"{'TOTAL':<15} {total_cb:>12,} {'':>10} ${total_cb_amount:>17,.2f}")
        print()

    # Check fraud losses
    print("=" * 120)
    print("FRAUD ANALYSIS")
    print("=" * 120)
    print()

    cursor.execute("""
        SELECT column_name, data_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'BAMBU_MART_VENDOR_REPORT'
        AND table_name = 'MART_SPLUNK_FRAUD_REPORT'
        ORDER BY ordinal_position
        LIMIT 30
    """)
    fraud_columns = cursor.fetchall()

    print("Fraud report columns (first 30):")
    for col in fraud_columns:
        print(f"  - {col[0]} ({col[1]})")
    print()

    # Summary
    print("=" * 120)
    print("SUMMARY OF MONTHLY LOSSES")
    print("=" * 120)
    print()

    if monthly_rege:
        latest_month = monthly_rege[0]
        month_str = str(latest_month[0])[:7]
        print(f"Latest Month: {month_str}")
        print(f"  Reg E Disputes: {latest_month[1]:,} disputes totaling ${latest_month[3]:,.2f}")
        print(f"  Estimated Reg E Losses: ${latest_month[6]:,.2f} ({latest_month[7]:,} cases)")
        print()

    if monthly_cb:
        latest_cb = monthly_cb[0]
        cb_month_str = str(latest_cb[0])[:7]
        print(f"  Chargebacks: {latest_cb[1]:,} chargebacks totaling ${latest_cb[3]:,.2f}")
        print()

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
