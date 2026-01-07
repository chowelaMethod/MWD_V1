"""
Validate General Wholesale/Distribution Sub-Clusters Using Product Offerings Data

This script validates Agent 1's proposed sub-clustering of General W/D accounts by analyzing
actual sold items from customer_product_offerings.csv.

Sub-clusters to validate:
1. Logistics & Fulfillment Services (184 accounts) - service-based business model
2. Industrial Supplies Distribution (31 accounts) - industrial products
3. Office & Technology Supplies (27 accounts) - office equipment/tech
4. True General Wholesale/Distribution (146 accounts) - mixed/generic products
"""

import pandas as pd
import numpy as np
from collections import Counter
import re

# Load datasets
print("Loading datasets...")
product_offerings = pd.read_csv('customer_product_offerings.csv')
accounts_v2 = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2.csv')

print(f"Product offerings: {len(product_offerings):,} records from {product_offerings['Account'].nunique():,} accounts")
print(f"Accounts V2: {len(accounts_v2):,} total accounts")

# Filter to General Wholesale/Distribution cluster - ACTIVE accounts only
general_wd = accounts_v2[
    (accounts_v2['Industry_Cluster_Enhanced_V2'] == 'General Wholesale/Distribution') &
    (accounts_v2['Active?'] == True)
].copy()

print(f"\nGeneral W/D cluster (ACTIVE): {len(general_wd)} accounts")

# Match with product offerings
general_wd_with_products = general_wd.merge(
    product_offerings,
    left_on='Account Name',
    right_on='Account',
    how='left'
)

print(f"Accounts with product data: {general_wd_with_products['Account'].notna().sum()}")
accounts_with_products = general_wd_with_products[general_wd_with_products['Account'].notna()]['Account Name'].nunique()
print(f"Unique accounts with products: {accounts_with_products} / {len(general_wd)} ({accounts_with_products/len(general_wd)*100:.1f}%)")

# Define keyword patterns for classification
LOGISTICS_KEYWORDS = [
    # Services
    r'\bfreight\b', r'\bshipping\b', r'\bdelivery\b', r'\bwarehousing\b', r'\bstorage\b',
    r'\bfulfillment\b', r'\b3pl\b', r'\btransport\b', r'\blogistics\b', r'\bservice\b',
    r'\bhandling\b', r'\bpicking\b', r'\bpacking\b', r'\blabor\b', r'\bconsulting\b',
    # Fee-based items
    r'\bfee\b', r'\bcharge\b', r'\brate\b', r'\bhourly\b', r'\bmonthly\b'
]

INDUSTRIAL_KEYWORDS = [
    # Industrial products
    r'\bvalve\b', r'\bpump\b', r'\bbearing\b', r'\bmotor\b', r'\bfilter\b',
    r'\bhose\b', r'\bfitting\b', r'\bgasket\b', r'\bseal\b', r'\bbelt\b',
    r'\bchain\b', r'\bsprocket\b', r'\bgear\b', r'\bhydraulic\b', r'\bpneumatic\b',
    r'\bindustrial\b', r'\bmachinery\b', r'\bequipment\b', r'\btool\b', r'\bhardware\b',
    r'\bfastener\b', r'\bbolt\b', r'\bnut\b', r'\bscrew\b', r'\bwasher\b',
    r'\bpipe\b', r'\btubing\b', r'\bwire\b', r'\bcable\b', r'\belectrical\b'
]

OFFICE_TECH_KEYWORDS = [
    # Office supplies
    r'\bpaper\b', r'\bprinter\b', r'\btoner\b', r'\bink\b', r'\bpen\b',
    r'\bpencil\b', r'\bnotebook\b', r'\bfolder\b', r'\benvelope\b', r'\bstapler\b',
    # Technology
    r'\bcomputer\b', r'\blaptop\b', r'\bmonitor\b', r'\bkeyboard\b', r'\bmouse\b',
    r'\bsoftware\b', r'\bhardware\b', r'\bcable\b', r'\brouter\b', r'\bswitch\b',
    r'\bserver\b', r'\belectronics\b', r'\btech\b', r'\bit\b', r'\boffice\b'
]

def classify_item(item_name):
    """Classify a single item based on keywords"""
    item_lower = str(item_name).lower()

    # Check for logistics/service keywords
    logistics_matches = sum(1 for pattern in LOGISTICS_KEYWORDS if re.search(pattern, item_lower))

    # Check for industrial keywords
    industrial_matches = sum(1 for pattern in INDUSTRIAL_KEYWORDS if re.search(pattern, item_lower))

    # Check for office/tech keywords
    office_tech_matches = sum(1 for pattern in OFFICE_TECH_KEYWORDS if re.search(pattern, item_lower))

    # Return category with most matches
    if logistics_matches > industrial_matches and logistics_matches > office_tech_matches:
        return 'Logistics'
    elif industrial_matches > office_tech_matches:
        return 'Industrial'
    elif office_tech_matches > 0:
        return 'Office_Tech'
    else:
        return 'General'

def classify_account(account_items):
    """Classify an account based on its sold items"""
    if len(account_items) == 0:
        return 'Unknown', 0.0

    # Classify each item
    classifications = [classify_item(item) for item in account_items]

    # Count classifications
    counts = Counter(classifications)

    # Calculate percentages
    total = len(classifications)
    logistics_pct = counts.get('Logistics', 0) / total
    industrial_pct = counts.get('Industrial', 0) / total
    office_tech_pct = counts.get('Office_Tech', 0) / total
    general_pct = counts.get('General', 0) / total

    # Determine primary classification (need >40% threshold for confidence)
    if logistics_pct > 0.4:
        return 'Logistics & Fulfillment Services', logistics_pct
    elif industrial_pct > 0.4:
        return 'Industrial Supplies Distribution', industrial_pct
    elif office_tech_pct > 0.4:
        return 'Office & Technology Supplies', office_tech_pct
    else:
        return 'True General Wholesale/Distribution', general_pct

# Analyze each account
print("\n" + "="*80)
print("ANALYZING ACCOUNTS WITH PRODUCT DATA")
print("="*80)

results = []

for account_name in general_wd['Account Name'].unique():
    # Get account data
    account_data = general_wd[general_wd['Account Name'] == account_name].iloc[0]

    # Get sold items
    items = product_offerings[product_offerings['Account'] == account_name]['Item'].tolist()

    if len(items) == 0:
        classification = 'No Product Data'
        confidence = 0.0
    else:
        classification, confidence = classify_account(items)

    results.append({
        'Account_Name': account_name,
        'Sector': account_data['Sector'],
        'QBOIndustryType': account_data['QBOIndustryType'],
        'Items_Count': len(items),
        'Evidence_Based_Classification': classification,
        'Confidence': confidence,
        'Sample_Items': ', '.join(items[:5]) if len(items) > 0 else 'None'
    })

results_df = pd.DataFrame(results)

# Summary statistics
print("\nCLASSIFICATION SUMMARY:")
print("="*80)
classification_counts = results_df['Evidence_Based_Classification'].value_counts()
print(classification_counts)
print()

# Show percentage breakdown
print("\nPERCENTAGE BREAKDOWN:")
for classification, count in classification_counts.items():
    pct = count / len(results_df) * 100
    print(f"{classification:.<50} {count:>4} ({pct:>5.1f}%)")

# Confidence analysis
print("\n" + "="*80)
print("CONFIDENCE ANALYSIS (accounts with product data only)")
print("="*80)

with_data = results_df[results_df['Evidence_Based_Classification'] != 'No Product Data'].copy()
print(f"\nAccounts with product data: {len(with_data)} / {len(results_df)}")

for classification in ['Logistics & Fulfillment Services', 'Industrial Supplies Distribution',
                       'Office & Technology Supplies', 'True General Wholesale/Distribution']:
    subset = with_data[with_data['Evidence_Based_Classification'] == classification]
    if len(subset) > 0:
        avg_confidence = subset['Confidence'].mean()
        print(f"\n{classification}:")
        print(f"  Count: {len(subset)}")
        print(f"  Avg Confidence: {avg_confidence:.1%}")
        print(f"  High Confidence (>60%): {(subset['Confidence'] > 0.6).sum()}")

# Show examples from each category
print("\n" + "="*80)
print("SAMPLE ACCOUNTS BY CLASSIFICATION")
print("="*80)

for classification in ['Logistics & Fulfillment Services', 'Industrial Supplies Distribution',
                       'Office & Technology Supplies', 'True General Wholesale/Distribution']:
    subset = results_df[results_df['Evidence_Based_Classification'] == classification]
    if len(subset) > 0:
        print(f"\n{classification} (showing top 5 by confidence):")
        print("-" * 80)
        top_5 = subset.nlargest(5, 'Confidence')
        for idx, row in top_5.iterrows():
            print(f"\n  {row['Account_Name']}")
            print(f"    Confidence: {row['Confidence']:.1%}")
            print(f"    Sector: {row['Sector']}")
            print(f"    Items analyzed: {row['Items_Count']}")
            print(f"    Sample items: {row['Sample_Items'][:150]}...")

# Save detailed results
output_file = 'general_wd_validation_results.csv'
results_df.to_csv(output_file, index=False)
print(f"\n" + "="*80)
print(f"Detailed results saved to: {output_file}")
print("="*80)

# Summary for decision-making
print("\n" + "="*80)
print("VALIDATION SUMMARY & RECOMMENDATIONS")
print("="*80)

total_accounts = len(general_wd)
with_product_data = len(with_data)
coverage = with_product_data / total_accounts * 100

print(f"\nData Coverage: {with_product_data}/{total_accounts} accounts ({coverage:.1f}%)")
print(f"\nProposed Sub-Clusters Validation:")

# Compare to Agent 1's proposed numbers
print(f"\n1. Logistics & Fulfillment Services")
print(f"   Evidence-based: {classification_counts.get('Logistics & Fulfillment Services', 0)} accounts")
print(f"   Agent 1 proposed: 184 accounts (keyword-based)")

print(f"\n2. Industrial Supplies Distribution")
print(f"   Evidence-based: {classification_counts.get('Industrial Supplies Distribution', 0)} accounts")
print(f"   Agent 1 proposed: 31 accounts (keyword-based)")

print(f"\n3. Office & Technology Supplies")
print(f"   Evidence-based: {classification_counts.get('Office & Technology Supplies', 0)} accounts")
print(f"   Agent 1 proposed: 27 accounts (keyword-based)")

print(f"\n4. True General Wholesale/Distribution")
print(f"   Evidence-based: {classification_counts.get('True General Wholesale/Distribution', 0)} accounts")
print(f"   Agent 1 proposed: 146 accounts (keyword-based)")

print("\n" + "="*80)
