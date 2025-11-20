# MyBambu October 2025 Analysis
## Part 3: Card Usage & Transactions

**Analysis Period:** October 1-31, 2025
**Prompt:** 3 of 11

---

## OBJECTIVE
Analyze debit card issuance, activation, usage patterns, and transaction performance. Card interchange is a primary revenue driver for MyBambu.

---

## 1. DEBIT CARD ISSUANCE & ACTIVATION

### Card Inventory Metrics (as of Oct 31, 2025)
- **Total debit cards issued** (cumulative since inception)
- **Active cards** (used at least once in last 90 days)
- **New cards issued in October**
- **Cards activated in October**
- **Card activation rate**
  - Formula: (Cards activated / Cards issued) × 100
  - Industry benchmark: 60-75%

### Card Usage in October
- **Cards used** in October (at least 1 transaction)
  - Count
  - % of total active cards
- **Average transactions per active card**
- **New card first-use rate** (cards issued in Oct that made first transaction)

---

## 2. TRANSACTION VOLUME & SPEND

### October Card Transaction Metrics
- **Total card transactions** (count)
- **Total card spend** (volume in USD)
- **Average transaction value**
- **Median transaction value**
- **Largest transaction** (amount and category)
- **Smallest transaction** (if relevant)

### Daily Transaction Patterns
- **Average daily transaction count**
- **Peak transaction day** (highest volume day in October)
- **Peak transaction value day** (highest spend day)
- **Day of week analysis**
  - Weekday vs. weekend transaction patterns
  - Monday-Sunday breakdown

### Transaction Size Distribution
| Transaction Range | Count | % of Total | Volume (USD) | % of Spend |
|-------------------|-------|------------|--------------|------------|
| $0-$10 | ? | ? | ? | ? |
| $10-$25 | ? | ? | ? | ? |
| $25-$50 | ? | ? | ? | ? |
| $50-$100 | ? | ? | ? | ? |
| $100-$250 | ? | ? | ? | ? |
| $250+ | ? | ? | ? | ? |

---

## 3. TRANSACTION CATEGORIES

Analyze card spend by merchant category code (MCC):

### Top Transaction Categories
| Category | Transaction Count | Volume (USD) | % of Total Spend | Avg Transaction |
|----------|-------------------|--------------|------------------|-----------------|
| Groceries/Supermarkets | ? | ? | ? | ? |
| Gas Stations | ? | ? | ? | ? |
| Restaurants/Dining | ? | ? | ? | ? |
| Online Shopping | ? | ? | ? | ? |
| Retail Stores | ? | ? | ? | ? |
| Bills/Utilities | ? | ? | ? | ? |
| Entertainment | ? | ? | ? | ? |
| Healthcare | ? | ? | ? | ? |
| Travel | ? | ? | ? | ? |
| Other | ? | ? | ? | ? |

### Category Insights
- **Top 3 categories** by transaction count
- **Top 3 categories** by spend volume
- **Fastest-growing category** (MoM comparison)

---

## 4. CARD PERFORMANCE BY SEGMENT

### Transaction Types
- **In-store/POS transactions**
  - Count and volume
  - % of total transactions
- **Online/e-commerce transactions**
  - Count and volume
  - % of total transactions
- **Contactless/tap payments**
  - Count and volume
  - % of in-store transactions (penetration rate)
- **ATM withdrawals** (via debit card)
  - Count and volume
  - Already captured in Banking section, reference here

### Geographic Breakdown
- **Domestic transactions** (within US)
  - Count and volume
- **Cross-border/international transactions**
  - Count and volume
  - Top countries for international spend
  - Foreign transaction fees collected

---

## 5. DECLINED TRANSACTIONS

### Decline Analysis
- **Total declined transactions** (count)
- **Decline rate** (% of attempted transactions)
  - Formula: (Declined / Total attempted) × 100
  - Industry benchmark: 10-15%

### Decline Reasons Breakdown
| Decline Reason | Count | % of Declines |
|----------------|-------|---------------|
| Insufficient funds | ? | ? |
| Card not activated | ? | ? |
| Suspected fraud | ? | ? |
| Incorrect PIN | ? | ? |
| Expired card | ? | ? |
| Card locked/frozen | ? | ? |
| Merchant category restriction | ? | ? |
| Daily limit exceeded | ? | ? |
| Other | ? | ? |

### Lost Revenue from Declines
- **Potential transaction volume** lost to declines
- **Estimated interchange revenue** lost

---

## 6. USER SEGMENTATION BY CARD USAGE

Categorize users based on October card activity:

| User Segment | Criteria | User Count | Avg Monthly Spend | % of Total Spend |
|--------------|----------|------------|-------------------|------------------|
| **Power users** | 50+ transactions/month | ? | ? | ? |
| **Regular users** | 10-49 transactions/month | ? | ? | ? |
| **Occasional users** | 1-9 transactions/month | ? | ? | ? |
| **Card inactive** | Card issued but 0 transactions in Oct | ? | ? | ? |

---

## 7. COMPARISON METRICS

### Month-over-Month (October vs. September 2025)
| Metric | October 2025 | September 2025 | Change (%) |
|--------|--------------|----------------|------------|
| Total card transactions | ? | ? | ? |
| Total card spend | ? | ? | ? |
| Cards used | ? | ? | ? |
| Avg transaction value | ? | ? | ? |
| New cards issued | ? | ? | ? |
| Contactless transactions | ? | ? | ? |

### Year-over-Year (October 2025 vs. October 2024)
| Metric | October 2025 | October 2024 | Growth (%) |
|--------|--------------|--------------|------------|
| Total card spend | ? | ? | ? |
| Cards in use | ? | ? | ? |
| Transactions per card | ? | ? | ? |

---

## 8. REVENUE IMPACT

### Interchange Revenue Estimate
- **Estimated interchange rate** (typically 1.5-2.0% of transaction volume)
- **Estimated interchange revenue** from October card spend
  - Formula: Total card spend × Interchange rate
- **Revenue per active card** (interchange revenue / cards used)
- **MoM revenue growth** from card interchange

---

## 9. SAMPLE SQL QUERIES

```sql
-- Total card transactions and spend in October
SELECT
  COUNT(*) as total_transactions,
  SUM(amount) as total_spend,
  AVG(amount) as avg_transaction_value,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median_transaction
FROM card_transactions
WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'APPROVED';

-- Cards used in October
SELECT
  COUNT(DISTINCT card_id) as cards_used,
  COUNT(*) as total_transactions,
  ROUND(COUNT(*) / COUNT(DISTINCT card_id), 2) as avg_transactions_per_card
FROM card_transactions
WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'APPROVED';

-- Transaction category breakdown
SELECT
  merchant_category,
  COUNT(*) as transaction_count,
  SUM(amount) as total_spend,
  ROUND(AVG(amount), 2) as avg_amount,
  ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM card_transactions WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31' AND status = 'APPROVED'), 2) as pct_of_total_spend
FROM card_transactions
WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'APPROVED'
GROUP BY merchant_category
ORDER BY total_spend DESC
LIMIT 10;

-- Transaction type breakdown
SELECT
  transaction_type,
  COUNT(*) as count,
  SUM(amount) as volume,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM card_transactions WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31' AND status = 'APPROVED'), 2) as pct_of_transactions
FROM card_transactions
WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'APPROVED'
GROUP BY transaction_type
ORDER BY count DESC;

-- Declined transactions analysis
SELECT
  decline_reason,
  COUNT(*) as decline_count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM card_transactions WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31' AND status = 'DECLINED'), 2) as pct_of_declines
FROM card_transactions
WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'DECLINED'
GROUP BY decline_reason
ORDER BY decline_count DESC;

-- User segmentation by card usage
SELECT
  CASE
    WHEN tx_count >= 50 THEN 'Power User'
    WHEN tx_count >= 10 THEN 'Regular User'
    WHEN tx_count >= 1 THEN 'Occasional User'
    ELSE 'Card Inactive'
  END as user_segment,
  COUNT(*) as user_count,
  AVG(total_spend) as avg_monthly_spend
FROM (
  SELECT
    user_id,
    COUNT(*) as tx_count,
    SUM(amount) as total_spend
  FROM card_transactions
  WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
    AND status = 'APPROVED'
  GROUP BY user_id
)
GROUP BY user_segment
ORDER BY avg_monthly_spend DESC;

-- Daily transaction pattern
SELECT
  DATE(transaction_date) as day,
  COUNT(*) as transaction_count,
  SUM(amount) as daily_spend,
  DAYNAME(transaction_date) as day_of_week
FROM card_transactions
WHERE transaction_date BETWEEN '2025-10-01' AND '2025-10-31'
  AND status = 'APPROVED'
GROUP BY DATE(transaction_date), DAYNAME(transaction_date)
ORDER BY day;
```

---

## 10. DELIVERABLES

### Required Outputs:
1. **Summary table** - all key card metrics
2. **Daily transaction trend** - line chart of transactions and spend
3. **Category breakdown** - pie chart of top spending categories
4. **Transaction type split** - in-store vs. online vs. contactless
5. **User segmentation chart** - power vs. regular vs. occasional users
6. **Decline analysis** - decline rate and reason breakdown
7. **Interchange revenue estimate** - projected revenue from card usage

### Format Options:
- Excel workbook with card metrics tab
- CSV exports
- Dashboard with category trends and user segments

---

## 11. KEY QUESTIONS TO ANSWER

1. **What's our card activation rate?** (vs. 60-75% industry benchmark)
2. **How many transactions per active card?** (vs. industry avg of 15-25/month)
3. **What's our average transaction value?** (higher = better for interchange)
4. **Which spending categories dominate?** (groceries, gas = high interchange)
5. **Is contactless adoption growing?** (modern payment preference)
6. **What's causing card declines?** (opportunity to reduce friction)
7. **How much interchange revenue did we generate?**

---

**Next Steps:** Proceed to [04-bambupay-p2p-payments.md](04-bambupay-p2p-payments.md) to analyze BambuPay performance (highest priority).
