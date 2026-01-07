#!/usr/bin/env python3
"""
Statistical Validation Script
Validates cluster classifications using statistical coherence checks.
Flags outliers that may be mis-classified.

Author: Evidence-Based Analysis
Date: January 7, 2026
"""

import pandas as pd
import numpy as np
from typing import Dict, List

def calculate_cluster_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate statistical profiles for each cluster.
    Returns DataFrame with cluster metrics.
    """
    profiles = df.groupby('Industry_Cluster_Enhanced_V2').agg({
        'Account Name': 'count',
        'MRR_Calculated': ['mean', 'median', 'std', 'min', 'max'],
        'Users': ['mean', 'median', 'std', 'min', 'max'],
        'Custom_Screens_Total': ['mean', 'median', 'std', 'min', 'max']
    }).round(2)

    # Flatten column names
    profiles.columns = ['_'.join(col).strip() if col[1] else col[0]
                       for col in profiles.columns.values]

    profiles = profiles.rename(columns={
        'Account Name_count': 'Total_Accounts',
        'MRR_Calculated_mean': 'MRR_Mean',
        'MRR_Calculated_median': 'MRR_Median',
        'MRR_Calculated_std': 'MRR_StdDev',
        'MRR_Calculated_min': 'MRR_Min',
        'MRR_Calculated_max': 'MRR_Max',
        'Users_mean': 'Users_Mean',
        'Users_median': 'Users_Median',
        'Users_std': 'Users_StdDev',
        'Users_min': 'Users_Min',
        'Users_max': 'Users_Max',
        'Custom_Screens_Total_mean': 'Screens_Mean',
        'Custom_Screens_Total_median': 'Screens_Median',
        'Custom_Screens_Total_std': 'Screens_StdDev',
        'Custom_Screens_Total_min': 'Screens_Min',
        'Custom_Screens_Total_max': 'Screens_Max'
    })

    return profiles


def calculate_z_scores(value: float, mean: float, std: float) -> float:
    """
    Calculate z-score (standard deviations from mean).
    """
    if pd.isna(value) or pd.isna(mean) or pd.isna(std) or std == 0:
        return 0.0
    return (value - mean) / std


def detect_outliers(account: pd.Series, cluster_profile: pd.Series,
                     threshold: float = 2.5) -> Dict:
    """
    Detect if account is a statistical outlier in its cluster.

    Args:
        account: Account data row
        cluster_profile: Cluster statistical profile
        threshold: Z-score threshold for outlier (default 2.5 std dev)

    Returns:
        Dict with outlier flags and z-scores
    """
    mrr = account.get('MRR_Calculated', 0)
    users = account.get('Users', 0)
    screens = account.get('Custom_Screens_Total', 0)

    # Calculate z-scores
    mrr_z = calculate_z_scores(mrr, cluster_profile['MRR_Mean'], cluster_profile['MRR_StdDev'])
    users_z = calculate_z_scores(users, cluster_profile['Users_Mean'], cluster_profile['Users_StdDev'])
    screens_z = calculate_z_scores(screens, cluster_profile['Screens_Mean'], cluster_profile['Screens_StdDev'])

    # Determine if outlier
    is_mrr_outlier = abs(mrr_z) > threshold
    is_users_outlier = abs(users_z) > threshold
    is_screens_outlier = abs(screens_z) > threshold

    # Overall outlier if 2+ metrics are outliers
    is_overall_outlier = sum([is_mrr_outlier, is_users_outlier, is_screens_outlier]) >= 2

    return {
        'MRR_ZScore': round(mrr_z, 2),
        'Users_ZScore': round(users_z, 2),
        'Screens_ZScore': round(screens_z, 2),
        'Is_MRR_Outlier': is_mrr_outlier,
        'Is_Users_Outlier': is_users_outlier,
        'Is_Screens_Outlier': is_screens_outlier,
        'Is_Overall_Outlier': is_overall_outlier,
        'Outlier_Score': abs(mrr_z) + abs(users_z) + abs(screens_z),  # Combined outlier score
        'MRR': mrr,
        'Users': users,
        'Screens': screens,
        'Cluster_MRR_Mean': cluster_profile['MRR_Mean'],
        'Cluster_Users_Mean': cluster_profile['Users_Mean']
    }


def validate_cluster_statistical(cluster_name: str = None,
                                   sample_size: int = None,
                                   outlier_threshold: float = 2.5,
                                   output_file: str = 'statistical_validation_results.csv'):
    """
    Validate accounts via statistical coherence checks.

    Args:
        cluster_name: If specified, only validate this cluster
        sample_size: If specified, limit to N accounts per cluster
        outlier_threshold: Z-score threshold for outlier detection (default 2.5)
        output_file: Output CSV filename
    """
    print("="*80)
    print("STATISTICAL VALIDATION")
    print("="*80)

    # Load data
    print("\nLoading dataset...")
    df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')
    active = df[df['Active?'] == True].copy()

    # Calculate Custom_Screens_Total if not present
    if 'Custom_Screens_Total' not in active.columns:
        active['Custom_Screens_Total'] = (
            active['Custom Screens New'].fillna(0) +
            active['Custom Screens Classic'].fillna(0)
        )

    # Fill NaN values
    active['MRR_Calculated'] = active['MRR_Calculated'].fillna(0)
    active['Users'] = active['Users'].fillna(0)
    active['Custom_Screens_Total'] = active['Custom_Screens_Total'].fillna(0)

    print(f"Total active accounts: {len(active)}")

    # Calculate cluster profiles
    print("\nCalculating cluster statistical profiles...")
    cluster_profiles = calculate_cluster_profiles(active)
    print(f"Cluster profiles calculated for {len(cluster_profiles)} clusters")

    # Filter by cluster if specified
    if cluster_name:
        active = active[active['Industry_Cluster_Enhanced_V2'] == cluster_name]
        print(f"\nFiltering to cluster: {cluster_name}")
        print(f"Accounts in cluster: {len(active)}")

    # Sample if specified
    if sample_size and len(active) > sample_size:
        active = active.sample(n=sample_size, random_state=42)
        print(f"\nSampling {sample_size} accounts for validation")

    # Validate each account
    print("\n" + "="*80)
    print("VALIDATION PROCESS")
    print("="*80)
    print(f"Outlier threshold: ±{outlier_threshold} standard deviations")

    results = []
    for idx, row in active.iterrows():
        account = row['Account Name']
        cluster = row['Industry_Cluster_Enhanced_V2']

        # Get cluster profile
        if cluster not in cluster_profiles.index:
            continue

        cluster_profile = cluster_profiles.loc[cluster]

        # Detect outliers
        outlier_analysis = detect_outliers(row, cluster_profile, outlier_threshold)

        result = {
            'Account_Name': account,
            'Cluster': cluster,
            'MRR': round(outlier_analysis['MRR'], 2),
            'Users': int(outlier_analysis['Users']),
            'Custom_Screens': int(outlier_analysis['Screens']),
            'Cluster_MRR_Mean': round(outlier_analysis['Cluster_MRR_Mean'], 2),
            'Cluster_Users_Mean': round(outlier_analysis['Cluster_Users_Mean'], 2),
            'MRR_ZScore': outlier_analysis['MRR_ZScore'],
            'Users_ZScore': outlier_analysis['Users_ZScore'],
            'Screens_ZScore': outlier_analysis['Screens_ZScore'],
            'Is_MRR_Outlier': outlier_analysis['Is_MRR_Outlier'],
            'Is_Users_Outlier': outlier_analysis['Is_Users_Outlier'],
            'Is_Screens_Outlier': outlier_analysis['Is_Screens_Outlier'],
            'Is_Overall_Outlier': outlier_analysis['Is_Overall_Outlier'],
            'Outlier_Score': round(outlier_analysis['Outlier_Score'], 2),
            'Statistical_Confidence': 'Low' if outlier_analysis['Is_Overall_Outlier'] else 'High',
            'Notes': ''
        }

        # Add notes for outliers
        if outlier_analysis['Is_Overall_Outlier']:
            outlier_flags = []
            if outlier_analysis['Is_MRR_Outlier']:
                outlier_flags.append(f"MRR (z={outlier_analysis['MRR_ZScore']:.1f})")
            if outlier_analysis['Is_Users_Outlier']:
                outlier_flags.append(f"Users (z={outlier_analysis['Users_ZScore']:.1f})")
            if outlier_analysis['Is_Screens_Outlier']:
                outlier_flags.append(f"Screens (z={outlier_analysis['Screens_ZScore']:.1f})")

            result['Notes'] = f"STATISTICAL OUTLIER: {', '.join(outlier_flags)}"

        results.append(result)

        if (idx + 1) % 100 == 0:
            print(f"Processed {len(results)} accounts...")

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Save results
    results_df.to_csv(output_file, index=False)
    print(f"\nSaved validation results to: {output_file}")

    # Summary statistics
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)

    total_validated = len(results_df)
    overall_outliers = results_df['Is_Overall_Outlier'].sum()
    mrr_outliers = results_df['Is_MRR_Outlier'].sum()
    users_outliers = results_df['Is_Users_Outlier'].sum()
    screens_outliers = results_df['Is_Screens_Outlier'].sum()

    print(f"\nTotal accounts validated: {total_validated}")
    print(f"Overall outliers (2+ metrics): {overall_outliers} ({overall_outliers/total_validated*100:.1f}%)")
    print(f"  - MRR outliers: {mrr_outliers} ({mrr_outliers/total_validated*100:.1f}%)")
    print(f"  - Users outliers: {users_outliers} ({users_outliers/total_validated*100:.1f}%)")
    print(f"  - Custom Screens outliers: {screens_outliers} ({screens_outliers/total_validated*100:.1f}%)")

    # Statistical confidence
    high_confidence = (results_df['Statistical_Confidence'] == 'High').sum()
    low_confidence = (results_df['Statistical_Confidence'] == 'Low').sum()

    print(f"\nStatistical Confidence:")
    print(f"  - High (not outlier): {high_confidence} ({high_confidence/total_validated*100:.1f}%)")
    print(f"  - Low (is outlier): {low_confidence} ({low_confidence/total_validated*100:.1f}%)")

    # Top outliers
    if overall_outliers > 0:
        print(f"\nTOP 10 STATISTICAL OUTLIERS (by outlier score):")
        print("-"*80)
        top_outliers = results_df[results_df['Is_Overall_Outlier']].sort_values(
            'Outlier_Score', ascending=False
        ).head(10)

        for _, row in top_outliers.iterrows():
            print(f"  {row['Account_Name']}")
            print(f"    Cluster: {row['Cluster']}")
            print(f"    MRR: ${row['MRR']:.0f} (cluster avg: ${row['Cluster_MRR_Mean']:.0f}, z={row['MRR_ZScore']:.1f})")
            print(f"    Users: {row['Users']} (cluster avg: {row['Cluster_Users_Mean']:.1f}, z={row['Users_ZScore']:.1f})")
            print()

    # Save cluster profiles
    cluster_profiles_file = 'cluster_statistical_profiles.csv'
    cluster_profiles.to_csv(cluster_profiles_file)
    print(f"\nSaved cluster profiles to: {cluster_profiles_file}")

    return results_df, cluster_profiles


if __name__ == '__main__':
    # Example: Validate Building Materials cluster (for pilot testing)
    print("\nPILOT TEST MODE: Building Materials & Construction")
    print("This will validate the cluster known to have 100% accuracy")
    print("-"*80)

    results, profiles = validate_cluster_statistical(
        cluster_name='Building Materials & Construction',
        outlier_threshold=2.5,
        output_file='statistical_validation_pilot_test.csv'
    )

    print("\n" + "="*80)
    print("Pilot test complete! Review results in statistical_validation_pilot_test.csv")
    print("="*80)
