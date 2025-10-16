#!/usr/bin/env python3.11
"""Compare Bambu loss rates to industry standards"""

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
    print("LOSS RATE ANALYSIS - INDUSTRY BENCHMARK COMPARISON")
    print("=" * 140)
    print()

    # Get transaction volume for context
    print("Calculating transaction volume for loss rate analysis...")
    cursor.execute("""
        SELECT
            DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME) as month,
            COUNT(*) as total_transactions,
            SUM(ABS(TRANSACTION_AMOUNT)) as total_volume,
            COUNT(DISTINCT PRN) as unique_customers
        FROM MART_SRDF_POSTED_TRANSACTIONS
        WHERE TRANSACTION_DATE_TIME >= DATEADD('MONTH', -12, CURRENT_DATE())
        GROUP BY DATE_TRUNC('MONTH', TRANSACTION_DATE_TIME)
        ORDER BY month DESC
    """)

    volume_data = cursor.fetchall()

    # Get loss data
    cursor.execute("""
        SELECT
            DATE_TRUNC('MONTH', DATE_LOGGED) as month,
            SUM(ABS(COALESCE(FINAL_RESOLUTION_AMOUNT, 0))) - SUM(ABS(COALESCE(PROV_CREDIT_REVERSAL_AMOUNT, 0))) as net_loss,
            COUNT(*) as dispute_count
        FROM MART_SRDF_CHARGEBACK_DISPUTES_REGE
        WHERE DATE_LOGGED >= DATEADD('MONTH', -12, CURRENT_DATE())
        GROUP BY DATE_TRUNC('MONTH', DATE_LOGGED)
        ORDER BY month DESC
    """)

    rege_losses = cursor.fetchall()

    cursor.execute("""
        SELECT
            DATE_TRUNC('MONTH', DATE_LOGGED) as month,
            SUM(ABS(DISPUTE_AMOUNT)) as total_amount,
            COUNT(*) as cb_count
        FROM MART_CDF_CHARGEBACK_AND_DISPUTE
        WHERE DATE_LOGGED >= DATEADD('MONTH', -12, CURRENT_DATE())
        GROUP BY DATE_TRUNC('MONTH', DATE_LOGGED)
        ORDER BY month DESC
    """)

    cb_losses = cursor.fetchall()

    # Create loss dictionary
    rege_dict = {str(row[0])[:7]: (row[1], row[2]) for row in rege_losses}
    cb_dict = {str(row[0])[:7]: (row[1], row[2]) for row in cb_losses}

    # Industry benchmarks (basis points = 0.01%)
    INDUSTRY_BENCHMARKS = {
        'Reg E Loss Rate': {
            'Low': 0.01,      # 1 basis point (0.01%)
            'Average': 0.05,  # 5 basis points (0.05%)
            'High': 0.10      # 10 basis points (0.10%)
        },
        'Chargeback Rate': {
            'Low': 0.20,      # 20 basis points (0.20%)
            'Average': 0.50,  # 50 basis points (0.50%)
            'High': 1.00      # 100 basis points (1.00%)
        },
        'Total Fraud Loss Rate': {
            'Low': 0.05,      # 5 basis points (0.05%)
            'Average': 0.15,  # 15 basis points (0.15%)
            'High': 0.30      # 30 basis points (0.30%)
        }
    }

    print("=" * 140)
    print("MONTHLY LOSS RATE COMPARISON")
    print("=" * 140)
    print()

    print(f"{'Month':<12} {'Volume':>18} {'Reg E Loss':>15} {'CB Loss':>15} {'Total Loss':>15} {'Reg E Rate':>12} {'CB Rate':>12} {'Total Rate':>12}")
    print("-" * 140)

    total_volume = 0
    total_rege_loss = 0
    total_cb_loss = 0

    for row in volume_data:
        month, txn_count, volume, customers = row
        month_str = str(month)[:7]

        # Handle nulls
        volume = volume or 0
        rege_loss, rege_count = rege_dict.get(month_str, (0, 0))
        cb_loss, cb_count = cb_dict.get(month_str, (0, 0))
        rege_loss = rege_loss or 0
        cb_loss = cb_loss or 0

        total_loss = rege_loss + cb_loss

        # Calculate rates as percentage of volume
        rege_rate = (rege_loss / volume * 100) if volume > 0 else 0
        cb_rate = (cb_loss / volume * 100) if volume > 0 else 0
        total_rate = (total_loss / volume * 100) if volume > 0 else 0

        total_volume += volume
        total_rege_loss += rege_loss
        total_cb_loss += cb_loss

        print(f"{month_str:<12} ${volume:>17,.0f} ${rege_loss:>14,.0f} ${cb_loss:>14,.0f} ${total_loss:>14,.0f} {rege_rate:>11.3f}% {cb_rate:>11.3f}% {total_rate:>11.3f}%")

    print("-" * 140)

    # Calculate overall rates
    overall_rege_rate = float((total_rege_loss / total_volume * 100) if total_volume > 0 else 0)
    overall_cb_rate = float((total_cb_loss / total_volume * 100) if total_volume > 0 else 0)
    overall_total_rate = float(((total_rege_loss + total_cb_loss) / total_volume * 100) if total_volume > 0 else 0)

    total_loss_amount = total_rege_loss + total_cb_loss

    print(f"{'TOTAL':<12} ${total_volume:>17,.0f} ${total_rege_loss:>14,.0f} ${total_cb_loss:>14,.0f} ${total_loss_amount:>14,.0f} {overall_rege_rate:>11.3f}% {overall_cb_rate:>11.3f}% {overall_total_rate:>11.3f}%")
    print()

    # Industry comparison
    print("=" * 140)
    print("INDUSTRY BENCHMARK COMPARISON")
    print("=" * 140)
    print()

    print(f"{'Metric':<30} {'Bambu Rate':>15} {'Industry Low':>15} {'Industry Avg':>15} {'Industry High':>15} {'Status':>15}")
    print("-" * 140)

    # Reg E comparison
    reg_e_bench = INDUSTRY_BENCHMARKS['Reg E Loss Rate']
    if overall_rege_rate < reg_e_bench['Low']:
        rege_status = "✓ EXCELLENT"
    elif overall_rege_rate < reg_e_bench['Average']:
        rege_status = "✓ GOOD"
    elif overall_rege_rate < reg_e_bench['High']:
        rege_status = "○ AVERAGE"
    else:
        rege_status = "✗ HIGH"

    print(f"{'Reg E Loss Rate':<30} {overall_rege_rate:>14.3f}% {reg_e_bench['Low']:>14.2f}% {reg_e_bench['Average']:>14.2f}% {reg_e_bench['High']:>14.2f}% {rege_status:>15}")

    # Chargeback comparison
    cb_bench = INDUSTRY_BENCHMARKS['Chargeback Rate']
    if overall_cb_rate < cb_bench['Low']:
        cb_status = "✓ EXCELLENT"
    elif overall_cb_rate < cb_bench['Average']:
        cb_status = "✓ GOOD"
    elif overall_cb_rate < cb_bench['High']:
        cb_status = "○ AVERAGE"
    else:
        cb_status = "✗ HIGH"

    print(f"{'Chargeback Rate':<30} {overall_cb_rate:>14.3f}% {cb_bench['Low']:>14.2f}% {cb_bench['Average']:>14.2f}% {cb_bench['High']:>14.2f}% {cb_status:>15}")

    # Total fraud comparison
    fraud_bench = INDUSTRY_BENCHMARKS['Total Fraud Loss Rate']
    if overall_total_rate < fraud_bench['Low']:
        total_status = "✓ EXCELLENT"
    elif overall_total_rate < fraud_bench['Average']:
        total_status = "✓ GOOD"
    elif overall_total_rate < fraud_bench['High']:
        total_status = "○ AVERAGE"
    else:
        total_status = "✗ HIGH"

    print(f"{'Total Loss Rate':<30} {overall_total_rate:>14.3f}% {fraud_bench['Low']:>14.2f}% {fraud_bench['Average']:>14.2f}% {fraud_bench['High']:>14.2f}% {total_status:>15}")

    print()
    print("=" * 140)
    print("KEY INSIGHTS")
    print("=" * 140)
    print()

    # Basis points explanation
    print(f"Your 12-Month Loss Rates:")
    print(f"  • Reg E Losses:         {overall_rege_rate:.3f}% ({overall_rege_rate*100:.1f} basis points)")
    print(f"  • Chargeback Rate:      {overall_cb_rate:.3f}% ({overall_cb_rate*100:.1f} basis points)")
    print(f"  • Total Loss Rate:      {overall_total_rate:.3f}% ({overall_total_rate*100:.1f} basis points)")
    print()

    print(f"Dollar Impact:")
    print(f"  • Total Transaction Volume:    ${total_volume:,.0f}")
    print(f"  • Total Losses (12 months):    ${total_loss_amount:,.0f}")
    print(f"  • Average Monthly Loss:        ${total_loss_amount/12:,.0f}")
    print()

    print("Performance vs Industry:")
    print(f"  • Reg E:                {rege_status}")
    if overall_rege_rate < reg_e_bench['Average']:
        print(f"    ✓ You are {reg_e_bench['Average'] - overall_rege_rate:.3f}% below industry average")
    else:
        print(f"    ✗ You are {overall_rege_rate - reg_e_bench['Average']:.3f}% above industry average")

    print(f"  • Chargebacks:          {cb_status}")
    if overall_cb_rate < cb_bench['Average']:
        print(f"    ✓ You are {cb_bench['Average'] - overall_cb_rate:.3f}% below industry average")
    else:
        print(f"    ✗ You are {overall_cb_rate - cb_bench['Average']:.3f}% above industry average")

    print(f"  • Total:                {total_status}")
    if overall_total_rate < fraud_bench['Average']:
        print(f"    ✓ You are {fraud_bench['Average'] - overall_total_rate:.3f}% below industry average")
        savings = float(total_volume) * (fraud_bench['Average'] - overall_total_rate) / 100
        print(f"    💰 This saves approximately ${savings:,.0f} compared to industry average")
    else:
        print(f"    ✗ You are {overall_total_rate - fraud_bench['Average']:.3f}% above industry average")
        excess = float(total_volume) * (overall_total_rate - fraud_bench['Average']) / 100
        print(f"    💸 This costs approximately ${excess:,.0f} more than industry average")

    print()

    # Card network thresholds
    print("=" * 140)
    print("CARD NETWORK COMPLIANCE")
    print("=" * 140)
    print()

    visa_threshold = 0.90  # 90 basis points (0.9%)
    mastercard_threshold = 1.00  # 100 basis points (1.0%)

    print(f"Card Network Chargeback Thresholds:")
    print(f"  • Visa Threshold:           {visa_threshold:.2f}% (90 basis points)")
    print(f"  • Mastercard Threshold:     {mastercard_threshold:.2f}% (100 basis points)")
    print(f"  • Your Current Rate:        {overall_cb_rate:.3f}% ({overall_cb_rate*100:.1f} basis points)")
    print()

    if overall_cb_rate < visa_threshold:
        margin = visa_threshold - overall_cb_rate
        print(f"✓ SAFE: You are {margin:.3f}% below Visa's threshold")
        print(f"  Headroom: ${float(total_volume) * margin / 100:,.0f} before reaching threshold")
    else:
        print(f"⚠️  WARNING: You are at risk of Visa's Excessive Chargeback Program")

    print()

    cursor.close()
    conn.close()

    print("=" * 140)
    print("END OF BENCHMARK REPORT")
    print("=" * 140)

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
