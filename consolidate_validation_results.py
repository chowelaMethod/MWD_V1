#!/usr/bin/env python3
"""
Validation Results Consolidation Script
Merges website, product, and statistical validation results into final report.

Author: Evidence-Based Analysis
Date: January 7, 2026
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def calculate_composite_confidence(website_conf: float, product_conf: float,
                                     statistical_conf: str) -> Tuple[float, str]:
    """
    Calculate composite confidence score from multiple validation sources.

    Scoring logic:
    - 3 sources agree (high confidence): 95%
    - 2 sources agree: 75-85%
    - 1 source only: 50-60%
    - Sources conflict: Flag for manual review

    Args:
        website_conf: Website validation confidence (0-100)
        product_conf: Product validation confidence (0-100)
        statistical_conf: Statistical confidence ('High' or 'Low')

    Returns:
        Tuple of (composite_confidence, confidence_level)
    """
    # Convert statistical confidence to numeric
    statistical_score = 100 if statistical_conf == 'High' else 30

    # Count available sources
    sources = []
    if not pd.isna(website_conf) and website_conf > 0:
        sources.append(('Website', website_conf))
    if not pd.isna(product_conf) and product_conf > 0:
        sources.append(('Product', product_conf))
    sources.append(('Statistical', statistical_score))

    num_sources = len(sources)

    if num_sources == 3:
        # All 3 sources available
        avg_conf = (website_conf + product_conf + statistical_score) / 3

        if avg_conf >= 70:
            composite = 95  # High confidence
            level = 'Very High (3 sources agree)'
        elif avg_conf >= 50:
            composite = 85  # Good confidence
            level = 'High (3 sources, medium agreement)'
        else:
            composite = 60  # Conflicts
            level = 'Medium (3 sources, conflicts)'

    elif num_sources == 2:
        # 2 sources available
        conf1, conf2 = sources[0][1], sources[1][1]
        source_names = f"{sources[0][0]} + {sources[1][1]}"

        avg_conf = (conf1 + conf2) / 2

        if avg_conf >= 60:
            composite = 80  # High-medium confidence
            level = f'High ({sources[0][0]} + {sources[1][0]} agree)'
        elif avg_conf >= 40:
            composite = 70  # Medium confidence
            level = f'Medium ({sources[0][0]} + {sources[1][0]})'
        else:
            composite = 50  # Low confidence
            level = f'Low ({sources[0][0]} + {sources[1][0]} conflict)'

    else:
        # Only 1 source
        conf = sources[0][1]
        source_name = sources[0][0]

        if conf >= 70:
            composite = 65  # Medium confidence
            level = f'Medium ({source_name} only, high)'
        elif conf >= 40:
            composite = 50  # Low-medium confidence
            level = f'Low-Medium ({source_name} only)'
        else:
            composite = 30  # Low confidence
            level = f'Low ({source_name} only, weak)'

    return composite, level


def determine_recommendation(composite_confidence: float, matches_expected: bool,
                               conflict_cluster: str = None) -> str:
    """
    Determine final recommendation based on confidence and matches.

    Returns: 'Accept', 'Accept with Monitoring', 'Review', or 'Re-classify'
    """
    if matches_expected:
        if composite_confidence >= 80:
            return 'Accept'
        elif composite_confidence >= 60:
            return 'Accept with Monitoring'
        else:
            return 'Review'
    else:
        # Doesn't match expected
        if composite_confidence >= 70 and conflict_cluster:
            return f'Re-classify to {conflict_cluster}'
        elif composite_confidence >= 50:
            return 'Review (Possible Mis-classification)'
        else:
            return 'Review (Unclear Classification)'


def consolidate_validation_results(website_file: str = None,
                                     product_file: str = None,
                                     statistical_file: str = None,
                                     output_file: str = 'final_validation_report.csv'):
    """
    Consolidate validation results from all sources.

    Args:
        website_file: Website validation results CSV
        product_file: Product validation results CSV
        statistical_file: Statistical validation results CSV
        output_file: Output consolidated report CSV
    """
    print("="*80)
    print("VALIDATION RESULTS CONSOLIDATION")
    print("="*80)

    # Load main dataset to get all accounts
    print("\nLoading main dataset...")
    df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')
    active = df[df['Active?'] == True].copy()

    base_df = active[['Account Name', 'Industry_Cluster_Enhanced_V2', 'MRR_Calculated',
                       'Users', 'Website', 'Primary_Business_Type']].copy()
    base_df = base_df.rename(columns={
        'Account Name': 'Account_Name',
        'Industry_Cluster_Enhanced_V2': 'Current_Cluster'
    })

    print(f"Base accounts loaded: {len(base_df)}")

    # Load validation results
    website_df = None
    product_df = None
    statistical_df = None

    if website_file:
        try:
            website_df = pd.read_csv(website_file)
            print(f"Website validation loaded: {len(website_df)} accounts")
        except FileNotFoundError:
            print(f"Website file not found: {website_file}")

    if product_file:
        try:
            product_df = pd.read_csv(product_file)
            print(f"Product validation loaded: {len(product_df)} accounts")
        except FileNotFoundError:
            print(f"Product file not found: {product_file}")

    if statistical_file:
        try:
            statistical_df = pd.read_csv(statistical_file)
            print(f"Statistical validation loaded: {len(statistical_df)} accounts")
        except FileNotFoundError:
            print(f"Statistical file not found: {statistical_file}")

    # Merge results
    print("\n" + "="*80)
    print("MERGING VALIDATION SOURCES")
    print("="*80)

    consolidated = base_df.copy()

    # Merge website results
    if website_df is not None:
        website_cols = ['Account_Name', 'Website_Confidence', 'Website_Classification']
        if all(col in website_df.columns for col in website_cols):
            consolidated = consolidated.merge(
                website_df[website_cols],
                on='Account_Name',
                how='left'
            )
            print(f"Merged website validation: {consolidated['Website_Confidence'].notna().sum()} accounts")

    # Merge product results
    if product_df is not None:
        product_cols = ['Account_Name', 'Product_Confidence', 'Product_Classification',
                        'Matches_Expected', 'Top_3_Clusters']
        available_cols = ['Account_Name'] + [col for col in product_cols[1:] if col in product_df.columns]

        consolidated = consolidated.merge(
            product_df[available_cols],
            on='Account_Name',
            how='left'
        )
        print(f"Merged product validation: {consolidated['Product_Confidence'].notna().sum()} accounts")

    # Merge statistical results
    if statistical_df is not None:
        stat_cols = ['Account_Name', 'Statistical_Confidence', 'Is_Overall_Outlier',
                     'MRR_ZScore', 'Users_ZScore']
        available_cols = ['Account_Name'] + [col for col in stat_cols[1:] if col in statistical_df.columns]

        consolidated = consolidated.merge(
            statistical_df[available_cols],
            on='Account_Name',
            how='left'
        )
        print(f"Merged statistical validation: {consolidated['Statistical_Confidence'].notna().sum()} accounts")

    # Calculate composite confidence scores
    print("\n" + "="*80)
    print("CALCULATING COMPOSITE CONFIDENCE SCORES")
    print("="*80)

    consolidated['Composite_Confidence'] = 0.0
    consolidated['Confidence_Level'] = ''
    consolidated['Recommended_Action'] = ''
    consolidated['Sources_Used'] = ''

    for idx, row in consolidated.iterrows():
        website_conf = row.get('Website_Confidence', np.nan)
        product_conf = row.get('Product_Confidence', np.nan)
        statistical_conf = row.get('Statistical_Confidence', 'High')

        # Calculate composite confidence
        composite, level = calculate_composite_confidence(
            website_conf, product_conf, statistical_conf
        )

        consolidated.at[idx, 'Composite_Confidence'] = composite
        consolidated.at[idx, 'Confidence_Level'] = level

        # Track sources used
        sources = []
        if not pd.isna(website_conf) and website_conf > 0:
            sources.append('W')
        if not pd.isna(product_conf) and product_conf > 0:
            sources.append('P')
        if statistical_conf == 'High':
            sources.append('S')

        consolidated.at[idx, 'Sources_Used'] = '+'.join(sources) if sources else 'None'

        # Determine recommendation
        matches = row.get('Matches_Expected', True)  # Default to True if not available
        conflict_cluster = row.get('Product_Classification', None)

        recommendation = determine_recommendation(composite, matches, conflict_cluster)
        consolidated.at[idx, 'Recommended_Action'] = recommendation

    # Reorder columns for output
    output_columns = [
        'Account_Name', 'Current_Cluster', 'Composite_Confidence', 'Confidence_Level',
        'Sources_Used', 'Recommended_Action'
    ]

    # Add optional columns if they exist
    optional_cols = ['Website_Confidence', 'Product_Confidence', 'Statistical_Confidence',
                     'Product_Classification', 'Top_3_Clusters', 'Is_Overall_Outlier',
                     'MRR_Calculated', 'Users', 'Primary_Business_Type']

    for col in optional_cols:
        if col in consolidated.columns:
            output_columns.append(col)

    final_df = consolidated[output_columns].copy()

    # Save results
    final_df.to_csv(output_file, index=False)
    print(f"\nSaved consolidated results to: {output_file}")

    # Summary statistics
    print("\n" + "="*80)
    print("CONSOLIDATION SUMMARY")
    print("="*80)

    total = len(final_df)
    print(f"\nTotal accounts in report: {total}")

    # Confidence distribution
    high_conf = (final_df['Composite_Confidence'] >= 80).sum()
    medium_conf = ((final_df['Composite_Confidence'] >= 60) &
                   (final_df['Composite_Confidence'] < 80)).sum()
    low_conf = (final_df['Composite_Confidence'] < 60).sum()

    print(f"\nConfidence Distribution:")
    print(f"  - High (80-100%): {high_conf} ({high_conf/total*100:.1f}%)")
    print(f"  - Medium (60-79%): {medium_conf} ({medium_conf/total*100:.1f}%)")
    print(f"  - Low (<60%): {low_conf} ({low_conf/total*100:.1f}%)")

    # Sources used
    print(f"\nValidation Sources Used:")
    source_counts = final_df['Sources_Used'].value_counts()
    for source, count in source_counts.items():
        print(f"  - {source}: {count} accounts ({count/total*100:.1f}%)")

    # Recommendations
    print(f"\nRecommendations:")
    rec_counts = final_df['Recommended_Action'].value_counts()
    for rec, count in rec_counts.items():
        print(f"  - {rec}: {count} accounts ({count/total*100:.1f}%)")

    # Accounts to re-classify
    reclassify = final_df[final_df['Recommended_Action'].str.contains('Re-classify', na=False)]
    if len(reclassify) > 0:
        print(f"\n" + "="*80)
        print(f"ACCOUNTS RECOMMENDED FOR RE-CLASSIFICATION: {len(reclassify)}")
        print("="*80)

        # Save to separate file
        reclassify_file = 'accounts_to_reclassify.csv'
        reclassify.to_csv(reclassify_file, index=False)
        print(f"Saved to: {reclassify_file}")

        print("\nTop 10 Re-classification Recommendations:")
        for _, row in reclassify.head(10).iterrows():
            print(f"  {row['Account_Name']}")
            print(f"    From: {row['Current_Cluster']}")
            print(f"    To: {row.get('Product_Classification', 'Unknown')}")
            print(f"    Confidence: {row['Composite_Confidence']:.0f}%")
            print()

    return final_df


if __name__ == '__main__':
    # Example: Consolidate pilot test results
    print("\nPILOT TEST MODE: Building Materials & Construction")
    print("Consolidating validation results from all sources")
    print("-"*80)

    results = consolidate_validation_results(
        website_file='website_validation_pilot_test.csv',  # If exists
        product_file='product_validation_pilot_test.csv',
        statistical_file='statistical_validation_pilot_test.csv',
        output_file='consolidated_validation_pilot_test.csv'
    )

    print("\n" + "="*80)
    print("Pilot test consolidation complete!")
    print("Review consolidated_validation_pilot_test.csv for final results")
    print("="*80)
