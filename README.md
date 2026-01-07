# CRM Industry Cluster Analysis

**Date**: January 7, 2026  
**Project**: Industry vertical analysis for product roadmap prioritization

## Project Structure

```
MWD_V1/
├── customermethodaccount_01-07-2026_11_10_09_am.csv                        # Original source data
├── customer_product_offerings_with_type.csv                                # Product sales data (top 50 SKUs/account)
├── customermethodaccount_01-07-2026_RECLUSTERED_V2.csv                     # V2 corrected cluster data
├── customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv  # ✅ USE THIS - Complete integrated dataset
├── product_type_analysis_results.csv                                       # Product type classification results
├── recluster_analysis.py                                                   # Re-clustering script
├── analyze_product_types.py                                                # Product type classification script
├── 01_HANDOFF_PACKAGE_README.md                                            # ✅ START HERE - Navigation guide
├── README.md                                                               # This file
└── analysis/                                                               # Analysis documentation
    ├── 02_FINAL_ANALYSIS_SUMMARY_2026-01-07.md                          # Complete analysis summary
    ├── 03_RE-CLUSTERING_CRITICAL_FINDINGS_2026-01-07.md                 # Critical bug discoveries
    ├── 04_CLUSTER_DEFINITIONS_LOGISTICS_VS_WHOLESALE.md                 # Logistics vs Wholesale definitions
    ├── 06_METHODOLOGY_SUMMARY.md                                        # Concise methodology overview
    ├── 05_METHODOLOGY_DETAILED_2026-01-07.md                            # Complete methodology (detailed)
    ├── 07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md                    # General W/D sub-clustering validation
    └── 08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md                       # Product type analysis findings
```

## Key Files

### Data Files
- **`data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv`** - ✅ **USE THIS** - Complete integrated dataset
  - Contains all V2 cluster data PLUS product type classification
  - 14,218 total accounts (1,096 active, 997 with product data)
  - Includes 91% of active accounts with product type classification
  - All original columns + product type metrics (see below)

- **`data/customermethodaccount_01-07-2026_RECLUSTERED_V2.csv`** - V2 corrected cluster data (without product types)
  - Contains corrected industry clusters with strict keyword matching
  - 14,218 total accounts (1,096 active)
  - Columns: `Industry_Cluster_Enhanced_V2`, `Business_Type_V2`, `Company_Size_V2`, `MRR_Calculated`

- **`customer_product_offerings_with_type.csv`** - Product sales data
  - 45,010 product records from 997 unique accounts
  - **Limitation**: Only top 50 sold items per account (data export limit)
  - Columns: Item, ItemType (Service/Inventory/NonInventory), Count, Account

- **`product_type_analysis_results.csv`** - Product type classification results
  - 997 accounts analyzed (91% coverage of active accounts)
  - Detailed product catalog metrics and business type classification
  - See [08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md](analysis/08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md) for methodology

- **`customermethodaccount_01-07-2026_11_10_09_am.csv`** - Original source data
  - Raw data before clustering (reference only)

### Analysis Scripts
- **`recluster_analysis.py`** - V2 re-clustering script
  - Applies strict industry categorization with word-boundary safe keywords
  - Calculates MRR, classifies B2B/B2C, and company size
  - Run from project root: `python recluster_analysis.py`

- **`analyze_product_types.py`** - Product type classification script
  - Analyzes actual sold items to determine what customers sell
  - Classifies into 5 business types based on ItemType mix
  - Calculates product catalog complexity metrics
  - Run from project root: `python analyze_product_types.py`

- **`validate_general_wd_subclusters.py`** - General W/D validation script
  - Evidence-based validation of proposed sub-clustering
  - Discovered 98% error rate in keyword-based approach
  - See [07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md](analysis/07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md)

### Documentation (Read in numbered order)
- **`01_HANDOFF_PACKAGE_README.md`** - **START HERE** - Navigation guide for all deliverables
- **`analysis/02_FINAL_ANALYSIS_SUMMARY_2026-01-07.md`** - Complete analysis summary with corrected V2 data
- **`analysis/03_RE-CLUSTERING_CRITICAL_FINDINGS_2026-01-07.md`** - Critical bug discoveries and impact analysis
- **`analysis/04_CLUSTER_DEFINITIONS_LOGISTICS_VS_WHOLESALE.md`** - Explains Logistics vs Wholesale business models
- **`analysis/06_METHODOLOGY_SUMMARY.md`** - Concise methodology overview (recommended)
- **`analysis/05_METHODOLOGY_DETAILED_2026-01-07.md`** - Complete methodology documentation (detailed reference)
- **`analysis/07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md`** - General W/D sub-clustering validation (98% error rate discovered)
- **`analysis/08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md`** - **NEW** Product type analysis findings

## Quick Start

1. **Read the handoff package guide first**: [01_HANDOFF_PACKAGE_README.md](01_HANDOFF_PACKAGE_README.md)
2. **Then read these documents in numbered order**:
   - [02_FINAL_ANALYSIS_SUMMARY_2026-01-07.md](analysis/02_FINAL_ANALYSIS_SUMMARY_2026-01-07.md) (30 min read)
   - [03_RE-CLUSTERING_CRITICAL_FINDINGS_2026-01-07.md](analysis/03_RE-CLUSTERING_CRITICAL_FINDINGS_2026-01-07.md) (15 min read)
   - [04_CLUSTER_DEFINITIONS_LOGISTICS_VS_WHOLESALE.md](analysis/04_CLUSTER_DEFINITIONS_LOGISTICS_VS_WHOLESALE.md) (10 min read)
   - [06_METHODOLOGY_SUMMARY.md](analysis/06_METHODOLOGY_SUMMARY.md) (10 min read, recommended)
   - [07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md](analysis/07_GENERAL_WD_VALIDATION_CRITICAL_FINDINGS.md) (10 min read)
   - [08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md](analysis/08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md) (20 min read) **← NEW**
   - [05_METHODOLOGY_DETAILED_2026-01-07.md](analysis/05_METHODOLOGY_DETAILED_2026-01-07.md) (optional, detailed reference)
3. **Use the complete integrated data file**: `data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv`
4. **Re-run analyses if needed**:
   - Industry clustering: `python recluster_analysis.py`
   - Product type classification: `python analyze_product_types.py`

## Product Type Classification Columns (NEW)

The integrated dataset includes these new columns from product type analysis:

**Product Catalog Metrics:**
- `SKU_Count` - Number of unique products sold (limited to top 50)
- `Avg_Delimiter_Count` - Average category depth in product names (colons/slashes)
- `Avg_Char_Length` - Average product name length in characters
- `Avg_Word_Count` - Average words per product name
- `Pct_With_SKU_Codes` - % of products with systematic SKU codes
- `Pct_With_Specs` - % of products with specifications (oz, lb, kg, etc.)
- `Pct_With_Brand_Prefix` - % of products with brand/vendor prefixes

**ItemType Distribution:**
- `Pct_Service_Items` - % of sold items that are services
- `Pct_Inventory_Items` - % of sold items that are physical inventory
- `Pct_NonInventory_Items` - % of sold items that are non-inventory (digital, consumables)
- `Pct_Fee_Items` - % of sold items that are fees/charges

**Business Type Classification:**
- `Primary_Business_Type` - 5 categories based on ItemType mix:
  - **Inventory-Based (Physical Products)** - 33.8% (337 accounts)
  - **NonInventory-Based (Digital/Services)** - 25.4% (253 accounts)
  - **Product-Based (Mixed Inventory)** - 20.0% (199 accounts)
  - **Service-Based** - 13.2% (132 accounts)
  - **Hybrid (Mixed)** - 7.6% (76 accounts)

**Complexity Scores:**
- `Catalog_Complexity_Score` - Composite score 0-100 (SKU count + naming sophistication)
- `Complexity_Tier` - Ultra-Simple / Simple / Standard / Complex / Very Complex
- `SKU_Tier` - 1-5 / 6-20 / 21-50 / 51-100 / etc.

**Examples:**
- `Sample_Products` - Top 3-5 sold items (for manual review)

## Key Findings from Product Type Analysis

1. **Product complexity does NOT correlate with workflow complexity**
   - SKU Count vs Users: 0.120 correlation
   - Catalog Complexity vs Users: -0.000 correlation
   - Having 500 SKUs doesn't mean more users or higher MRR

2. **Business type DOES influence workflows**
   - Hybrid accounts: 5.9 avg users, $167 MRR (need both inventory + service features)
   - Product-Based: 5.8 avg users, $155 MRR (complex catalogs)
   - Service-Based: 4.0 avg users, $136 MRR (time tracking, billing)

3. **Segmentation recommendation**
   - ✅ USE: `Primary_Business_Type` (5 categories based on what they sell)
   - ❌ DO NOT USE: SKU count or catalog complexity alone
   - ✅ COMBINE: Product type + User count + Industry cluster + B2B/B2C

See [08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md](analysis/08_PRODUCT_TYPE_CLASSIFICATION_FINDINGS.md) for full analysis.

## Notes

- The V1 enhanced file (`customermethodaccount_01-07-2026_ENHANCED_WITH_CLUSTERS.csv`) was removed as it contained incorrect classifications (89% mis-classification in Food & Beverage cluster)
- Product data limited to top 50 sold items per account (91% of accounts have exactly 50 SKUs due to export limit)
- 91% coverage: 997 out of 1,096 active accounts have product type classification
- All analysis should use the V2 re-clustered file with product types
