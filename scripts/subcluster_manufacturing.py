"""
Manufacturing Sub-Clustering Script

This script breaks down the Generic "General/Specialty Manufacturing" cluster (348 accounts)
into meaningful sub-clusters based on:
1. Website domain keywords
2. Product naming patterns
3. Account name keywords
"""

import pandas as pd
import re

# Load data
df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv', low_memory=False)

# Filter to active General/Specialty Manufacturing
mfg = df[(df['Industry_Cluster_Enhanced_V2'] == 'General/Specialty Manufacturing') &
         (df['Active?'] == True)].copy()

print("="*80)
print("MANUFACTURING SUB-CLUSTERING")
print("="*80)
print(f"Total Active Manufacturing Accounts: {len(mfg)}")
print(f"Total MRR: ${mfg['MRR_Calculated'].sum():,.2f}")
print()

def classify_manufacturing_subtype(row):
    """Classify manufacturing account into sub-type based on available data"""

    # Combine all text fields for keyword matching
    account_name = str(row.get('Account Name', '')).lower()
    website = str(row.get('Website', '')).lower()
    products = str(row.get('Sample_Products', '')).lower()

    combined_text = f"{account_name} {website} {products}"

    # Food & Beverage Manufacturing
    food_keywords = ['beverage', 'food', 'brewing', 'brewery', 'winery', 'coffee', 'kombucha',
                     'bakery', 'snack', 'meat', 'produce', 'dairy', 'bottling', 'distillery']
    if any(kw in combined_text for kw in food_keywords):
        return 'Food & Beverage Manufacturing'

    # Medical Device & Equipment Manufacturing
    medical_keywords = ['medical', 'catheter', 'surgical', 'healthcare', 'diagnostic', 'biotech',
                       'pharmaceutical', 'lab', 'clinical', 'health']
    if any(kw in combined_text for kw in medical_keywords):
        return 'Medical Device & Equipment Mfg'

    # Chemical Manufacturing
    chemical_keywords = ['chemical', 'laboratory', 'laboratories', 'formula', 'compound', 'resin',
                        'polymer', 'coating', 'adhesive', 'solvent', 'cleaning', 'sanitizer']
    if any(kw in combined_text for kw in chemical_keywords):
        return 'Chemical Manufacturing'

    # Electronics & Technology Manufacturing
    electronics_keywords = ['electronic', 'circuit', 'semiconductor', 'led', 'fiber optic', 'cable',
                           'sensor', 'pcb', 'microcontroller', 'radio', 'audio', 'video']
    if any(kw in combined_text for kw in electronics_keywords):
        return 'Electronics & Technology Mfg'

    # Industrial Equipment & Machinery
    equipment_keywords = ['equipment', 'machinery', 'forklift', 'pump', 'valve', 'motor', 'compressor',
                         'conveyor', 'hydraulic', 'pneumatic', 'automation', 'industrial']
    if any(kw in combined_text for kw in equipment_keywords):
        return 'Industrial Equipment & Machinery Mfg'

    # Metal Fabrication & Custom Manufacturing
    metal_keywords = ['fabrication', 'metal', 'steel', 'aluminum', 'welding', 'machining', 'cnc',
                     'sheet metal', 'casting', 'forging', 'stamping']
    if any(kw in combined_text for kw in metal_keywords):
        return 'Metal Fabrication & Steel'

    # Packaging & Printing
    packaging_keywords = ['packaging', 'printing', 'label', 'box', 'carton', 'bag', 'graphics',
                         'signage', 'decal', 'screen print']
    if any(kw in combined_text for kw in packaging_keywords):
        return 'Packaging & Printing Services'

    # Apparel & Textiles Manufacturing
    apparel_keywords = ['apparel', 'clothing', 'garment', 'textile', 'fabric', 'embroidery',
                       'screen printing', 't-shirt', 'uniform']
    if any(kw in combined_text for kw in apparel_keywords):
        return 'Apparel & Textiles'

    # Furniture & Woodworking
    furniture_keywords = ['furniture', 'cabinet', 'woodwork', 'millwork', 'carpentry', 'joinery']
    if any(kw in combined_text for kw in furniture_keywords):
        return 'Furniture & Home Furnishings'

    # Manufacturer Representatives (not actual manufacturers)
    rep_keywords = ['representative', 'rep', 'sales rep', 'agent', 'broker']
    sector = str(row.get('Sector', '')).lower()
    qbo_type = str(row.get('QBOIndustryType', '')).lower()
    if any(kw in f"{sector} {qbo_type}" for kw in rep_keywords):
        return 'Manufacturer Representatives'

    # Default: Keep as General/Specialty Manufacturing
    return 'General/Specialty Manufacturing (Uncategorized)'

# Apply classification
mfg['Manufacturing_Subcluster'] = mfg.apply(classify_manufacturing_subtype, axis=1)

# Results
print("\n" + "="*80)
print("SUB-CLUSTER RESULTS")
print("="*80)

results = mfg.groupby('Manufacturing_Subcluster').agg({
    'Account Name': 'count',
    'MRR_Calculated': ['sum', 'mean']
}).round(2)

results.columns = ['Account_Count', 'Total_MRR', 'Avg_MRR']
results = results.sort_values('Total_MRR', ascending=False)

for subcluster, row in results.iterrows():
    pct = (row['Account_Count'] / len(mfg)) * 100
    mrr_pct = (row['Total_MRR'] / mfg['MRR_Calculated'].sum()) * 100
    print(f"\n{subcluster}:")
    print(f"  Accounts: {int(row['Account_Count'])} ({pct:.1f}%)")
    print(f"  Total MRR: ${row['Total_MRR']:,.2f} ({mrr_pct:.1f}%)")
    print(f"  Avg MRR: ${row['Avg_MRR']:.2f}")

# Save results
output_df = df.copy()
mfg_with_subcluster = mfg[['Account Name', 'Manufacturing_Subcluster']]
output_df = output_df.merge(mfg_with_subcluster, on='Account Name', how='left')

# Fill in subclusters for non-manufacturing accounts
output_df['Manufacturing_Subcluster'] = output_df['Manufacturing_Subcluster'].fillna(output_df['Industry_Cluster_Enhanced_V2'])

# For manufacturing accounts, use subcluster as the new cluster
output_df['Industry_Cluster_V3'] = output_df.apply(
    lambda row: row['Manufacturing_Subcluster']
    if row['Industry_Cluster_Enhanced_V2'] == 'General/Specialty Manufacturing' and row['Active?'] == True
    else row['Industry_Cluster_Enhanced_V2'],
    axis=1
)

output_df.to_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V3_WITH_MFG_SUBCLUSTERS.csv', index=False)

print("\n" + "="*80)
print("✅ SAVED: data/customermethodaccount_01-07-2026_RECLUSTERED_V3_WITH_MFG_SUBCLUSTERS.csv")
print("="*80)

# Show examples from each subcluster
print("\n" + "="*80)
print("EXAMPLE ACCOUNTS FROM EACH SUB-CLUSTER")
print("="*80)

for subcluster in results.index:
    if subcluster == 'General/Specialty Manufacturing (Uncategorized)':
        continue

    examples = mfg[mfg['Manufacturing_Subcluster'] == subcluster].nlargest(3, 'MRR_Calculated')

    print(f"\n{subcluster}:")
    for idx, row in examples.iterrows():
        website = row.get('Website', 'N/A')
        if pd.notna(website):
            print(f"  • {row['Account Name']} (${row['MRR_Calculated']:.0f} MRR) - {website}")
        else:
            print(f"  • {row['Account Name']} (${row['MRR_Calculated']:.0f} MRR)")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
