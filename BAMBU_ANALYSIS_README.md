# Bambu Financial Loss Analysis

Comprehensive analysis of Regulation E disputes, chargebacks, and industry benchmark comparisons using Snowflake MCP integration.

## Overview

This repository contains Python scripts and analysis tools for monitoring and analyzing financial losses at Bambu, including:
- Regulation E dispute analysis
- Chargeback monitoring
- Industry benchmark comparisons
- MoneyGram customer behavior analysis

## Key Findings

- **Reg E Loss Rate**: 0.033% (✓ GOOD - below industry average)
- **Chargeback Rate**: 0.484% (✓ GOOD - below industry average)
- **Total Loss Rate**: 0.517% (✗ HIGH - 3.4x industry average)
- **12-Month Total Losses**: $10,378,790
- **Potential Annual Savings**: $7.4M by achieving industry average

See [PRESENTATION.md](PRESENTATION.md) for detailed analysis and recommendations.

## Repository Structure

```
snowflake-mcp/
├── BAMBU_ANALYSIS_README.md              # This file
├── PRESENTATION.md                        # Comprehensive analysis presentation
├── .env                                   # Snowflake credentials (not committed)
├── .gitignore                            # Git ignore rules
│
├── keys/                                  # Authentication keys (not committed)
│   ├── snowflake_private_key.pem         # RSA private key (PEM format)
│   └── snowflake_private_key.p8          # RSA private key (DER format)
│
├── Analysis Scripts/
├── comprehensive_loss_report.py          # Monthly Reg E and chargeback analysis
├── industry_benchmark_comparison.py      # Industry standard comparisons
├── analyze_losses.py                     # Loss exploration and analysis
├── query_moneygram_customers.py          # MoneyGram customer identification
├── moneygram_mtd_analysis.py            # MoneyGram MTD comparisons
├── verify_moneygram_only.py             # Data verification script
└── find_loss_tables.py                   # Table discovery utility
```

## Prerequisites

- Python 3.11 or higher
- Snowflake account with ACCOUNTADMIN role
- Private key authentication configured

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/snowflake-mcp.git
cd snowflake-mcp
```

### 2. Install Python Dependencies

```bash
pip install snowflake-connector-python
```

### 3. Configure Credentials

Create a `.env` file with your Snowflake credentials:

```bash
SNOWFLAKE_ACCOUNT=YOUR_ACCOUNT
SNOWFLAKE_USER=YOUR_USERNAME
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=MYBAMBU_PROD
SNOWFLAKE_SCHEMA=BAMBU_MART_GALILEO
SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/your/private_key.p8
```

### 4. Set Up Authentication

Generate RSA key pair:

```bash
# Generate private key
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out keys/snowflake_private_key.pem -nocrypt

# Generate public key for Snowflake
openssl rsa -in keys/snowflake_private_key.pem -pubout -out keys/snowflake_public_key.pem

# Convert to DER format for Python connector
openssl pkcs8 -topk8 -inform PEM -outform DER -in keys/snowflake_private_key.pem -out keys/snowflake_private_key.p8 -nocrypt
```

Upload the public key to Snowflake:

```sql
ALTER USER YOUR_USERNAME SET RSA_PUBLIC_KEY='YOUR_PUBLIC_KEY_STRING';
```

## Usage

### Run Comprehensive Loss Report

```bash
python3.11 comprehensive_loss_report.py
```

Generates:
- Monthly Reg E dispute breakdown
- Monthly chargeback analysis
- Executive summary
- 12-month totals

### Run Industry Benchmark Comparison

```bash
python3.11 industry_benchmark_comparison.py
```

Generates:
- Loss rate vs industry standards
- Monthly rate comparisons
- Card network compliance status
- Savings/cost analysis

### Run MoneyGram Analysis

```bash
python3.11 moneygram_mtd_analysis.py
```

Generates:
- Month-over-month comparisons
- New customer identification
- Churn analysis
- Volume and frequency metrics

## Data Sources

### Snowflake Tables

**Database**: MYBAMBU_PROD
**Schema**: BAMBU_MART_GALILEO

- `MART_SRDF_CHARGEBACK_DISPUTES_REGE` - Regulation E disputes
- `MART_CDF_CHARGEBACK_AND_DISPUTE` - Chargebacks
- `MART_SRDF_POSTED_TRANSACTIONS` - Transaction data

### Key Metrics

| Metric | Calculation |
|--------|-------------|
| Reg E Net Loss | FINAL_RESOLUTION_AMOUNT - PROV_CREDIT_REVERSAL_AMOUNT |
| Chargeback Loss | SUM(DISPUTE_AMOUNT) |
| Loss Rate | (Total Losses / Transaction Volume) × 100 |

## Industry Benchmarks

### Loss Rate Standards (Fintech/Banking)

| Category | Low | Average | High |
|----------|-----|---------|------|
| Reg E | 0.01% | 0.05% | 0.10% |
| Chargebacks | 0.20% | 0.50% | 1.00% |
| Total Fraud | 0.05% | 0.15% | 0.30% |

### Card Network Thresholds

- **Visa**: 0.90% (90 basis points)
- **Mastercard**: 1.00% (100 basis points)

## Key Results (12 Months: Oct 2024 - Oct 2025)

### Financial Impact

```
Transaction Volume:        $2,008,992,292
Reg E Net Losses:          $653,944 (0.033%)
Chargeback Amounts:        $9,724,845 (0.484%)
Total Losses:              $10,378,790 (0.517%)
Average Monthly Loss:      $864,899
```

### Performance vs Industry

```
Reg E:         ✓ GOOD (0.017% below average)
Chargebacks:   ✓ GOOD (0.016% below average)
Total:         ✗ HIGH (0.367% above average)
Card Network:  ✓ SAFE (well below thresholds)
```

### October 2025 Performance

```
Total Loss:        $169,899 (80% below 12-month average)
Reg E Disputes:    34 cases (lowest in 12 months)
Chargebacks:       1,223 cases (lowest in 12 months)
Trend:             ↓↓ Strong improvement
```

## Recommendations

### Immediate Actions (0-30 days)

1. Investigate November-December 2024 loss spike ($3.3M anomaly)
2. Enhance MoneyGram transaction monitoring
3. Implement pre-dispute resolution strategies

### Short-Term (1-3 months)

4. Improve Reg E recovery rate from 25% to 30%
5. Launch customer dispute education program
6. Build real-time loss monitoring dashboard

### Long-Term (3-12 months)

7. Target industry average total loss rate (0.15%)
8. Deploy ML-based fraud detection
9. Address MoneyGram customer churn (currently 60%)

**Potential Annual Savings**: $7.4M by achieving industry average

## Security Notes

**IMPORTANT**: Never commit sensitive files:
- `.env` (credentials)
- `keys/` directory (private keys)
- Any files containing passwords or secrets

The `.gitignore` file is configured to exclude these automatically.

## Contributing

This is an internal analysis repository. For questions or suggestions, contact the Data Analytics team.

## License

Internal Use Only - Bambu Financial

## Changelog

### October 2025
- Initial analysis covering 12-month period (Oct 2024 - Oct 2025)
- Industry benchmark comparison implemented
- MoneyGram customer cohort analysis added
- MCP server integration configured

---

**Last Updated**: October 2025
**Analysis Period**: October 2024 - October 2025
**Database**: Snowflake MYBAMBU_PROD
**Next Review**: November 2025
