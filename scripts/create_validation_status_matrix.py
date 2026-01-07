#!/usr/bin/env python3
"""
Validation Status Matrix Creator
Documents which clusters have been validated, partially validated, or not validated yet.

Author: Evidence-Based Analysis
Date: January 7, 2026
"""

import pandas as pd

def create_validation_status_matrix():
    """
    Create a matrix showing validation status for all 23 industry clusters.
    """
    print("Creating Validation Status Matrix...")
    print("="*80)

    # Load data to get cluster sizes
    df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')
    active = df[df['Active?'] == True].copy()

    cluster_counts = active.groupby('Industry_Cluster_Enhanced_V2').size().to_dict()

    # Define validation status for each cluster
    validation_status = [
        # TIER 3 - Already Validated (DO NOT RE-VALIDATE)
        {
            'Cluster': 'Building Materials & Construction',
            'Total_Accounts': cluster_counts.get('Building Materials & Construction', 0),
            'Status': 'Validated',
            'Accuracy_Rate': '100%',
            'Validation_Method': 'Website Verification',
            'Sample_Size': '5 accounts',
            'Issues_Found': 'None',
            'Confidence_Level': 'Very High',
            'Notes': 'All 5 sampled accounts verified via website. 100% accuracy confirmed.'
        },
        {
            'Cluster': 'Industrial Equipment & Machinery',
            'Total_Accounts': cluster_counts.get('Industrial Equipment & Machinery', 0),
            'Status': 'Validated',
            'Accuracy_Rate': '96%',
            'Validation_Method': 'Website Verification',
            'Sample_Size': 'Multiple accounts',
            'Issues_Found': 'Minor edge cases',
            'Confidence_Level': 'Very High',
            'Notes': '96% accuracy confirmed via website validation.'
        },
        {
            'Cluster': 'Chemicals, Plastics & Rubber',
            'Total_Accounts': cluster_counts.get('Chemicals, Plastics & Rubber', 0),
            'Status': 'Validated',
            'Accuracy_Rate': '92%',
            'Validation_Method': 'Website Verification',
            'Sample_Size': 'Multiple accounts',
            'Issues_Found': 'Minor mis-classifications',
            'Confidence_Level': 'High',
            'Notes': '92% accuracy confirmed via website validation.'
        },
        {
            'Cluster': 'Electronics & Technology',
            'Total_Accounts': cluster_counts.get('Electronics & Technology', 0),
            'Status': 'Validated',
            'Accuracy_Rate': '95%',
            'Validation_Method': 'Website Verification',
            'Sample_Size': 'Multiple accounts',
            'Issues_Found': 'Minor edge cases',
            'Confidence_Level': 'Very High',
            'Notes': '95% accuracy confirmed via website validation.'
        },
        {
            'Cluster': 'General Wholesale/Distribution',
            'Total_Accounts': cluster_counts.get('General Wholesale/Distribution', 0),
            'Status': 'Validated',
            'Accuracy_Rate': '78.1% (True General)',
            'Validation_Method': 'Product Data (Evidence-Based)',
            'Sample_Size': '336 accounts (79.8% coverage)',
            'Issues_Found': '7 specialized accounts flagged (3 logistics, 3 industrial, 1 office)',
            'Confidence_Level': 'High',
            'Notes': 'Full evidence-based validation using actual sold items. 78.1% confirmed as truly general wholesalers. Sub-clustering invalidated (98%+ error rate).'
        },

        # TIER 1 - Partially Validated (NEED FOLLOW-UP)
        {
            'Cluster': 'Medical Equipment & Supplies',
            'Total_Accounts': cluster_counts.get('Medical Equipment & Supplies', 0),
            'Status': 'Partially Validated',
            'Accuracy_Rate': '80%',
            'Validation_Method': 'Website Verification (Partial)',
            'Sample_Size': 'Partial sample',
            'Issues_Found': '1 equine company mis-classified (finishfirstequine)',
            'Confidence_Level': 'Medium-High',
            'Notes': 'NEED FULL VALIDATION: Remove equine/veterinary companies. Expected ~13 true medical, ~3 to re-classify.'
        },
        {
            'Cluster': 'Food & Beverage Dist/Mfg',
            'Total_Accounts': cluster_counts.get('Food & Beverage Dist/Mfg', 0),
            'Status': 'Partially Validated',
            'Accuracy_Rate': '67%',
            'Validation_Method': 'Keyword Fix (V2)',
            'Sample_Size': '30 accounts (V1 had 284, V2 reduced to 30)',
            'Issues_Found': 'V1 had 89% mis-classification due to "ale" substring bug (fixed in V2). ~10 false positives remain.',
            'Confidence_Level': 'Medium',
            'Notes': 'NEED FULL VALIDATION: V2 fixed substring bug but accuracy still only 67%. Expected ~20 true F&B, ~10 to remove.'
        },
        {
            'Cluster': 'Apparel & Textiles',
            'Total_Accounts': cluster_counts.get('Apparel & Textiles', 0),
            'Status': 'Partially Validated',
            'Accuracy_Rate': '68% (13/(13+40))',
            'Validation_Method': 'Website Verification (Partial)',
            'Sample_Size': 'Partial sample',
            'Issues_Found': '40 metal fabrication companies mis-classified',
            'Confidence_Level': 'Medium',
            'Notes': 'CRITICAL ISSUE: 40 metal fabrication companies need to move to Metal Fabrication & Steel cluster. Expected ~13 true apparel/textiles remain.'
        },
        {
            'Cluster': 'Furniture & Home Furnishings',
            'Total_Accounts': cluster_counts.get('Furniture & Home Furnishings', 0),
            'Status': 'Partially Validated',
            'Accuracy_Rate': '86%',
            'Validation_Method': 'Website Verification (Partial)',
            'Sample_Size': 'Partial sample',
            'Issues_Found': 'Some kitchen cabinets (may belong in Building Materials)',
            'Confidence_Level': 'Medium-High',
            'Notes': 'NEED FULL VALIDATION: Expected ~12 true furniture, ~2 to re-classify.'
        },

        # TIER 1 & 2 - Unvalidated
        {
            'Cluster': 'General/Specialty Manufacturing',
            'Total_Accounts': cluster_counts.get('General/Specialty Manufacturing', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'LARGEST UNVALIDATED CLUSTER. Requires stratified sampling (60 accounts: 20 low + 20 mid + 20 high MRR).'
        },
        {
            'Cluster': 'General Retail',
            'Total_Accounts': cluster_counts.get('General Retail', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': '3RD LARGEST CLUSTER. Requires stratified sampling (50 accounts). Validate B2C focus vs B2B wholesale.'
        },
        {
            'Cluster': 'Metal Fabrication & Steel',
            'Total_Accounts': cluster_counts.get('Metal Fabrication & Steel', 0) + 40,  # Add 40 from Apparel
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Will receive 40 accounts from Apparel & Textiles',
            'Confidence_Level': 'Unknown',
            'Notes': 'WILL GROW TO 44 ACCOUNTS. Validate all 44: 4 current + 40 incoming from Apparel.'
        },
        {
            'Cluster': 'Services & Other',
            'Total_Accounts': 15,  # Estimate
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Catch-all category - most should be re-classified',
            'Confidence_Level': 'Unknown',
            'Notes': 'CATCH-ALL CLUSTER. Expected: Most accounts should move to specific clusters.'
        },
        {
            'Cluster': 'Electrical & Lighting Equipment',
            'Total_Accounts': cluster_counts.get('Electrical & Lighting Equipment', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Small cluster. Full census validation (all accounts).'
        },
        {
            'Cluster': 'Packaging & Printing',
            'Total_Accounts': cluster_counts.get('Packaging & Printing', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Small cluster. Full census validation (all accounts).'
        },
        {
            'Cluster': 'Office Supplies & Equipment',
            'Total_Accounts': cluster_counts.get('Office Supplies & Equipment', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Small cluster. Full census validation (all accounts).'
        },
        {
            'Cluster': 'Safety & Security Equipment',
            'Total_Accounts': cluster_counts.get('Safety & Security Equipment', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Small cluster. Full census validation (all accounts).'
        },
        {
            'Cluster': 'Sporting Goods & Fitness Equipment',
            'Total_Accounts': cluster_counts.get('Sporting Goods & Fitness Equipment', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Small cluster. Full census validation (all accounts).'
        },
        {
            'Cluster': 'Signs, Graphics & Displays',
            'Total_Accounts': cluster_counts.get('Signs, Graphics & Displays', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Tiny cluster (1 account). Full census validation.'
        },
        {
            'Cluster': 'Agriculture & Greenhouse/Nursery',
            'Total_Accounts': cluster_counts.get('Agriculture & Greenhouse/Nursery', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Small cluster. Full census validation (all accounts).'
        },
        {
            'Cluster': 'Wood Products & Lumber',
            'Total_Accounts': cluster_counts.get('Wood Products & Lumber', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Tiny cluster (1 account). Full census validation.'
        },
        {
            'Cluster': 'HVAC & Refrigeration Equipment',
            'Total_Accounts': cluster_counts.get('HVAC & Refrigeration Equipment', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Tiny cluster (2 accounts). Full census validation.'
        },
        {
            'Cluster': 'Manufacturer Representatives',
            'Total_Accounts': cluster_counts.get('Manufacturer Representatives', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Small cluster. Full census validation (all accounts).'
        },
        {
            'Cluster': 'Automotive & Transportation',
            'Total_Accounts': cluster_counts.get('Automotive & Transportation', 0),
            'Status': 'Not Validated',
            'Accuracy_Rate': 'Unknown',
            'Validation_Method': 'None',
            'Sample_Size': 'None',
            'Issues_Found': 'Unknown',
            'Confidence_Level': 'Unknown',
            'Notes': 'Tiny cluster (2 accounts). Full census validation. 100% website + product coverage!'
        },
    ]

    # Create DataFrame
    validation_df = pd.DataFrame(validation_status)

    # Reorder columns
    validation_df = validation_df[['Cluster', 'Total_Accounts', 'Status', 'Accuracy_Rate',
                                     'Validation_Method', 'Sample_Size', 'Issues_Found',
                                     'Confidence_Level', 'Notes']]

    # Sort by status (Validated > Partially Validated > Not Validated), then by total accounts
    status_order = {'Validated': 1, 'Partially Validated': 2, 'Not Validated': 3}
    validation_df['_sort_order'] = validation_df['Status'].map(status_order)
    validation_df = validation_df.sort_values(['_sort_order', 'Total_Accounts'], ascending=[True, False])
    validation_df = validation_df.drop('_sort_order', axis=1)

    # Save to CSV
    output_file = 'validation_status_matrix.csv'
    validation_df.to_csv(output_file, index=False)
    print(f"\nSaved validation status matrix to: {output_file}")

    # Display summary
    print("\n" + "="*120)
    print("VALIDATION STATUS SUMMARY")
    print("="*120)

    status_summary = validation_df.groupby('Status').agg({
        'Total_Accounts': ['count', 'sum']
    })
    status_summary.columns = ['Clusters', 'Total_Accounts']

    print(f"\n{'Status':<20} {'Clusters':>10} {'Accounts':>12}")
    print("-"*45)
    for status in ['Validated', 'Partially Validated', 'Not Validated']:
        if status in status_summary.index:
            row = status_summary.loc[status]
            print(f"{status:<20} {int(row['Clusters']):10d} {int(row['Total_Accounts']):12d}")

    # Display detailed table
    print("\n" + "="*120)
    print("DETAILED VALIDATION STATUS")
    print("="*120)
    print(f"\n{'Cluster':<40} {'Accts':>6} {'Status':<20} {'Accuracy':<10} {'Notes':<40}")
    print("-"*120)

    for _, row in validation_df.iterrows():
        cluster_name = row['Cluster'][:38]
        notes = row['Notes'][:38] if pd.notna(row['Notes']) else ''
        print(f"{cluster_name:<40} {int(row['Total_Accounts']):6d} {row['Status']:<20} {row['Accuracy_Rate']:<10} {notes:<40}")

    print("\n" + "="*80)
    print("Validation status matrix created successfully!")
    print("="*80)

    return validation_df


if __name__ == '__main__':
    validation_df = create_validation_status_matrix()
