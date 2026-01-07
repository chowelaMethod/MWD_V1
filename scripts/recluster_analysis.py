#!/usr/bin/env python3
"""
Re-clustering script with strict food & beverage keywords only.
Removes generic wholesale/distribution terms that were causing mis-classification.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def categorize_industry_strict(row):
    """
    Strict clustering - only specific industry keywords, no generic terms.
    """
    sector = str(row['Sector']).lower() if pd.notna(row['Sector']) else ''
    qbo_type = str(row['QBOIndustryType']).lower() if pd.notna(row['QBOIndustryType']) else ''
    vertical = str(row['Vertical']).lower() if pd.notna(row['Vertical']) else ''
    combined = sector + ' ' + qbo_type

    # MEDICAL - specific keywords only
    if any(x in combined for x in ['medical', 'dental', 'hospital', 'healthcare', 'pharma',
                                     'surgical', 'clinic', 'diagnostic']):
        return 'Medical Equipment & Supplies'

    # FOOD & BEVERAGE - STRICT specific keywords only, NO generic wholesale
    # Removed: 'wholesale', 'distribution', 'merchant' - these are too generic
    # CRITICAL: Use word-boundary safe keywords to avoid matching 'ale' in 'sales' or 'brew' in 'hebrew'
    food_keywords = ['food manufacturing', 'bakery', 'bakeries', 'dairy', 'meat', 'poultry', 'seafood',
                     'fruit', 'vegetable', 'produce', 'snack', 'candy', 'confection',
                     'grain', 'cereal', 'flour', 'sugar', 'grocery']
    beverage_keywords = ['beverage', 'coffee and tea', 'winery', 'wineries', 'beer ', ' ale ',
                        'brewery', 'breweries', 'distillery', 'distilleries',
                        'juice', 'soft drink', 'water bottl']
    restaurant_keywords = ['restaurant', 'food service', 'eating place', 'drinking place',
                          'cafe', 'cafes', ' bar ', 'catering']

    if any(x in combined for x in food_keywords + beverage_keywords + restaurant_keywords):
        return 'Food & Beverage Dist/Mfg'

    # BUILDING MATERIALS - specific keywords
    if any(x in combined for x in ['lumber', 'wood product', 'flooring', 'carpet',
                                     'concrete', 'cement', 'brick', 'stone', 'granite',
                                     'building material', 'construction material',
                                     'drywall', 'insulation', 'roofing']):
        return 'Building Materials & Construction'

    # INDUSTRIAL EQUIPMENT - specific keywords
    if any(x in combined for x in ['industrial machinery', 'industrial equipment',
                                     'valve', 'pump', 'compressor', 'hvac equipment',
                                     'fork truck', 'forklift', 'conveyor',
                                     'machinery merchant', 'equipment rental']):
        return 'Industrial Equipment & Machinery'

    # CHEMICALS - specific keywords
    if any(x in combined for x in ['chemical', 'plastic', 'rubber', 'resin', 'polymer',
                                     'paint', 'coating', 'adhesive', 'fertilizer']):
        return 'Chemicals, Plastics & Rubber'

    # ELECTRONICS - specific keywords
    if any(x in combined for x in ['computer', 'electronic part', 'electronic component',
                                     'semiconductor', 'circuit', 'software']):
        return 'Electronics & Technology'

    # FURNITURE - specific keywords
    if any(x in combined for x in ['furniture', 'furnishing', 'cabinet', 'seating']):
        return 'Furniture & Home Furnishings'

    # APPAREL - specific keywords
    if any(x in combined for x in ['apparel', 'clothing', 'textile', 'fabric', 'garment',
                                     'fashion', 'footwear', 'shoe']):
        return 'Apparel & Textiles'

    # AUTOMOTIVE - specific keywords
    if any(x in combined for x in ['automotive', 'automobile', 'vehicle', 'auto part',
                                     'tire', 'motor vehicle']):
        return 'Automotive & Transportation'

    # METAL - specific keywords
    if any(x in combined for x in ['metal', 'steel', 'aluminum', 'iron', 'fabrication',
                                     'welding', 'machining']):
        return 'Metal Fabrication & Steel'

    # ELECTRICAL - specific keywords
    if any(x in combined for x in ['electrical equipment', 'lighting', 'wiring', 'lamp']):
        return 'Electrical & Lighting Equipment'

    # PACKAGING - specific keywords
    if any(x in combined for x in ['packaging', 'container', 'box', 'printing', 'label']):
        return 'Packaging & Printing'

    # OFFICE SUPPLIES - specific keywords
    if any(x in combined for x in ['office equipment', 'office supply', 'stationery',
                                     'paper product']):
        return 'Office Supplies & Equipment'

    # SAFETY - specific keywords
    if any(x in combined for x in ['safety', 'security', 'surveillance', 'fire protection',
                                     'first aid']):
        return 'Safety & Security Equipment'

    # SPORTING GOODS - specific keywords
    if any(x in combined for x in ['sporting goods', 'sport', 'athletic', 'fitness', 'recreation']):
        return 'Sporting Goods & Fitness Equipment'

    # SIGNS - specific keywords
    if any(x in combined for x in ['sign', 'banner', 'display', 'advertising specialt']):
        return 'Signs, Graphics & Displays'

    # AGRICULTURE - specific keywords
    if any(x in combined for x in ['greenhouse', 'nursery', 'garden', 'agricultural',
                                     'farm supply', 'seed', 'fertilizer']):
        return 'Agriculture & Greenhouse/Nursery'

    # WOOD PRODUCTS - specific keywords
    if any(x in combined for x in ['wood product', 'lumber', 'millwork', 'sawmill']):
        return 'Wood Products & Lumber'

    # HVAC - specific keywords
    if any(x in combined for x in ['hvac', 'heating', 'air conditioning', 'refrigeration',
                                     'ventilation']):
        return 'HVAC & Refrigeration Equipment'

    # MANUFACTURER REPRESENTATIVES - specific keywords
    if any(x in combined for x in ['manufacturer rep', 'manufacturers rep', 'sales agent',
                                     'wholesale agent', 'broker']):
        return 'Manufacturer Representatives'

    # GENERAL RETAIL - only if clearly retail
    if 'retail' in vertical or any(x in combined for x in ['retail store', 'shop', 'boutique']):
        # But NOT if it's wholesale or manufacturing
        if 'wholesale' not in combined and 'manufact' not in combined:
            return 'General Retail'

    # GENERAL WHOLESALE/DISTRIBUTION - catch generic wholesale
    # This now catches everything that wasn't specifically categorized above
    if 'wholesale' in vertical or any(x in combined for x in ['wholesale', 'distribution',
                                                                'merchant wholesale', 'distributor']):
        return 'General Wholesale/Distribution'

    # GENERAL MANUFACTURING - catch generic manufacturing
    if 'manufacturing' in vertical or 'manufacturing' in combined or 'manufacturer' in combined:
        return 'General/Specialty Manufacturing'

    # SERVICES & OTHER - everything else
    return 'Services & Other'

def calculate_mrr(row):
    """Calculate Monthly Recurring Revenue based on payment type"""
    if pd.isna(row['Last Invoice $']):
        return 0

    if row['SaaS Pay Type'] == 'Monthly':
        return row['Last Invoice $']
    elif row['SaaS Pay Type'] == 'Prepay' or row['SaaS Pay Type'] == 'Annual':
        return row['Last Invoice $'] / 12
    else:
        return row['Last Invoice $']

def classify_b2b_b2c(row):
    """Classify business type based on cluster and customer count"""
    cluster = str(row['Industry_Cluster_Enhanced_V2'])
    customers = row['Customers'] if pd.notna(row['Customers']) else 0

    # B2C indicators - retail with many individual customers
    if 'General Retail' in cluster:
        if customers > 1000:
            return 'B2C'
        elif customers > 100:
            return 'Hybrid (B2B & B2C)'
        else:
            return 'B2B'

    # Food & Beverage - depends on customer count
    if 'Food & Beverage' in cluster:
        if customers > 500:  # Restaurants/cafes
            return 'B2C'
        elif customers > 100:
            return 'Hybrid (B2B & B2C)'
        else:
            return 'B2B'

    # Apparel - depends on customer count
    if 'Apparel' in cluster:
        if customers > 500:
            return 'B2C'
        elif customers > 100:
            return 'Hybrid (B2B & B2C)'
        else:
            return 'B2B'

    # Everything else is predominantly B2B
    return 'B2B'

def classify_company_size(employees):
    """Classify company size based on employee count"""
    if pd.isna(employees) or employees == 0:
        return 'Unknown'
    elif employees <= 5:
        return 'Micro (1-5 employees)'
    elif employees <= 20:
        return 'Small (6-20 employees)'
    elif employees <= 50:
        return 'Medium (21-50 employees)'
    elif employees <= 200:
        return 'Large (51-200 employees)'
    else:
        return 'Enterprise (200+ employees)'

# Main execution
if __name__ == '__main__':
    print("Loading data...")
    df = pd.read_csv('../data/customermethodaccount_01-07-2026_11_10_09_am.csv')

    print(f"Total records: {len(df):,}")

    # Apply strict clustering
    print("\nApplying strict industry clustering...")
    df['Industry_Cluster_Enhanced_V2'] = df.apply(categorize_industry_strict, axis=1)

    # Calculate MRR
    print("Calculating MRR...")
    df['MRR_Calculated'] = df.apply(calculate_mrr, axis=1)

    # Classify B2B/B2C
    print("Classifying business type...")
    df['Business_Type_V2'] = df.apply(classify_b2b_b2c, axis=1)

    # Classify company size
    print("Classifying company size...")
    df['Company_Size_V2'] = df['Employees'].apply(classify_company_size)

    # Summary statistics
    print("\n" + "="*80)
    print("CLUSTER DISTRIBUTION (ALL ACCOUNTS)")
    print("="*80)
    cluster_counts = df['Industry_Cluster_Enhanced_V2'].value_counts()
    for cluster, count in cluster_counts.items():
        pct = count / len(df) * 100
        print(f"{cluster:<40} {count:>6,} ({pct:>5.1f}%)")

    # Active accounts only
    active = df[df['Active?'] == True]
    print("\n" + "="*80)
    print(f"CLUSTER DISTRIBUTION (ACTIVE ACCOUNTS, n={len(active):,})")
    print("="*80)
    active_cluster_counts = active['Industry_Cluster_Enhanced_V2'].value_counts()
    for cluster, count in active_cluster_counts.items():
        pct = count / len(active) * 100
        total_mrr = active[active['Industry_Cluster_Enhanced_V2'] == cluster]['MRR_Calculated'].sum()
        avg_mrr = active[active['Industry_Cluster_Enhanced_V2'] == cluster]['MRR_Calculated'].mean()
        print(f"{cluster:<40} {count:>6,} ({pct:>5.1f}%) | MRR: ${total_mrr:>8,.0f} | Avg: ${avg_mrr:>6,.0f}")

    # Save enhanced file
    output_file = '../data/customermethodaccount_01-07-2026_RECLUSTERED_V2.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Saved re-clustered data to: {output_file}")

    print("\n" + "="*80)
    print("Re-clustering complete! Next step: Review uncertain accounts and validate with websites.")
    print("="*80)
