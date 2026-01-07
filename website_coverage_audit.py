#!/usr/bin/env python3
"""
Website Coverage Audit Script
Analyzes which accounts have website URLs and determines primary validation method per cluster.

Author: Evidence-Based Analysis
Date: January 7, 2026
"""

import pandas as pd
import numpy as np

def analyze_website_coverage():
    """
    Analyze website and domain coverage by industry cluster.
    Determine primary validation method for each cluster.
    """
    print("Loading dataset...")
    df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')

    # Filter to active accounts only
    active = df[df['Active?'] == True].copy()
    print(f"Total active accounts: {len(active)}")

    # Check for website and domain data
    active['Has_Website_URL'] = active['Website'].notna() & (active['Website'] != '') & (active['Website'] != 'nan')
    active['Has_Domains'] = active['Domains'].notna() & (active['Domains'] != '') & (active['Domains'] != 'nan')
    active['Has_Product_Data'] = active['Primary_Business_Type'].notna()

    # Overall coverage
    print("\n" + "="*80)
    print("OVERALL COVERAGE")
    print("="*80)
    total_accounts = len(active)
    website_count = active['Has_Website_URL'].sum()
    domain_count = active['Has_Domains'].sum()
    product_count = active['Has_Product_Data'].sum()

    print(f"Website URLs:     {website_count:4d} / {total_accounts} ({website_count/total_accounts*100:.1f}%)")
    print(f"Domains:          {domain_count:4d} / {total_accounts} ({domain_count/total_accounts*100:.1f}%)")
    print(f"Product Data:     {product_count:4d} / {total_accounts} ({product_count/total_accounts*100:.1f}%)")
    print(f"Any Validation:   {active[(active['Has_Website_URL']) | (active['Has_Product_Data'])].shape[0]:4d} / {total_accounts} ({active[(active['Has_Website_URL']) | (active['Has_Product_Data'])].shape[0]/total_accounts*100:.1f}%)")

    # Coverage by cluster
    print("\n" + "="*80)
    print("COVERAGE BY INDUSTRY CLUSTER")
    print("="*80)

    coverage = active.groupby('Industry_Cluster_Enhanced_V2').agg({
        'Account Name': 'count',
        'Has_Website_URL': 'sum',
        'Has_Domains': 'sum',
        'Has_Product_Data': 'sum',
        'MRR_Calculated': 'sum'
    }).rename(columns={'Account Name': 'Total_Accounts', 'MRR_Calculated': 'Total_MRR'})

    # Calculate percentages
    coverage['Website_Coverage_Pct'] = (coverage['Has_Website_URL'] / coverage['Total_Accounts'] * 100).round(1)
    coverage['Domain_Coverage_Pct'] = (coverage['Has_Domains'] / coverage['Total_Accounts'] * 100).round(1)
    coverage['Product_Data_Coverage_Pct'] = (coverage['Has_Product_Data'] / coverage['Total_Accounts'] * 100).round(1)

    # Determine primary validation method
    def determine_validation_method(row):
        website_pct = row['Website_Coverage_Pct']
        product_pct = row['Product_Data_Coverage_Pct']

        if website_pct >= 60 and product_pct >= 80:
            return 'Hybrid (Excellent)'
        elif website_pct >= 50 and product_pct >= 70:
            return 'Hybrid (Good)'
        elif website_pct >= 50:
            return 'Website Primary'
        elif product_pct >= 70:
            return 'Product Data Primary'
        elif website_pct >= 30 and product_pct >= 50:
            return 'Hybrid + Statistical'
        else:
            return 'Statistical + Manual Review'

    coverage['Primary_Validation_Method'] = coverage.apply(determine_validation_method, axis=1)

    # Add validation feasibility score (0-100)
    coverage['Validation_Feasibility'] = (
        coverage['Website_Coverage_Pct'] * 0.4 +
        coverage['Product_Data_Coverage_Pct'] * 0.5 +
        10  # Base 10 points for statistical validation always available
    ).round(1)

    # Sort by total accounts (descending)
    coverage = coverage.sort_values('Total_Accounts', ascending=False)

    # Rename columns for output
    coverage = coverage.rename(columns={
        'Has_Website_URL': 'Accounts_With_Website',
        'Has_Domains': 'Accounts_With_Domains',
        'Has_Product_Data': 'Accounts_With_Product_Data'
    })

    # Save to CSV
    output_file = 'website_coverage_by_cluster.csv'
    coverage.to_csv(output_file)
    print(f"\nSaved coverage report to: {output_file}")

    # Display summary table
    print("\n" + "="*120)
    print(f"{'Cluster':<40} {'Accts':>6} {'Website':>8} {'Product':>8} {'Validation Method':<25} {'Feasibility':>12}")
    print("="*120)

    for cluster, row in coverage.iterrows():
        print(f"{cluster:<40} "
              f"{int(row['Total_Accounts']):6d} "
              f"{row['Website_Coverage_Pct']:7.1f}% "
              f"{row['Product_Data_Coverage_Pct']:7.1f}% "
              f"{row['Primary_Validation_Method']:<25} "
              f"{row['Validation_Feasibility']:11.1f}")

    # Summary statistics
    print("\n" + "="*80)
    print("VALIDATION METHOD DISTRIBUTION")
    print("="*80)
    method_counts = coverage.groupby('Primary_Validation_Method').agg({
        'Total_Accounts': 'sum'
    }).sort_values('Total_Accounts', ascending=False)

    for method, row in method_counts.iterrows():
        count = int(row['Total_Accounts'])
        pct = count / total_accounts * 100
        print(f"{method:<30} {count:4d} accounts ({pct:5.1f}%)")

    # Identify high-priority validation targets
    print("\n" + "="*80)
    print("HIGH-PRIORITY VALIDATION TARGETS")
    print("="*80)

    # Clusters with low website coverage but high account count
    low_website = coverage[
        (coverage['Website_Coverage_Pct'] < 40) &
        (coverage['Total_Accounts'] >= 20)
    ]

    if len(low_website) > 0:
        print("\nLarge clusters with low website coverage (need product data validation):")
        for cluster, row in low_website.iterrows():
            print(f"  - {cluster}: {int(row['Total_Accounts'])} accounts, {row['Website_Coverage_Pct']:.1f}% website coverage")

    # Clusters with low product coverage
    low_product = coverage[
        (coverage['Product_Data_Coverage_Pct'] < 70) &
        (coverage['Total_Accounts'] >= 10)
    ]

    if len(low_product) > 0:
        print("\nClusters with low product data coverage (need website validation):")
        for cluster, row in low_product.iterrows():
            print(f"  - {cluster}: {int(row['Total_Accounts'])} accounts, {row['Product_Data_Coverage_Pct']:.1f}% product coverage")

    # Clusters with excellent coverage (easiest to validate)
    excellent = coverage[
        (coverage['Website_Coverage_Pct'] >= 50) &
        (coverage['Product_Data_Coverage_Pct'] >= 80)
    ]

    if len(excellent) > 0:
        print("\nClusters with excellent data coverage (easiest to validate):")
        for cluster, row in excellent.iterrows():
            print(f"  - {cluster}: {int(row['Total_Accounts'])} accounts, {row['Website_Coverage_Pct']:.1f}% website, {row['Product_Data_Coverage_Pct']:.1f}% product")

    print("\n" + "="*80)
    print("Coverage audit complete!")
    print("="*80)

    return coverage


if __name__ == '__main__':
    coverage = analyze_website_coverage()
