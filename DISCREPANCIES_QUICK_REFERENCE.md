# Dataset Comparison - Quick Reference Guide

## Overview
- **Research Accounts:** 589
- **Enriched Accounts:** 1,204
- **Match Rate:** 100% (all research accounts found)
- **Total Discrepancies:** 4,277

---

## The Big Picture: What's Wrong?

### 🚨 Critical Issue
**NONE of the research classifications have been integrated into the enriched dataset.**

All 589 accounts show `"PENDING RESEARCH"` in the enriched file's `Industry (Research)` field, despite having complete classifications in the research file.

---

## Discrepancy Summary

| Issue | Count | % | Severity | Action Required |
|-------|-------|---|----------|-----------------|
| Research not integrated | 589 | 100% | 🔴 CRITICAL | Update enriched dataset NOW |
| Sub-industry missing | 589 | 100% | 🔴 CRITICAL | Add field to enriched dataset |
| Industry mismatch | 586 | 99.5% | 🟡 HIGH | Map research → MWD categories |
| Workflow pattern diff | 589 | 100% | 🟡 HIGH | Reconcile definitions |
| Classification source missing | 589 | 100% | 🟠 MEDIUM | Add metadata field |
| Confidence missing | 437 | 74% | 🟠 MEDIUM | Add metadata field |
| Event counts missing | 589 | 100% | 🟢 LOW | Add metadata field |
| QBO/Sector diff | 309 | 52% | 🟢 LOW | Validate and update |

---

## What's Missing from Enriched Dataset?

### 1. Research Classifications (ALL 589 accounts)
```
Research File Has:          Enriched File Has:
- Food & Beverage          → PENDING RESEARCH
- Consumer Goods           → PENDING RESEARCH
- Industrial               → PENDING RESEARCH
- Healthcare & Medical     → PENDING RESEARCH
```

### 2. Sub-Industry Detail (ALL 589 accounts)
```
Research File Has:              Enriched File Has:
- Craft Beverages (Kombucha)   → (field doesn't exist)
- Industrial Hose              → (field doesn't exist)
- Powder Coating Services      → (field doesn't exist)
- Coffee Roasting              → (field doesn't exist)
```

### 3. Classification Metadata (ALL 589 accounts)
```
Research File Has:          Enriched File Has:
- Source: manual_verification  → (field doesn't exist)
- Confidence: high             → (field doesn't exist)
- Total Events: 2752           → (field doesn't exist)
```

---

## Classification Source Breakdown (Research Only)

| Source | Count | Confidence |
|--------|-------|-----------|
| `llm_classification` | 393 | medium |
| `manual_verification` | 144 | high/medium |
| `unclassified` | 52 | N/A |

**Note:** These 144 manually verified accounts are the highest quality - prioritize integrating these first.

---

## Industry Mapping Issues

### Research Industries → MWD Verticals

The research file uses **specific industries**, enriched uses **broad MWD categories**:

| Research Category | Count | MWD Vertical |
|-------------------|-------|--------------|
| Food & Beverage | 120+ | → Manufacturing / Wholesale / Retail |
| Consumer Goods | 80+ | → Manufacturing / Wholesale / Retail |
| Industrial | 60+ | → Manufacturing / Wholesale |
| Construction & Building | 70+ | → Manufacturing / Retail |
| Healthcare & Medical | 25+ | → Wholesale |

**Problem:** 586 accounts show industry vs vertical mismatch

---

## Unresearched Accounts

**615 accounts in enriched dataset have NO research classification**

These need to be prioritized and classified using the same methodology.

---

## Top Priority Actions

### 1. Immediate (This Week)
- [ ] Update enriched dataset with research industry classifications
- [ ] Replace all "PENDING RESEARCH" entries
- [ ] Add `sub_industry` column to enriched dataset
- [ ] Import sub_industry values from research

### 2. Short Term (This Month)
- [ ] Add classification metadata columns:
  - `classification_source`
  - `classification_confidence`
  - `total_events`
- [ ] Create industry mapping document (research ↔ MWD)
- [ ] Reconcile workflow pattern definitions
- [ ] Validate QBO industry vs Sector mismatches

### 3. Medium Term (Next Quarter)
- [ ] Classify remaining 615 unresearched accounts
- [ ] Prioritize by revenue/value
- [ ] Update enriched dataset with new classifications
- [ ] Implement ongoing classification process

---

## Sample Discrepancies

### Example 1: deansbeansorganiccoffee4
```
Research:
- Industry: Food & Beverage
- Sub-Industry: Coffee Roasting
- Workflow: crm_pipeline
- Events: 18
- Source: manual_verification
- Confidence: high
- Website: deansbeans.com

Enriched:
- Vertical: Wholesale and distribution services (MWD)
- Industry (Research): PENDING RESEARCH
- Sub-Industry: (doesn't exist)
- Workflow Type: (may differ)
- Events: (doesn't exist)
- Source: (doesn't exist)
- Confidence: (doesn't exist)
```

### Example 2: moderncompressorsales
```
Research:
- Industry: Industrial
- Sub-Industry: Compressor Equipment
- Workflow: quote_driven
- Events: 2752 (highest activity!)
- Source: manual_verification
- Confidence: high

Enriched:
- Vertical: Manufacturing (MWD)
- Industry (Research): PENDING RESEARCH
- (all metadata missing)
```

### Example 3: helenarosejewelry
```
Research:
- Industry: Consumer Goods
- Sub-Industry: Jewelry
- Workflow: quote_driven
- Events: 422
- Source: manual_verification
- Confidence: high
- Annual Sales: $2,949,164

Enriched:
- Vertical: Wholesale and distribution services (MWD)
- Industry (Research): PENDING RESEARCH
- (all metadata missing)
```

---

## Files Generated

All detailed analysis available in: `results/dataset_comparison/`

### Key Files:
1. `all_discrepancies.csv` - All 4,277 discrepancies
2. `discrepancies_by_account.csv` - Summary per account
3. `discrepancies_industry_vs_industry_research.csv` - 589 pending items
4. `discrepancies_sub_industry.csv` - 589 missing classifications
5. `accounts_only_in_enriched.csv` - 615 unresearched accounts

---

## Questions to Answer

1. **Why wasn't research data integrated?**
   - Was this intentional?
   - Is there a process issue?

2. **Which classification is authoritative?**
   - Research industries (specific)?
   - MWD verticals (broad)?
   - Both (need mapping)?

3. **What about the 615 unresearched accounts?**
   - What's the plan to classify them?
   - Who owns this work?
   - What's the timeline?

4. **Data governance:**
   - Who updates the enriched dataset?
   - How often?
   - What's the approval process?

---

## Bottom Line

**The research work exists but hasn't been integrated.** The enriched dataset is waiting for this data (shown by "PENDING RESEARCH" placeholders). The immediate priority is merging these two datasets to create a single source of truth with both:
- Detailed research classifications (from research file)
- Comprehensive business metrics (from enriched file)

**Estimated impact:** Once integrated, 589 accounts (49% of customer base) will have high-quality, granular industry classifications instead of broad MWD categories.

---

**Last Updated:** January 8, 2026
