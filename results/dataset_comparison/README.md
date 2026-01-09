# Dataset Comparison Analysis Results

This directory contains a comprehensive comparison between `classification_research.csv` and `MWD_Enriched_Accounts.csv`.

## Summary

- **Total Research Accounts:** 589
- **Total Enriched Accounts:** 1,204
- **Accounts Matched:** 589 (100%)
- **Total Discrepancies:** 4,277

## Key Finding

🚨 **CRITICAL:** None of the research classifications have been integrated into the enriched dataset. All 589 accounts show "PENDING RESEARCH" in the enriched file's `Industry (Research)` field.

## Main Reports

1. **[COMPREHENSIVE_DATASET_COMPARISON_REPORT.md](../../COMPREHENSIVE_DATASET_COMPARISON_REPORT.md)**
   - Full detailed analysis of all discrepancies
   - Field-by-field comparison
   - Data quality assessment
   - Complete recommendations

2. **[DISCREPANCIES_QUICK_REFERENCE.md](../../DISCREPANCIES_QUICK_REFERENCE.md)**
   - Quick reference guide
   - Priority actions
   - Sample discrepancies
   - Bottom line summary

3. **[DATASET_COMPARISON_EXECUTIVE_SUMMARY.md](../../DATASET_COMPARISON_EXECUTIVE_SUMMARY.md)**
   - Executive-level overview
   - Key metrics and statistics
   - Industry patterns
   - Next steps

## Data Files

### Main Discrepancy Files

- **all_discrepancies.csv** (4,277 records)
  - Complete list of every discrepancy found
  
- **discrepancies_by_account.csv** (589 accounts)
  - Summary showing number of discrepancies per account
  
- **accounts_only_in_enriched.csv** (615 accounts)
  - Accounts that need research classification

### Detailed Discrepancy Files (by type)

- **discrepancies_industry_vs_vertical.csv** (586 records)
  - Industry classification mismatches
  
- **discrepancies_industry_vs_industry_research.csv** (589 records)
  - All showing "PENDING RESEARCH" in enriched
  
- **discrepancies_sub_industry.csv** (589 records)
  - Sub-industry missing from enriched dataset
  
- **discrepancies_workflow_pattern.csv** (589 records)
  - Workflow type differences
  
- **discrepancies_qbo_industry_vs_sector.csv** (309 records)
  - QBO industry vs Sector field mismatches
  
- **discrepancies_total_events.csv** (589 records)
  - Event counts missing from enriched
  
- **discrepancies_classification_source.csv** (589 records)
  - Classification source metadata missing
  
- **discrepancies_confidence.csv** (437 records)
  - Confidence level metadata missing

### Analysis Files

- **industry_mapping_analysis.csv**
  - Cross-tabulation: Research industries → MWD verticals
  
- **high_priority_manual_verified.csv** (135 accounts)
  - Highest quality manually verified classifications
  
- **high_confidence_classifications.csv** (105 accounts)
  - All high-confidence classifications
  
- **unclassified_need_review.csv** (152 accounts)
  - Accounts marked as "Other/Unclassified" in research

### Example Files

- **SIDE_BY_SIDE_EXAMPLES.txt**
  - Visual side-by-side comparison of 10 sample accounts

## Discrepancy Breakdown

| Issue | Count | % | Severity |
|-------|-------|---|----------|
| Research not integrated | 589 | 100% | 🔴 CRITICAL |
| Sub-industry missing | 589 | 100% | 🔴 CRITICAL |
| Industry vs Vertical mismatch | 586 | 99.5% | 🟡 HIGH |
| Workflow pattern differences | 589 | 100% | 🟡 HIGH |
| Classification source missing | 589 | 100% | 🟠 MEDIUM |
| Confidence level missing | 437 | 74% | 🟠 MEDIUM |
| Event counts missing | 589 | 100% | 🟢 LOW |
| QBO/Sector differences | 309 | 52% | 🟢 LOW |

## Data Quality

### Research File
- ✅ 135 manually verified accounts (highest quality)
- ✅ 437 accounts with sub-industry detail (74%)
- ✅ 437 accounts with confidence scores (74%)
- ✅ 589 accounts with event counts (100%)
- ❌ 152 accounts unclassified (26%)

### Enriched File
- ✅ 1,204 accounts (complete customer base)
- ✅ 30+ fields of rich metadata
- ❌ All research showing "PENDING RESEARCH"
- ❌ Sub-industry field doesn't exist
- ❌ Classification metadata fields missing

## Immediate Actions Required

1. **Update enriched dataset** with research classifications
2. **Add sub_industry field** to enriched schema
3. **Add metadata fields** (source, confidence, events)
4. **Classify remaining 615 accounts** not in research

## Industry Statistics

### Research Industries (Top 10)
1. Other (unclassified) - 152 accounts
2. Food & Beverage - 104 accounts
3. Consumer Goods - 70 accounts
4. Construction & Building - 66 accounts
5. Industrial - 44 accounts
6. Healthcare & Medical - 32 accounts
7. Manufacturing - 26 accounts
8. Technology - 21 accounts
9. Services - 18 accounts
10. Furniture - 16 accounts

### Sub-Industry Detail
- **178 unique sub-industry types**
- Examples:
  - Food & Beverage: Coffee Roasting, Craft Beer, Wine, Spirits
  - Industrial: Compressor Equipment, Industrial Hose, Filtration
  - Consumer Goods: Jewelry, Promotional Products, Beauty/Personal Care
  - Construction & Building: Doors & Windows, Flooring, HVAC

## High-Activity Accounts (by event count)

1. celluma - 90,126 events (Healthcare & Medical)
2. holdit - 57,216 events (Retail Fixtures)
3. brownsafe - 33,497 events (Security Equipment)
4. fujimats - 33,716 events (Sports & Recreation)
5. rexdistributioninc - 33,541 events (Food & Beverage)

## Questions & Support

For questions about this analysis:
1. Review the main reports (listed above)
2. Check the detailed CSV files for specific accounts
3. Review the side-by-side examples

---

**Analysis Date:** January 8, 2026
**Tool:** compare_datasets_detailed.py
**Analyst:** Claude Code Analysis
