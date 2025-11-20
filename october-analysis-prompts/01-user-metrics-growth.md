# MyBambu October 2025 Analysis
## Part 1: User Metrics & Growth

**Analysis Period:** October 1-31, 2025
**Prompt:** 1 of 11

---

## OBJECTIVE
Analyze overall platform user growth, engagement, and geographic distribution for October 2025. This provides the foundation for understanding total addressable users across all MyBambu products.

---

## 1. USER BASE & GROWTH

### Cumulative User Metrics
Generate the following metrics as of **October 31, 2025 23:59:59 UTC**:

- **Total registered users** (cumulative since inception)
- **Verified/Active accounts** vs. pending verification
- **Net new users** added in October

### October New User Registrations
- **Total new signups** in October
- **Daily breakdown** (Oct 1-31, identify peak signup days)
- **Weekly breakdown** (4-5 weeks in October)
- **Signup completion rate** (started registration vs. completed)

### User Activity Metrics
- **Monthly Active Users (MAU)** - users with ANY activity in October
  - Definition: Users who logged in, made a transaction, or performed any platform action
- **Daily Active Users (DAU)** - average across all days in October
- **DAU/MAU ratio** - engagement health metric
  - Industry benchmark: 15-25% is typical for fintech
  - MyBambu target: TBD

### User Retention & Churn
- **User churn rate** - accounts closed or abandoned in October
  - Calculate: (Users who left / Beginning active users) × 100
- **User retention rates** by cohort:
  - **30-day retention** (Sept 2025 signups still active in Oct)
  - **90-day retention** (July 2025 signups still active in Oct)
  - **180-day retention** (April 2025 signups still active in Oct)
- **Reactivated users** - dormant users (no activity in 90+ days) who returned in October

---

## 2. ACCOUNT STATUS BREAKDOWN

Categorize all users as of October 31, 2025:

| Status Category | Definition | Count | % of Total |
|----------------|------------|-------|------------|
| **Active accounts** | Activity within last 30 days | ? | ? |
| **Dormant accounts** | No activity in 90+ days but account open | ? | ? |
| **Suspended/frozen** | Temporarily restricted (compliance, fraud, user request) | ? | ? |
| **Closed in October** | Accounts permanently closed during October | ? | ? |
| **Pending verification** | Awaiting KYC/identity verification | ? | ? |

---

## 3. GEOGRAPHIC DISTRIBUTION

### Users by State/Territory
- **Top 10 states** by user count
- **Bottom 5 states** (identify underserved markets)
- **State-level growth rates** (Oct vs. Sept)

### Users by City
- **Top 10 cities** by user count
- **Top 5 fastest-growing cities** (% growth Oct vs. Sept)

### Domestic vs. International
- **US-based users** (count and %)
- **International users** (count and %, if applicable)
  - Break down by country if significant volume

### New Market Penetration
- **Newly served regions** in October (cities/states with first-time users)
- **Geographic expansion metrics**

---

## 4. USER DEMOGRAPHICS (if available)

If demographic data is tracked:
- **Age distribution** (18-24, 25-34, 35-44, 45-54, 55+)
- **Language preference** (English, Spanish, other)
- **Account type** (individual, joint, business - if applicable)

---

## 5. COMPARISON METRICS

### Month-over-Month (October vs. September 2025)
| Metric | October 2025 | September 2025 | Change (%) |
|--------|--------------|----------------|------------|
| Total users | ? | ? | ? |
| MAU | ? | ? | ? |
| DAU (avg) | ? | ? | ? |
| New signups | ? | ? | ? |
| Churn rate | ? | ? | ? |

### Year-over-Year (October 2025 vs. October 2024)
| Metric | October 2025 | October 2024 | Growth (%) |
|--------|--------------|--------------|------------|
| Total users | ? | ? | ? |
| MAU | ? | ? | ? |
| New signups | ? | ? | ? |

---

## 6. SAMPLE SQL QUERIES

```sql
-- Total registered users as of Oct 31, 2025
SELECT COUNT(*) as total_users
FROM users
WHERE created_at <= '2025-10-31 23:59:59';

-- Monthly Active Users (MAU) in October
SELECT COUNT(DISTINCT user_id) as mau
FROM user_activity
WHERE activity_date BETWEEN '2025-10-01' AND '2025-10-31';

-- Daily Active Users (DAU) - average for October
SELECT AVG(daily_users) as avg_dau
FROM (
  SELECT DATE(activity_date) as day, COUNT(DISTINCT user_id) as daily_users
  FROM user_activity
  WHERE activity_date BETWEEN '2025-10-01' AND '2025-10-31'
  GROUP BY DATE(activity_date)
);

-- New user signups in October (daily breakdown)
SELECT
  DATE(created_at) as signup_date,
  COUNT(*) as new_users
FROM users
WHERE created_at BETWEEN '2025-10-01' AND '2025-10-31'
GROUP BY DATE(created_at)
ORDER BY signup_date;

-- User retention rate (30-day cohort)
WITH sept_signups AS (
  SELECT user_id
  FROM users
  WHERE created_at BETWEEN '2025-09-01' AND '2025-09-30'
),
oct_active AS (
  SELECT DISTINCT user_id
  FROM user_activity
  WHERE activity_date BETWEEN '2025-10-01' AND '2025-10-31'
)
SELECT
  COUNT(DISTINCT s.user_id) as sept_signups,
  COUNT(DISTINCT a.user_id) as still_active_in_oct,
  ROUND(COUNT(DISTINCT a.user_id) * 100.0 / COUNT(DISTINCT s.user_id), 2) as retention_rate_pct
FROM sept_signups s
LEFT JOIN oct_active a ON s.user_id = a.user_id;

-- Users by state (top 10)
SELECT
  state,
  COUNT(*) as user_count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as pct_of_total
FROM users
GROUP BY state
ORDER BY user_count DESC
LIMIT 10;

-- Account status breakdown
SELECT
  CASE
    WHEN last_activity_date >= DATE_SUB('2025-10-31', INTERVAL 30 DAY) THEN 'Active'
    WHEN last_activity_date >= DATE_SUB('2025-10-31', INTERVAL 90 DAY) THEN 'Recent'
    WHEN status = 'closed' THEN 'Closed'
    WHEN status = 'suspended' THEN 'Suspended'
    WHEN kyc_status = 'pending' THEN 'Pending Verification'
    ELSE 'Dormant'
  END as account_status,
  COUNT(*) as user_count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as pct
FROM users
GROUP BY account_status
ORDER BY user_count DESC;
```

---

## 7. DELIVERABLES

### Required Outputs:
1. **Summary table** with all key metrics
2. **Daily trend chart** - new signups by day in October
3. **DAU/MAU line chart** - daily DAU and monthly MAU
4. **Geographic heatmap** - users by state
5. **Retention curve** - 30/60/90/180-day retention rates
6. **Account status pie chart** - active, dormant, pending, etc.
7. **MoM comparison table** - Oct vs. Sept growth rates

### Format Options:
- Excel workbook with tabs for each section
- CSV files (one per table)
- Interactive dashboard (Tableau/Looker)
- PDF summary with charts

---

## 8. KEY QUESTIONS TO ANSWER

1. **Did we hit our MAU targets for October?**
2. **What was our user growth rate (MoM and YoY)?**
3. **Are we retaining new users effectively?** (30-day retention vs. industry benchmark)
4. **Which geographic markets are growing fastest?**
5. **What percentage of users are dormant?** (opportunity for reactivation)
6. **How does our DAU/MAU ratio compare to industry standards?**

---

**Next Steps:** Proceed to [02-banking-financial-activity.md](02-banking-financial-activity.md) to analyze deposit and transaction activity.
