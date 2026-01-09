#!/usr/bin/env python3
"""
Analyze cancellation/churn reasons from customer data
Find the most compelling and common reasons for cancellation
"""

import pandas as pd
import numpy as np
from collections import Counter
import re

# Load the data
print("Loading customer data...")
df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V3_UPDATED.csv', encoding='utf-8-sig')

print(f"Total records: {len(df):,}")
print(f"Total cancellations: {df['Cancellation Date'].notna().sum():,}")

# Filter to cancelled accounts only
cancelled = df[df['Cancellation Date'].notna()].copy()
print(f"\nAnalyzing {len(cancelled):,} cancelled accounts...\n")

# Analyze Cancellation Reason field
print("="*80)
print("CANCELLATION REASONS - PRIMARY FIELD")
print("="*80)

reason_counts = cancelled['Cancellation Reason'].value_counts(dropna=False)
reason_pct = (reason_counts / len(cancelled) * 100).round(2)

print(f"\nTop Cancellation Reasons (n={len(cancelled):,}):\n")
for reason, count in reason_counts.head(20).items():
    pct = reason_pct[reason]
    if pd.isna(reason):
        print(f"  {count:>5} ({pct:>5.1f}%)  [BLANK/MISSING]")
    else:
        print(f"  {count:>5} ({pct:>5.1f}%)  {reason}")

# Analyze Cancellation Reason Other (free text)
print("\n" + "="*80)
print("CANCELLATION REASONS - OTHER (FREE TEXT)")
print("="*80)

other_reasons = cancelled[cancelled['Cancellation Reason Other'].notna()]['Cancellation Reason Other']
print(f"\nTotal free-text reasons: {len(other_reasons):,}")

if len(other_reasons) > 0:
    print("\nSample free-text cancellation reasons:\n")
    for i, reason in enumerate(other_reasons.head(30).values, 1):
        # Clean up the text
        reason_clean = str(reason).strip()
        if len(reason_clean) > 100:
            reason_clean = reason_clean[:97] + "..."
        print(f"  {i:2}. {reason_clean}")

# Analyze by key metrics
print("\n" + "="*80)
print("CANCELLATION ANALYSIS BY CUSTOMER SEGMENT")
print("="*80)

# Add tenure calculation
cancelled['SignUpDate'] = pd.to_datetime(cancelled['Sign Up Date'], errors='coerce')
cancelled['CancellationDate'] = pd.to_datetime(cancelled['Cancellation Date'], errors='coerce')
cancelled['Tenure_Days'] = (cancelled['CancellationDate'] - cancelled['SignUpDate']).dt.days
cancelled['Tenure_Months'] = (cancelled['Tenure_Days'] / 30.44).round(1)

# Categorize tenure
def categorize_tenure(months):
    if pd.isna(months) or months < 0:
        return 'Unknown'
    elif months < 3:
        return '0-3 months (Early Churn)'
    elif months < 12:
        return '3-12 months'
    elif months < 36:
        return '1-3 years'
    else:
        return '3+ years'

cancelled['Tenure_Category'] = cancelled['Tenure_Months'].apply(categorize_tenure)

print("\nChurn by Tenure:")
tenure_stats = cancelled.groupby('Tenure_Category').agg({
    'Record ID': 'count',
    'Last Invoice $': 'mean',
    'Tenure_Months': 'mean'
}).round(2)
tenure_stats.columns = ['Count', 'Avg MRR', 'Avg Tenure (mo)']
tenure_stats = tenure_stats.sort_values('Avg Tenure (mo)')
print(tenure_stats)

# Most common reasons by tenure
print("\n" + "="*80)
print("TOP 3 CANCELLATION REASONS BY TENURE STAGE")
print("="*80)

for tenure_cat in ['0-3 months (Early Churn)', '3-12 months', '1-3 years', '3+ years']:
    tenure_group = cancelled[cancelled['Tenure_Category'] == tenure_cat]
    if len(tenure_group) > 0:
        print(f"\n{tenure_cat} (n={len(tenure_group):,}):")
        top_reasons = tenure_group['Cancellation Reason'].value_counts().head(3)
        for reason, count in top_reasons.items():
            pct = count / len(tenure_group) * 100
            if pd.isna(reason):
                print(f"  • {count:>4} ({pct:>4.1f}%)  [BLANK]")
            else:
                print(f"  • {count:>4} ({pct:>4.1f}%)  {reason}")

# Analyze by MRR (value of lost customers)
print("\n" + "="*80)
print("HIGH-VALUE CUSTOMER CHURN (MRR > $200)")
print("="*80)

high_value = cancelled[cancelled['Last Invoice $'] > 200].copy()
print(f"\nHigh-value churned customers: {len(high_value):,}")
print(f"Total MRR lost: ${high_value['Last Invoice $'].sum():,.2f}/month\n")

if len(high_value) > 0:
    print("Top reasons for high-value churn:")
    hv_reasons = high_value['Cancellation Reason'].value_counts().head(10)
    for reason, count in hv_reasons.items():
        pct = count / len(high_value) * 100
        avg_mrr = high_value[high_value['Cancellation Reason'] == reason]['Last Invoice $'].mean()
        if pd.isna(reason):
            print(f"  • {count:>3} ({pct:>5.1f}%)  Avg MRR: ${avg_mrr:>6.2f}  [BLANK]")
        else:
            print(f"  • {count:>3} ({pct:>5.1f}%)  Avg MRR: ${avg_mrr:>6.2f}  {reason}")

# Analyze by Industry Cluster
print("\n" + "="*80)
print("CHURN REASONS BY TOP 5 INDUSTRY CLUSTERS")
print("="*80)

if 'Industry_Cluster' in cancelled.columns:
    top_clusters = cancelled['Industry_Cluster'].value_counts().head(5).index

    for cluster in top_clusters:
        cluster_data = cancelled[cancelled['Industry_Cluster'] == cluster]
        print(f"\n{cluster} (n={len(cluster_data):,}):")
        cluster_reasons = cluster_data['Cancellation Reason'].value_counts().head(3)
        for reason, count in cluster_reasons.items():
            pct = count / len(cluster_data) * 100
            if pd.isna(reason):
                print(f"  • {count:>4} ({pct:>4.1f}%)  [BLANK]")
            else:
                print(f"  • {count:>4} ({pct:>4.1f}%)  {reason}")

# Save detailed analysis
print("\n" + "="*80)
print("SAVING DETAILED REPORTS")
print("="*80)

# Create detailed churn reasons report
churn_detail = cancelled[[
    'Account Name', 'Cancellation Reason', 'Cancellation Reason Other',
    'Tenure_Months', 'Last Invoice $', 'Employees', 'Customers',
    'Sign Up Date', 'Cancellation Date'
]].copy()

churn_detail = churn_detail.sort_values('Last Invoice $', ascending=False)
churn_detail.to_csv('results/churn_reasons_detailed.csv', index=False)
print("✓ Saved: results/churn_reasons_detailed.csv")

# Create summary by reason
reason_summary = cancelled.groupby('Cancellation Reason').agg({
    'Record ID': 'count',
    'Last Invoice $': ['sum', 'mean', 'median'],
    'Tenure_Months': ['mean', 'median'],
    'Employees': 'median'
}).round(2)

reason_summary.columns = ['Count', 'Total MRR Lost', 'Avg MRR', 'Median MRR',
                          'Avg Tenure (mo)', 'Median Tenure (mo)', 'Median Employees']
reason_summary = reason_summary.sort_values('Count', ascending=False)
reason_summary.to_csv('results/churn_reasons_summary.csv')
print("✓ Saved: results/churn_reasons_summary.csv")

# Extract compelling free-text reasons
if len(other_reasons) > 0:
    columns_to_include = ['Account Name', 'Cancellation Reason', 'Cancellation Reason Other',
                          'Tenure_Months', 'Last Invoice $']
    if 'Industry_Cluster' in cancelled.columns:
        columns_to_include.append('Industry_Cluster')

    other_df = cancelled[cancelled['Cancellation Reason Other'].notna()][columns_to_include].copy()
    other_df = other_df.sort_values('Last Invoice $', ascending=False)
    other_df.to_csv('results/churn_reasons_freetext.csv', index=False)
    print("✓ Saved: results/churn_reasons_freetext.csv")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nKey Files Generated:")
print("  • results/churn_reasons_detailed.csv - All cancelled accounts with reasons")
print("  • results/churn_reasons_summary.csv - Summary statistics by reason")
print("  • results/churn_reasons_freetext.csv - All free-text cancellation reasons")
