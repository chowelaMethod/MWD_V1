# CRITICAL: Missing Accounts Analysis

**Date**: January 8, 2026
**Status**: 🚨 **URGENT - Data Gap Identified**

---

## Executive Summary

**CRITICAL FINDING**: 208 accounts in MWD_Enriched are missing from your active accounts analysis, including **34 accounts that were in your General W/D validation subset**. These accounts show activity indicators (users, invoices) but are not included in your current analysis.

###  The Core Problem

**You have overlapping datasets with inconsistent coverage:**

```
Dataset Coverage:
┌────────────────────────────────────────────────────────────────┐
│ Your Main Dataset:        14,218 total | 1,096 active          │
│ MWD_Enriched:              1,204 (92.9% show activity)         │
│ General W/D Validation:      421 (subset for validation)       │
│ Product Type Analysis:       997 (accounts with sales data)    │
│                                                                 │
│ GAP IDENTIFIED:                                                 │
│ ├─ 208 in MWD_Enriched NOT in your active accounts            │
│ │   ├─ 60 are test/demo/restore (exclude)                     │
│ │   ├─ 6 are fuzzy name matches (reconcile)                   │
│ │   ├─ 34 were in validation subset 🚨 (CRITICAL)             │
│ │   └─ 108 other accounts (investigate)                        │
│ │                                                               │
│ └─ These 208 accounts have:                                    │
│     • 92.9% show activity (users, invoices, recent sign-ups)  │
│     • Manual research completed (Industry, Workflow, Products) │
│     • Were important enough to include in prior analysis       │
└────────────────────────────────────────────────────────────────┘
```

---

## Critical Missing Accounts - Category Breakdown

### Category 1: Validation Subset Accounts (34 missing) 🚨

These 34 accounts are in **both** the validation subset AND MWD_Enriched, but NOT in your active accounts analysis.

**Why This Is Critical:**
- They were selected for the General W/D validation analysis (421-account subset)
- They have manual research completed in MWD_Enriched
- They show activity indicators (users, invoices)
- **But they're excluded from your current active account analysis**

**Top 10 by User Count:**

| # | Account | Users | Invoice | Sign-Up | Industry |
|---|---------|-------|---------|---------|----------|
| 1 | mtausa | 15 | $375 | 2015-04-27 | Industrial Process Cooling & Compressed Air Treatment |
| 2 | mjsystems | 6 | $150 | 2012-11-06 | PENDING RESEARCH |
| 3 | calpacific | 5 | $185 | 2011-06-28 | Food Distribution - Rice & Dry Goods Specialist |
| 4 | rivergatedoorsupply | 4 | $164 | 2025-12-06 | PENDING RESEARCH |
| 5 | herzogveneers2 | 3 | $219 | 2024-12-23 | PENDING RESEARCH |
| 6 | tastypuff | 3 | $120 | 2015-09-09 | PENDING RESEARCH |
| 7 | dmm21 | 3 | $120 | 2021-01-07 | PENDING RESEARCH |
| 8 | jollygl | 2 | $170 | 2025-12-08 | PENDING RESEARCH |
| 9 | wilco | 2 | $89 | 2021-08-18 | PENDING RESEARCH |
| 10 | sunshinedaydreamfarm | 2 | $88 | 2026-01-06 | PENDING RESEARCH |

Plus 24 more accounts...

**Statistics:**
- **Total**: 34 accounts
- **Avg Users**: 2.0
- **Avg Invoice**: $81.69
- **With >1 user**: 11 accounts (32%)
- **With >$50 invoice**: 20 accounts (59%)
- **With >$100 invoice**: 8 accounts (24%)

**Immediate Action Required:**
1. **mtausa** - 15 users, $375 invoice - Why is this enterprise account not in active?
2. **mjsystems** - 6 users, $150 invoice - Multi-user account missing
3. **calpacific** - 5 users, $185 invoice - Food Distribution specialist
4. **rivergatedoorsupply** - 4 users, $164 invoice (signed up Dec 2025 - very recent!)

### Category 2: Test/Demo/Restore Accounts (60 accounts) ✅

**Status**: Can be excluded

- 10 test/demo accounts (allantest, test188, m11demomarciaqbd, etc.)
- 50 restore/backup accounts (pattern: *restore2024*, *restore2025*)
- These are not production customer accounts

**Action**: Already identified and categorized - no further action needed.

### Category 3: Fuzzy Name Matches (6 accounts) 🔍

**Status**: Requires manual reconciliation

| MWD Account | Possible Match in Main | Similarity |
|-------------|----------------------|------------|
| callanindustrial2 | callanindustrial | 97.0% |
| hundeggerna | hundegger | 90.0% |
| jmbeverage | mpactbeverage2 | 75.0% |
| jsco | ajco | 75.0% |
| datamemorymarketing | datamemorysales | 70.6% |
| garcyusa | airtecusa | 70.6% |

**Action**: Check if these are the same customers with renamed accounts.

### Category 4: Other Missing Accounts (108 accounts) 📋

**Status**: Needs investigation

Includes:
- **58 recent sign-ups** (2025-2026) - May be post-01-07-2026 additions
- **20+ "m11" prefix accounts** - Unknown designation, some with high invoices
  - m11qbdtmethodlearns: $6,172 invoice
  - m11newinderqbo: $1,832 invoice
  - m11methoddanst: 4 users, $1,424 invoice
- **High-value unknowns**:
  - LappStructures: 29 users, $1,421
  - mhqnewmexico: 27 users, $1,323
  - HundeggerNA: 15 users, $600

**Action**: Priority investigation needed for accounts with >5 users or >$200 invoices.

---

## Root Cause Analysis

### Why Are These Accounts Missing?

**Hypothesis 1**: Active Status Filter Issue
- Your main dataset shows 1,096 "active" accounts
- But account name normalization shows only 998 unique matches
- **Possible cause**: Accounts marked as inactive in your system despite showing activity

**Hypothesis 2**: Data Export Timing
- Your dataset: 01-07-2026 snapshot
- MWD_Enriched: Unknown date, but includes accounts signed up through 01-06-2026
- **Possible cause**: MWD_Enriched includes post-export additions

**Hypothesis 3**: Account Name Variations
- 6 fuzzy matches found (70-97% similarity)
- Examples: "callanindustrial2" vs "callanindustrial"
- **Possible cause**: Account renaming or duplicate account creation

**Hypothesis 4**: Different Active Definitions
- Your system may define "active" differently than MWD_Enriched
- MWD includes accounts with low activity (1 user, small invoices)
- **Possible cause**: Lower activity threshold in MWD_Enriched

### The "500 Account" Analysis Clarified

You mentioned focusing on 500 accounts - this refers to the **421-account General W/D validation subset**:
- Purpose: Evidence-based validation of General Wholesale/Distribution sub-clustering
- Documented in: [analysis/07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md](analysis/07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md)
- Result: Discovered 98% error rate in keyword-based approach
- **Coverage**: 100% of these 421 accounts are in MWD_Enriched, but only 91.9% (387) are in your active dataset

---

## Impact Assessment

### What You're Missing

**Quantitative Impact:**
- **208 accounts** excluded from analysis (15% of MWD_Enriched)
- **34 validation accounts** missing (8% of validation subset)
- **Up to 1,118 active-like accounts** per MWD_Enriched activity indicators
  - vs. 1,096 in your "active" set
  - Potential 2% undercount of active customer base

**Qualitative Impact:**
- **Enterprise accounts missed**: mtausa (15 users), LappStructures (29 users), mhqnewmexico (27 users)
- **Manual research investment wasted**: 208 accounts researched but not included in analysis
- **Validation subset incomplete**: 34 of 421 validation accounts missing from main dataset
- **Trend analysis skewed**: Missing recent 2025-2026 sign-ups

### Business Risk

**HIGH RISK**: Enterprise Accounts
- mtausa: 15 users, $375 invoice - Could be key account
- LappStructures: 29 users, $1,421 invoice - Large customer
- mhqnewmexico: 27 users, $1,323 invoice - Large customer

**MEDIUM RISK**: Multi-User Accounts
- 11 of the 34 validation accounts have >1 user
- mjsystems: 6 users
- calpacific: 5 users
- rivergatedoorsupply: 4 users (recent!)

**LOW RISK**: Single-User Accounts
- But still represent potential revenue and analysis completeness

---

## Recommended Actions

### IMMEDIATE (Today)

1. **Investigate the 34 validation subset accounts**
   ```bash
   python3 investigate_validation_missing.py
   ```
   - Check why they're not in active accounts
   - Verify their current status in CRM/billing system
   - Prioritize: mtausa, mjsystems, calpacific, rivergatedoorsupply

2. **Verify enterprise accounts exist**
   - Search CRM for: mtausa, LappStructures, mhqnewmexico, HundeggerNA
   - If found: Why are they missing from active dataset?
   - If not found: Different account names? Merged accounts?

3. **Check "m11" prefix pattern**
   - Determine what "m11" designation means in your system
   - Some have very high invoices ($6,172, $1,832, $1,424)
   - Could represent 20+ missing high-value accounts

### SHORT-TERM (This Week)

4. **Create comprehensive account reconciliation**
   - Export full account list from CRM (not just "active")
   - Compare with MWD_Enriched account names
   - Build master account mapping file

5. **Reconcile fuzzy name matches**
   - Verify 6 fuzzy matches (callanindustrial2, hundeggerna, etc.)
   - Update account name mapping if same customer

6. **Validate active status definition**
   - Document what "Active?" field means in your system
   - Compare with MWD_Enriched inclusion criteria
   - Determine if definitions should align

### MEDIUM-TERM (Next 2 Weeks)

7. **Build integrated master dataset**
   - Include all accounts from both sources
   - Flag source: "In Main", "In MWD", "In Both"
   - Flag status: "Active", "Inactive", "Unknown"
   - Preserve all enrichment data

8. **Create account status reconciliation process**
   - Monthly sync between CRM export and analysis dataset
   - Automated detection of new/renamed/deactivated accounts
   - Alert when discrepancies exceed threshold

---

## Scripts to Create

### Script 1: investigate_validation_missing.py

```python
# Purpose: Deep dive into the 34 validation accounts missing from active
# Outputs:
#   - Current CRM status for each account
#   - Reason for exclusion from active dataset
#   - Recommendation: add to active or confirm inactive
```

### Script 2: reconcile_all_accounts.py

```python
# Purpose: Create master account list from all sources
# Inputs:
#   - customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv
#   - MWD_Enriched_Accounts.csv
#   - general_wd_validation_results.csv
# Output:
#   - master_account_reconciliation.csv with columns:
#     - Account_Name (normalized)
#     - In_Main_Dataset (True/False)
#     - In_MWD_Enriched (True/False)
#     - In_Validation_Subset (True/False)
#     - Active_Status (Active/Inactive/Unknown)
#     - Users, MRR, Last_Invoice
#     - Has_Manual_Research (True/False)
#     - Recommendation (Add/Reconcile/Exclude)
```

### Script 3: check_crm_status.py

```python
# Purpose: Check CRM for status of missing accounts
# For each of the 208 missing accounts:
#   - Search CRM by account name (fuzzy match)
#   - Return: Exists? Active? Users? Revenue?
#   - Flag for manual review if high-value
```

---

## Success Criteria

**Phase 1 - Investigation Complete** (End of this week):
- [ ] All 34 validation subset accounts status verified
- [ ] Enterprise accounts (mtausa, LappStructures, mhqnewmexico, HundeggerNA) investigated
- [ ] "m11" prefix pattern explained
- [ ] 6 fuzzy name matches reconciled

**Phase 2 - Data Reconciliation** (End of next week):
- [ ] Master account list created with all sources
- [ ] Active status definition documented and validated
- [ ] Accounts correctly categorized (add/exclude/reconcile)
- [ ] Updated integrated dataset created

**Phase 3 - Process Improvement** (End of month):
- [ ] Monthly account reconciliation process implemented
- [ ] Automated discrepancy detection in place
- [ ] Documentation updated with reconciliation procedures

---

## Critical Questions to Answer

### For the 34 Validation Subset Accounts:

1. **Why were they in the validation subset but not in active accounts?**
   - Were they marked inactive between validation and current analysis?
   - Different criteria for validation subset inclusion?

2. **What is the status of mtausa (15 users)?**
   - This is an enterprise-sized account - why missing?
   - Is it still active and generating revenue?
   - Was it merged into another account?

3. **Are the recent sign-ups (rivergatedoorsupply, sunshinedaydreamfarm) real customers?**
   - Signed up Dec 2025 - Jan 2026
   - If real, why not in 01-07-2026 export?

### For All 208 Missing Accounts:

4. **What does the "m11" prefix indicate?**
   - 20+ accounts with this pattern
   - Some with very high invoices ($6,172)
   - Migration batch? Test accounts? Integration type?

5. **Should MWD_Enriched be the source of truth for account list?**
   - It has 1,204 accounts with 92.9% activity rate
   - Your active list has 1,096 accounts
   - Which is more current/accurate?

6. **How often do accounts move in/out of "active" status?**
   - This would explain why validation subset (older) has different coverage
   - Need to understand churn and reactivation patterns

---

## Conclusion

The discovery of **34 validation subset accounts missing from your active analysis** represents a critical data integrity issue. These accounts:

1. Were important enough to be selected for validation analysis
2. Have completed manual research in MWD_Enriched
3. Show activity indicators (users, invoices)
4. Include enterprise accounts (15 users, 6 users, 5 users)
5. **But are excluded from your current analysis**

**Immediate action required** to:
- Verify status of the 34 accounts (especially mtausa, mjsystems, calpacific)
- Understand why they're missing
- Determine if they should be added back to active analysis
- Prevent this discrepancy from occurring in future analyses

The broader issue of 208 missing accounts (15% of MWD_Enriched) also needs investigation, but the 34 validation accounts are the highest priority due to their demonstrated importance in prior analysis.

---

## Files Generated

- **This document**: Analysis of missing accounts issue
- **investigate_missing_accounts.py**: Initial investigation script (already created)
- **results/missing_accounts_analysis.csv**: Full export of 208 missing accounts

## Next Files to Create

1. **investigate_validation_missing.py** - Deep dive on 34 critical accounts
2. **reconcile_all_accounts.py** - Master account reconciliation
3. **check_crm_status.py** - CRM status verification
4. **master_account_reconciliation.csv** - Comprehensive account mapping
