#!/usr/bin/env python3
"""
Extract the most compelling customer churn quotes by category
"""

import pandas as pd
import re

# Load the free-text data
df = pd.read_csv('results/churn_reasons_freetext.csv', encoding='utf-8-sig')
print(f"Loaded {len(df):,} free-text cancellation reasons\n")

# Filter out duplicate account references and very short reasons
df['Reason_Clean'] = df['Cancellation Reason Other'].str.strip()
df = df[~df['Reason_Clean'].str.contains('Conversion Exception Reason|Duplicate|other account|Original is:|Actual account:',
                                         case=False, na=False)]
df = df[df['Reason_Clean'].str.len() > 30]  # At least 30 chars
print(f"After filtering duplicates and short reasons: {len(df):,}\n")

# Define categories with keywords
categories = {
    'Competitor Loss': ['salesforce', 'different crm', 'another crm', 'switch', 'moved to',
                       'netsuite', 'different direction', 'other crm', 'competing'],

    'Feature Gaps': ['limited features', 'missing', 'need more', 'doesn\'t have', 'no dashboards',
                    'no reporting', 'can\'t do', 'unable to', 'not enough', 'lack of',
                    'feature', 'functionality', 'capability'],

    'Too Complex/Clunky': ['clunky', 'difficult', 'complicated', 'too complex', 'hard to use',
                          'confusing', 'not intuitive', 'steep learning'],

    'Poor Customization': ['customize', 'customization', 'exorbitant fees', 'too expensive to',
                          'can\'t customize', 'customizing'],

    'Integration Issues': ['integration', 'sync', 'quickbooks', 'doesn\'t integrate',
                          'not integrated', 'qb', 'connection'],

    'Not Meeting Needs': ['not what we need', 'doesn\'t fit', 'not suitable', 'not the right',
                         'not for us', 'doesn\'t work for', 'not meeting'],

    'Outgrew Product': ['outgrow', 'outgrown', 'need more power', 'too basic', 'need enterprise',
                       'need advanced', 'scaling', 'expand'],

    'UX/UI Issues': ['interface', 'user experience', 'ui', 'design', 'layout', 'navigation'],

    'Price/Value': ['too expensive', 'price', 'cost', 'budget', 'afford', 'expensive',
                   'pricing', 'pay too much'],

    'Onboarding Failed': ['no time', 'couldn\'t implement', 'implementation', 'onboard',
                         'getting started', 'setup', 'initial'],

    'QuickBooks Dependency': ['no longer use quickbooks', 'moved from qb', 'quit quickbooks',
                             'stopped using qb', 'switch from quickbooks'],

    'Performance Issues': ['slow', 'freezing', 'crash', 'bug', 'error', 'not working',
                          'technical issue', 'doesn\'t work']
}

# Categorize each reason
def categorize_reason(text):
    if pd.isna(text):
        return 'Uncategorized'

    text_lower = str(text).lower()
    matches = []

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                matches.append(category)
                break

    if not matches:
        return 'Uncategorized'
    elif len(matches) == 1:
        return matches[0]
    else:
        return matches[0]  # Take first match

df['Category'] = df['Reason_Clean'].apply(categorize_reason)

# Print best quotes by category
print("="*100)
print("MOST COMPELLING CUSTOMER QUOTES BY CATEGORY")
print("="*100)

for category in sorted(categories.keys()):
    cat_data = df[df['Category'] == category].sort_values('Last Invoice $', ascending=False)

    if len(cat_data) == 0:
        continue

    print(f"\n{'='*100}")
    print(f"{category.upper()}")
    print(f"{'='*100}")
    print(f"Count: {len(cat_data):,} | Avg MRR: ${cat_data['Last Invoice $'].mean():.2f} | "
          f"Total MRR Lost: ${cat_data['Last Invoice $'].sum():,.2f}\n")

    # Show top 10 by MRR
    for idx, row in cat_data.head(10).iterrows():
        account = row['Account Name']
        mrr = row['Last Invoice $']
        tenure = row.get('Tenure_Months', 'N/A')
        reason = row['Reason_Clean']

        # Clean up reason text
        if len(reason) > 200:
            reason = reason[:197] + "..."

        print(f"• [{account}] ${mrr:,.0f}/mo | {tenure} months")
        print(f"  \"{reason}\"")
        print()

# Save categorized data
df_output = df.sort_values('Last Invoice $', ascending=False)
df_output.to_csv('results/churn_quotes_categorized.csv', index=False)
print(f"\n{'='*100}")
print("✓ Saved: results/churn_quotes_categorized.csv")
print(f"{'='*100}\n")

# Summary stats by category
print("\nSUMMARY BY CATEGORY:\n")
summary = df.groupby('Category').agg({
    'Account Name': 'count',
    'Last Invoice $': ['sum', 'mean', 'median']
}).round(2)
summary.columns = ['Count', 'Total MRR Lost', 'Avg MRR', 'Median MRR']
summary = summary.sort_values('Total MRR Lost', ascending=False)
print(summary)
