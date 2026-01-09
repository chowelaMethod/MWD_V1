#!/usr/bin/env python3
"""
Comprehensive comparison between classification_research.csv and MWD_Enriched_Accounts.csv
This script identifies ALL discrepancies between the two datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File paths
RESEARCH_FILE = "data/classification_research.csv"
ENRICHED_FILE = "data/MWD_Enriched_Accounts.csv"
OUTPUT_DIR = Path("results/dataset_comparison")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def normalize_account_name(name):
    """Normalize account names for comparison"""
    if pd.isna(name):
        return None
    return str(name).lower().strip()

def load_datasets():
    """Load both datasets"""
    print("Loading datasets...")

    # Load research data
    research_df = pd.read_csv(RESEARCH_FILE)
    print(f"Research file: {len(research_df)} records")
    print(f"Research columns: {list(research_df.columns)}")

    # Load enriched data
    enriched_df = pd.read_csv(ENRICHED_FILE)
    print(f"Enriched file: {len(enriched_df)} records")
    print(f"Enriched columns: {list(enriched_df.columns)}")

    return research_df, enriched_df

def normalize_for_comparison(value):
    """Normalize values for comparison"""
    if pd.isna(value) or value == '' or value == 0 or value == '0':
        return None
    return str(value).strip()

def compare_field(research_val, enriched_val, field_name):
    """Compare two field values and return discrepancy info"""
    research_norm = normalize_for_comparison(research_val)
    enriched_norm = normalize_for_comparison(enriched_val)

    if research_norm == enriched_norm:
        return None

    return {
        'field': field_name,
        'research_value': research_val,
        'enriched_value': enriched_val,
        'research_normalized': research_norm,
        'enriched_normalized': enriched_norm
    }

def main():
    # Load data
    research_df, enriched_df = load_datasets()

    # Normalize account names for matching
    research_df['account_normalized'] = research_df['account'].apply(normalize_account_name)
    enriched_df['account_normalized'] = enriched_df['Account Name'].apply(normalize_account_name)

    # Create lookup dictionary for enriched data
    enriched_lookup = enriched_df.set_index('account_normalized').to_dict('index')

    print(f"\n{'='*80}")
    print("STARTING COMPREHENSIVE COMPARISON")
    print(f"{'='*80}\n")

    # Field mappings between datasets
    field_mappings = {
        'industry': ('Industry (Research)', 'Vertical'),
        'sub_industry': ('Industry (Research)', None),  # No direct equivalent
        'workflow_pattern': ('Workflow Type', None),
        'total_events': (None, None),  # Not in enriched
        'classification_source': (None, None),  # Not in enriched
        'confidence': (None, None),  # Not in enriched
        'website': ('Website', 'Website'),
        'annual_sales': ('Annual Sales', 'Annual Sales'),
        'qbo_industry': (None, 'Sector')
    }

    all_discrepancies = []
    accounts_not_in_enriched = []
    accounts_matched = []

    # Process each research record
    for idx, research_row in research_df.iterrows():
        account_name = research_row['account']
        account_norm = research_row['account_normalized']

        if account_norm not in enriched_lookup:
            accounts_not_in_enriched.append({
                'account': account_name,
                'industry': research_row.get('industry'),
                'sub_industry': research_row.get('sub_industry'),
                'website': research_row.get('website'),
                'annual_sales': research_row.get('annual_sales'),
                'total_events': research_row.get('total_events'),
                'classification_source': research_row.get('classification_source'),
                'confidence': research_row.get('confidence')
            })
            continue

        enriched_row = enriched_lookup[account_norm]
        accounts_matched.append(account_name)

        # Compare each field
        discrepancies = []

        # Industry comparison
        research_industry = research_row.get('industry')
        enriched_vertical = enriched_row.get('Vertical')
        enriched_industry_research = enriched_row.get('Industry (Research)')

        disc = compare_field(research_industry, enriched_vertical, 'industry_vs_vertical')
        if disc:
            disc['account'] = account_name
            disc['enriched_industry_research'] = enriched_industry_research
            discrepancies.append(disc)

        disc = compare_field(research_industry, enriched_industry_research, 'industry_vs_industry_research')
        if disc:
            disc['account'] = account_name
            disc['enriched_vertical'] = enriched_vertical
            discrepancies.append(disc)

        # Sub-industry (only in research)
        sub_industry = research_row.get('sub_industry')
        if normalize_for_comparison(sub_industry):
            discrepancies.append({
                'account': account_name,
                'field': 'sub_industry',
                'research_value': sub_industry,
                'enriched_value': 'NOT_IN_ENRICHED',
                'note': 'Sub-industry detail exists in research but not tracked in enriched'
            })

        # Workflow pattern
        research_workflow = research_row.get('workflow_pattern')
        enriched_workflow = enriched_row.get('Workflow Type')
        disc = compare_field(research_workflow, enriched_workflow, 'workflow_pattern')
        if disc:
            disc['account'] = account_name
            discrepancies.append(disc)

        # Website
        research_website = research_row.get('website')
        enriched_website = enriched_row.get('Website')
        disc = compare_field(research_website, enriched_website, 'website')
        if disc:
            disc['account'] = account_name
            discrepancies.append(disc)

        # Annual Sales
        research_sales = research_row.get('annual_sales')
        enriched_sales = enriched_row.get('Annual Sales')

        # Clean and compare sales values
        def clean_sales(val):
            if pd.isna(val):
                return None
            # Remove commas and quotes
            val_str = str(val).replace(',', '').replace('"', '').replace("'", "").strip()
            if val_str == '' or val_str == '0':
                return None
            try:
                return float(val_str)
            except:
                return val_str

        research_sales_clean = clean_sales(research_sales)
        enriched_sales_clean = clean_sales(enriched_sales)

        if research_sales_clean != enriched_sales_clean:
            discrepancies.append({
                'account': account_name,
                'field': 'annual_sales',
                'research_value': research_sales,
                'enriched_value': enriched_sales,
                'research_clean': research_sales_clean,
                'enriched_clean': enriched_sales_clean
            })

        # QBO Industry / Sector
        research_qbo = research_row.get('qbo_industry')
        enriched_sector = enriched_row.get('Sector')
        disc = compare_field(research_qbo, enriched_sector, 'qbo_industry_vs_sector')
        if disc:
            disc['account'] = account_name
            discrepancies.append(disc)

        # Research-only fields
        if normalize_for_comparison(research_row.get('total_events')):
            discrepancies.append({
                'account': account_name,
                'field': 'total_events',
                'research_value': research_row.get('total_events'),
                'enriched_value': 'NOT_IN_ENRICHED',
                'note': 'Event count tracked in research only'
            })

        if normalize_for_comparison(research_row.get('classification_source')):
            discrepancies.append({
                'account': account_name,
                'field': 'classification_source',
                'research_value': research_row.get('classification_source'),
                'enriched_value': 'NOT_IN_ENRICHED',
                'note': 'Classification source tracked in research only'
            })

        if normalize_for_comparison(research_row.get('confidence')):
            discrepancies.append({
                'account': account_name,
                'field': 'confidence',
                'research_value': research_row.get('confidence'),
                'enriched_value': 'NOT_IN_ENRICHED',
                'note': 'Confidence level tracked in research only'
            })

        if discrepancies:
            all_discrepancies.extend(discrepancies)

    # Create output dataframes
    discrepancies_df = pd.DataFrame(all_discrepancies)
    not_in_enriched_df = pd.DataFrame(accounts_not_in_enriched)

    # Summary statistics
    print("\n" + "="*80)
    print("COMPARISON SUMMARY")
    print("="*80)
    print(f"\nTotal accounts in research file: {len(research_df)}")
    print(f"Total accounts in enriched file: {len(enriched_df)}")
    print(f"Accounts matched: {len(accounts_matched)}")
    print(f"Accounts in research but NOT in enriched: {len(accounts_not_in_enriched)}")
    print(f"Total discrepancies found: {len(all_discrepancies)}")

    if len(discrepancies_df) > 0:
        print(f"\nDiscrepancies by field:")
        print(discrepancies_df['field'].value_counts().to_string())

    # Save results
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)

    if len(discrepancies_df) > 0:
        output_file = OUTPUT_DIR / "all_discrepancies.csv"
        discrepancies_df.to_csv(output_file, index=False)
        print(f"\nSaved {len(discrepancies_df)} discrepancies to: {output_file}")

        # Group by account for easier review
        if len(discrepancies_df) > 0:
            account_summary = discrepancies_df.groupby('account').agg({
                'field': lambda x: ', '.join(x),
                'research_value': 'count'
            }).rename(columns={'research_value': 'num_discrepancies'})
            account_summary = account_summary.sort_values('num_discrepancies', ascending=False)

            summary_file = OUTPUT_DIR / "discrepancies_by_account.csv"
            account_summary.to_csv(summary_file)
            print(f"Saved account summary to: {summary_file}")

    if len(not_in_enriched_df) > 0:
        missing_file = OUTPUT_DIR / "accounts_not_in_enriched.csv"
        not_in_enriched_df.to_csv(missing_file, index=False)
        print(f"Saved {len(not_in_enriched_df)} missing accounts to: {missing_file}")

    # Detailed analysis by field type
    print("\n" + "="*80)
    print("DETAILED DISCREPANCY ANALYSIS")
    print("="*80)

    if len(discrepancies_df) > 0:
        for field in discrepancies_df['field'].unique():
            field_discreps = discrepancies_df[discrepancies_df['field'] == field]
            output_file = OUTPUT_DIR / f"discrepancies_{field}.csv"
            field_discreps.to_csv(output_file, index=False)
            print(f"\n{field}: {len(field_discreps)} discrepancies")
            print(f"  Saved to: {output_file}")

    # Check for accounts in enriched but not in research
    enriched_accounts = set(enriched_df['account_normalized'].dropna())
    research_accounts = set(research_df['account_normalized'].dropna())
    only_in_enriched = enriched_accounts - research_accounts

    if only_in_enriched:
        print(f"\n\nAccounts in enriched but NOT in research: {len(only_in_enriched)}")
        enriched_only_df = enriched_df[enriched_df['account_normalized'].isin(only_in_enriched)]
        enriched_only_file = OUTPUT_DIR / "accounts_only_in_enriched.csv"
        enriched_only_df[['Account Name', 'Vertical', 'Industry (Research)', 'Website', 'Annual Sales']].to_csv(enriched_only_file, index=False)
        print(f"Saved to: {enriched_only_file}")

    print("\n" + "="*80)
    print("COMPARISON COMPLETE")
    print("="*80)
    print(f"\nAll results saved to: {OUTPUT_DIR}/")

    return discrepancies_df, not_in_enriched_df

if __name__ == "__main__":
    discrepancies_df, not_in_enriched_df = main()
