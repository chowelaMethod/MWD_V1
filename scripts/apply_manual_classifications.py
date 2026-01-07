"""
Apply Manual Manufacturing Classifications

This script applies the manual website-based classifications to the manufacturing accounts
and updates the sub-cluster assignments.
"""

import pandas as pd

# Load data
df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V3_WITH_MFG_SUBCLUSTERS.csv', low_memory=False)
manual = pd.read_csv('analysis/manufacturing_manual_classifications.csv')

print("="*80)
print("APPLYING MANUAL MANUFACTURING CLASSIFICATIONS")
print("="*80)
print(f"Total manual classifications: {len(manual)}")

# Create mapping dictionary
manual_mapping = dict(zip(manual['Account Name'], manual['New_Subcluster']))

# Apply manual classifications
for account_name, new_cluster in manual_mapping.items():
    mask = df['Account Name'] == account_name
    if mask.sum() > 0:
        old_cluster = df.loc[mask, 'Manufacturing_Subcluster'].values[0]
        df.loc[mask, 'Manufacturing_Subcluster'] = new_cluster
        df.loc[mask, 'Industry_Cluster_V3'] = new_cluster
        print(f"✅ {account_name}: {old_cluster} → {new_cluster}")
    else:
        print(f"⚠️  {account_name}: NOT FOUND")

# Save updated dataset
df.to_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V3_UPDATED.csv', index=False)

print("\n" + "="*80)
print("✅ SAVED: data/customermethodaccount_01-07-2026_RECLUSTERED_V3_UPDATED.csv")
print("="*80)

# Recalculate statistics for active manufacturing
mfg = df[(df['Industry_Cluster_Enhanced_V2'] == 'General/Specialty Manufacturing') &
         (df['Active?'] == True)].copy()

print("\n" + "="*80)
print("UPDATED SUB-CLUSTER STATISTICS")
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

# Calculate improvement
uncategorized = results.loc['General/Specialty Manufacturing (Uncategorized)', 'Account_Count']
categorized = len(mfg) - uncategorized
pct_categorized = (categorized / len(mfg)) * 100

print("\n" + "="*80)
print(f"COVERAGE: {int(categorized)}/{len(mfg)} accounts categorized ({pct_categorized:.1f}%)")
print(f"REMAINING UNCATEGORIZED: {int(uncategorized)} accounts")
print("="*80)
