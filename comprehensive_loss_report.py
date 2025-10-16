#!/usr/bin/env python3.11
"""Comprehensive Loss Report - Reg E, Chargebacks, and Fraud"""

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

    print("=" * 140)
    print("COMPREHENSIVE MONTHLY LOSS REPORT")
    print("=" * 140)
    print()

    # First, understand the status values
    print("Analyzing dispute statuses to identify losses...")
    cursor.execute("""
        SELECT
            ENDING_STATUS,
            COUNT(*) as count,
            SUM(ABS(COALESCE(FINAL_RESOLUTION_AMOUNT, DISPUTE_AMOUNT))) as total_amount
        FROM MART_SRDF_CHARGEBACK_DISPUTES_REGE
        WHERE DATE_LOGGED >= DATEADD('MONTH', -6, CURRENT_DATE())
        GROUP BY ENDING_STATUS
        ORDER BY total_amount DESC
    """)

    statuses = cursor.fetchall()
    print(f"\n{'Ending Status':<40} {'Count':>10} {'Total Amount':>20}")
    print("-" * 75)
    for status, count, amount in statuses:
        print(f"{str(status):<40} {count:>10,} ${amount:>19,.2f}")
    print()

    # REG E MONTHLY ANALYSIS WITH ALL RESOLUTION AMOUNTS
    print("=" * 140)
    print("REG E DISPUTES - MONTHLY BREAKDOWN")
    print("=" * 140)
    print()

    cursor.execute("""
        SELECT
            DATE_TRUNC('MONTH', DATE_LOGGED) as month,
            COUNT(*) as total_disputes,
            COUNT(DISTINCT ACCOUNT_ID) as unique_customers,

            -- Total disputed amounts
            SUM(ABS(DISPUTE_AMOUNT)) as total_disputed,

            -- Total resolved (what we actually paid/credited)
            SUM(ABS(FINAL_RESOLUTION_AMOUNT)) as total_resolved,

            -- Provisional credits given
            SUM(ABS(PROVISIONAL_CREDIT_AMOUNT)) as total_prov_credit,

            -- Provisional credits reversed (recovered)
            SUM(ABS(PROV_CREDIT_REVERSAL_AMOUNT)) as total_prov_reversed,

            -- Net loss calculation: what we gave - what we got back
            SUM(ABS(COALESCE(FINAL_RESOLUTION_AMOUNT, 0))) - SUM(ABS(COALESCE(PROV_CREDIT_REVERSAL_AMOUNT, 0))) as net_loss,

            -- Average amounts
            AVG(ABS(DISPUTE_AMOUNT)) as avg_dispute

        FROM MART_SRDF_CHARGEBACK_DISPUTES_REGE
        WHERE DATE_LOGGED >= DATEADD('MONTH', -12, CURRENT_DATE())
        GROUP BY DATE_TRUNC('MONTH', DATE_LOGGED)
        ORDER BY month DESC
    """)

    monthly_data = cursor.fetchall()

    print(f"{'Month':<12} {'Disputes':>10} {'Customers':>10} {'Disputed':>15} {'Resolved':>15} {'Prov Credit':>15} {'Recovered':>15} {'Net Loss':>15}")
    print("-" * 140)

    total_disputes = 0
    total_disputed = 0
    total_resolved = 0
    total_net_loss = 0

    for row in monthly_data:
        month, disputes, customers, disputed, resolved, prov_credit, prov_reversed, net_loss, avg_dispute = row

        total_disputes += disputes
        total_disputed += disputed or 0
        total_resolved += resolved or 0
        total_net_loss += net_loss or 0

        month_str = str(month)[:7]
        print(f"{month_str:<12} {disputes:>10,} {customers:>10,} ${disputed:>14,.0f} ${resolved:>14,.0f} ${prov_credit:>14,.0f} ${prov_reversed:>14,.0f} ${net_loss:>14,.0f}")

    print("-" * 140)
    print(f"{'TOTAL':<12} {total_disputes:>10,} {'':>10} ${total_disputed:>14,.0f} ${total_resolved:>14,.0f} {'':>15} {'':>15} ${total_net_loss:>14,.0f}")
    print()
    avg_monthly_loss = total_net_loss / len(monthly_data) if monthly_data else 0
    print(f"Average Monthly Net Loss (Reg E): ${avg_monthly_loss:,.2f}")
    print()

    # CHARGEBACK ANALYSIS
    print("=" * 140)
    print("CHARGEBACKS - MONTHLY BREAKDOWN")
    print("=" * 140)
    print()

    cursor.execute("""
        SELECT
            DATE_TRUNC('MONTH', DATE_LOGGED) as month,
            COUNT(*) as total_chargebacks,
            COUNT(DISTINCT PRN) as unique_customers,
            SUM(ABS(DISPUTE_AMOUNT)) as total_amount,
            AVG(ABS(DISPUTE_AMOUNT)) as avg_amount,
            SUM(ABS(PC_AMOUNT)) as prov_credit_amount
        FROM MART_CDF_CHARGEBACK_AND_DISPUTE
        WHERE DATE_LOGGED >= DATEADD('MONTH', -12, CURRENT_DATE())
        GROUP BY DATE_TRUNC('MONTH', DATE_LOGGED)
        ORDER BY month DESC
    """)

    cb_data = cursor.fetchall()

    print(f"{'Month':<12} {'Chargebacks':>12} {'Customers':>10} {'Total Amount':>18} {'Prov Credit':>18} {'Avg Amount':>15}")
    print("-" * 140)

    total_cb = 0
    total_cb_amount = 0
    total_cb_prov = 0

    for row in cb_data:
        month, cb_count, customers, amount, avg_amt, prov_amt = row

        total_cb += cb_count
        total_cb_amount += amount or 0
        total_cb_prov += prov_amt or 0

        month_str = str(month)[:7]
        print(f"{month_str:<12} {cb_count:>12,} {customers:>10,} ${amount:>17,.2f} ${prov_amt:>17,.2f} ${avg_amt:>14,.2f}")

    print("-" * 140)
    print(f"{'TOTAL':<12} {total_cb:>12,} {'':>10} ${total_cb_amount:>17,.2f} ${total_cb_prov:>17,.2f}")
    print()
    avg_monthly_cb = total_cb_amount / len(cb_data) if cb_data else 0
    print(f"Average Monthly Chargeback Amount: ${avg_monthly_cb:,.2f}")
    print()

    # SUMMARY
    print("=" * 140)
    print("EXECUTIVE SUMMARY - LATEST MONTH")
    print("=" * 140)
    print()

    if monthly_data:
        latest = monthly_data[0]
        month_str = str(latest[0])[:7]

        print(f"Period: {month_str}")
        print()
        print("REG E DISPUTES:")
        print(f"  Total Disputes:           {latest[1]:>10,}")
        print(f"  Unique Customers:         {latest[2]:>10,}")
        print(f"  Amount Disputed:          ${latest[3]:>14,.2f}")
        print(f"  Amount Resolved:          ${latest[4]:>14,.2f}")
        print(f"  Provisional Credit Given: ${latest[5]:>14,.2f}")
        print(f"  Amount Recovered:         ${latest[6]:>14,.2f}")
        print(f"  NET LOSS:                 ${latest[7]:>14,.2f}")
        print()

    if cb_data:
        latest_cb = cb_data[0]
        cb_month_str = str(latest_cb[0])[:7]

        print("CHARGEBACKS:")
        print(f"  Total Chargebacks:        {latest_cb[1]:>10,}")
        print(f"  Unique Customers:         {latest_cb[2]:>10,}")
        print(f"  Total Amount:             ${latest_cb[3]:>14,.2f}")
        print(f"  Provisional Credit:       ${latest_cb[5]:>14,.2f}")
        print()

    if monthly_data and cb_data:
        total_latest_loss = (latest[7] or 0) + (latest_cb[3] or 0)
        print(f"TOTAL ESTIMATED MONTHLY LOSS: ${total_latest_loss:,.2f}")
        print()

    # 12 month totals
    print("=" * 140)
    print("12-MONTH TOTALS")
    print("=" * 140)
    print()
    print(f"Reg E Net Losses (12 months):         ${total_net_loss:,.2f}")
    print(f"Chargeback Amounts (12 months):       ${total_cb_amount:,.2f}")
    print(f"Combined Total:                       ${total_net_loss + total_cb_amount:,.2f}")
    print()
    print(f"Average Monthly Combined Loss:        ${(total_net_loss + total_cb_amount) / 12:,.2f}")
    print()

    cursor.close()
    conn.close()

    print("=" * 140)
    print("END OF REPORT")
    print("=" * 140)

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
