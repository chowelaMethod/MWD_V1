#!/usr/bin/env python3
"""
Compare MWD_Enriched_Accounts with existing integrated dataset
Identifies discrepancies in account data, coverage, and enrichment fields
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_datasets():
    """Load both datasets"""
    print("Loading datasets...")

    # Load MWD_Enriched_Accounts (new external data)
    mwd_path = Path('data/MWD_Enriched_Accounts.csv')
    mwd_df = pd.read_csv(mwd_path)
    print(f"✓ MWD_Enriched_Accounts: {len(mwd_df):,} rows, {len(mwd_df.columns)} columns")

    # Load existing integrated dataset
    existing_path = Path('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')
    existing_df = pd.read_csv(existing_path)
    print(f"✓ Existing dataset: {len(existing_df):,} rows, {len(existing_df.columns)} columns")

    return mwd_df, existing_df

def compare_account_coverage(mwd_df, existing_df):
    """Compare which accounts are in each dataset"""
    print("\n" + "="*80)
    print("ACCOUNT COVERAGE COMPARISON")
    print("="*80)

    # Normalize account names for matching
    mwd_accounts = set(mwd_df['Account Name'].str.lower().str.strip())
    existing_accounts = set(existing_df['Account'].str.lower().str.strip())

    # Find differences
    only_in_mwd = mwd_accounts - existing_accounts
    only_in_existing = existing_accounts - mwd_accounts
    in_both = mwd_accounts & existing_accounts

    print(f"\n📊 Account Coverage:")
    print(f"   Accounts in MWD_Enriched_Accounts: {len(mwd_accounts):,}")
    print(f"   Accounts in Existing Dataset: {len(existing_accounts):,}")
    print(f"   Accounts in BOTH datasets: {len(in_both):,}")
    print(f"   ONLY in MWD_Enriched: {len(only_in_mwd):,}")
    print(f"   ONLY in Existing: {len(only_in_existing):,}")

    if len(only_in_mwd) > 0:
        print(f"\n⚠️  {len(only_in_mwd)} accounts in MWD_Enriched but NOT in existing data:")
        for i, acct in enumerate(sorted(only_in_mwd)[:10], 1):
            print(f"   {i}. {acct}")
        if len(only_in_mwd) > 10:
            print(f"   ... and {len(only_in_mwd) - 10} more")

    return in_both, only_in_mwd, only_in_existing

def compare_column_structure(mwd_df, existing_df):
    """Compare column structures between datasets"""
    print("\n" + "="*80)
    print("COLUMN STRUCTURE COMPARISON")
    print("="*80)

    mwd_cols = set(mwd_df.columns)
    existing_cols = set(existing_df.columns)

    # New columns in MWD that we don't have
    new_enrichment_cols = mwd_cols - existing_cols

    # Columns we have that MWD doesn't
    our_unique_cols = existing_cols - mwd_cols

    print(f"\n📋 Column Analysis:")
    print(f"   MWD_Enriched_Accounts columns: {len(mwd_cols)}")
    print(f"   Existing dataset columns: {len(existing_cols)}")

    if new_enrichment_cols:
        print(f"\n✨ NEW ENRICHMENT FIELDS in MWD_Enriched ({len(new_enrichment_cols)}):")
        for col in sorted(new_enrichment_cols):
            non_null = mwd_df[col].notna().sum()
            pct = (non_null / len(mwd_df)) * 100
            print(f"   • {col}: {non_null:,} populated ({pct:.1f}%)")

    if our_unique_cols:
        print(f"\n🔧 COLUMNS ONLY IN EXISTING DATASET ({len(our_unique_cols)}):")
        for col in sorted(our_unique_cols)[:20]:
            print(f"   • {col}")
        if len(our_unique_cols) > 20:
            print(f"   ... and {len(our_unique_cols) - 20} more")

def compare_field_values(mwd_df, existing_df, common_accounts):
    """Compare field values for accounts that exist in both datasets"""
    print("\n" + "="*80)
    print("FIELD VALUE DISCREPANCIES")
    print("="*80)

    if len(common_accounts) == 0:
        print("\n⚠️  No common accounts found - cannot compare field values")
        return

    print(f"\nComparing {len(common_accounts):,} common accounts...")

    # Create normalized lookup
    mwd_lookup = mwd_df.set_index(mwd_df['Account Name'].str.lower().str.strip())
    existing_lookup = existing_df.set_index(existing_df['Account'].str.lower().str.strip())

    # Find common columns to compare
    mwd_cols = set(mwd_df.columns)
    existing_cols = set(existing_df.columns)

    # Map MWD columns to existing columns (accounting for naming differences)
    column_mapping = {
        'Account Name': 'Account',
        'Company Name in QB': 'CompanyName',
        'Users': 'Users',
        'Employees': 'Employees',
        'Website': 'Website',
        'Vertical': 'Industry_Cluster_Enhanced_V2',  # May differ
        'Sector': 'Industry_Cluster_Enhanced_V2',    # May differ
    }

    discrepancies = []

    for mwd_col, existing_col in column_mapping.items():
        if mwd_col not in mwd_cols or existing_col not in existing_cols:
            continue

        print(f"\n🔍 Comparing: {mwd_col} (MWD) vs {existing_col} (Existing)")

        mismatches = 0
        examples = []

        for acct in list(common_accounts)[:100]:  # Sample first 100 for performance
            if acct not in mwd_lookup.index or acct not in existing_lookup.index:
                continue

            mwd_val = mwd_lookup.loc[acct, mwd_col]
            existing_val = existing_lookup.loc[acct, existing_col]

            # Normalize for comparison
            mwd_val_str = str(mwd_val).strip().lower() if pd.notna(mwd_val) else ''
            existing_val_str = str(existing_val).strip().lower() if pd.notna(existing_val) else ''

            if mwd_val_str != existing_val_str:
                mismatches += 1
                if len(examples) < 5:
                    examples.append({
                        'account': acct,
                        'mwd': mwd_val,
                        'existing': existing_val
                    })

        if mismatches > 0:
            print(f"   ⚠️  {mismatches} mismatches found (in sample of 100)")
            for ex in examples:
                print(f"      • {ex['account'][:40]}")
                print(f"        MWD: '{ex['mwd']}'")
                print(f"        Existing: '{ex['existing']}'")
            discrepancies.append({
                'field': f"{mwd_col} vs {existing_col}",
                'mismatches': mismatches
            })

def analyze_enrichment_quality(mwd_df):
    """Analyze the quality and completeness of enrichment data"""
    print("\n" + "="*80)
    print("MWD ENRICHMENT DATA QUALITY")
    print("="*80)

    # Key enrichment fields to analyze
    enrichment_fields = [
        'Industry (Research)',
        'Workflow Type',
        'Company Description',
        'Product Types',
        'Product Complexity',
        'Website',
        'Annual Sales',
        'Vertical',
        'Sector'
    ]

    print("\n📈 Data Completeness:")
    for field in enrichment_fields:
        if field in mwd_df.columns:
            non_null = mwd_df[field].notna().sum()
            pct = (non_null / len(mwd_df)) * 100
            print(f"   • {field}: {non_null:,}/{len(mwd_df):,} ({pct:.1f}%)")

            # Show sample values
            if non_null > 0:
                sample = mwd_df[mwd_df[field].notna()][field].head(3).tolist()
                print(f"     Samples: {sample}")

def compare_industry_classifications(mwd_df, existing_df, common_accounts):
    """Compare industry/vertical classifications between datasets"""
    print("\n" + "="*80)
    print("INDUSTRY CLASSIFICATION COMPARISON")
    print("="*80)

    if len(common_accounts) == 0:
        print("\n⚠️  No common accounts to compare")
        return

    # Create lookups
    mwd_lookup = mwd_df.set_index(mwd_df['Account Name'].str.lower().str.strip())
    existing_lookup = existing_df.set_index(existing_df['Account'].str.lower().str.strip())

    # Compare classifications
    print("\n🏷️  Comparing Industry Classifications:")
    print("\nMWD fields:")
    print("  • Vertical")
    print("  • Sector")
    print("  • Industry (Research)")
    print("\nExisting fields:")
    print("  • Industry_Cluster_Enhanced_V2")
    print("  • Business_Type_V2")

    # Sample comparison
    print("\n📋 Sample Classification Comparison (first 10 common accounts):")

    count = 0
    for acct in sorted(common_accounts):
        if count >= 10:
            break
        if acct not in mwd_lookup.index or acct not in existing_lookup.index:
            continue

        count += 1
        print(f"\n{count}. {acct[:50]}")

        # MWD classifications
        if 'Vertical' in mwd_df.columns:
            print(f"   MWD Vertical: {mwd_lookup.loc[acct, 'Vertical']}")
        if 'Sector' in mwd_df.columns:
            print(f"   MWD Sector: {mwd_lookup.loc[acct, 'Sector']}")
        if 'Industry (Research)' in mwd_df.columns:
            print(f"   MWD Industry: {mwd_lookup.loc[acct, 'Industry (Research)']}")

        # Existing classifications
        if 'Industry_Cluster_Enhanced_V2' in existing_df.columns:
            print(f"   Existing Cluster: {existing_lookup.loc[acct, 'Industry_Cluster_Enhanced_V2']}")
        if 'Business_Type_V2' in existing_df.columns:
            print(f"   Existing Business Type: {existing_lookup.loc[acct, 'Business_Type_V2']}")

def main():
    """Main comparison analysis"""
    print("\n" + "="*80)
    print("MWD_ENRICHED_ACCOUNTS vs EXISTING DATASET COMPARISON")
    print("="*80)

    # Load datasets
    mwd_df, existing_df = load_datasets()

    # 1. Compare account coverage
    common_accounts, only_mwd, only_existing = compare_account_coverage(mwd_df, existing_df)

    # 2. Compare column structures
    compare_column_structure(mwd_df, existing_df)

    # 3. Analyze enrichment data quality
    analyze_enrichment_quality(mwd_df)

    # 4. Compare field values for common accounts
    compare_field_values(mwd_df, existing_df, common_accounts)

    # 5. Compare industry classifications
    compare_industry_classifications(mwd_df, existing_df, common_accounts)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n✅ Analysis complete!")
    print(f"\n📊 Key Findings:")
    print(f"   • MWD_Enriched has {len(mwd_df):,} accounts")
    print(f"   • Existing dataset has {len(existing_df):,} accounts")
    print(f"   • {len(common_accounts):,} accounts in both")
    print(f"   • {len(only_mwd):,} unique to MWD_Enriched")
    print(f"   • {len(only_existing):,} unique to Existing")

    print("\n📋 Next Steps:")
    print("   1. Review enrichment fields in MWD_Enriched for potential integration")
    print("   2. Investigate discrepancies in common accounts")
    print("   3. Decide which classification system to use (MWD vs V2)")
    print("   4. Determine if MWD accounts not in existing should be added")

if __name__ == '__main__':
    main()
