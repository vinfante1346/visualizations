# MyBambu October 2025 Analysis
## Part 2: Banking & Financial Activity

**Analysis Period:** October 1-31, 2025
**Prompt:** 2 of 11

---

## OBJECTIVE
Analyze deposit accounts, balances, cash flows, and traditional banking transaction volumes for October 2025. This measures the core banking health of the platform.

---

## 1. ACCOUNT BALANCES & DEPOSITS

### Aggregate Balance Metrics (as of Oct 31, 2025)
- **Total deposits** - sum of all account balances across platform
- **Average account balance** (mean)
- **Median account balance** (50th percentile)
- **Account balance distribution:**
  - Accounts with $0 balance
  - Accounts with $0.01-$100
  - Accounts with $100-$500
  - Accounts with $500-$1,000
  - Accounts with $1,000-$5,000
  - Accounts with $5,000-$10,000
  - Accounts with $10,000+

### October Cash Flows
- **New deposits** (total inflow in October)
  - Include: Direct deposits, ACH transfers in, check deposits, cash loads
- **Withdrawals** (total outflow in October)
  - Include: ACH transfers out, ATM withdrawals, card spending, bill payments
- **Net deposit flow** (deposits - withdrawals)
  - Positive = growing deposit base
  - Negative = shrinking deposit base

### Balance Growth Analysis
- **Beginning balance** (Oct 1, 2025 00:00:00)
- **Ending balance** (Oct 31, 2025 23:59:59)
- **Net growth** (dollar amount and %)
- **MoM comparison** (Oct vs. Sept deposit growth)

---

## 2. DIRECT DEPOSIT ADOPTION

Direct deposit is a key engagement and retention driver.

### Enrollment Metrics
- **Users with active direct deposit** setup
  - Total count
  - % of total active users
- **New direct deposit enrollments** in October
- **Direct deposit drop-offs** (users who stopped DD in October)

### Direct Deposit Volume
- **Total direct deposit transactions** (count)
- **Total direct deposit value** (USD)
- **Average direct deposit amount** per transaction
- **Median direct deposit amount**

### Direct Deposit Frequency
Categorize users by DD frequency:
- **Weekly** (4+ DD transactions in October)
- **Bi-weekly** (2 DD transactions in October)
- **Monthly** (1 DD transaction in October)
- **Irregular** (DD setup but no October deposits)

### Employer Partnerships
If tracked:
- **Top 10 employer sources** by DD volume
- **Payroll processor breakdown** (ADP, Paychex, etc.)
- **Government benefits** (Social Security, VA, etc.)

---

## 3. TRADITIONAL BANKING TRANSACTIONS

### ACH Transfers
- **ACH transfers OUT** (user-initiated withdrawals)
  - Transaction count
  - Total volume (USD)
  - Average amount
  - Failed ACH transactions (count and reasons)
- **ACH transfers IN** (excluding direct deposit)
  - Transaction count
  - Total volume (USD)
  - Average amount

### Wire Transfers
- **Domestic wires sent**
  - Count and total volume
  - Average wire amount
  - Wire fees collected
- **Domestic wires received**
  - Count and total volume
- **International wires** (if applicable)
  - Count, volume, destinations

### Check Deposits (Mobile Deposit)
- **Total check deposits** (count)
- **Total check deposit value** (USD)
- **Average check amount**
- **Failed/rejected checks** (count and reasons)
- **Check deposit users** (unique users who deposited checks)

### ATM Withdrawals
- **Total ATM withdrawals** (count)
- **Total ATM withdrawal volume** (USD)
- **Average ATM withdrawal amount**
- **In-network ATM usage** (fee-free)
- **Out-of-network ATM usage** (fee-generating)
- **ATM fee revenue** collected

### Bill Payments
- **Bill payment transactions** (count)
- **Bill payment volume** (USD)
- **Unique users paying bills**
- **Top biller categories** (utilities, credit cards, loans, etc.)

---

## 4. TRANSACTION PATTERNS

### Daily Transaction Volume
- **Peak transaction days** (day of week analysis)
- **Month-end spike** (last 3 days of October vs. month average)
- **Payday correlation** (1st, 15th of month if detectable)

### User Segmentation by Banking Activity
| Segment | Criteria | Count | Avg Balance |
|---------|----------|-------|-------------|
| **High-value depositors** | Balance > $5,000 | ? | ? |
| **Active bankers** | 10+ transactions/month | ? | ? |
| **Direct deposit users** | Active DD setup | ? | ? |
| **Savings-focused** | Positive net flow in Oct | ? | ? |
| **Transactional only** | Low balance, high activity | ? | ? |

---

## 5. COMPARISON METRICS

### Month-over-Month (October vs. September 2025)
| Metric | October 2025 | September 2025 | Change (%) |
|--------|--------------|----------------|------------|
| Total deposits (balance) | ? | ? | ? |
| New deposits (inflow) | ? | ? | ? |
| Withdrawals (outflow) | ? | ? | ? |
| Net deposit flow | ? | ? | ? |
| Direct deposit users | ? | ? | ? |
| ACH transactions | ? | ? | ? |
| Check deposits | ? | ? | ? |

### Year-over-Year (October 2025 vs. October 2024)
| Metric | October 2025 | October 2024 | Growth (%) |
|--------|--------------|--------------|------------|
| Total deposits | ? | ? | ? |
| Direct deposit users | ? | ? | ? |
| Transaction volume | ? | ? | ? |

---

## 6. SAMPLE SQL QUERIES

```sql
-- Total deposits (aggregate balances) as of Oct 31
SELECT
  SUM(balance) as total_deposits,
  AVG(balance) as avg_balance,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY balance) as median_balance,
  COUNT(*) as total_accounts
FROM account_balances
WHERE snapshot_date = '2025-10-31';

-- Account balance distribution
SELECT
  CASE
    WHEN balance = 0 THEN '$0'
    WHEN balance <= 100 THEN '$0.01 - $100'
    WHEN balance <= 500 THEN '$100 - $500'
    WHEN balance <= 1000 THEN '$500 - $1,000'
    WHEN balance <= 5000 THEN '$1,000 - $5,000'
    WHEN balance <= 10000 THEN '$5,000 - $10,000'
    ELSE '$10,000+'
  END as balance_tier,
  COUNT(*) as account_count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM account_balances WHERE snapshot_date = '2025-10-31'), 2) as pct
FROM account_balances
WHERE snapshot_date = '2025-10-31'
GROUP BY balance_tier
ORDER BY MIN(balance);

-- Direct deposit adoption
SELECT
  COUNT(DISTINCT user_id) as dd_users,
  SUM(amount) as total_dd_volume,
  COUNT(*) as total_dd_transactions,
  AVG(amount) as avg_dd_amount
FROM transactions
WHERE transaction_type = 'DIRECT_DEPOSIT'
  AND transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'COMPLETED';

-- October cash flows
WITH inflows AS (
  SELECT SUM(amount) as total_inflow
  FROM transactions
  WHERE transaction_type IN ('DIRECT_DEPOSIT', 'ACH_CREDIT', 'CHECK_DEPOSIT', 'CASH_LOAD')
    AND transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
    AND status = 'COMPLETED'
),
outflows AS (
  SELECT SUM(amount) as total_outflow
  FROM transactions
  WHERE transaction_type IN ('ACH_DEBIT', 'ATM_WITHDRAWAL', 'CARD_PURCHASE', 'BILL_PAYMENT', 'WIRE_TRANSFER')
    AND transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
    AND status = 'COMPLETED'
)
SELECT
  i.total_inflow,
  o.total_outflow,
  (i.total_inflow - o.total_outflow) as net_deposit_flow,
  ROUND(((i.total_inflow - o.total_outflow) / i.total_inflow) * 100, 2) as net_flow_rate_pct
FROM inflows i, outflows o;

-- ACH transaction analysis
SELECT
  CASE
    WHEN amount > 0 THEN 'ACH Credit (Incoming)'
    ELSE 'ACH Debit (Outgoing)'
  END as ach_type,
  COUNT(*) as transaction_count,
  SUM(ABS(amount)) as total_volume,
  AVG(ABS(amount)) as avg_amount
FROM transactions
WHERE transaction_type LIKE 'ACH%'
  AND transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'COMPLETED'
GROUP BY ach_type;

-- ATM withdrawal analysis
SELECT
  CASE
    WHEN network = 'IN_NETWORK' THEN 'In-Network (Fee-Free)'
    ELSE 'Out-of-Network (Fee)'
  END as atm_type,
  COUNT(*) as withdrawal_count,
  SUM(amount) as total_withdrawn,
  AVG(amount) as avg_withdrawal,
  SUM(fee) as total_fees_collected
FROM transactions
WHERE transaction_type = 'ATM_WITHDRAWAL'
  AND transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'COMPLETED'
GROUP BY atm_type;
```

---

## 7. DELIVERABLES

### Required Outputs:
1. **Summary table** - all key banking metrics
2. **Balance distribution chart** - histogram of account balances
3. **Cash flow waterfall** - inflows vs. outflows visualization
4. **Direct deposit trend** - daily DD volume throughout October
5. **Transaction type breakdown** - pie chart of ACH, ATM, checks, bills
6. **MoM growth chart** - deposit balance growth trend

### Format Options:
- Excel workbook with banking metrics tab
- CSV exports for each table
- Dashboard with balance trends and DD adoption

---

## 8. KEY QUESTIONS TO ANSWER

1. **Is our deposit base growing or shrinking?** (net deposit flow)
2. **What percentage of users have direct deposit?** (vs. industry benchmark of 40-60%)
3. **Are high-balance accounts growing?** (users with $5K+)
4. **What's our average account balance?** (industry avg: $1,500-$3,000 for neobanks)
5. **Are we generating ATM fee revenue?** (out-of-network usage)
6. **Which transaction types are most popular?** (ACH, ATM, checks, bills)

---

**Next Steps:** Proceed to [03-card-usage-transactions.md](03-card-usage-transactions.md) to analyze debit card activity.
