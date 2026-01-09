# Dataset Comparison Executive Summary
## classification_research.csv vs MWD_Enriched_Accounts.csv

**Report Date:** January 8, 2026
**Analysis Type:** Comprehensive Field-by-Field Comparison
**Total Discrepancies Found:** 4,277

---

## 🎯 Key Finding

**THE RESEARCH DATA HAS NOT BEEN INTEGRATED INTO THE ENRICHED DATASET**

All 589 researched accounts show `"PENDING RESEARCH"` in the enriched file, despite having complete classifications in the research file.

---

## 📊 Numbers at a Glance

| Metric | Value |
|--------|-------|
| Research accounts analyzed | 589 |
| Enriched accounts total | 1,204 |
| Accounts matched (overlap) | 589 (100%) |
| Unresearched accounts | 615 (51%) |
| Total discrepancies | 4,277 |

---

## 🔍 Discrepancy Breakdown

### Critical Issues (100% of accounts affected)

| Issue | Count | Impact |
|-------|-------|--------|
| **Research not integrated** | 589 | All research showing "PENDING RESEARCH" in enriched |
| **Sub-industry missing** | 589 | Detailed classifications lost |
| **Industry vs Vertical mismatch** | 586 | Classification inconsistency |
| **Workflow pattern differences** | 589 | Business process mismatch |
| **Classification source missing** | 589 | No methodology tracking |
| **Event counts missing** | 589 | No activity metrics |

### Medium Priority Issues

| Issue | Count | Impact |
|-------|-------|--------|
| **Confidence level missing** | 437 | No quality scoring |
| **QBO industry mismatch** | 309 | Data inconsistency |

---

## 💎 Data Quality Analysis

### Research File Classifications

**Total Accounts:** 589

| Classification Source | Count | Quality |
|----------------------|-------|---------|
| **Manual Verification** | 135 | ⭐⭐⭐ HIGHEST |
| **LLM Classification** | 302 | ⭐⭐ MEDIUM |
| **Unclassified** | 152 | ⭐ NEEDS WORK |

**Confidence Distribution:**
- High confidence: 105 accounts (manually verified)
- Medium confidence: 327 accounts (LLM classified)
- Low confidence: 5 accounts (manual, but uncertain)
- No confidence: 152 accounts (unclassified)

---

## 🏭 Industry Classification Patterns

### Research Industries (Top 10)

| Industry | Count | % |
|----------|-------|---|
| Other (unclassified) | 152 | 25.8% |
| Food & Beverage | 104 | 17.7% |
| Consumer Goods | 70 | 11.9% |
| Construction & Building | 66 | 11.2% |
| Industrial | 44 | 7.5% |
| Healthcare & Medical | 32 | 5.4% |
| Manufacturing | 26 | 4.4% |
| Technology | 21 | 3.6% |
| Services | 18 | 3.1% |
| Furniture | 16 | 2.7% |

### MWD Verticals (Enriched File)

| MWD Vertical | Count | % |
|--------------|-------|---|
| Manufacturing (MWD) | 246 | 42.0% |
| Wholesale and distribution services (MWD) | 246 | 42.0% |
| Retail | 94 | 16.0% |

**Issue:** Research uses specific categories (19 types), enriched uses 3 broad categories

---

## 🎨 Sub-Industry Granularity

**Accounts with detailed sub-industry:** 437 out of 589 (74%)

### Sample Sub-Industry Categories (178 unique types)

**Food & Beverage (19 types):**
- Craft Beverages (Kombucha)
- Coffee Roasting, Craft Beer, Wine
- Spirits, Meat Processing, Seafood
- Restaurant Supply, Food Distribution
- Tortilla Manufacturing, Cooking Oils

**Industrial (36 types):**
- Compressor Equipment, Industrial Hose
- Casters & Wheels, Abrasives, Filtration
- Ammunition Components, Thermal Management
- Power Tools/Drilling Equipment
- Sewer Cleaning Equipment

**Consumer Goods (21 types):**
- Jewelry, Promotional Products
- Apparel, Beauty/Personal Care
- Baby Products, Kitchen Appliances
- Religious Products, Adaptive Fashion
- Home Fragrance/Candles

**Construction & Building (22 types):**
- Doors & Windows, Flooring, HVAC
- Lumber, Concrete/Masonry
- Fencing/Decking, Roofing
- Plumbing, Insulation

**Healthcare & Medical (10 types):**
- Medical Equipment, Lab Equipment
- Medical Training Simulators
- Mobility Equipment, Privacy Systems
- Contract Manufacturing (cGMP)

---

## 🏆 High-Value Classifications

### Manual Verification (135 accounts - Priority 1)

Top manually verified industries:
1. Industrial - 32 accounts
2. Consumer Goods - 19 accounts
3. Construction & Building - 17 accounts
4. Food & Beverage - 14 accounts
5. Manufacturing - 11 accounts

**These are the HIGHEST QUALITY classifications and should be integrated first.**

### High Confidence (105 accounts)

All manually verified with high confidence scores:
- Industrial: 24 accounts
- Consumer Goods: 15 accounts
- Construction & Building: 14 accounts
- Food & Beverage: 13 accounts

**Examples:**
- `moderncompressorsales` - Industrial: Compressor Equipment (2,752 events!)
- `davishoseinc` - Industrial: Industrial Hose (1,996 events)
- `accesscasters3` - Industrial: Casters & Wheels (102 events)
- `fibercablesdirect` - Technology: Fiber Optics (230 events)

---

## ⚠️ Unclassified Accounts (152 - Need Attention)

These accounts are marked as "Other: Unclassified" in research:

**Sample unclassified accounts:**
- synova
- ssisanitary
- hyfloequipmentcompany3
- missionlaundryequipment3
- industrimax2
- concealite
- gsinks
- burnewiin2
- gorillahammers4
- acentel
- radsuramerica
- gothamlgt
- hendersonenterprises

**Action needed:** Manual classification required

---

## 📈 Activity Metrics (Research Only)

**Event Count Range:** 2 to 90,126 events per account

**Top 10 Most Active Accounts:**
1. `celluma` - 90,126 events
2. `holdit` - 57,216 events
3. `brownsafe` - 33,497 events
4. `fujimats` - 33,716 events
5. `rexdistributioninc` - 33,541 events
6. `procurementequipment` - 32,314 events
7. `multiseal2` - 30,177 events
8. `firestationfurniture` - 28,452 events
9. `dewesoft` - 26,707 events
10. `yoderbilt` - 25,905 events

**This activity data is NOT in the enriched dataset.**

---

## 🚨 Critical Data Gaps

### What's Missing from Enriched Dataset

1. **Research Classifications** (589 accounts)
   - All show "PENDING RESEARCH"
   - Should have specific industries

2. **Sub-Industry Detail** (437 detailed classifications)
   - 178 unique sub-industry types
   - Provides granular segmentation
   - Field doesn't exist in enriched

3. **Classification Metadata** (589 accounts)
   - Source (manual vs LLM)
   - Confidence level
   - Event counts
   - None of these fields exist

### What's Missing from Research File

**615 accounts in enriched have NO research classification**

These are 51% of the total customer base and need to be classified.

---

## 📋 Industry Mapping Challenge

### Cross-Tabulation: Research → MWD Verticals

| Research Industry | Manufacturing | Retail | Wholesale | Total |
|-------------------|--------------|--------|-----------|-------|
| Food & Beverage | 41 | 13 | 50 | 104 |
| Consumer Goods | 28 | 11 | 31 | 70 |
| Construction & Building | 32 | 14 | 20 | 66 |
| Industrial | 19 | 4 | 21 | 44 |
| Healthcare & Medical | 12 | 8 | 12 | 32 |
| Manufacturing | 17 | 0 | 9 | 26 |
| Technology | 10 | 2 | 9 | 21 |

**Problem:** The same research industry maps to multiple MWD verticals
- Need clear mapping rules
- Or choose one classification system as primary

---

## 🎯 Immediate Action Items

### Week 1: Data Integration
- [ ] Update enriched dataset's "Industry (Research)" field
- [ ] Replace all "PENDING RESEARCH" with actual values
- [ ] Add sub_industry column to enriched schema
- [ ] Import all 589 sub_industry values

### Week 2: Add Metadata
- [ ] Add classification_source column
- [ ] Add classification_confidence column
- [ ] Add total_events column
- [ ] Import metadata for all 589 accounts

### Week 3: Validation
- [ ] Validate QBO industry vs Sector (309 mismatches)
- [ ] Reconcile workflow pattern definitions
- [ ] Create industry mapping documentation

---

## 📊 Expected Outcomes

### After Integration

**Before:**
- 1,204 accounts with broad MWD verticals (3 categories)
- 589 showing "PENDING RESEARCH"
- No sub-industry detail
- No classification quality metrics

**After:**
- 589 accounts with specific industries (19 categories)
- 437 accounts with detailed sub-industries (178 types)
- Classification source and confidence for all
- Activity metrics (event counts)
- Clear data quality indicators

**Impact:**
- 49% of customer base gets high-quality classifications
- 74% of researched accounts get granular sub-industry detail
- 135 accounts have highest-quality manual verification
- Business can segment and target based on specific industries

---

## 💡 Recommendations

### Priority 1: Integrate Existing Research (1 week)
Merge the 589 researched accounts into enriched dataset. This is low-hanging fruit with high impact.

### Priority 2: Complete Unclassified (2-4 weeks)
Classify the 152 "Other/Unclassified" accounts in research file using same methodology.

### Priority 3: Research Remaining Accounts (1-2 months)
Classify the 615 accounts that are in enriched but not in research.

### Priority 4: Establish Process (ongoing)
- Who owns classifications?
- How often are they updated?
- What's the approval workflow?
- How are new accounts classified?

---

## 📂 Deliverables

All analysis files saved to: `results/dataset_comparison/`

### Main Reports
1. **COMPREHENSIVE_DATASET_COMPARISON_REPORT.md** - Full detailed analysis
2. **DISCREPANCIES_QUICK_REFERENCE.md** - Quick reference guide
3. **DATASET_COMPARISON_EXECUTIVE_SUMMARY.md** - This document

### Data Files
1. `all_discrepancies.csv` - All 4,277 discrepancies
2. `discrepancies_by_account.csv` - Summary per account
3. `accounts_only_in_enriched.csv` - 615 unresearched accounts
4. `industry_mapping_analysis.csv` - Cross-tabulation of classifications
5. `high_priority_manual_verified.csv` - 135 highest quality accounts
6. `high_confidence_classifications.csv` - 105 high-confidence accounts
7. `unclassified_need_review.csv` - 152 accounts needing classification

### Detailed Discrepancy Files (by type)
- `discrepancies_industry_vs_vertical.csv` - 586 records
- `discrepancies_industry_vs_industry_research.csv` - 589 records
- `discrepancies_sub_industry.csv` - 589 records
- `discrepancies_workflow_pattern.csv` - 589 records
- `discrepancies_qbo_industry_vs_sector.csv` - 309 records
- `discrepancies_total_events.csv` - 589 records
- `discrepancies_classification_source.csv` - 589 records
- `discrepancies_confidence.csv` - 437 records

---

## ✅ Validation

### Data Quality Checks Performed
- ✅ 100% account name matching (589/589 found)
- ✅ Null and empty value handling
- ✅ Numeric value normalization
- ✅ Case-insensitive text comparison
- ✅ Cross-validation of all field mappings
- ✅ Bidirectional comparison (research ↔ enriched)

### Coverage Analysis
- ✅ Research covers 49% of customer base (589/1,204)
- ✅ 74% of research accounts have sub-industries (437/589)
- ✅ 23% have manual verification (135/589)
- ✅ 74% have confidence scores (437/589)
- ✅ 100% have event counts in research

---

## 🎬 Next Steps

1. **Review this analysis** with stakeholders
2. **Decide on classification system** (research vs MWD vs both)
3. **Approve integration plan** and timeline
4. **Execute data merge** (weeks 1-2)
5. **Classify remaining accounts** (weeks 3-8)
6. **Establish ongoing process** (month 3+)

---

**Questions? See the detailed reports or contact the analysis team.**

---

**Report generated:** January 8, 2026
**Analyst:** Claude Code Analysis
**Data sources:**
- `data/classification_research.csv` (589 records)
- `data/MWD_Enriched_Accounts.csv` (1,204 records)
