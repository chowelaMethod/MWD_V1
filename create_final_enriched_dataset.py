#!/usr/bin/env python3
"""
Create final enriched dataset with:
- All classification data (industry, sub_industry, workflow_pattern)
- Account-level metrics (LTV, MRR, users, invoices, estimates, opportunities, activities)
- Aggregate metrics by industry/sub-industry (avg LTV, median users, etc.)
- Website URLs
- Company descriptions
"""

import pandas as pd
import numpy as np

print("Loading data files...")

# Load classification research (589 accounts with industry/sub_industry)
research = pd.read_csv('data/classification_research.csv')
print(f"Loaded classification_research.csv: {len(research)} accounts")

# Load enriched classifications (has some metrics like invoices/estimates/opportunities/activities)
enriched_class = pd.read_csv('data/enriched_classifications.csv')
print(f"Loaded enriched_classifications.csv: {len(enriched_class)} accounts")

# Load MWD Enriched Accounts (has LTV, company descriptions, websites, etc.)
mwd_enriched = pd.read_csv('data/MWD_Enriched_Accounts.csv')
print(f"Loaded MWD_Enriched_Accounts.csv: {len(mwd_enriched)} accounts")

# Normalize account names for matching
research['account_lower'] = research['account'].str.lower().str.strip()
enriched_class['account_lower'] = enriched_class['account'].str.lower().str.strip()
mwd_enriched['account_lower'] = mwd_enriched['Account Name'].str.lower().str.strip()

print("\nMerging datasets...")

# Start with research as base (has the classifications we care about)
final_df = research.copy()

# Merge metrics from enriched_classifications
metrics_from_enriched = enriched_class[['account_lower', 'invoices', 'estimates',
                                         'opportunities', 'activities', 'mrr',
                                         'account_age_days', 'user_count', 'ltv']]
final_df = final_df.merge(metrics_from_enriched, on='account_lower', how='left')

# Merge additional data from MWD_Enriched_Accounts
mwd_cols = ['account_lower', 'Company Name in QB', 'Website', 'Annual Sales',
            'PS Amount to Date', 'SAAS Amount to Date', 'Company Description',
            'Product Types', 'Product Complexity', 'Users', 'Customers',
            'Health Score', 'Sign Up Date', 'Vertical', 'Sector']
mwd_subset = mwd_enriched[mwd_cols].copy()
final_df = final_df.merge(mwd_subset, on='account_lower', how='left')

# Prefer Website from MWD_Enriched_Accounts, fallback to research
final_df['website_final'] = final_df['Website'].fillna(final_df['website'])

# Clean up numeric columns
def clean_numeric(series):
    """Remove commas, quotes, convert to float"""
    if series.dtype == 'object':
        return pd.to_numeric(series.str.replace(',', '').str.replace('"', ''), errors='coerce')
    return series

numeric_cols = ['annual_sales', 'Annual Sales', 'PS Amount to Date', 'SAAS Amount to Date',
                'ltv', 'mrr', 'user_count', 'account_age_days', 'invoices', 'estimates',
                'opportunities', 'activities', 'Users', 'Customers', 'Health Score']

for col in numeric_cols:
    if col in final_df.columns:
        final_df[col] = clean_numeric(final_df[col])

# Prefer LTV from SAAS Amount to Date if available (it's actual revenue)
final_df['ltv_final'] = final_df['SAAS Amount to Date'].fillna(final_df['ltv'])

# Prefer user_count from enriched_classifications, fallback to Users from MWD
final_df['users_final'] = final_df['user_count'].fillna(final_df['Users'])

print("\nCalculating aggregate metrics by industry and sub_industry...")

# Calculate aggregate metrics by industry
industry_agg = final_df.groupby('industry').agg({
    'ltv_final': ['count', 'mean', 'median', 'sum', 'std'],
    'users_final': ['mean', 'median', 'sum'],
    'mrr': ['mean', 'median', 'sum'],
    'invoices': ['mean', 'median', 'sum'],
    'estimates': ['mean', 'median', 'sum'],
    'opportunities': ['mean', 'median', 'sum'],
    'activities': ['mean', 'median', 'sum'],
    'annual_sales': ['mean', 'median'],
    'Customers': ['mean', 'median']
}).round(2)

industry_agg.columns = ['_'.join(col).strip() for col in industry_agg.columns.values]
industry_agg = industry_agg.reset_index()
industry_agg = industry_agg.rename(columns={
    'ltv_final_count': 'account_count',
    'ltv_final_mean': 'avg_ltv',
    'ltv_final_median': 'median_ltv',
    'ltv_final_sum': 'total_ltv',
    'ltv_final_std': 'std_ltv',
    'users_final_mean': 'avg_users',
    'users_final_median': 'median_users',
    'users_final_sum': 'total_users',
    'mrr_mean': 'avg_mrr',
    'mrr_median': 'median_mrr',
    'mrr_sum': 'total_mrr',
    'invoices_mean': 'avg_invoices',
    'invoices_median': 'median_invoices',
    'invoices_sum': 'total_invoices',
    'estimates_mean': 'avg_estimates',
    'estimates_median': 'median_estimates',
    'estimates_sum': 'total_estimates',
    'opportunities_mean': 'avg_opportunities',
    'opportunities_median': 'median_opportunities',
    'opportunities_sum': 'total_opportunities',
    'activities_mean': 'avg_activities',
    'activities_median': 'median_activities',
    'activities_sum': 'total_activities',
    'annual_sales_mean': 'avg_annual_sales',
    'annual_sales_median': 'median_annual_sales',
    'Customers_mean': 'avg_customers',
    'Customers_median': 'median_customers'
})

# Calculate aggregate metrics by sub_industry (for non-unclassified only)
sub_industry_df = final_df[final_df['sub_industry'] != 'Unclassified'].copy()
sub_industry_agg = sub_industry_df.groupby(['industry', 'sub_industry']).agg({
    'ltv_final': ['count', 'mean', 'median', 'sum'],
    'users_final': ['mean', 'median'],
    'mrr': ['mean', 'median'],
    'invoices': ['mean', 'median'],
    'estimates': ['mean', 'median'],
    'opportunities': ['mean', 'median'],
    'activities': ['mean', 'median']
}).round(2)

sub_industry_agg.columns = ['_'.join(col).strip() for col in sub_industry_agg.columns.values]
sub_industry_agg = sub_industry_agg.reset_index()
sub_industry_agg = sub_industry_agg.rename(columns={
    'ltv_final_count': 'account_count',
    'ltv_final_mean': 'avg_ltv',
    'ltv_final_median': 'median_ltv',
    'ltv_final_sum': 'total_ltv',
    'users_final_mean': 'avg_users',
    'users_final_median': 'median_users',
    'mrr_mean': 'avg_mrr',
    'mrr_median': 'median_mrr',
    'invoices_mean': 'avg_invoices',
    'invoices_median': 'median_invoices',
    'estimates_mean': 'avg_estimates',
    'estimates_median': 'median_estimates',
    'opportunities_mean': 'avg_opportunities',
    'opportunities_median': 'median_opportunities',
    'activities_mean': 'avg_activities',
    'activities_median': 'median_activities'
})

# Merge aggregate metrics back into final_df
final_df = final_df.merge(
    industry_agg.add_prefix('industry_'),
    left_on='industry',
    right_on='industry_industry',
    how='left'
)

final_df = final_df.merge(
    sub_industry_agg.add_prefix('sub_'),
    left_on=['industry', 'sub_industry'],
    right_on=['sub_industry', 'sub_sub_industry'],
    how='left'
)

# Select and order final columns
final_columns = [
    # Account identification
    'account',
    'Company Name in QB',

    # Classification
    'industry',
    'sub_industry',
    'workflow_pattern',
    'classification_source',
    'confidence',

    # Account-level metrics
    'ltv_final',
    'mrr',
    'users_final',
    'account_age_days',
    'Annual Sales',
    'Customers',
    'Health Score',

    # Usage metrics
    'total_events',
    'invoices',
    'estimates',
    'opportunities',
    'activities',

    # Industry aggregates
    'industry_account_count',
    'industry_avg_ltv',
    'industry_median_ltv',
    'industry_total_ltv',
    'industry_avg_users',
    'industry_median_users',
    'industry_avg_mrr',
    'industry_median_mrr',
    'industry_avg_invoices',
    'industry_avg_estimates',
    'industry_avg_opportunities',
    'industry_avg_activities',

    # Sub-industry aggregates
    'sub_account_count',
    'sub_avg_ltv',
    'sub_median_ltv',
    'sub_avg_users',
    'sub_median_users',
    'sub_avg_mrr',
    'sub_avg_invoices',
    'sub_avg_estimates',
    'sub_avg_opportunities',
    'sub_avg_activities',

    # Additional context
    'website_final',
    'Company Description',
    'Product Types',
    'Product Complexity',
    'Vertical',
    'Sector',
    'Sign Up Date',
    'qbo_industry'
]

# Only keep columns that exist
final_columns = [col for col in final_columns if col in final_df.columns]
final_export = final_df[final_columns].copy()

# Rename for clarity
final_export = final_export.rename(columns={
    'ltv_final': 'ltv',
    'users_final': 'users',
    'website_final': 'website',
    'Company Name in QB': 'company_name',
    'Annual Sales': 'annual_sales',
    'Customers': 'qb_customers',
    'Health Score': 'health_score',
    'Company Description': 'description',
    'Product Types': 'product_types',
    'Product Complexity': 'product_complexity',
    'Vertical': 'mwd_vertical',
    'Sector': 'sector',
    'Sign Up Date': 'signup_date'
})

print(f"\nFinal dataset shape: {final_export.shape}")
print(f"Columns: {len(final_export.columns)}")

# Save the final enriched dataset
output_file = 'results/FINAL_ENRICHED_DATASET.csv'
final_export.to_csv(output_file, index=False)
print(f"\n✅ Saved: {output_file}")

# Also save the aggregate summaries separately for easy reference
industry_agg.to_csv('results/INDUSTRY_AGGREGATES.csv', index=False)
print(f"✅ Saved: results/INDUSTRY_AGGREGATES.csv")

sub_industry_agg.to_csv('results/SUB_INDUSTRY_AGGREGATES.csv', index=False)
print(f"✅ Saved: results/SUB_INDUSTRY_AGGREGATES.csv")

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

# Overall stats
print(f"\nTotal accounts: {len(final_export)}")
print(f"Classified accounts: {len(final_export[final_export['sub_industry'] != 'Unclassified'])}")
print(f"Unclassified accounts: {len(final_export[final_export['sub_industry'] == 'Unclassified'])}")

print(f"\nTotal LTV: ${final_export['ltv'].sum():,.2f}")
print(f"Average LTV: ${final_export['ltv'].mean():,.2f}")
print(f"Median LTV: ${final_export['ltv'].median():,.2f}")

print(f"\nTotal Users: {final_export['users'].sum():,.0f}")
print(f"Average Users: {final_export['users'].mean():.1f}")
print(f"Median Users: {final_export['users'].median():.0f}")

print(f"\nTotal MRR: ${final_export['mrr'].sum():,.2f}")
print(f"Average MRR: ${final_export['mrr'].mean():,.2f}")
print(f"Median MRR: ${final_export['mrr'].median():,.2f}")

print("\n" + "="*80)
print("TOP 10 INDUSTRIES BY TOTAL LTV")
print("="*80)
print(industry_agg.nlargest(10, 'total_ltv')[['industry', 'account_count', 'total_ltv', 'avg_ltv', 'median_ltv', 'avg_users']].to_string(index=False))

print("\n" + "="*80)
print("TOP 10 SUB-INDUSTRIES BY TOTAL LTV")
print("="*80)
print(sub_industry_agg.nlargest(10, 'total_ltv')[['industry', 'sub_industry', 'account_count', 'total_ltv', 'avg_ltv', 'median_ltv']].to_string(index=False))

print("\n" + "="*80)
print("TOP 10 INDUSTRIES BY AVERAGE LTV")
print("="*80)
top_by_avg = industry_agg[industry_agg['account_count'] >= 5].nlargest(10, 'avg_ltv')
print(top_by_avg[['industry', 'account_count', 'avg_ltv', 'median_ltv', 'avg_users', 'avg_mrr']].to_string(index=False))

print("\n✅ Complete!")
