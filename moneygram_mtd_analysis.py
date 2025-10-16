#!/usr/bin/env python3.11
"""Comprehensive MoneyGram MTD (Month-to-Date) Analysis"""

from snowflake.connector import connect
from datetime import datetime
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
        database='MYBAMBU_PROD',
        schema='BAMBU_MART_GALILEO'
    )

    cursor = conn.cursor()

    print("=" * 100)
    print("MONEYGRAM MONTH-TO-DATE (MTD) COMPREHENSIVE ANALYSIS")
    print("=" * 100)
    print()

    # Get current date context
    cursor.execute("SELECT CURRENT_DATE(), DATEADD('MONTH', -1, CURRENT_DATE())")
    dates = cursor.fetchone()
    current_date = dates[0]
    print(f"Report Date: {current_date}")
    print(f"Comparing: October 2025 MTD vs September 2025 MTD (same day of month)")
    print()

    # Main comprehensive analysis query
    query = """
    WITH current_month_mtd AS (
        SELECT
            COUNT(DISTINCT PRN) as unique_customers,
            COUNT(*) as total_transactions,
            SUM(ABS(TRANSACTION_AMOUNT)) as total_volume,
            AVG(ABS(TRANSACTION_AMOUNT)) as avg_transaction_amount,
            MIN(ABS(TRANSACTION_AMOUNT)) as min_transaction,
            MAX(ABS(TRANSACTION_AMOUNT)) as max_transaction,
            MEDIAN(ABS(TRANSACTION_AMOUNT)) as median_transaction,
            COUNT(DISTINCT DATE(TRANSACTION_DATE_TIME)) as active_days
        FROM MART_SRDF_POSTED_TRANSACTIONS
        WHERE (
            LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
            OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
        )
        AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
        AND DAY(TRANSACTION_DATE_TIME) <= DAY(CURRENT_DATE())
    ),
    prior_month_mtd AS (
        SELECT
            COUNT(DISTINCT PRN) as unique_customers,
            COUNT(*) as total_transactions,
            SUM(ABS(TRANSACTION_AMOUNT)) as total_volume,
            AVG(ABS(TRANSACTION_AMOUNT)) as avg_transaction_amount,
            MIN(ABS(TRANSACTION_AMOUNT)) as min_transaction,
            MAX(ABS(TRANSACTION_AMOUNT)) as max_transaction,
            MEDIAN(ABS(TRANSACTION_AMOUNT)) as median_transaction,
            COUNT(DISTINCT DATE(TRANSACTION_DATE_TIME)) as active_days
        FROM MART_SRDF_POSTED_TRANSACTIONS
        WHERE (
            LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
            OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
            OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
        )
        AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATEADD('MONTH', -1, DATE_TRUNC('MONTH', CURRENT_DATE()))
        AND DAY(TRANSACTION_DATE_TIME) <= DAY(CURRENT_DATE())
    ),
    new_customers AS (
        SELECT COUNT(DISTINCT curr.PRN) as new_customer_count
        FROM (
            SELECT DISTINCT PRN
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
            AND DAY(TRANSACTION_DATE_TIME) <= DAY(CURRENT_DATE())
        ) curr
        LEFT JOIN (
            SELECT DISTINCT PRN
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATEADD('MONTH', -1, DATE_TRUNC('MONTH', CURRENT_DATE()))
        ) prior ON curr.PRN = prior.PRN
        WHERE prior.PRN IS NULL
    ),
    churned_customers AS (
        SELECT COUNT(DISTINCT prior.PRN) as churned_customer_count
        FROM (
            SELECT DISTINCT PRN
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATEADD('MONTH', -1, DATE_TRUNC('MONTH', CURRENT_DATE()))
            AND DAY(TRANSACTION_DATE_TIME) <= DAY(CURRENT_DATE())
        ) prior
        LEFT JOIN (
            SELECT DISTINCT PRN
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
        ) curr ON prior.PRN = curr.PRN
        WHERE curr.PRN IS NULL
    )
    SELECT
        -- Current Month MTD
        cm.unique_customers as current_customers,
        cm.total_transactions as current_transactions,
        cm.total_volume as current_volume,
        cm.avg_transaction_amount as current_avg_amount,
        cm.min_transaction as current_min,
        cm.max_transaction as current_max,
        cm.median_transaction as current_median,
        cm.active_days as current_active_days,

        -- Prior Month MTD
        pm.unique_customers as prior_customers,
        pm.total_transactions as prior_transactions,
        pm.total_volume as prior_volume,
        pm.avg_transaction_amount as prior_avg_amount,
        pm.min_transaction as prior_min,
        pm.max_transaction as prior_max,
        pm.median_transaction as prior_median,
        pm.active_days as prior_active_days,

        -- Customer Movement
        nc.new_customer_count,
        cc.churned_customer_count,

        -- Growth Metrics
        ((cm.unique_customers - pm.unique_customers) / NULLIF(pm.unique_customers, 0) * 100) as customer_growth_pct,
        ((cm.total_transactions - pm.total_transactions) / NULLIF(pm.total_transactions, 0) * 100) as transaction_growth_pct,
        ((cm.total_volume - pm.total_volume) / NULLIF(pm.total_volume, 0) * 100) as volume_growth_pct,
        ((cm.avg_transaction_amount - pm.avg_transaction_amount) / NULLIF(pm.avg_transaction_amount, 0) * 100) as avg_amount_growth_pct,

        -- Transactions per customer
        cm.total_transactions / NULLIF(cm.unique_customers, 0) as current_txns_per_customer,
        pm.total_transactions / NULLIF(pm.unique_customers, 0) as prior_txns_per_customer

    FROM current_month_mtd cm
    CROSS JOIN prior_month_mtd pm
    CROSS JOIN new_customers nc
    CROSS JOIN churned_customers cc
    """

    print("Executing comprehensive analysis query...")
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        # Unpack results
        (curr_cust, curr_txn, curr_vol, curr_avg, curr_min, curr_max, curr_med, curr_days,
         prior_cust, prior_txn, prior_vol, prior_avg, prior_min, prior_max, prior_med, prior_days,
         new_cust, churned_cust, cust_growth, txn_growth, vol_growth, avg_growth,
         curr_tpc, prior_tpc) = result

        print("=" * 100)
        print("CUSTOMER METRICS")
        print("=" * 100)
        print(f"Current Month (Oct) MTD Unique Customers:  {curr_cust:>15,}")
        print(f"Prior Month (Sep) MTD Unique Customers:    {prior_cust:>15,}")
        print(f"Customer Growth:                           {cust_growth:>14.2f}%")
        print()
        print(f"New Customers (not in prior month):        {new_cust:>15,}")
        print(f"Churned Customers (not in current month):  {churned_cust:>15,}")
        print(f"Retention Rate:                            {(1 - churned_cust/max(prior_cust,1))*100:>14.2f}%")
        print()

        print("=" * 100)
        print("TRANSACTION METRICS")
        print("=" * 100)
        print(f"Current Month (Oct) MTD Transactions:      {curr_txn:>15,}")
        print(f"Prior Month (Sep) MTD Transactions:        {prior_txn:>15,}")
        print(f"Transaction Growth:                        {txn_growth:>14.2f}%")
        print()
        print(f"Current Transactions per Customer:         {curr_tpc:>15.2f}")
        print(f"Prior Transactions per Customer:           {prior_tpc:>15.2f}")
        print(f"Frequency Change:                          {((curr_tpc - prior_tpc)/max(prior_tpc,0.01))*100:>14.2f}%")
        print()

        print("=" * 100)
        print("VOLUME METRICS")
        print("=" * 100)
        print(f"Current Month (Oct) MTD Volume:            ${curr_vol:>14,.2f}")
        print(f"Prior Month (Sep) MTD Volume:              ${prior_vol:>14,.2f}")
        print(f"Volume Growth:                             {vol_growth:>14.2f}%")
        print(f"Absolute Volume Change:                    ${curr_vol - prior_vol:>14,.2f}")
        print()

        print("=" * 100)
        print("TRANSACTION SIZE METRICS")
        print("=" * 100)
        print(f"Current Month Avg Transaction:             ${curr_avg:>14,.2f}")
        print(f"Prior Month Avg Transaction:               ${prior_avg:>14,.2f}")
        print(f"Avg Transaction Growth:                    {avg_growth:>14.2f}%")
        print()
        print(f"Current Month Median Transaction:          ${curr_med:>14,.2f}")
        print(f"Prior Month Median Transaction:            ${prior_med:>14,.2f}")
        print()
        print(f"Current Month Min Transaction:             ${curr_min:>14,.2f}")
        print(f"Current Month Max Transaction:             ${curr_max:>14,.2f}")
        print(f"Prior Month Min Transaction:               ${prior_min:>14,.2f}")
        print(f"Prior Month Max Transaction:               ${prior_max:>14,.2f}")
        print()

        print("=" * 100)
        print("ACTIVITY METRICS")
        print("=" * 100)
        print(f"Current Month Active Days:                 {curr_days:>15,}")
        print(f"Prior Month Active Days:                   {prior_days:>15,}")
        print(f"Avg Transactions per Active Day (Curr):    {curr_txn/max(curr_days,1):>15.2f}")
        print(f"Avg Transactions per Active Day (Prior):   {prior_txn/max(prior_days,1):>15.2f}")
        print()

        # Daily breakdown
        print("=" * 100)
        print("DAILY TRANSACTION TRENDS - CURRENT MONTH")
        print("=" * 100)
        cursor.execute("""
            SELECT
                DATE(TRANSACTION_DATE_TIME) as transaction_date,
                COUNT(DISTINCT PRN) as unique_customers,
                COUNT(*) as transactions,
                SUM(ABS(TRANSACTION_AMOUNT)) as volume,
                AVG(ABS(TRANSACTION_AMOUNT)) as avg_amount
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
            AND DAY(TRANSACTION_DATE_TIME) <= DAY(CURRENT_DATE())
            GROUP BY DATE(TRANSACTION_DATE_TIME)
            ORDER BY transaction_date DESC
            LIMIT 7
        """)
        daily_data = cursor.fetchall()

        print()
        print("Last 7 Days:")
        print(f"{'Date':<12} {'Customers':>12} {'Transactions':>15} {'Volume':>18} {'Avg Amount':>15}")
        print("-" * 100)
        for row in daily_data:
            date, cust, txn, vol, avg = row
            print(f"{str(date):<12} {cust:>12,} {txn:>15,} ${vol:>17,.2f} ${avg:>14,.2f}")

        print()

        # Top transaction amounts
        print("=" * 100)
        print("TRANSACTION SIZE DISTRIBUTION - CURRENT MONTH")
        print("=" * 100)
        cursor.execute("""
            SELECT
                CASE
                    WHEN ABS(TRANSACTION_AMOUNT) < 50 THEN '$0-$50'
                    WHEN ABS(TRANSACTION_AMOUNT) < 100 THEN '$50-$100'
                    WHEN ABS(TRANSACTION_AMOUNT) < 200 THEN '$100-$200'
                    WHEN ABS(TRANSACTION_AMOUNT) < 500 THEN '$200-$500'
                    ELSE '$500+'
                END as amount_range,
                COUNT(*) as transaction_count,
                COUNT(DISTINCT PRN) as unique_customers,
                SUM(ABS(TRANSACTION_AMOUNT)) as total_volume,
                AVG(ABS(TRANSACTION_AMOUNT)) as avg_amount
            FROM MART_SRDF_POSTED_TRANSACTIONS
            WHERE (
                LOWER(MERCHANT_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(MERCHANT_FULL_DESCRIPTION) LIKE '%moneygram%'
                OR LOWER(COMPANY_NAME) LIKE '%moneygram%'
                OR LOWER(COMPANY_DESC) LIKE '%moneygram%'
            )
            AND DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) = DATE_TRUNC('MONTH', CURRENT_DATE())
            AND DAY(TRANSACTION_DATE_TIME) <= DAY(CURRENT_DATE())
            GROUP BY amount_range
            ORDER BY
                CASE amount_range
                    WHEN '$0-$50' THEN 1
                    WHEN '$50-$100' THEN 2
                    WHEN '$100-$200' THEN 3
                    WHEN '$200-$500' THEN 4
                    WHEN '$500+' THEN 5
                END
        """)
        distribution = cursor.fetchall()

        print()
        print(f"{'Amount Range':<15} {'Transactions':>15} {'Customers':>12} {'Volume':>18} {'Avg Amount':>15}")
        print("-" * 100)
        for row in distribution:
            range_name, txn_count, customers, volume, avg_amt = row
            print(f"{range_name:<15} {txn_count:>15,} {customers:>12,} ${volume:>17,.2f} ${avg_amt:>14,.2f}")

        print()
        print("=" * 100)
        print("KEY INSIGHTS")
        print("=" * 100)
        print()

        # Generate insights
        if cust_growth > 0:
            print(f"✓ Customer base grew by {abs(cust_growth):.1f}% MTD")
        else:
            print(f"✗ Customer base declined by {abs(cust_growth):.1f}% MTD")

        if txn_growth > 0:
            print(f"✓ Transaction volume grew by {abs(txn_growth):.1f}% MTD")
        else:
            print(f"✗ Transaction volume declined by {abs(txn_growth):.1f}% MTD")

        if vol_growth > 0:
            print(f"✓ Dollar volume grew by {abs(vol_growth):.1f}% MTD")
        else:
            print(f"✗ Dollar volume declined by {abs(vol_growth):.1f}% MTD")

        print(f"• {new_cust} new customers acquired this month")
        print(f"• {churned_cust} customers from last month have not transacted yet")
        print(f"• Average transaction frequency: {curr_tpc:.2f} transactions per customer")
        print(f"• Typical transaction size: ${curr_med:.2f} (median)")

        print()

    cursor.close()
    conn.close()

    print("=" * 100)
    print("END OF REPORT")
    print("=" * 100)

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
