#!/usr/bin/env python3
"""
Validation Queue Prioritization Script
Creates a prioritized queue for cluster validation (TIER 1, 2, 3).

Author: Evidence-Based Analysis
Date: January 7, 2026
"""

import pandas as pd

def create_validation_queue():
    """
    Create prioritized validation queue based on:
    - Known issues (highest priority)
    - Large unvalidated clusters
    - Small unvalidated clusters
    - Already validated (documentation only)
    """
    print("Creating Validation Queue...")
    print("="*80)

    # Load data
    df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')
    active = df[df['Active?'] == True].copy()

    # Get cluster sizes and MRR
    cluster_stats = active.groupby('Industry_Cluster_Enhanced_V2').agg({
        'Account Name': 'count',
        'MRR_Calculated': 'sum'
    }).rename(columns={'Account Name': 'Total_Accounts', 'MRR_Calculated': 'Total_MRR'})

    # Define validation queue
    validation_queue = [
        # TIER 1 - HIGH PRIORITY (8 clusters, 502 accounts)
        {
            'Tier': 1,
            'Priority': 1,
            'Cluster': 'Food & Beverage Dist/Mfg',
            'Total_Accounts': cluster_stats.loc['Food & Beverage Dist/Mfg', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 30,
            'Reason': 'Known issue: 67% accuracy, ~10 false positives to remove',
            'Expected_Outcome': '~20 true F&B, ~10 to re-classify',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 8
        },
        {
            'Tier': 1,
            'Priority': 2,
            'Cluster': 'Medical Equipment & Supplies',
            'Total_Accounts': cluster_stats.loc['Medical Equipment & Supplies', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 16,
            'Reason': 'Known issue: 80% accuracy, 1 equine company to remove',
            'Expected_Outcome': '~13 true medical, ~3 to re-classify',
            'Validation_Methods': 'Website + Product Data',
            'Estimated_Hours': 5
        },
        {
            'Tier': 1,
            'Priority': 3,
            'Cluster': 'Apparel & Textiles',
            'Total_Accounts': cluster_stats.loc['Apparel & Textiles', 'Total_Accounts'] + 40,  # Will have 40 metal fab
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 53,  # 13 current + 40 metal fab
            'Reason': 'CRITICAL: 40 metal fabrication companies mis-classified',
            'Expected_Outcome': '~13 true apparel, ~40 to Metal Fabrication',
            'Validation_Methods': 'Website + Product Data',
            'Estimated_Hours': 12
        },
        {
            'Tier': 1,
            'Priority': 4,
            'Cluster': 'General/Specialty Manufacturing',
            'Total_Accounts': cluster_stats.loc['General/Specialty Manufacturing', 'Total_Accounts'],
            'Validation_Strategy': 'Stratified Sample',
            'Sample_Size': 60,
            'Reason': 'LARGEST unvalidated cluster (348 accounts)',
            'Expected_Outcome': 'Identify any sub-clusters or mis-classifications',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 15
        },
        {
            'Tier': 1,
            'Priority': 5,
            'Cluster': 'General Retail',
            'Total_Accounts': cluster_stats.loc['General Retail', 'Total_Accounts'],
            'Validation_Strategy': 'Stratified Sample',
            'Sample_Size': 50,
            'Reason': '3RD LARGEST unvalidated cluster (148 accounts)',
            'Expected_Outcome': 'Validate B2C focus, identify wholesale mis-classifications',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 12
        },
        {
            'Tier': 1,
            'Priority': 6,
            'Cluster': 'Furniture & Home Furnishings',
            'Total_Accounts': cluster_stats.loc['Furniture & Home Furnishings', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 14,
            'Reason': 'Partially validated: 86% accuracy, kitchen cabinets may belong in Building Materials',
            'Expected_Outcome': '~12 true furniture, ~2 to re-classify',
            'Validation_Methods': 'Website + Product Data',
            'Estimated_Hours': 4
        },
        {
            'Tier': 1,
            'Priority': 7,
            'Cluster': 'Metal Fabrication & Steel',
            'Total_Accounts': cluster_stats.loc['Metal Fabrication & Steel', 'Total_Accounts'] + 40,  # Will grow
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 44,  # 4 current + 40 incoming
            'Reason': 'Will grow to 44 accounts (receiving 40 from Apparel)',
            'Expected_Outcome': 'Validate all 44 accounts',
            'Validation_Methods': 'Website + Product Data',
            'Estimated_Hours': 10
        },
        {
            'Tier': 1,
            'Priority': 8,
            'Cluster': 'Services & Other',
            'Total_Accounts': 15,  # Estimate
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 15,
            'Reason': 'Catch-all category - most should be re-classified',
            'Expected_Outcome': 'Most accounts to move to specific clusters',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 6
        },

        # TIER 2 - MEDIUM PRIORITY (10 clusters, 86 accounts)
        {
            'Tier': 2,
            'Priority': 9,
            'Cluster': 'Safety & Security Equipment',
            'Total_Accounts': cluster_stats.loc['Safety & Security Equipment', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 8,
            'Reason': 'Small unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 2
        },
        {
            'Tier': 2,
            'Priority': 10,
            'Cluster': 'Electrical & Lighting Equipment',
            'Total_Accounts': cluster_stats.loc['Electrical & Lighting Equipment', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 7,
            'Reason': 'Small unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 2
        },
        {
            'Tier': 2,
            'Priority': 11,
            'Cluster': 'Sporting Goods & Fitness Equipment',
            'Total_Accounts': cluster_stats.loc['Sporting Goods & Fitness Equipment', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 7,
            'Reason': 'Small unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 2
        },
        {
            'Tier': 2,
            'Priority': 12,
            'Cluster': 'Manufacturer Representatives',
            'Total_Accounts': cluster_stats.loc['Manufacturer Representatives', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 6,
            'Reason': 'Small unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 2
        },
        {
            'Tier': 2,
            'Priority': 13,
            'Cluster': 'Packaging & Printing',
            'Total_Accounts': cluster_stats.loc['Packaging & Printing', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 5,
            'Reason': 'Small unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 2
        },
        {
            'Tier': 2,
            'Priority': 14,
            'Cluster': 'Office Supplies & Equipment',
            'Total_Accounts': cluster_stats.loc['Office Supplies & Equipment', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 5,
            'Reason': 'Small unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 2
        },
        {
            'Tier': 2,
            'Priority': 15,
            'Cluster': 'Agriculture & Greenhouse/Nursery',
            'Total_Accounts': cluster_stats.loc['Agriculture & Greenhouse/Nursery', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 5,
            'Reason': 'Small unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 2
        },
        {
            'Tier': 2,
            'Priority': 16,
            'Cluster': 'HVAC & Refrigeration Equipment',
            'Total_Accounts': cluster_stats.loc['HVAC & Refrigeration Equipment', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 2,
            'Reason': 'Tiny unvalidated cluster',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 1
        },
        {
            'Tier': 2,
            'Priority': 17,
            'Cluster': 'Automotive & Transportation',
            'Total_Accounts': cluster_stats.loc['Automotive & Transportation', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 2,
            'Reason': 'Tiny unvalidated cluster (100% website + product coverage!)',
            'Expected_Outcome': 'Confirm cluster accuracy',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 1
        },
        {
            'Tier': 2,
            'Priority': 18,
            'Cluster': 'Signs, Graphics & Displays',
            'Total_Accounts': cluster_stats.loc['Signs, Graphics & Displays', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 1,
            'Reason': 'Single account cluster',
            'Expected_Outcome': 'Confirm classification',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 0.5
        },
        {
            'Tier': 2,
            'Priority': 19,
            'Cluster': 'Wood Products & Lumber',
            'Total_Accounts': cluster_stats.loc['Wood Products & Lumber', 'Total_Accounts'],
            'Validation_Strategy': 'Full Census',
            'Sample_Size': 1,
            'Reason': 'Single account cluster',
            'Expected_Outcome': 'Confirm classification',
            'Validation_Methods': 'Website + Product Data + Statistical',
            'Estimated_Hours': 0.5
        },

        # TIER 3 - ALREADY VALIDATED (5 clusters, 474 accounts) - Documentation Only
        {
            'Tier': 3,
            'Priority': 20,
            'Cluster': 'General Wholesale/Distribution',
            'Total_Accounts': cluster_stats.loc['General Wholesale/Distribution', 'Total_Accounts'],
            'Validation_Strategy': 'Already Validated (78.1%)',
            'Sample_Size': 336,
            'Reason': 'Validated via product data (78.1% true general)',
            'Expected_Outcome': 'Documentation update only',
            'Validation_Methods': 'N/A (Already validated)',
            'Estimated_Hours': 0
        },
        {
            'Tier': 3,
            'Priority': 21,
            'Cluster': 'Building Materials & Construction',
            'Total_Accounts': cluster_stats.loc['Building Materials & Construction', 'Total_Accounts'],
            'Validation_Strategy': 'Already Validated (100%)',
            'Sample_Size': 5,
            'Reason': 'Validated via website (100% accuracy)',
            'Expected_Outcome': 'Documentation update only',
            'Validation_Methods': 'N/A (Already validated)',
            'Estimated_Hours': 0
        },
        {
            'Tier': 3,
            'Priority': 22,
            'Cluster': 'Industrial Equipment & Machinery',
            'Total_Accounts': cluster_stats.loc['Industrial Equipment & Machinery', 'Total_Accounts'],
            'Validation_Strategy': 'Already Validated (96%)',
            'Sample_Size': 0,  # Changed from 'Multiple' to 0
            'Reason': 'Validated via website (96% accuracy)',
            'Expected_Outcome': 'Documentation update only',
            'Validation_Methods': 'N/A (Already validated)',
            'Estimated_Hours': 0
        },
        {
            'Tier': 3,
            'Priority': 23,
            'Cluster': 'Chemicals, Plastics & Rubber',
            'Total_Accounts': cluster_stats.loc['Chemicals, Plastics & Rubber', 'Total_Accounts'],
            'Validation_Strategy': 'Already Validated (92%)',
            'Sample_Size': 0,  # Changed from 'Multiple' to 0
            'Reason': 'Validated via website (92% accuracy)',
            'Expected_Outcome': 'Documentation update only',
            'Validation_Methods': 'N/A (Already validated)',
            'Estimated_Hours': 0
        },
        {
            'Tier': 3,
            'Priority': 24,
            'Cluster': 'Electronics & Technology',
            'Total_Accounts': cluster_stats.loc['Electronics & Technology', 'Total_Accounts'],
            'Validation_Strategy': 'Already Validated (95%)',
            'Sample_Size': 0,  # Changed from 'Multiple' to 0
            'Reason': 'Validated via website (95% accuracy)',
            'Expected_Outcome': 'Documentation update only',
            'Validation_Methods': 'N/A (Already validated)',
            'Estimated_Hours': 0
        },
    ]

    # Create DataFrame
    queue_df = pd.DataFrame(validation_queue)

    # Add total MRR and strategic importance
    queue_df['Total_MRR'] = queue_df['Cluster'].map(cluster_stats['Total_MRR'].to_dict())
    queue_df['Total_MRR'] = queue_df['Total_MRR'].fillna(0).round(2)

    # Reorder columns
    queue_df = queue_df[['Tier', 'Priority', 'Cluster', 'Total_Accounts', 'Total_MRR',
                         'Validation_Strategy', 'Sample_Size', 'Reason',
                         'Expected_Outcome', 'Validation_Methods', 'Estimated_Hours']]

    # Save to CSV
    output_file = 'validation_queue_prioritized.csv'
    queue_df.to_csv(output_file, index=False)
    print(f"\nSaved validation queue to: {output_file}")

    # Display summary
    print("\n" + "="*120)
    print("VALIDATION QUEUE SUMMARY")
    print("="*120)

    tier_summary = queue_df.groupby('Tier').agg({
        'Cluster': 'count',
        'Total_Accounts': 'sum',
        'Sample_Size': 'sum',
        'Estimated_Hours': 'sum'
    }).rename(columns={'Cluster': 'Clusters'})

    print(f"\n{'Tier':<6} {'Clusters':>10} {'Total Accts':>13} {'Sample Size':>13} {'Est. Hours':>12}")
    print("-"*60)
    for tier in [1, 2, 3]:
        if tier in tier_summary.index:
            row = tier_summary.loc[tier]
            print(f"TIER {tier} {int(row['Clusters']):10d} {int(row['Total_Accounts']):13d} {int(row['Sample_Size']):13d} {row['Estimated_Hours']:12.1f}")

    total_hours = queue_df['Estimated_Hours'].sum()
    print(f"\nTOTAL ESTIMATED HOURS: {total_hours:.1f} hours")

    # Display detailed queue
    print("\n" + "="*120)
    print("TIER 1 - HIGH PRIORITY (8 clusters)")
    print("="*120)
    print(f"\n{'Pri':>3} {'Cluster':<40} {'Accts':>6} {'Strategy':<20} {'Hours':>6}")
    print("-"*80)

    for _, row in queue_df[queue_df['Tier'] == 1].iterrows():
        cluster_name = row['Cluster'][:38]
        strategy = row['Validation_Strategy'][:18]
        print(f"{int(row['Priority']):3d}. {cluster_name:<40} {int(row['Total_Accounts']):6d} {strategy:<20} {row['Estimated_Hours']:6.1f}h")

    print("\n" + "="*120)
    print("TIER 2 - MEDIUM PRIORITY (11 clusters)")
    print("="*120)
    print(f"\n{'Pri':>3} {'Cluster':<40} {'Accts':>6} {'Strategy':<20} {'Hours':>6}")
    print("-"*80)

    for _, row in queue_df[queue_df['Tier'] == 2].iterrows():
        cluster_name = row['Cluster'][:38]
        strategy = row['Validation_Strategy'][:18]
        print(f"{int(row['Priority']):3d}. {cluster_name:<40} {int(row['Total_Accounts']):6d} {strategy:<20} {row['Estimated_Hours']:6.1f}h")

    print("\n" + "="*120)
    print("TIER 3 - ALREADY VALIDATED (5 clusters) - Documentation Only")
    print("="*120)
    print(f"\n{'Pri':>3} {'Cluster':<40} {'Accts':>6} {'Accuracy':<20}")
    print("-"*80)

    for _, row in queue_df[queue_df['Tier'] == 3].iterrows():
        cluster_name = row['Cluster'][:38]
        accuracy = row['Validation_Strategy'][:18]
        print(f"{int(row['Priority']):3d}. {cluster_name:<40} {int(row['Total_Accounts']):6d} {accuracy:<20}")

    print("\n" + "="*80)
    print("Validation queue created successfully!")
    print("="*80)

    return queue_df


if __name__ == '__main__':
    queue_df = create_validation_queue()
