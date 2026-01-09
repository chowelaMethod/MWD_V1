# MWD_Enriched_Accounts vs Existing Dataset - Executive Summary

**Date**: January 8, 2026
**Analysis**: Comprehensive comparison of external enrichment data vs internal dataset

---

## Key Findings at a Glance

### Account Coverage
- **MWD_Enriched_Accounts**: 1,204 accounts with 100% manual research
- **Your Existing Dataset**: 14,218 total accounts (1,096 active)
- **Overlap**: 996 accounts (82.7% of MWD accounts)
- **208 accounts ONLY in MWD_Enriched**:
  - 60 are test/demo/restore accounts (exclude)
  - 6 appear to be renamed versions of existing accounts
  - 1 suspicious name (very short: "aw")
  - **~141 potentially genuine new accounts** to investigate

### Data Quality Comparison

| Aspect | MWD_Enriched ✅ | Your Existing Dataset ✅ |
|--------|----------------|--------------------------|
| **Coverage** | 1,204 MWD-focused accounts | 14,218 complete account base |
| **Manual Research** | 100% (Industry, Workflow, Descriptions) | 0% |
| **Quantitative Metrics** | Limited (Users, basic financials) | Rich (SKU count, complexity scores, MRR) |
| **Industry Classification** | 3-tier (Vertical/Sector/Research) | V2 automated clusters |
| **Product Analysis** | Qualitative descriptions | Quantitative ItemType analysis |
| **Workflow Insights** | Workflow Type field (100%) | None |
| **Data Freshness** | Unknown date | 01-07-2026 snapshot |

---

## Critical Discrepancies

### 1. Industry Classifications (All 996 common accounts differ)
**This is EXPECTED** - different classification systems, not a data error.

**MWD Approach**:
- Broad "Vertical": "Wholesale and distribution services (MWD)", "Manufacturing (MWD)", "Retail"
- Specific "Industry (Research)": "Construction Equipment & Heavy Machinery Parts Distribution"
- NAICS-style "Sector": "Medical supplies merchant wholesalers" (40.8% populated)

**Your V2 Approach**:
- 12 standardized clusters: "General Wholesale/Distribution", "General Retail", etc.
- Automated keyword-based classification
- Business_Type_V2: B2B, B2C, Hybrid

**Recommendation**: Keep BOTH. Use V2 as primary (consistent, automated), add MWD "Industry (Research)" as secondary enrichment for the 996 accounts with manual research.

### 2. Field Value Discrepancies
- **Users field**: 100% "mismatch" is FALSE POSITIVE (just data type: "1" vs "1.0")
- **Employees, Website**: No real discrepancies found
- **Industry fields**: Expected differences due to different taxonomies

### 3. Account Name Variations
Found **6 fuzzy matches** that may be renamed accounts:
1. `callanindustrial2` (MWD) vs `callanindustrial` (Existing) - 97.0% similar
2. `datamemorymarketing` (MWD) vs `datamemorysales` (Existing) - 70.6% similar
3. `hundeggerna` (MWD) vs `hundegger` (Existing) - 90.0% similar
4. Plus 3 more potential matches

**Action**: Manually verify and reconcile these 6 accounts.

---

## Valuable New Enrichment Fields in MWD_Enriched

### High-Value Fields to Import (100% coverage in MWD data)

1. **Industry (Research)** - Highly specific manual research
   - Examples: "Construction Equipment & Heavy Machinery Parts Distribution", "Medical Equipment & Supplies Wholesale Distribution"
   - Much more specific than your automated V2 clusters

2. **Workflow Type** - Direct mapping to workflow needs
   - Examples: "Parts Distribution - Multi-Brand", "Medical Supply Distribution - Wholesale & Direct"
   - Could inform feature prioritization and use case development

3. **Company Description** - Rich narrative context
   - Full paragraph descriptions of business model, operations, scale
   - Provides qualitative context your quantitative metrics lack

4. **Product Types** - Detailed product catalog descriptions
   - Examples: "Construction equipment parts (excavators, wheel loaders...)", "PPE (nitrile gloves, isolation gowns...)"
   - Complements your automated ItemType analysis

5. **Product Complexity** - Qualitative complexity assessment
   - Categories: Ultra-Simple, Simple, Standard, High, Very High
   - Includes narrative explaining WHY complexity exists
   - Example: "Very High - 300,000+ SKUs from 5,000+ manufacturers. Complex inventory with FDA compliance requirements"

6. **Company Name in QB** - Actual QuickBooks company name
   - May differ from account name
   - Useful for reconciliation

7. **Convert Pay Date** - Conversion lifecycle tracking (88.5% coverage)

### Medium-Value Fields (Partial coverage)

- **Sector** - NAICS-style codes (40.8% coverage)
- **Website** - Company websites (42.9% coverage)
- **Annual Sales** - Company size indicator (99.9% coverage, but may not match Method revenue)

---

## Recommended Integration Strategy

### Phase 1: Immediate (This Week)

1. **Merge enrichment fields for 996 common accounts**
   - Add 7 new columns to your existing dataset: Industry (Research), Workflow Type, Company Description, Product Types, Product Complexity, Company Name in QB, Convert Pay Date
   - Keep your existing V2 clusters AND add MWD research as supplementary data
   - Best of both: quantitative metrics + qualitative context

2. **Exclude 60 test/restore accounts from MWD data**
   - 10 test/demo accounts
   - 50 restore/backup accounts
   - These are not production customer accounts

3. **Reconcile 6 fuzzy name matches**
   - Manually verify if they're the same accounts with different names
   - Update account name mapping if needed

### Phase 2: Short-Term (Next 2 Weeks)

4. **Investigate remaining 141 accounts**
   - Check if they're active customers (have recent invoices, users, MRR)
   - Verify sign-up dates - many are recent (2025-2026)
   - Examples of potentially valuable accounts:
     - `calpacific` - 5 users, $185 invoice, "Food Distribution - Rice & Dry Goods Specialist"
     - `boeckeler` - 4 users, $148 invoice, "Scientific Sample Preparation Equipment Manufacturing"
     - `digpig` - 5 users, $353 invoice
   - Add to your primary dataset if they're active customers

5. **Validate data quality**
   - Spot-check MWD company descriptions against actual websites
   - Verify MWD product types align with your automated ItemType analysis
   - Cross-check complexity ratings with your SKU counts

### Phase 3: Long-Term (Next Month)

6. **Build integrated classification framework**
   - **Level 1**: Your V2 clusters (broad, automated, consistent)
   - **Level 2**: MWD Workflow Types (specific, feature-oriented)
   - **Level 3**: MWD Industry Research (detailed, context-rich)

7. **Create enhanced segmentation**
   - Combine quantitative (SKU count, users, MRR, catalog complexity scores)
   - With qualitative (workflow type, complexity narratives, company descriptions)
   - Map to product roadmap priorities
   - Identify high-value micro-segments

---

## Files Generated

1. **[analysis/09_MWD_ENRICHED_COMPARISON.md](analysis/09_MWD_ENRICHED_COMPARISON.md)** - Full detailed analysis (this document)
2. **[compare_datasets.py](compare_datasets.py)** - Comparison script (can be re-run)
3. **[investigate_missing_accounts.py](investigate_missing_accounts.py)** - Missing accounts investigation script
4. **[results/missing_accounts_analysis.csv](results/missing_accounts_analysis.csv)** - Full list of 208 missing accounts with metadata

---

## Next Steps

### Immediate Actions Required

1. **Review the 6 fuzzy name matches** - Are these duplicates?
   - callanindustrial2 vs callanindustrial (97% match)
   - hundeggerna vs hundegger (90% match)
   - datamemorymarketing vs datamemorysales (71% match)
   - etc.

2. **Decide on 141 "new" accounts**
   - Are they genuinely new customers added after 01-07-2026?
   - Or were they filtered out as inactive in your existing dataset?
   - Check account status in your CRM/billing system

3. **Create merged dataset** (if valuable)
   - Script to join MWD enrichment fields to your existing 996 common accounts
   - Preserve both V2 clusters AND MWD research data
   - Output: `customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES_AND_MWD_RESEARCH.csv`

### Questions to Answer

1. **Data Source**: Where did MWD_Enriched_Accounts come from?
   - Different CRM system?
   - Different date range than 01-07-2026?
   - Manually curated subset?

2. **Coverage Strategy**: Should all active accounts get manual research?
   - MWD_Enriched only covers 1,204 accounts (8.5% of your total, 110% of active)
   - Cost/benefit of extending research to remaining accounts?

3. **Classification Standard**: Which system should be primary?
   - Keep V2 automated clusters for consistency?
   - Or adopt MWD manual research as new standard?
   - Or maintain both in parallel?

---

## Conclusion

The MWD_Enriched_Accounts dataset provides **highly valuable qualitative enrichment** for 996 of your accounts (90.8% of active accounts). The manual research fields - especially **Industry (Research)**, **Workflow Type**, and **Company Description** - add context that your quantitative analysis lacks.

**Primary Recommendation**: Merge the enrichment fields into your existing dataset for the 996 common accounts. This combines the best of both worlds:
- Your comprehensive coverage and quantitative metrics
- MWD's specific industry insights and workflow context

**Secondary Recommendation**: Investigate the ~141 genuinely new accounts to determine if they should be added to your primary dataset.

**Do NOT**: Replace your existing V2 classification system. The MWD research is complementary, not a replacement. Your V2 clusters are consistent, automated, and cover all accounts. The MWD research adds valuable detail for specific accounts but shouldn't replace your systematic approach.
