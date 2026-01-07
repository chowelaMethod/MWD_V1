"""
80/20 Pareto Analysis: Customer Value Insights

This script analyzes customer value using the Pareto Principle (80/20 rule) to identify:
1. Which customers drive the majority of revenue (MRR and LTV)
2. Characteristics of high-value customer segments
3. Revenue concentration patterns and risks
4. Actionable insights for growth and retention

Metrics:
- MRR_Calculated: Monthly Recurring Revenue
- SAAS Amount to Date: Cumulative Lifetime Value
"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("80/20 PARETO ANALYSIS: CUSTOMER VALUE INSIGHTS")
print("="*80)

# Create output directories
os.makedirs('data/pareto_results', exist_ok=True)
os.makedirs('analysis/pareto_analysis', exist_ok=True)
os.makedirs('analysis/pareto_analysis/charts', exist_ok=True)

# Load data
print("\nLoading datasets...")
accounts = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2.csv')
product_complexity = pd.read_csv('product_type_analysis_results.csv')

print(f"Total accounts: {len(accounts):,}")
print(f"Product complexity data: {len(product_complexity):,} accounts")

# Filter to active accounts
active_accounts = accounts[accounts['Active?'] == True].copy()
print(f"Active accounts: {len(active_accounts):,}")

# Filter to accounts with MRR > 0
mrr_accounts = active_accounts[active_accounts['MRR_Calculated'] > 0].copy()
print(f"Active accounts with MRR > 0: {len(mrr_accounts):,}")

# Filter to accounts with LTV > 0
ltv_accounts = active_accounts[active_accounts['SAAS Amount to Date'] > 0].copy()
print(f"Active accounts with LTV > 0: {len(ltv_accounts):,}")

print("\n" + "="*80)
print("PHASE 1: CORE 80/20 PARETO ANALYSIS")
print("="*80)

# === MRR PARETO ANALYSIS ===
print("\n--- MRR (Monthly Recurring Revenue) Analysis ---")

mrr_sorted = mrr_accounts.sort_values('MRR_Calculated', ascending=False).copy()
mrr_sorted['MRR_Rank'] = range(1, len(mrr_sorted) + 1)
mrr_sorted['MRR_Cumulative'] = mrr_sorted['MRR_Calculated'].cumsum()
total_mrr = mrr_sorted['MRR_Calculated'].sum()
mrr_sorted['MRR_Cumulative_Pct'] = (mrr_sorted['MRR_Cumulative'] / total_mrr * 100)
mrr_sorted['Customer_Pct'] = (mrr_sorted['MRR_Rank'] / len(mrr_sorted) * 100)

# Find 80% threshold
mrr_80_idx = (mrr_sorted['MRR_Cumulative_Pct'] >= 80).idxmax()
mrr_80_count = mrr_sorted.loc[mrr_80_idx, 'MRR_Rank']
mrr_80_pct = (mrr_80_count / len(mrr_sorted)) * 100

print(f"Total MRR: ${total_mrr:,.2f}")
print(f"80% of MRR (${total_mrr * 0.8:,.2f}) comes from: {mrr_80_count} customers ({mrr_80_pct:.1f}%)")
print(f"Top 20% customers ({int(len(mrr_sorted) * 0.2)}) contribute: ${mrr_sorted.head(int(len(mrr_sorted) * 0.2))['MRR_Calculated'].sum():,.2f} ({mrr_sorted.head(int(len(mrr_sorted) * 0.2))['MRR_Calculated'].sum() / total_mrr * 100:.1f}%)")

# Calculate percentiles
percentiles = [1, 5, 10, 20, 50]
print("\nMRR Percentiles:")
for p in percentiles:
    idx = int(len(mrr_sorted) * p / 100)
    if idx > 0:
        threshold = mrr_sorted.iloc[idx-1]['MRR_Calculated']
        cum_pct = mrr_sorted.iloc[idx-1]['MRR_Cumulative_Pct']
        print(f"  Top {p}%: ${threshold:.2f}+ (contributes {cum_pct:.1f}% of total MRR)")

median_mrr = mrr_sorted['MRR_Calculated'].median()
print(f"  Median MRR: ${median_mrr:.2f}")

# === LTV PARETO ANALYSIS ===
print("\n--- LTV (Lifetime Value - SAAS Amount to Date) Analysis ---")

ltv_sorted = ltv_accounts.sort_values('SAAS Amount to Date', ascending=False).copy()
ltv_sorted['LTV_Rank'] = range(1, len(ltv_sorted) + 1)
ltv_sorted['LTV_Cumulative'] = ltv_sorted['SAAS Amount to Date'].cumsum()
total_ltv = ltv_sorted['SAAS Amount to Date'].sum()
ltv_sorted['LTV_Cumulative_Pct'] = (ltv_sorted['LTV_Cumulative'] / total_ltv * 100)
ltv_sorted['Customer_Pct'] = (ltv_sorted['LTV_Rank'] / len(ltv_sorted) * 100)

# Find 80% threshold
ltv_80_idx = (ltv_sorted['LTV_Cumulative_Pct'] >= 80).idxmax()
ltv_80_count = ltv_sorted.loc[ltv_80_idx, 'LTV_Rank']
ltv_80_pct = (ltv_80_count / len(ltv_sorted)) * 100

print(f"Total LTV: ${total_ltv:,.2f}")
print(f"80% of LTV (${total_ltv * 0.8:,.2f}) comes from: {ltv_80_count} customers ({ltv_80_pct:.1f}%)")
print(f"Top 20% customers ({int(len(ltv_sorted) * 0.2)}) contribute: ${ltv_sorted.head(int(len(ltv_sorted) * 0.2))['SAAS Amount to Date'].sum():,.2f} ({ltv_sorted.head(int(len(ltv_sorted) * 0.2))['SAAS Amount to Date'].sum() / total_ltv * 100:.1f}%)")

# Calculate percentiles
print("\nLTV Percentiles:")
for p in percentiles:
    idx = int(len(ltv_sorted) * p / 100)
    if idx > 0:
        threshold = ltv_sorted.iloc[idx-1]['SAAS Amount to Date']
        cum_pct = ltv_sorted.iloc[idx-1]['LTV_Cumulative_Pct']
        print(f"  Top {p}%: ${threshold:,.2f}+ (contributes {cum_pct:.1f}% of total LTV)")

median_ltv = ltv_sorted['SAAS Amount to Date'].median()
print(f"  Median LTV: ${median_ltv:,.2f}")

# === CREATE VALUE TIERS ===
print("\n--- Creating Value Tiers ---")

# Merge MRR and LTV data
customer_tiers = active_accounts[['Account Name', 'MRR_Calculated', 'SAAS Amount to Date',
                                   'Industry_Cluster_Enhanced_V2', 'Company_Size_V2',
                                   'Business_Type_V2', 'Signup Country', 'Employees', 'Users',
                                   'Custom Screens New', 'Custom Screens Classic']].copy()

# Add MRR tiers
customer_tiers = customer_tiers.merge(
    mrr_sorted[['Account Name', 'MRR_Rank', 'MRR_Cumulative_Pct', 'Customer_Pct']].rename(columns={'Customer_Pct': 'MRR_Percentile'}),
    on='Account Name',
    how='left'
)

# Add LTV tiers
customer_tiers = customer_tiers.merge(
    ltv_sorted[['Account Name', 'LTV_Rank', 'LTV_Cumulative_Pct', 'Customer_Pct']].rename(columns={'Customer_Pct': 'LTV_Percentile'}),
    on='Account Name',
    how='left'
)

# Assign tier labels
def assign_tier(percentile):
    if pd.isna(percentile):
        return 'No Revenue'
    elif percentile <= 10:
        return 'Top 10%'
    elif percentile <= 20:
        return 'Top 20%'
    elif percentile <= 50:
        return 'Top 50%'
    else:
        return 'Bottom 50%'

customer_tiers['MRR_Tier'] = customer_tiers['MRR_Percentile'].apply(assign_tier)
customer_tiers['LTV_Tier'] = customer_tiers['LTV_Percentile'].apply(assign_tier)

print(f"Customer tiers created for {len(customer_tiers):,} active accounts")

# Save Pareto curves for visualization
pareto_curve_mrr = mrr_sorted[['MRR_Rank', 'Customer_Pct', 'MRR_Cumulative_Pct']].copy()
pareto_curve_mrr.to_csv('analysis/pareto_analysis/charts/pareto_curve_mrr.csv', index=False)

pareto_curve_ltv = ltv_sorted[['LTV_Rank', 'Customer_Pct', 'LTV_Cumulative_Pct']].copy()
pareto_curve_ltv.to_csv('analysis/pareto_analysis/charts/pareto_curve_ltv.csv', index=False)

print("Pareto curves saved to analysis/pareto_analysis/charts/")

print("\n" + "="*80)
print("PHASE 2: SEGMENTATION ANALYSIS")
print("="*80)

# === 2A: INDUSTRY CLUSTER ANALYSIS ===
print("\n--- 2A: Industry Cluster Analysis ---")

industry_stats = customer_tiers[customer_tiers['MRR_Calculated'] > 0].groupby('Industry_Cluster_Enhanced_V2').agg({
    'Account Name': 'count',
    'MRR_Calculated': ['sum', 'mean', 'median'],
    'SAAS Amount to Date': ['sum', 'mean', 'median']
}).round(2)

industry_stats.columns = ['Customer_Count', 'Total_MRR', 'Avg_MRR', 'Median_MRR',
                          'Total_LTV', 'Avg_LTV', 'Median_LTV']
industry_stats['MRR_Pct'] = (industry_stats['Total_MRR'] / total_mrr * 100).round(1)
industry_stats['LTV_Pct'] = (industry_stats['Total_LTV'] / total_ltv * 100).round(1)

# Count top 20% customers by industry
top20_by_industry = customer_tiers[customer_tiers['MRR_Tier'] == 'Top 20%'].groupby('Industry_Cluster_Enhanced_V2').size()
industry_stats['Top_20_Pct_Count'] = top20_by_industry
industry_stats['Top_20_Pct_Count'] = industry_stats['Top_20_Pct_Count'].fillna(0).astype(int)

industry_stats = industry_stats.sort_values('Total_MRR', ascending=False)

print(f"\nTop 10 Industries by Total MRR:")
for idx, (industry, row) in enumerate(industry_stats.head(10).iterrows(), 1):
    print(f"{idx}. {industry}")
    print(f"   Customers: {int(row['Customer_Count']):,} | Total MRR: ${row['Total_MRR']:,.2f} ({row['MRR_Pct']:.1f}%) | Avg MRR: ${row['Avg_MRR']:.2f}")
    print(f"   Top 20% customers: {row['Top_20_Pct_Count']}")

industry_stats.to_csv('data/pareto_results/industry_cluster_pareto.csv')
industry_stats[['Customer_Count', 'Total_MRR', 'Avg_MRR', 'MRR_Pct']].to_csv('analysis/pareto_analysis/charts/revenue_by_industry.csv')

# === 2B: COMPANY SIZE ANALYSIS ===
print("\n--- 2B: Company Size Analysis ---")

size_stats = customer_tiers[customer_tiers['MRR_Calculated'] > 0].groupby('Company_Size_V2').agg({
    'Account Name': 'count',
    'MRR_Calculated': ['sum', 'mean', 'median'],
    'SAAS Amount to Date': ['sum', 'mean', 'median']
}).round(2)

size_stats.columns = ['Customer_Count', 'Total_MRR', 'Avg_MRR', 'Median_MRR',
                      'Total_LTV', 'Avg_LTV', 'Median_LTV']
size_stats['MRR_Pct'] = (size_stats['Total_MRR'] / total_mrr * 100).round(1)
size_stats['LTV_Pct'] = (size_stats['Total_LTV'] / total_ltv * 100).round(1)

# Count top 20% customers by size
top20_by_size = customer_tiers[customer_tiers['MRR_Tier'] == 'Top 20%'].groupby('Company_Size_V2').size()
size_stats['Top_20_Pct_Count'] = top20_by_size
size_stats['Top_20_Pct_Count'] = size_stats['Top_20_Pct_Count'].fillna(0).astype(int)
size_stats['Pct_in_Top_20'] = (size_stats['Top_20_Pct_Count'] / size_stats['Customer_Count'] * 100).round(1)

# Order by size
size_order = ['Enterprise (200+ employees)', 'Large (51-200 employees)', 'Medium (21-50 employees)',
              'Small (6-20 employees)', 'Micro (1-5 employees)', 'Unknown']
size_stats = size_stats.reindex([s for s in size_order if s in size_stats.index])

print(f"\nRevenue by Company Size:")
for size, row in size_stats.iterrows():
    print(f"\n{size}:")
    print(f"   Customers: {int(row['Customer_Count']):,} | Total MRR: ${row['Total_MRR']:,.2f} ({row['MRR_Pct']:.1f}%)")
    print(f"   Avg MRR: ${row['Avg_MRR']:.2f} | Median MRR: ${row['Median_MRR']:.2f}")
    print(f"   {row['Pct_in_Top_20']:.1f}% of this segment are in top 20% overall")

size_stats.to_csv('data/pareto_results/company_size_pareto.csv')
size_stats[['Customer_Count', 'Total_MRR', 'Avg_MRR', 'MRR_Pct']].to_csv('analysis/pareto_analysis/charts/revenue_by_company_size.csv')

# === 2C: PRODUCT COMPLEXITY ANALYSIS ===
print("\n--- 2C: Product Complexity Analysis (Subset) ---")

# Merge with product complexity data
customer_with_complexity = customer_tiers.merge(
    product_complexity[['Account', 'SKU_Count', 'Catalog_Complexity_Score', 'Complexity_Tier', 'Primary_Business_Type']],
    left_on='Account Name',
    right_on='Account',
    how='left'
)

complexity_subset = customer_with_complexity[
    (customer_with_complexity['MRR_Calculated'] > 0) &
    (customer_with_complexity['SKU_Count'].notna())
].copy()

print(f"Active accounts with both MRR and product complexity data: {len(complexity_subset):,}")

if len(complexity_subset) > 0:
    complexity_stats = complexity_subset.groupby('Complexity_Tier').agg({
        'Account Name': 'count',
        'MRR_Calculated': ['mean', 'median'],
        'SAAS Amount to Date': ['mean', 'median'],
        'SKU_Count': 'mean',
        'Catalog_Complexity_Score': 'mean'
    }).round(2)

    complexity_stats.columns = ['Customer_Count', 'Avg_MRR', 'Median_MRR', 'Avg_LTV', 'Median_LTV', 'Avg_SKU_Count', 'Avg_Complexity_Score']

    # Order by complexity
    complexity_order = ['Very Complex', 'Complex', 'Standard', 'Simple', 'Ultra-Simple']
    complexity_stats = complexity_stats.reindex([c for c in complexity_order if c in complexity_stats.index])

    print(f"\nRevenue by Product Catalog Complexity:")
    for tier, row in complexity_stats.iterrows():
        print(f"\n{tier}:")
        print(f"   Customers: {int(row['Customer_Count']):,} | Avg MRR: ${row['Avg_MRR']:.2f} | Avg LTV: ${row['Avg_LTV']:,.2f}")
        print(f"   Avg SKU Count: {row['Avg_SKU_Count']:.0f} | Complexity Score: {row['Avg_Complexity_Score']:.1f}")

    # Calculate correlations
    print(f"\nCorrelations with Revenue:")
    if len(complexity_subset) > 10:
        corr_sku_mrr = complexity_subset['SKU_Count'].corr(complexity_subset['MRR_Calculated'])
        corr_complexity_mrr = complexity_subset['Catalog_Complexity_Score'].corr(complexity_subset['MRR_Calculated'])
        corr_sku_ltv = complexity_subset['SKU_Count'].corr(complexity_subset['SAAS Amount to Date'])
        corr_complexity_ltv = complexity_subset['Catalog_Complexity_Score'].corr(complexity_subset['SAAS Amount to Date'])

        print(f"   SKU Count vs MRR: {corr_sku_mrr:.3f}")
        print(f"   Complexity Score vs MRR: {corr_complexity_mrr:.3f}")
        print(f"   SKU Count vs LTV: {corr_sku_ltv:.3f}")
        print(f"   Complexity Score vs LTV: {corr_complexity_ltv:.3f}")

    complexity_stats.to_csv('data/pareto_results/product_complexity_pareto.csv')

# === 2D: GEOGRAPHIC ANALYSIS ===
print("\n--- 2D: Geographic Analysis ---")

geo_stats = customer_tiers[customer_tiers['MRR_Calculated'] > 0].groupby('Signup Country').agg({
    'Account Name': 'count',
    'MRR_Calculated': ['sum', 'mean'],
    'SAAS Amount to Date': ['sum', 'mean']
}).round(2)

geo_stats.columns = ['Customer_Count', 'Total_MRR', 'Avg_MRR', 'Total_LTV', 'Avg_LTV']
geo_stats['MRR_Pct'] = (geo_stats['Total_MRR'] / total_mrr * 100).round(1)
geo_stats['LTV_Pct'] = (geo_stats['Total_LTV'] / total_ltv * 100).round(1)
geo_stats = geo_stats.sort_values('Total_MRR', ascending=False)

print(f"\nTop 10 Countries by Total MRR:")
for idx, (country, row) in enumerate(geo_stats.head(10).iterrows(), 1):
    print(f"{idx}. {country}: {int(row['Customer_Count']):,} customers | ${row['Total_MRR']:,.2f} ({row['MRR_Pct']:.1f}%) | Avg: ${row['Avg_MRR']:.2f}")

geo_stats.to_csv('data/pareto_results/geographic_pareto.csv')
geo_stats.to_csv('analysis/pareto_analysis/charts/geographic_revenue.csv')

# === 2E: BUSINESS TYPE ANALYSIS ===
print("\n--- 2E: Business Type Analysis ---")

biz_stats = customer_tiers[customer_tiers['MRR_Calculated'] > 0].groupby('Business_Type_V2').agg({
    'Account Name': 'count',
    'MRR_Calculated': ['sum', 'mean', 'median'],
    'SAAS Amount to Date': ['sum', 'mean', 'median']
}).round(2)

biz_stats.columns = ['Customer_Count', 'Total_MRR', 'Avg_MRR', 'Median_MRR', 'Total_LTV', 'Avg_LTV', 'Median_LTV']
biz_stats['MRR_Pct'] = (biz_stats['Total_MRR'] / total_mrr * 100).round(1)

print(f"\nRevenue by Business Type:")
for biz_type, row in biz_stats.sort_values('Total_MRR', ascending=False).iterrows():
    print(f"\n{biz_type}:")
    print(f"   Customers: {int(row['Customer_Count']):,} | Total MRR: ${row['Total_MRR']:,.2f} ({row['MRR_Pct']:.1f}%)")
    print(f"   Avg MRR: ${row['Avg_MRR']:.2f} | Median MRR: ${row['Median_MRR']:.2f}")

print("\n" + "="*80)
print("PHASE 3: CROSS-SEGMENT PATTERN DISCOVERY")
print("="*80)

# === TOP 20% CUSTOMER PROFILE ===
print("\n--- Top 20% Customer Characteristics ---")

top20_customers = customer_tiers[customer_tiers['MRR_Tier'] == 'Top 20%'].copy()
all_customers = customer_tiers[customer_tiers['MRR_Calculated'] > 0].copy()

print(f"\nTop 20% Profile ({len(top20_customers):,} customers):")

# Industry distribution
print("\nIndustry Distribution (Top 5):")
top20_industries = top20_customers['Industry_Cluster_Enhanced_V2'].value_counts()
all_industries = all_customers['Industry_Cluster_Enhanced_V2'].value_counts(normalize=True) * 100
for industry in top20_industries.head(5).index:
    top20_pct = (top20_industries[industry] / len(top20_customers)) * 100
    all_pct = all_industries.get(industry, 0)
    enrichment = top20_pct / all_pct if all_pct > 0 else 0
    print(f"   {industry}: {top20_pct:.1f}% (vs {all_pct:.1f}% overall, {enrichment:.1f}x enrichment)")

# Company size distribution
print("\nCompany Size Distribution:")
top20_sizes = top20_customers['Company_Size_V2'].value_counts()
all_sizes = all_customers['Company_Size_V2'].value_counts(normalize=True) * 100
for size in size_order:
    if size in top20_sizes.index:
        top20_pct = (top20_sizes[size] / len(top20_customers)) * 100
        all_pct = all_sizes.get(size, 0)
        enrichment = top20_pct / all_pct if all_pct > 0 else 0
        print(f"   {size}: {top20_pct:.1f}% (vs {all_pct:.1f}% overall, {enrichment:.1f}x enrichment)")

# Geographic distribution
print("\nTop Geographic Markets:")
top20_geo = top20_customers['Signup Country'].value_counts()
all_geo = all_customers['Signup Country'].value_counts(normalize=True) * 100
for country in top20_geo.head(5).index:
    top20_pct = (top20_geo[country] / len(top20_customers)) * 100
    all_pct = all_geo.get(country, 0)
    print(f"   {country}: {top20_pct:.1f}% (vs {all_pct:.1f}% overall)")

# === MRR VS LTV QUADRANTS ===
print("\n--- MRR vs LTV Quadrant Analysis ---")

# Define quadrants based on median
median_mrr_overall = customer_tiers[customer_tiers['MRR_Calculated'] > 0]['MRR_Calculated'].median()
median_ltv_overall = customer_tiers[customer_tiers['SAAS Amount to Date'] > 0]['SAAS Amount to Date'].median()

quadrant_data = customer_tiers[
    (customer_tiers['MRR_Calculated'] > 0) &
    (customer_tiers['SAAS Amount to Date'] > 0)
].copy()

def assign_quadrant(row):
    if row['MRR_Calculated'] >= median_mrr_overall and row['SAAS Amount to Date'] >= median_ltv_overall:
        return 'Core Champions'
    elif row['MRR_Calculated'] >= median_mrr_overall and row['SAAS Amount to Date'] < median_ltv_overall:
        return 'Rising Stars'
    elif row['MRR_Calculated'] < median_mrr_overall and row['SAAS Amount to Date'] >= median_ltv_overall:
        return 'At Risk'
    else:
        return 'Base Customers'

quadrant_data['Quadrant'] = quadrant_data.apply(assign_quadrant, axis=1)

print(f"\nCustomer Quadrants (based on median MRR: ${median_mrr_overall:.2f}, median LTV: ${median_ltv_overall:,.2f}):")
for quadrant in ['Core Champions', 'Rising Stars', 'At Risk', 'Base Customers']:
    count = (quadrant_data['Quadrant'] == quadrant).sum()
    pct = (count / len(quadrant_data)) * 100
    avg_mrr = quadrant_data[quadrant_data['Quadrant'] == quadrant]['MRR_Calculated'].mean()
    avg_ltv = quadrant_data[quadrant_data['Quadrant'] == quadrant]['SAAS Amount to Date'].mean()
    print(f"   {quadrant}: {count:,} customers ({pct:.1f}%) | Avg MRR: ${avg_mrr:.2f} | Avg LTV: ${avg_ltv:,.2f}")

# Save scatter plot data
scatter_data = quadrant_data[['Account Name', 'MRR_Calculated', 'SAAS Amount to Date', 'Quadrant',
                               'Industry_Cluster_Enhanced_V2', 'Company_Size_V2']].copy()
scatter_data.to_csv('analysis/pareto_analysis/charts/mrr_ltv_scatter.csv', index=False)

# === SAVE ALL RESULTS ===
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save customer tiers
customer_tiers.to_csv('data/pareto_results/customer_value_tiers.csv', index=False)
print(f"Saved customer_value_tiers.csv ({len(customer_tiers):,} customers)")

# Save top 20% customers
top20_detailed = customer_tiers[customer_tiers['MRR_Tier'] == 'Top 20%'].copy()
top20_detailed = top20_detailed.sort_values('MRR_Calculated', ascending=False)
top20_detailed.to_csv('data/pareto_results/top_20_percent_customers.csv', index=False)
print(f"Saved top_20_percent_customers.csv ({len(top20_detailed):,} customers)")

# Save segment summaries
all_segments = pd.DataFrame({
    'Segment_Type': ['Overall'] * 5,
    'Segment': ['Top 1%', 'Top 5%', 'Top 10%', 'Top 20%', 'Top 50%'],
    'Customer_Count': [
        int(len(mrr_sorted) * 0.01),
        int(len(mrr_sorted) * 0.05),
        int(len(mrr_sorted) * 0.10),
        int(len(mrr_sorted) * 0.20),
        int(len(mrr_sorted) * 0.50)
    ]
})

for idx, p in enumerate([1, 5, 10, 20, 50]):
    count = int(len(mrr_sorted) * p / 100)
    all_segments.loc[idx, 'Total_MRR'] = mrr_sorted.head(count)['MRR_Calculated'].sum()
    all_segments.loc[idx, 'MRR_Pct'] = (all_segments.loc[idx, 'Total_MRR'] / total_mrr * 100)
    all_segments.loc[idx, 'Total_LTV'] = mrr_sorted.head(count)['SAAS Amount to Date'].sum()
    all_segments.loc[idx, 'LTV_Pct'] = (all_segments.loc[idx, 'Total_LTV'] / total_ltv * 100) if total_ltv > 0 else 0

all_segments.to_csv('data/pareto_results/segment_summary_statistics.csv', index=False)

# Save cross-segment patterns
cross_segment = quadrant_data.groupby(['Quadrant', 'Industry_Cluster_Enhanced_V2', 'Company_Size_V2']).agg({
    'Account Name': 'count',
    'MRR_Calculated': 'mean',
    'SAAS Amount to Date': 'mean'
}).reset_index()
cross_segment.columns = ['Quadrant', 'Industry', 'Company_Size', 'Customer_Count', 'Avg_MRR', 'Avg_LTV']
cross_segment = cross_segment[cross_segment['Customer_Count'] >= 2].sort_values('Customer_Count', ascending=False)
cross_segment.to_csv('data/pareto_results/cross_segment_patterns.csv', index=False)

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nResults saved to:")
print(f"  - data/pareto_results/ (8 CSV files)")
print(f"  - analysis/pareto_analysis/charts/ (7 CSV files)")
print(f"\nNext: Review the data and create summary report")
