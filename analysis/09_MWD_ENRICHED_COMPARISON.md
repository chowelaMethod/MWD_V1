# MWD_Enriched_Accounts vs Existing Dataset Comparison

**Date**: January 8, 2026
**Analysis**: Dataset discrepancy identification and enrichment field review

---

## Executive Summary

The MWD_Enriched_Accounts dataset contains **1,204 accounts** with rich manual research data, while your existing integrated dataset has **14,218 total accounts** (1,096 active). There are **996 accounts in common** between the two datasets.

### Critical Discrepancies Identified

1. **Coverage Gap**: 208 accounts (17.3%) exist ONLY in MWD_Enriched but not in your existing data
2. **Dataset Size Difference**: MWD_Enriched is a filtered subset (1,204) vs your complete dataset (14,218)
3. **Classification Differences**: Industry classifications differ systematically between the two sources
4. **New Enrichment Fields**: MWD_Enriched has 7 valuable manual research fields not in your data

---

## 1. Account Coverage Analysis

### Numbers
- **MWD_Enriched_Accounts**: 1,204 accounts
- **Existing Dataset**: 14,218 total accounts (1,096 active, 997 with product data)
- **In BOTH datasets**: 996 accounts (82.7% of MWD)
- **ONLY in MWD_Enriched**: 208 accounts (17.3%)
- **ONLY in Existing**: 2 accounts

### Key Questions to Resolve

**Q1: Why are 208 accounts in MWD_Enriched but not in your existing data?**
- Are these newly added accounts?
- Were they filtered out as inactive in your dataset?
- Different account name formatting?
- Accounts added after your 01-07-2026 data export?

**Q2: What is the criteria for inclusion in MWD_Enriched?**
- Appears to be a curated subset of "Manufacturing & Wholesale Distribution" focused accounts
- All 1,204 have 100% manual research coverage (Company Description, Product Types, etc.)
- Likely represents prioritized/high-value segment

**Q3: Should you add the 208 missing accounts to your dataset?**
- Depends on their active status and business value
- Need to investigate if they're truly new or just reformatted names

### Sample Accounts ONLY in MWD_Enriched (first 10)
1. abcorlandolumberandhardware2
2. agralarm1restore20241015
3. agralarm1restore20251012
4. allantest
5. artisanclassicorganinc
6. atlanticgraphicsrestore20250507
7. aw
8. b2bepartners
9. bedsbydesign3
10. bellevilleindustries

**Note**: Some account names suggest test accounts ("allantest", "aw") or restore operations ("restore20241015")

---

## 2. New Enrichment Fields in MWD_Enriched

MWD_Enriched contains **7 valuable manual research fields** not present in your existing dataset:

### High-Value Enrichment Fields (100% Coverage)

#### 1. **Industry (Research)** - 1,204/1,204 (100%)
Manual research on actual business operations.

**Examples:**
- "Construction Equipment & Heavy Machinery Parts Distribution"
- "Medical Equipment & Supplies Wholesale Distribution"
- "Data Acquisition Systems & Test Measurement Solutions"
- "Push-to-Talk Telecommunications"
- "Mobility Equipment & Accessibility Solutions"

**Value**: Much more specific than your V2 clusters. Shows actual product/service specialization.

#### 2. **Workflow Type** - 1,204/1,204 (100%)
Specific workflow description for each business.

**Examples:**
- "Parts Distribution - Multi-Brand"
- "Medical Supply Distribution - Wholesale & Direct"
- "Manufacturing & Software - European DAQ Systems Specialist"

**Value**: Could directly inform feature prioritization and use case development.

#### 3. **Company Description** - 1,204/1,204 (100%)
Rich narrative description of business model and operations.

**Example:**
> "Distributor of new, aftermarket, used, and rebuilt parts for heavy construction equipment. Provides parts for all brands including CAT, Komatsu, Case, Deere, Kobelco, Cummins, Volvo CE, and more through warehouse network in USA, Canada & UK."

**Value**: Provides deep context for understanding business complexity and feature needs.

#### 4. **Product Types** - 1,204/1,204 (100%)
Detailed list of actual products sold.

**Example:**
> "Construction equipment parts (excavators, wheel loaders, backhoe loaders, crawler loaders, bulldozers, off-road trucks, mining equipment). Diesel engine parts for all makes and models."

**Value**: Complements your automated product type analysis. Manual research captures nuance.

#### 5. **Product Complexity** - 1,204/1,204 (100%)
Qualitative assessment of product catalog complexity.

**Levels**: Ultra-Simple, Simple, Standard, High, Very High

**Example:**
> "Very High - 300,000+ SKUs from 5,000+ manufacturers. Complex inventory with FDA compliance requirements, bulk distribution, and private-label manufacturing."

**Value**: Adds business context to your quantitative SKU metrics. Explains *why* catalogs are complex.

#### 6. **Company Name in QB** - 1,204/1,204 (100%)
The actual company name as it appears in QuickBooks.

**Value**: May differ from account name. Useful for reconciliation and customer communications.

#### 7. **Convert Pay Date** - 1,066/1,204 (88.5%)
Date account converted to paid status.

**Value**: Customer lifecycle tracking and cohort analysis.

### Medium-Value Fields (Partial Coverage)

- **Sector** - 491/1,204 (40.8%)
  - NAICS-style sector codes
  - Examples: "Medical supplies merchant wholesalers", "Computer and Electronic Product Manufacturing"

- **Website** - 517/1,204 (42.9%)
  - Actual company websites
  - Can be used for validation and enrichment

- **Annual Sales** - 1,203/1,204 (99.9%)
  - Company size indicator
  - May not match your MRR data (could be total business, not just Method revenue)

---

## 3. Classification System Differences

### Your Existing V2 Clustering
- **Industry_Cluster_Enhanced_V2**: 12 high-level clusters
  - General Wholesale/Distribution
  - General Retail
  - Apparel & Textiles
  - Food & Beverage
  - etc.

- **Business_Type_V2**: B2B, B2C, Hybrid
- **Company_Size_V2**: Micro, Small, Medium, Large, Enterprise

### MWD_Enriched Classification
- **Vertical**: Broad categories (MWD-focused)
  - "Wholesale and distribution services (MWD)"
  - "Manufacturing (MWD)"
  - "Retail"

- **Sector**: NAICS-style codes (40.8% coverage)
- **Industry (Research)**: Highly specific manual research (100% coverage)

### Sample Comparison

| Account | MWD Vertical | MWD Industry (Research) | Your V2 Cluster | Your Business Type |
|---------|--------------|-------------------------|-----------------|-------------------|
| conequipparts | Wholesale and distribution services (MWD) | Construction Equipment & Heavy Machinery Parts Distribution | General Wholesale/Distribution | B2B |
| j2medicalsupply | Wholesale and distribution services (MWD) | Medical Equipment & Supplies Wholesale Distribution | General Wholesale/Distribution | B2B |
| abeep | Wholesale and distribution services (MWD) | Push-to-Talk Telecommunications | General Wholesale/Distribution | B2B |
| access2mobility | Retail | Mobility Equipment & Accessibility Solutions | General Retail | B2C |

### Key Observations

1. **MWD Vertical is too broad** - Almost everything is "Wholesale and distribution services (MWD)"
   - Not useful for segmentation

2. **Industry (Research) is highly specific** - This is the most valuable classification
   - Manual research captures actual business operations
   - Much more detailed than your automated V2 clusters

3. **Your V2 clusters are consistent** - All 100 samples matched expected format
   - No data quality issues found

4. **Classification philosophies differ**:
   - **MWD approach**: Manual research → specific industry descriptions
   - **Your V2 approach**: Automated keyword matching → 12 standardized clusters

---

## 4. Field Value Discrepancies in Common Accounts

For the 996 accounts that exist in both datasets:

### Users Field (100% mismatch - FALSE POSITIVE)
- **Issue**: Data type difference only
- MWD: String format "1"
- Existing: Float format "1.0"
- **No actual data discrepancy** - just formatting

### Employees Field (No discrepancies found)
- Values match exactly where populated

### Website Field (No discrepancies found)
- Values match exactly where populated

### Vertical/Industry Classification (100% mismatch - EXPECTED)
- **Expected difference** - completely different classification systems
- MWD uses broad "Wholesale and distribution services (MWD)" categories
- Your V2 uses specific industry clusters
- **Not a data error** - just different taxonomies

---

## 5. Data Quality Assessment

### MWD_Enriched Strengths ✅
1. **100% manual research coverage** - Every account has rich descriptions
2. **Highly specific industry insights** - Captures nuanced business models
3. **Workflow type classification** - Directly relevant to feature needs
4. **Product complexity narratives** - Explains *why* businesses are complex
5. **Consistent data quality** - No missing values in key enrichment fields

### MWD_Enriched Limitations ⚠️
1. **Limited to 1,204 accounts** - Only 8.5% of your total dataset (14,218)
2. **MWD-focused** - Appears to prioritize Manufacturing & W/D verticals
3. **No product transaction data** - Lacks your detailed SKU/sales analysis
4. **Sector field incomplete** - Only 40.8% coverage
5. **May include test accounts** - Some account names suspicious ("allantest", "aw")

### Your Existing Dataset Strengths ✅
1. **Complete coverage** - All 14,218 accounts (1,096 active)
2. **Quantitative product analysis** - SKU counts, catalog complexity scores
3. **Automated and reproducible** - V2 clustering can be re-run
4. **Integration with product data** - 997 accounts with actual sales data
5. **User/MRR behavioral data** - Connects to usage patterns

### Your Existing Dataset Gaps 📊
1. **No manual research** - Lacks qualitative business context
2. **Generic cluster names** - "General Wholesale/Distribution" is broad
3. **No workflow type classification** - Missing direct feature mapping
4. **No company descriptions** - Harder to understand business nuances

---

## 6. Recommended Actions

### Immediate (This Week)

1. **Investigate the 208 accounts only in MWD_Enriched**
   ```python
   # Run this to check their status
   python scripts/investigate_missing_accounts.py
   ```
   - Are they active customers?
   - Were they renamed in your system?
   - Should they be added to your dataset?

2. **Create combined dataset** with enrichment fields for common 996 accounts
   - Add `Industry (Research)`, `Workflow Type`, `Company Description`, `Product Types`, `Product Complexity`
   - Keep your V2 clusters AND add MWD research as additional columns
   - Best of both: quantitative metrics + qualitative context

3. **Review test accounts** in MWD_Enriched
   - Filter out obvious test accounts: "allantest", "aw", etc.
   - Check "restore" accounts - may be backup/archive records

### Short-Term (Next 2 Weeks)

4. **Reconcile classification systems**
   - Keep your V2 clusters as primary (consistent, automated)
   - Add MWD `Industry (Research)` as secondary (specific, manual)
   - Create mapping between the two for analysis

5. **Extend manual research to high-value accounts**
   - Use MWD approach to research top 200 accounts by MRR
   - Focus on accounts NOT already in MWD_Enriched
   - Prioritize clusters with unclear workflow needs

6. **Validate MWD data quality**
   - Spot-check company descriptions against websites
   - Verify product types match your automated classification
   - Confirm complexity ratings align with SKU counts

### Long-Term (Next Month)

7. **Build integrated classification framework**
   - **Level 1**: Your V2 industry clusters (broad, automated)
   - **Level 2**: MWD workflow types (specific, use case focused)
   - **Level 3**: Manual research descriptions (context, nuance)

8. **Create segmentation strategy**
   - Combine quantitative (SKU count, users, MRR) + qualitative (workflow type, complexity narrative)
   - Map to product roadmap priorities
   - Identify high-value micro-segments

---

## 7. Critical Questions to Answer

### Data Integrity
1. ❓ Why do 208 accounts exist in MWD_Enriched but not in your 01-07-2026 export?
2. ❓ Are any of these 208 accounts active and generating revenue?
3. ❓ What is the source of MWD_Enriched data? (Different CRM? Different date range?)

### Classification Strategy
4. ❓ Should you use MWD's "Industry (Research)" or your V2 clusters as primary?
5. ❓ Can you map MWD workflow types to specific Method features?
6. ❓ Do you want to extend manual research to all active accounts?

### Integration Approach
7. ❓ Should you merge MWD enrichment fields into your primary dataset?
8. ❓ How to handle conflicts when classifications differ?
9. ❓ Which dataset should be "source of truth" for each field?

---

## 8. Comparison Summary Table

| Metric | MWD_Enriched | Your Existing Dataset | Recommendation |
|--------|--------------|----------------------|----------------|
| **Account Count** | 1,204 | 14,218 (1,096 active) | Keep existing as base, enrich from MWD |
| **Common Accounts** | 996 (82.7%) | 996 (7.0% of total, 90.8% of active) | Merge enrichment for these |
| **Unique Accounts** | 208 in MWD only | 13,222 not in MWD | Investigate 208 missing |
| **Manual Research** | 100% coverage | None | Add MWD research fields |
| **Industry Classification** | 3 levels (Vertical/Sector/Research) | V2 clusters + Business Type | Use both - V2 primary, Research secondary |
| **Product Analysis** | Qualitative descriptions | Quantitative metrics (SKUs, complexity scores) | Combine both for full picture |
| **Workflow Insights** | Workflow Type (100% coverage) | None | High value - integrate this |
| **Data Completeness** | Rich but limited scope | Complete but lacks context | Complementary strengths |

---

## 9. Next Steps Script

Created: [compare_datasets.py](../compare_datasets.py)

This script performs comprehensive comparison and can be extended to:
- Generate merge proposals
- Identify data quality issues
- Create combined datasets
- Map between classification systems

---

## Files Referenced
- [data/MWD_Enriched_Accounts.csv](../data/MWD_Enriched_Accounts.csv) - External enrichment data (1,204 accounts)
- [data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv](../data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv) - Your integrated dataset (14,218 accounts)
- [compare_datasets.py](../compare_datasets.py) - Comparison analysis script
