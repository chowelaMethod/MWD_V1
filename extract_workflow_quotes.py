#!/usr/bin/env python3
"""
Extract the most powerful quotes that encapsulate MWD's workflow problems
Focus on: UX issues, workflow challenges, complexity, and what needs to be fixed
"""

import pandas as pd

# Load the categorized quotes
df = pd.read_csv('results/churn_quotes_categorized.csv', encoding='utf-8-sig')

print("="*100)
print("MOST POWERFUL QUOTES HIGHLIGHTING METHOD'S WORKFLOW PROBLEMS")
print("="*100)

# Define the categories that highlight workflow/product issues
workflow_categories = [
    'Too Complex/Clunky',
    'Difficult Workflows / Workflow Challenges',
    'UX/UI Issues',
    'Poor Customization',
    'Feature Gaps',
    'Performance Issues',
    'Onboarding Failed'
]

# Create a scoring system to find the most impactful quotes
def quote_impact_score(row):
    """Score quotes based on MRR, tenure, and specificity"""
    mrr = row['Last Invoice $']
    tenure = row.get('Tenure_Months', 0)
    reason_length = len(str(row['Reason_Clean']))

    # Higher MRR = more valuable customer
    # Longer tenure = more credible (they really tried)
    # Longer reason = more specific feedback
    score = (mrr * 0.5) + (tenure * 2) + (reason_length * 0.1)
    return score

df['Impact_Score'] = df.apply(quote_impact_score, axis=1)

# Get most impactful quotes by category
print("\n" + "="*100)
print("TOP WORKFLOW PROBLEM QUOTES BY CATEGORY")
print("="*100)

categories_to_analyze = {
    'Too Complex/Clunky': 'COMPLEXITY & USABILITY PROBLEMS',
    'UX/UI Issues': 'USER EXPERIENCE FAILURES',
    'Poor Customization': 'CUSTOMIZATION IS TOO HARD/EXPENSIVE',
    'Feature Gaps': 'MISSING CRITICAL FEATURES',
    'Performance Issues': 'PERFORMANCE & RELIABILITY PROBLEMS',
    'Onboarding Failed': 'ONBOARDING & IMPLEMENTATION FAILURES'
}

all_powerful_quotes = []

for category, title in categories_to_analyze.items():
    cat_data = df[df['Category'] == category].copy()

    if len(cat_data) == 0:
        continue

    print(f"\n{'='*100}")
    print(f"{title}")
    print(f"{'='*100}")

    # Sort by impact score
    cat_data = cat_data.sort_values('Impact_Score', ascending=False)

    # Get top 5 most impactful
    for idx, row in cat_data.head(5).iterrows():
        account = row['Account Name']
        mrr = row['Last Invoice $']
        tenure = row.get('Tenure_Months', 'N/A')
        reason = row['Reason_Clean']

        quote_data = {
            'category': title,
            'account': account,
            'mrr': mrr,
            'tenure': tenure,
            'quote': reason
        }
        all_powerful_quotes.append(quote_data)

        print(f"\n• [{account}] ${mrr:,.0f}/mo | {tenure} months tenure")
        print(f"  \"{reason}\"")

# Now find quotes that mention specific problems
print("\n" + "="*100)
print("QUOTES HIGHLIGHTING SPECIFIC PROBLEMS TO FIX")
print("="*100)

specific_problems = {
    'Field/Mobile Issues': ['ipad', 'mobile', 'field', 'tablet', 'phone', 'android', 'ios'],
    'Slow Performance': ['slow', 'freezing', 'freeze', 'lag', 'white screen', 'loading'],
    'Workflow Complexity': ['too many steps', 'cumbersome', 'complicated', 'difficult to navigate', 'not intuitive'],
    'Sales Team Problems': ['sales team', 'sales rep', 'sales people', 'salesforce', 'sales-first'],
    'Reporting Gaps': ['no reporting', 'no dashboard', 'reporting', 'reports', 'analytics', 'visibility'],
    'Customization Cost': ['exorbitant', 'too expensive', 'professional services', 'customization fee', '$10k'],
    'QB Sync Issues': ['sync', 'disconnect', 'reconnect', 'unstable', 'quickbooks crash', 'qb issue'],
    'Manual Work': ['manual', 'data entry', 'time consuming', 'labor intensive', 'too much work']
}

for problem, keywords in specific_problems.items():
    matching_quotes = df[df['Reason_Clean'].str.lower().str.contains('|'.join(keywords), na=False, case=False)]

    if len(matching_quotes) == 0:
        continue

    # Get highest-value examples
    matching_quotes = matching_quotes.sort_values('Last Invoice $', ascending=False)

    print(f"\n{'='*100}")
    print(f"{problem.upper()} ({len(matching_quotes)} customers mentioned this)")
    print(f"{'='*100}")

    for idx, row in matching_quotes.head(3).iterrows():
        account = row['Account Name']
        mrr = row['Last Invoice $']
        tenure = row.get('Tenure_Months', 'N/A')
        reason = row['Reason_Clean']

        # Truncate if too long
        if len(reason) > 250:
            reason = reason[:247] + "..."

        print(f"\n• [{account}] ${mrr:,.0f}/mo | {tenure} months")
        print(f"  \"{reason}\"")

# Print the absolute most damaging quotes
print("\n" + "="*100)
print("🔥 THE 10 MOST DAMAGING QUOTES (By Impact Score)")
print("="*100)

top_10 = df.nlargest(10, 'Impact_Score')

for idx, row in top_10.iterrows():
    account = row['Account Name']
    mrr = row['Last Invoice $']
    tenure = row.get('Tenure_Months', 'N/A')
    category = row['Category']
    reason = row['Reason_Clean']

    if len(reason) > 300:
        reason = reason[:297] + "..."

    print(f"\n{top_10.index.get_loc(idx) + 1}. [{account}] ${mrr:,.0f}/mo | {tenure} months | {category}")
    print(f"   \"{reason}\"")

print("\n" + "="*100)
print("ANALYSIS COMPLETE")
print("="*100)
