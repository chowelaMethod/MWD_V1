# Comprehensive Dataset Comparison Report
## classification_research.csv vs MWD_Enriched_Accounts.csv

**Date:** January 8, 2026
**Analysis Type:** Complete Field-by-Field Comparison

---

## Executive Summary

This report documents **ALL** discrepancies between the `classification_research.csv` file and the `MWD_Enriched_Accounts.csv` dataset.

### Key Findings

| Metric | Count |
|--------|-------|
| **Total Accounts in Research File** | 589 |
| **Total Accounts in Enriched File** | 1,204 |
| **Accounts Matched** | 589 (100% of research accounts found) |
| **Accounts in Research but NOT in Enriched** | 0 |
| **Accounts in Enriched but NOT in Research** | 615 |
| **Total Discrepancies Found** | 4,277 |

---

## Discrepancy Breakdown by Field

### 1. Industry vs Industry (Research) Field
- **Count:** 589 discrepancies (100% of accounts)
- **Type:** Every account shows discrepancy
- **Reason:** The research file's `industry` field is being compared against the enriched file's `Industry (Research)` field, which shows "PENDING RESEARCH" for all accounts

**Example:**
- Account: `magicbreezekombucha`
- Research Industry: `Food & Beverage`
- Enriched Industry (Research): `PENDING RESEARCH`
- Enriched Vertical: `Manufacturing (MWD)`

**Impact:** This indicates the enriched dataset has not been updated with the research classifications

---

### 2. Industry vs Vertical Field
- **Count:** 586 discrepancies (99.5% of accounts)
- **Type:** Industry classification mismatch
- **Reason:** The research file uses detailed industry categories while the enriched file uses broader MWD verticals

**Pattern Analysis:**
- Research uses specific industries: `Food & Beverage`, `Consumer Goods`, `Industrial`, `Healthcare & Medical`, etc.
- Enriched uses MWD categories: `Manufacturing (MWD)`, `Wholesale and distribution services (MWD)`, `Retail`, etc.
- Only 3 accounts have matching values

**Examples:**
- `deansbeansorganiccoffee4`: Research = `Food & Beverage` → Enriched = `Wholesale and distribution services (MWD)`
- `helenarosejewelry`: Research = `Consumer Goods` → Enriched = `Wholesale and distribution services (MWD)`
- `davishoseinc`: Research = `Industrial` → Enriched = `Wholesale and distribution services (MWD)`

---

### 3. Sub-Industry Field
- **Count:** 589 discrepancies (100% of accounts)
- **Type:** Field missing in enriched dataset
- **Reason:** The `sub_industry` field exists ONLY in the research file

**Research File Has Detailed Sub-Industries:**
- `Craft Beverages (Kombucha)`
- `Appliances`
- `Safes/Security`
- `Craft Beer`
- `Coffee Roasting`
- `Fiber Optics`
- `Adaptive Fashion`
- `Powder Coating Services`
- `Industrial Hose`
- `Portable Sanitation`
- And 100+ more detailed classifications

**Impact:** The enriched dataset lacks the granular sub-industry classifications performed in research

---

### 4. Workflow Pattern
- **Count:** 589 discrepancies (100% of accounts)
- **Type:** Field values differ or missing
- **Reason:** The research file has workflow patterns that differ from the enriched file's `Workflow Type`

**Research Workflow Patterns:**
- `crm_pipeline`
- `quote_driven`
- `transactional`
- `mixed`

**Enriched Workflow Types:**
- May be empty or have different values
- Requires mapping verification

---

### 5. Total Events
- **Count:** 589 discrepancies (100% of accounts)
- **Type:** Field missing in enriched dataset
- **Reason:** Event count data tracked ONLY in research file

**Research Tracks Event Counts:**
- Range: 2 to 90,126 events per account
- Useful for activity analysis
- Not present in enriched dataset

---

### 6. Classification Source
- **Count:** 589 discrepancies (100% of accounts)
- **Type:** Field missing in enriched dataset
- **Reason:** Classification methodology tracked ONLY in research file

**Research Classification Sources:**
- `manual_verification` (highest confidence)
- `llm_classification` (medium confidence)
- `unclassified`

**Examples:**
- `magicbreezekombucha`: `manual_verification`
- `moderncompressorsales`: `manual_verification`
- `deansbeansorganiccoffee4`: `manual_verification`
- `allmakeappliances`: `llm_classification`

**Impact:** The enriched dataset doesn't track HOW classifications were made

---

### 7. Confidence Level
- **Count:** 437 discrepancies (74% of accounts)
- **Type:** Field missing in enriched dataset
- **Reason:** Confidence scores tracked ONLY in research file

**Research Confidence Levels:**
- `high` - manually verified
- `medium` - LLM classified
- `low` - lower confidence
- Missing for `unclassified` accounts

**Impact:** The enriched dataset doesn't track classification confidence

---

### 8. QBO Industry vs Sector
- **Count:** 309 discrepancies (52% of accounts)
- **Type:** Field values differ
- **Reason:** Different data sources or updates

**Examples:**
- Account variations in QBO industry coding
- Sector field may have different or updated values

---

## Accounts Analysis

### Accounts with Maximum Discrepancies (8 fields)

All accounts have at minimum 7-8 discrepancies due to structural differences between datasets. Sample accounts with 8 discrepancies:

1. `rhinoskintoughusainc`
2. `classicrockfaceblock`
3. `commfitness3`
4. `commonwealthindustrialinc`
5. `cooksmart2`
6. `coolsealgaskets`
7. `cpvusanew`
8. `crimsonimaging`
9. `safetnose`
10. `sacredstudiosinc`

... and 200+ more accounts

### Accounts ONLY in Enriched Dataset
- **Count:** 615 accounts
- **Location:** `results/dataset_comparison/accounts_only_in_enriched.csv`
- **Implication:** These accounts have not been researched/classified yet

---

## Critical Issues Identified

### 1. **Research Data Not Integrated**
- **Issue:** The enriched dataset's `Industry (Research)` field shows "PENDING RESEARCH" for ALL 589 accounts
- **Impact:** Research work hasn't been merged into the production dataset
- **Action Needed:** Update enriched dataset with research classifications

### 2. **Missing Granular Classifications**
- **Issue:** Sub-industry details from research not in enriched dataset
- **Impact:** Loss of detailed classification information
- **Action Needed:** Add sub_industry field to enriched dataset

### 3. **Missing Metadata Fields**
- **Issue:** Research tracking fields missing from enriched dataset:
  - `total_events`
  - `classification_source`
  - `confidence`
- **Impact:** Cannot assess data quality or classification methodology
- **Action Needed:** Add these metadata fields

### 4. **Industry/Vertical Mapping Mismatch**
- **Issue:** Research uses specific industries, enriched uses MWD broad categories
- **Impact:** 586 accounts show mismatched industry classifications
- **Action Needed:** Define mapping between research industries and MWD verticals

### 5. **Workflow Pattern Discrepancies**
- **Issue:** All 589 accounts show workflow pattern differences
- **Impact:** Business process classifications may be inconsistent
- **Action Needed:** Reconcile workflow type definitions

---

## Data Quality Assessment

### Research File Quality
✅ **Strengths:**
- Detailed sub-industry classifications
- Classification source tracking
- Confidence level tracking
- Event count data
- Manual verification for high-value accounts
- Comprehensive workflow patterns

❌ **Gaps:**
- Only covers 589 of 1,204 accounts (49%)
- Remaining 615 accounts not yet researched

### Enriched File Quality
✅ **Strengths:**
- More comprehensive (1,204 accounts)
- Rich metadata (30+ fields)
- Business metrics (MRR, LTV, etc.)
- Customer lifecycle data

❌ **Gaps:**
- Research classifications not integrated
- Missing granular sub-industry data
- No classification methodology tracking
- No confidence scoring

---

## Recommendations

### Priority 1: Data Integration
1. **Update enriched dataset** with research classifications
   - Replace "PENDING RESEARCH" with actual industry values
   - Add sub_industry field
   - Add classification_source field
   - Add confidence field

### Priority 2: Field Mapping
2. **Create mapping documentation** between:
   - Research industries ↔ MWD verticals
   - Research workflow patterns ↔ Enriched workflow types
   - QBO industry ↔ Sector

### Priority 3: Complete Research
3. **Classify remaining 615 accounts** in enriched dataset
   - Prioritize by revenue/value
   - Use same methodology as existing research
   - Track source and confidence

### Priority 4: Data Validation
4. **Audit and reconcile** the 586 industry mismatches
   - Determine which classification is correct
   - Update as needed
   - Document business rules for future

### Priority 5: Process Documentation
5. **Document classification process**
   - Criteria for manual vs. LLM classification
   - Confidence level assignment rules
   - Sub-industry taxonomy
   - Update frequency and ownership

---

## Detailed Results Files

All detailed analysis files saved to: `results/dataset_comparison/`

### Key Files:
1. **`all_discrepancies.csv`** - Complete list of 4,277 discrepancies
2. **`discrepancies_by_account.csv`** - Summary by account showing number and types of discrepancies
3. **`discrepancies_industry_vs_vertical.csv`** - 586 industry classification mismatches
4. **`discrepancies_industry_vs_industry_research.csv`** - 589 pending research items
5. **`discrepancies_sub_industry.csv`** - 589 missing sub-industry classifications
6. **`discrepancies_workflow_pattern.csv`** - 589 workflow pattern differences
7. **`discrepancies_qbo_industry_vs_sector.csv`** - 309 QBO/Sector mismatches
8. **`discrepancies_total_events.csv`** - 589 missing event counts
9. **`discrepancies_classification_source.csv`** - 589 missing source tracking
10. **`discrepancies_confidence.csv`** - 437 missing confidence scores
11. **`accounts_only_in_enriched.csv`** - 615 unresearched accounts

---

## Technical Notes

### Comparison Methodology
- Account names normalized (lowercase, trimmed) for matching
- 100% match rate for research accounts (589/589 found)
- Field-by-field comparison with null handling
- Sales values normalized (removed commas, quotes)

### Data Quality Rules Applied
- Empty strings, zeros, and nulls treated as missing
- Case-insensitive text matching
- Numeric values compared after cleaning

### Coverage Analysis
- Research file: 589 accounts (49% of total)
- Enriched file: 1,204 accounts (100% of customer base)
- Overlap: 589 accounts (100% of research, 49% of enriched)
- Gap: 615 accounts need research (51% of enriched)

---

## Conclusion

The comparison reveals **systematic structural differences** between the two datasets:

1. **Research classifications have NOT been integrated** into the enriched dataset (all show "PENDING RESEARCH")
2. **Granular sub-industry data exists only in research** - this valuable detail is missing from enriched
3. **Classification metadata is missing** - source, confidence, and event counts not in enriched dataset
4. **51% of accounts (615) lack research classifications** entirely

**Next Steps:**
The enriched dataset requires immediate update to incorporate the research findings. The 615 remaining accounts need classification using the same methodology. Once integrated, this will provide a complete, high-quality customer dataset with both granular classifications and comprehensive business metrics.

---

**Report Generated:** January 8, 2026
**Analysis Tool:** compare_datasets_detailed.py
**Data Sources:**
- `data/classification_research.csv` (589 records)
- `data/MWD_Enriched_Accounts.csv` (1,204 records)
