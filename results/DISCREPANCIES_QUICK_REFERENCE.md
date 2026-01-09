# Dataset Comparison - Quick Reference Guide

**Date**: January 8, 2026

---

## Account Coverage Breakdown

```
Total Accounts Analysis:
┌─────────────────────────────────────────────────────────────┐
│ MWD_Enriched_Accounts:        1,204 accounts                │
│ Your Existing Dataset:       14,218 accounts (1,096 active) │
│                                                              │
│ ✓ Common to Both:               996 accounts (82.7%)        │
│ ⚠ Only in MWD_Enriched:         208 accounts (17.3%)        │
│   ├─ Test/Demo:                  10 (exclude)               │
│   ├─ Restore/Backup:             50 (exclude)               │
│   ├─ Suspicious Names:            1 (review)                │
│   ├─ Fuzzy Name Matches:          6 (reconcile)             │
│   └─ Likely New Accounts:       141 (investigate)           │
│                                                              │
│ ✓ Only in Existing:               2 accounts                │
└─────────────────────────────────────────────────────────────┘
```

---

## The 208 "Missing" Accounts - Categorized

### 🗑️ Exclude from Analysis (60 accounts)

**Test/Demo Accounts (10)**:
- allantest, test188, m11demomarciaqbd, m11michaeldemo2025
- m11sammydemo, m11testaccount3, m11testqbdtanna, m1testmethod
- m11errolqbdtrightdemo, statestreetproductsllc

**Restore/Backup Accounts (50)**:
- Pattern: `*restore2024*`, `*restore2025*`
- Examples: agralarm1restore20241015, atlanticgraphicsrestore20250507, blkcorprestore20240930
- These are backup/recovery snapshots, not active accounts

### 🔍 Reconcile (6 accounts - Potential Name Variations)

| MWD Account Name | Possible Match in Existing | Similarity |
|------------------|---------------------------|------------|
| callanindustrial2 | callanindustrial | 97.0% |
| hundeggerna | hundegger | 90.0% |
| jmbeverage | mpactbeverage2 | 75.0% |
| jsco | ajco | 75.0% |
| datamemorymarketing | datamemorysales | 70.6% |
| garcyusa | airtecusa | 70.6% |

**Action Required**: Manually verify if these are renamed versions of same accounts.

### ⚠️ Review (1 account - Suspicious)

- **aw** - Very short name, but legitimate: "Appalachian Woods, LLC" (4 users, Sign Up: 2015-01-07)
  - Actually appears to be a real business account

### 🆕 Investigate (141 accounts - Likely Genuine)

**Key Statistics:**
- **137 have "PENDING RESEARCH"** (not fully researched yet)
- **10 have completed research** (industry descriptions done)
- **58 signed up in 2025-2026** (very recent customers)
- **96 show activity indicators** (>1 user OR invoice >$50)

**Top 10 by Invoice Amount:**

| Account | Users | Last Invoice | Vertical | Research Status |
|---------|-------|--------------|----------|-----------------|
| m11qbdtmethodlearns | 1 | $6,172 | Retail | PENDING |
| m11newinderqbo | 1 | $1,832 | MWD | PENDING |
| m11methoddanst | 4 | $1,424 | Retail | PENDING |
| LappStructures | 29 | $1,421 | Manufacturing | ✓ Custom Outdoor Structures |
| mhqnewmexico | 27 | $1,323 | Manufacturing | PENDING |
| m11marinaqbg | 1 | $912 | Retail | PENDING |
| m112025salesa | 1 | $729 | MWD | PENDING |
| HundeggerNA | 15 | $600 | Manufacturing | ✓ CNC Timber Machinery |
| m11AcentrixStockCA | 1 | $519 | Retail | PENDING |
| m11glicksmanglicklane | 1 | $510 | Retail | PENDING |

**Notable High-Value Accounts to Investigate:**
- **LappStructures**: 29 users, $1,421 invoice - Custom Outdoor Structures Manufacturing
- **mhqnewmexico**: 27 users, $1,323 invoice - Manufacturing (pending research)
- **HundeggerNA**: 15 users, $600 invoice - CNC Timber Construction Machinery

**Pattern Observation**: Many accounts have "m11" prefix - may indicate specific account type or migration batch.

---

## New Enrichment Fields Available (from MWD_Enriched)

### ✅ Fields with 100% Coverage (1,204 accounts)

| Field Name | Description | Example Value |
|------------|-------------|---------------|
| **Industry (Research)** | Specific manual research | "Construction Equipment & Heavy Machinery Parts Distribution" |
| **Workflow Type** | Workflow classification | "Parts Distribution - Multi-Brand" |
| **Company Description** | Rich narrative | "Distributor of new, aftermarket, used, and rebuilt parts..." |
| **Product Types** | Detailed product list | "Construction equipment parts (excavators, wheel loaders...)" |
| **Product Complexity** | Qualitative assessment | "Very High - 300,000+ SKUs from 5,000+ manufacturers..." |
| **Company Name in QB** | QB company name | "Conequip Parts & Equipment LLC" |
| **Vertical** | Broad category | "Wholesale and distribution services (MWD)" |

### ⚠️ Fields with Partial Coverage

| Field Name | Coverage | Example Value |
|------------|----------|---------------|
| **Convert Pay Date** | 88.5% | "2014-07-12" |
| **Annual Sales** | 99.9% | "$83,325" |
| **Sector** | 40.8% | "Medical supplies merchant wholesalers" |
| **Website** | 42.9% | "conequipparts.com" |

---

## Classification System Comparison

### For 996 Common Accounts:

**100% have DIFFERENT industry classifications** (EXPECTED - different systems)

#### Your V2 System (Automated)
- **Industry_Cluster_Enhanced_V2**: 12 standardized clusters
  - Examples: "General Wholesale/Distribution", "General Retail", "Apparel & Textiles"
- **Business_Type_V2**: B2B, B2C, Hybrid (automated inference)
- **Company_Size_V2**: Micro, Small, Medium, Large, Enterprise

#### MWD System (Manual Research)
- **Vertical**: 3 broad categories
  - "Wholesale and distribution services (MWD)" (most common)
  - "Manufacturing (MWD)"
  - "Retail"
- **Industry (Research)**: Highly specific (100% coverage)
  - "Push-to-Talk Telecommunications"
  - "Scientific Sample Preparation Equipment Manufacturing"
  - "Food Distribution - Rice & Dry Goods Specialist"
- **Sector**: NAICS-style (40.8% coverage)

#### Example Comparison:

| Account | MWD Vertical | MWD Industry (Research) | Your V2 Cluster | Your Business Type |
|---------|--------------|-------------------------|-----------------|-------------------|
| conequipparts | Wholesale and distribution services (MWD) | Construction Equipment & Heavy Machinery Parts Distribution | General Wholesale/Distribution | B2B |
| j2medicalsupply | Wholesale and distribution services (MWD) | Medical Equipment & Supplies Wholesale Distribution | General Wholesale/Distribution | B2B |
| access2mobility | Retail | Mobility Equipment & Accessibility Solutions | General Retail | B2C |

**Recommendation**: Keep BOTH systems
- V2 = Primary (consistent, automated, complete coverage)
- MWD Research = Secondary enrichment (adds specificity and context)

---

## Data Quality Issues Found

### ✅ No Real Discrepancies in Common Accounts

1. **Users field "mismatch"** - FALSE POSITIVE
   - Just data type difference: "1" (string) vs "1.0" (float)
   - Actual values are identical

2. **Industry classification "mismatch"** - EXPECTED
   - Different taxonomies, not data errors
   - Both are valid, just different approaches

3. **Employees, Website fields** - NO ISSUES
   - Values match exactly where both datasets have data

### ⚠️ Observations

1. **MWD "Vertical" field is too broad**
   - Almost everything labeled "Wholesale and distribution services (MWD)"
   - Not useful for segmentation on its own

2. **MWD "Industry (Research)" is highly valuable**
   - Much more specific than your V2 clusters
   - Captures actual business specialization

3. **137 of 141 "new" accounts have "PENDING RESEARCH"**
   - Suggests MWD_Enriched dataset is work-in-progress
   - Manual research not yet completed for these accounts

---

## Recommended Action Priority

### 🔴 HIGH PRIORITY (This Week)

1. **Merge enrichment data for 996 common accounts**
   - Add 7 MWD columns to your existing dataset
   - Script needed to join on normalized account names

2. **Exclude 60 test/restore accounts**
   - Filter them out of any MWD analysis

3. **Reconcile 6 fuzzy name matches**
   - Manual verification needed (highest match is 97% similar)

### 🟡 MEDIUM PRIORITY (Next 2 Weeks)

4. **Investigate high-value "new" accounts**
   - Focus on 29 accounts with 5+ users (LappStructures, mhqnewmexico, HundeggerNA, etc.)
   - Check if they're actually new or just renamed/filtered

5. **Understand "m11" prefix pattern**
   - 20+ accounts with this prefix in "new" list
   - May indicate migration batch or specific account type

6. **Validate MWD research quality**
   - Spot-check company descriptions against websites
   - Verify product types match your ItemType analysis

### 🟢 LOW PRIORITY (Next Month)

7. **Decide on remaining 112 "new" accounts**
   - Lower users/invoice amounts
   - May be inactive or test accounts not flagged by keywords

8. **Create integrated classification framework**
   - Level 1: V2 clusters (broad)
   - Level 2: MWD Workflow Types (specific)
   - Level 3: MWD Research (detailed context)

---

## Files Created

1. **[DATASET_COMPARISON_SUMMARY.md](../DATASET_COMPARISON_SUMMARY.md)** - Executive summary
2. **[analysis/09_MWD_ENRICHED_COMPARISON.md](../analysis/09_MWD_ENRICHED_COMPARISON.md)** - Full detailed analysis
3. **[compare_datasets.py](../compare_datasets.py)** - Comparison script
4. **[investigate_missing_accounts.py](../investigate_missing_accounts.py)** - Missing accounts script
5. **[results/missing_accounts_analysis.csv](missing_accounts_analysis.csv)** - Full missing accounts export
6. **This file** - Quick reference guide

---

## Questions to Answer

1. **Where did MWD_Enriched_Accounts come from?**
   - Different system? Different date? Manually curated?

2. **Why are 58 accounts from 2025-2026 "missing" from your 01-07-2026 export?**
   - Were they added AFTER your export date?
   - Or filtered out as inactive?

3. **What is the "m11" prefix?**
   - Special account type? Migration batch?
   - 20+ accounts have this pattern

4. **Should the 141 accounts be added to your primary dataset?**
   - Need to check active status in CRM
   - Verify they're not duplicates with different names

5. **Should manual research be extended to all active accounts?**
   - MWD only covers 1,204 (8.5% of total, 110% of active)
   - Cost/benefit of researching remaining accounts?
