"""
Product Type Classification Analysis for MWD Customers

This script analyzes actual product offerings to understand:
1. Product catalog complexity (SKU counts, naming patterns)
2. Product categorization depth (hierarchical structure)
3. Service vs Product mix
4. Business sophistication indicators

Goal: Classify accounts by what they actually sell, not self-reported industry.
"""

import pandas as pd
import numpy as np
import re
from collections import Counter

print("="*80)
print("PRODUCT TYPE CLASSIFICATION ANALYSIS")
print("="*80)

# Load data
print("\nLoading datasets...")
product_offerings = pd.read_csv('customer_product_offerings_with_type.csv')
accounts_v2 = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2.csv')

# Filter to active accounts only
active_accounts = accounts_v2[accounts_v2['Active?'] == True].copy()

print(f"Product offerings: {len(product_offerings):,} records")
print(f"Unique accounts with products: {product_offerings['Account'].nunique():,}")
print(f"Active accounts in CRM: {len(active_accounts):,}")

# Match active accounts with product data
active_with_products = active_accounts.merge(
    product_offerings.groupby('Account').size().reset_index(name='product_count'),
    left_on='Account Name',
    right_on='Account',
    how='left'
)

coverage = active_with_products['Account'].notna().sum()
print(f"Active accounts with product data: {coverage} / {len(active_accounts)} ({coverage/len(active_accounts)*100:.1f}%)")

print("\n" + "="*80)
print("PHASE 1: PRODUCT CATALOG COMPLEXITY ANALYSIS")
print("="*80)

# Function to analyze product names
def analyze_product_name(product_name):
    """Extract features from a single product name"""
    name = str(product_name)

    # Count delimiters (hierarchy depth)
    colon_count = name.count(':')
    slash_count = name.count('/')
    pipe_count = name.count('|')
    delimiter_count = colon_count + slash_count + pipe_count

    # Name length and complexity
    char_length = len(name)
    word_count = len(name.split())

    # Check for SKU codes (alphanumeric patterns)
    has_sku_code = bool(re.search(r'\b[A-Z0-9]{3,}-?[A-Z0-9]{2,}\b', name))

    # Check for specifications (numbers with units)
    has_specs = bool(re.search(r'\d+\s*(oz|lb|kg|ml|l|gal|ft|in|mm|cm|m)', name, re.IGNORECASE))

    # Check for brand/vendor prefix pattern (e.g., "ACME:", "Brand:")
    has_brand_prefix = bool(re.search(r'^[A-Z][a-zA-Z0-9\s&]+:', name))

    return {
        'delimiter_count': delimiter_count,
        'char_length': char_length,
        'word_count': word_count,
        'has_sku_code': has_sku_code,
        'has_specs': has_specs,
        'has_brand_prefix': has_brand_prefix
    }

# Function to classify item type
def classify_item_type(product_name):
    """Classify item as Service, Fee, or Product"""
    name = str(product_name).lower()

    # Service keywords
    service_keywords = [
        r'\bservice\b', r'\bconsulting\b', r'\blabor\b', r'\bhourly\b',
        r'\bfreight\b', r'\bshipping\b', r'\bdelivery\b', r'\bhandling\b',
        r'\bwarehousing\b', r'\bstorage\b', r'\bpicking\b', r'\bpacking\b',
        r'\binstallation\b', r'\bmaintenance\b', r'\brepair\b'
    ]

    # Fee keywords
    fee_keywords = [
        r'\bfee\b', r'\bcharge\b', r'\bsurcharge\b', r'\btariff\b',
        r'\blate\s+fee\b', r'\bprocessing\b', r'\badmin\b', r'\bfinance\b'
    ]

    for keyword in service_keywords:
        if re.search(keyword, name):
            return 'Service'

    for keyword in fee_keywords:
        if re.search(keyword, name):
            return 'Fee'

    return 'Product'

print("\nAnalyzing product catalog for each account...")

results = []

for account_name in product_offerings['Account'].unique():
    # Get all products for this account
    account_products = product_offerings[product_offerings['Account'] == account_name]['Item'].tolist()

    if len(account_products) == 0:
        continue

    # SKU count
    sku_count = len(account_products)

    # Analyze each product name
    name_features = [analyze_product_name(p) for p in account_products]

    # Aggregate metrics
    avg_delimiter_count = np.mean([f['delimiter_count'] for f in name_features])
    avg_char_length = np.mean([f['char_length'] for f in name_features])
    avg_word_count = np.mean([f['word_count'] for f in name_features])
    pct_with_sku_codes = sum([f['has_sku_code'] for f in name_features]) / len(name_features) * 100
    pct_with_specs = sum([f['has_specs'] for f in name_features]) / len(name_features) * 100
    pct_with_brand_prefix = sum([f['has_brand_prefix'] for f in name_features]) / len(name_features) * 100

    # Get item types from the data (ItemType column)
    account_data = product_offerings[product_offerings['Account'] == account_name]
    item_types_from_data = account_data['ItemType'].tolist()
    type_counts = Counter(item_types_from_data)

    # Calculate percentages
    total_items = len(item_types_from_data)
    pct_service = type_counts.get('Service', 0) / total_items * 100
    pct_inventory = type_counts.get('Inventory', 0) / total_items * 100
    pct_non_inventory = type_counts.get('NonInventory', 0) / total_items * 100

    # Also do keyword-based classification for comparison
    item_types_classified = [classify_item_type(p) for p in account_products]
    classified_counts = Counter(item_types_classified)
    pct_fee = classified_counts.get('Fee', 0) / len(item_types_classified) * 100
    pct_product = classified_counts.get('Product', 0) / len(item_types_classified) * 100

    # Determine primary business type based on ItemType from data
    if pct_service > 50:
        primary_type = 'Service-Based'
    elif pct_inventory > 70:
        primary_type = 'Inventory-Based (Physical Products)'
    elif pct_non_inventory > 50:
        primary_type = 'NonInventory-Based (Digital/Services)'
    elif pct_service > 20:
        primary_type = 'Hybrid (Mixed)'
    else:
        primary_type = 'Product-Based (Mixed Inventory)'

    # Calculate catalog complexity score (0-100)
    # Factors: SKU count, naming depth, sophistication indicators
    sku_score = min(sku_count / 500 * 40, 40)  # Max 40 points for SKU count
    depth_score = min(avg_delimiter_count / 3 * 20, 20)  # Max 20 points for categorization depth
    sophistication_score = (
        (pct_with_sku_codes / 100 * 15) +  # 15 points for SKU codes
        (pct_with_specs / 100 * 10) +      # 10 points for specifications
        (pct_with_brand_prefix / 100 * 15) # 15 points for brand prefixes
    )

    catalog_complexity_score = sku_score + depth_score + sophistication_score

    # Determine complexity tier
    if catalog_complexity_score < 20:
        complexity_tier = 'Ultra-Simple'
    elif catalog_complexity_score < 40:
        complexity_tier = 'Simple'
    elif catalog_complexity_score < 60:
        complexity_tier = 'Standard'
    elif catalog_complexity_score < 80:
        complexity_tier = 'Complex'
    else:
        complexity_tier = 'Very Complex'

    results.append({
        'Account': account_name,
        'SKU_Count': sku_count,
        'Avg_Delimiter_Count': round(avg_delimiter_count, 2),
        'Avg_Char_Length': round(avg_char_length, 1),
        'Avg_Word_Count': round(avg_word_count, 1),
        'Pct_With_SKU_Codes': round(pct_with_sku_codes, 1),
        'Pct_With_Specs': round(pct_with_specs, 1),
        'Pct_With_Brand_Prefix': round(pct_with_brand_prefix, 1),
        'Pct_Service_Items': round(pct_service, 1),
        'Pct_Inventory_Items': round(pct_inventory, 1),
        'Pct_NonInventory_Items': round(pct_non_inventory, 1),
        'Pct_Fee_Items': round(pct_fee, 1),
        'Primary_Business_Type': primary_type,
        'Catalog_Complexity_Score': round(catalog_complexity_score, 1),
        'Complexity_Tier': complexity_tier,
        'Sample_Products': ', '.join(account_products[:3])
    })

results_df = pd.DataFrame(results)

print(f"\nAnalyzed {len(results_df)} accounts with product data")

# Summary statistics
print("\n" + "="*80)
print("SKU COUNT DISTRIBUTION")
print("="*80)

print("\nSKU Count Statistics:")
print(results_df['SKU_Count'].describe())

print("\nSKU Count Percentiles:")
for p in [10, 25, 50, 75, 90, 95, 99]:
    val = results_df['SKU_Count'].quantile(p/100)
    print(f"{p}th percentile: {val:.0f} SKUs")

# SKU count tiers
def categorize_sku_count(count):
    if count <= 5:
        return '1-5 (Ultra-Simple)'
    elif count <= 20:
        return '6-20 (Simple)'
    elif count <= 50:
        return '21-50 (Standard)'
    elif count <= 100:
        return '51-100 (Complex)'
    elif count <= 500:
        return '101-500 (Very Complex)'
    else:
        return '500+ (Ultra-Complex)'

results_df['SKU_Tier'] = results_df['SKU_Count'].apply(categorize_sku_count)

print("\nSKU Count Tiers:")
sku_tier_counts = results_df['SKU_Tier'].value_counts().sort_index()
for tier, count in sku_tier_counts.items():
    pct = count / len(results_df) * 100
    print(f"  {tier:.<40} {count:>4} ({pct:>5.1f}%)")

print("\n" + "="*80)
print("PRODUCT NAMING PATTERNS")
print("="*80)

print("\nCategorization Depth (avg delimiters per product name):")
print(results_df['Avg_Delimiter_Count'].describe())

print("\nProduct Name Length:")
print(f"  Avg characters: {results_df['Avg_Char_Length'].mean():.1f}")
print(f"  Avg words: {results_df['Avg_Word_Count'].mean():.1f}")

print("\nSophistication Indicators:")
print(f"  Accounts with SKU codes: {(results_df['Pct_With_SKU_Codes'] > 0).sum()} ({(results_df['Pct_With_SKU_Codes'] > 0).sum()/len(results_df)*100:.1f}%)")
print(f"  Accounts with specifications: {(results_df['Pct_With_Specs'] > 0).sum()} ({(results_df['Pct_With_Specs'] > 0).sum()/len(results_df)*100:.1f}%)")
print(f"  Accounts with brand prefixes: {(results_df['Pct_With_Brand_Prefix'] > 0).sum()} ({(results_df['Pct_With_Brand_Prefix'] > 0).sum()/len(results_df)*100:.1f}%)")

print("\n" + "="*80)
print("SERVICE VS PRODUCT MIX")
print("="*80)

print("\nPrimary Business Type Distribution:")
business_type_counts = results_df['Primary_Business_Type'].value_counts()
for btype, count in business_type_counts.items():
    pct = count / len(results_df) * 100
    print(f"  {btype:.<40} {count:>4} ({pct:>5.1f}%)")

print("\n" + "="*80)
print("CATALOG COMPLEXITY SCORES")
print("="*80)

print("\nComplexity Score Statistics:")
print(results_df['Catalog_Complexity_Score'].describe())

print("\nComplexity Tiers:")
complexity_tier_counts = results_df['Complexity_Tier'].value_counts()
tier_order = ['Ultra-Simple', 'Simple', 'Standard', 'Complex', 'Very Complex']
for tier in tier_order:
    count = complexity_tier_counts.get(tier, 0)
    pct = count / len(results_df) * 100
    print(f"  {tier:.<40} {count:>4} ({pct:>5.1f}%)")

print("\n" + "="*80)
print("SAMPLE ACCOUNTS BY COMPLEXITY TIER")
print("="*80)

for tier in tier_order:
    tier_accounts = results_df[results_df['Complexity_Tier'] == tier]
    if len(tier_accounts) > 0:
        print(f"\n{tier} (showing 3 examples):")
        print("-" * 80)
        for idx, row in tier_accounts.head(3).iterrows():
            print(f"\n  {row['Account']}")
            print(f"    SKUs: {row['SKU_Count']}")
            print(f"    Complexity Score: {row['Catalog_Complexity_Score']:.1f}")
            print(f"    Business Type: {row['Primary_Business_Type']}")
            print(f"    Avg Delimiter Count: {row['Avg_Delimiter_Count']:.1f}")
            print(f"    Sample Products: {row['Sample_Products'][:100]}...")

# Save results
output_file = 'product_type_analysis_results.csv'
results_df.to_csv(output_file, index=False)
print(f"\n" + "="*80)
print(f"Results saved to: {output_file}")
print("="*80)

# Merge with V2 account data for validation
print("\n" + "="*80)
print("MERGING WITH ACCOUNT DATA FOR VALIDATION")
print("="*80)

merged = active_accounts.merge(
    results_df,
    left_on='Account Name',
    right_on='Account',
    how='left'
)

print(f"\nMerged {len(merged)} active accounts")
print(f"With product data: {merged['SKU_Count'].notna().sum()}")

# Correlation with workflow complexity indicators
print("\n" + "="*80)
print("CORRELATION WITH WORKFLOW COMPLEXITY INDICATORS")
print("="*80)

# Calculate correlations (only for accounts with product data)
merged_with_products = merged[merged['SKU_Count'].notna()].copy()

# Convert custom screens to numeric
merged_with_products['Total_Custom_Screens'] = pd.to_numeric(
    merged_with_products['Custom Screens New'], errors='coerce'
).fillna(0) + pd.to_numeric(
    merged_with_products['Custom Screens Classic'], errors='coerce'
).fillna(0)

print("\nSKU Count vs Users:")
correlation = merged_with_products[['SKU_Count', 'Users']].corr()
print(f"  Correlation: {correlation.iloc[0,1]:.3f}")

print("\nSKU Count vs Custom Screens:")
correlation = merged_with_products[['SKU_Count', 'Total_Custom_Screens']].corr()
print(f"  Correlation: {correlation.iloc[0,1]:.3f}")

print("\nSKU Count vs MRR:")
correlation = merged_with_products[['SKU_Count', 'MRR_Calculated']].corr()
print(f"  Correlation: {correlation.iloc[0,1]:.3f}")

print("\nCatalog Complexity Score vs Users:")
correlation = merged_with_products[['Catalog_Complexity_Score', 'Users']].corr()
print(f"  Correlation: {correlation.iloc[0,1]:.3f}")

print("\nCatalog Complexity Score vs Custom Screens:")
correlation = merged_with_products[['Catalog_Complexity_Score', 'Total_Custom_Screens']].corr()
print(f"  Correlation: {correlation.iloc[0,1]:.3f}")

print("\nCatalog Complexity Score vs MRR:")
correlation = merged_with_products[['Catalog_Complexity_Score', 'MRR_Calculated']].corr()
print(f"  Correlation: {correlation.iloc[0,1]:.3f}")

# Cross-tabulations
print("\n" + "="*80)
print("COMPLEXITY TIER VS USER COUNT")
print("="*80)

def categorize_users(count):
    if count == 1:
        return '1 user'
    elif count <= 3:
        return '2-3 users'
    elif count <= 5:
        return '4-5 users'
    elif count <= 10:
        return '6-10 users'
    else:
        return '11+ users'

merged_with_products['User_Tier'] = merged_with_products['Users'].apply(categorize_users)

crosstab = pd.crosstab(
    merged_with_products['Complexity_Tier'],
    merged_with_products['User_Tier'],
    normalize='index'
) * 100

print("\n% of accounts in each user tier (by complexity tier):")
print(crosstab.round(1))

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)

print("\nKey Deliverables:")
print(f"1. {output_file} - Detailed product analysis for all accounts")
print("2. Console output above - Statistical summaries and insights")
print("\nNext Steps:")
print("- Review the correlations between product complexity and workflow indicators")
print("- Examine sample accounts in each complexity tier")
print("- Use this data to segment customers for targeted features")
