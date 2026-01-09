#!/usr/bin/env python3
"""
Investigate the 208 accounts in MWD_Enriched but not in existing dataset
Checks for fuzzy name matches, test accounts, and active status indicators
"""

import pandas as pd
from pathlib import Path
from difflib import SequenceMatcher

def similar(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def main():
    print("="*80)
    print("INVESTIGATING 208 MISSING ACCOUNTS")
    print("="*80)

    # Load datasets
    mwd_df = pd.read_csv('data/MWD_Enriched_Accounts.csv')
    existing_df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')

    # Normalize names
    mwd_accounts = set(mwd_df['Account Name'].str.lower().str.strip())
    existing_accounts = set(existing_df['Account'].str.lower().str.strip())

    # Find missing accounts
    missing = mwd_accounts - existing_accounts
    print(f"\n📊 Found {len(missing)} accounts in MWD_Enriched but not in existing data\n")

    # Create lookup for analysis
    missing_df = mwd_df[mwd_df['Account Name'].str.lower().str.strip().isin(missing)].copy()

    # Categorize missing accounts
    test_accounts = []
    restore_accounts = []
    suspicious_names = []
    likely_real = []

    test_keywords = ['test', 'demo', 'training', 'sample', 'example']
    suspicious_patterns = [
        lambda x: len(x) <= 2,  # Very short names like "aw"
        lambda x: 'restore' in x.lower(),
        lambda x: '20241015' in x or '20251012' in x,  # Date-like patterns
        lambda x: any(kw in x.lower() for kw in test_keywords)
    ]

    for acct in sorted(missing):
        mwd_row = missing_df[missing_df['Account Name'].str.lower().str.strip() == acct].iloc[0]

        if any(kw in acct for kw in test_keywords):
            test_accounts.append({
                'account': acct,
                'users': mwd_row.get('Users', 'N/A'),
                'sign_up_date': mwd_row.get('Sign Up Date', 'N/A'),
                'industry': mwd_row.get('Industry (Research)', 'N/A')
            })
        elif 'restore' in acct:
            restore_accounts.append({
                'account': acct,
                'users': mwd_row.get('Users', 'N/A'),
                'sign_up_date': mwd_row.get('Sign Up Date', 'N/A')
            })
        elif any(check(acct) for check in suspicious_patterns):
            suspicious_names.append({
                'account': acct,
                'users': mwd_row.get('Users', 'N/A'),
                'sign_up_date': mwd_row.get('Sign Up Date', 'N/A'),
                'company_name': mwd_row.get('Company Name in QB', 'N/A')
            })
        else:
            likely_real.append({
                'account': acct,
                'users': mwd_row.get('Users', 'N/A'),
                'sign_up_date': mwd_row.get('Sign Up Date', 'N/A'),
                'industry': mwd_row.get('Industry (Research)', 'N/A'),
                'vertical': mwd_row.get('Vertical', 'N/A'),
                'mrr_estimate': mwd_row.get('Last Invoice $', 'N/A')
            })

    # Report findings
    print("🔬 CATEGORIZATION OF MISSING ACCOUNTS")
    print("="*80)

    print(f"\n1. TEST/DEMO ACCOUNTS ({len(test_accounts)}):")
    if test_accounts:
        for i, acct in enumerate(test_accounts[:10], 1):
            print(f"   {i}. {acct['account']}")
            print(f"      Users: {acct['users']}, Sign Up: {acct['sign_up_date']}")
            print(f"      Industry: {acct['industry']}")
        if len(test_accounts) > 10:
            print(f"   ... and {len(test_accounts) - 10} more")
    else:
        print("   None found")

    print(f"\n2. RESTORE/BACKUP ACCOUNTS ({len(restore_accounts)}):")
    if restore_accounts:
        for i, acct in enumerate(restore_accounts[:10], 1):
            print(f"   {i}. {acct['account']}")
            print(f"      Users: {acct['users']}, Sign Up: {acct['sign_up_date']}")
        if len(restore_accounts) > 10:
            print(f"   ... and {len(restore_accounts) - 10} more")
    else:
        print("   None found")

    print(f"\n3. SUSPICIOUS NAMES ({len(suspicious_names)}):")
    if suspicious_names:
        for i, acct in enumerate(suspicious_names[:10], 1):
            print(f"   {i}. {acct['account']}")
            print(f"      Company: {acct['company_name']}")
            print(f"      Users: {acct['users']}, Sign Up: {acct['sign_up_date']}")
        if len(suspicious_names) > 10:
            print(f"   ... and {len(suspicious_names) - 10} more")
    else:
        print("   None found")

    print(f"\n4. LIKELY REAL ACCOUNTS ({len(likely_real)}):")
    print("   These appear to be legitimate business accounts")
    if likely_real:
        for i, acct in enumerate(likely_real[:20], 1):
            print(f"\n   {i}. {acct['account']}")
            print(f"      Industry: {acct['industry']}")
            print(f"      Vertical: {acct['vertical']}")
            print(f"      Users: {acct['users']}, Last Invoice: ${acct['mrr_estimate']}")
            print(f"      Sign Up: {acct['sign_up_date']}")
        if len(likely_real) > 20:
            print(f"\n   ... and {len(likely_real) - 20} more")

    # Check for fuzzy matches
    print(f"\n" + "="*80)
    print("🔍 CHECKING FOR FUZZY NAME MATCHES")
    print("="*80)
    print("\nLooking for accounts that might be renamed versions...\n")

    fuzzy_matches = []
    for missing_acct in list(likely_real)[:50]:  # Sample first 50 for performance
        missing_name = missing_acct['account']
        best_match = None
        best_ratio = 0

        for existing_acct in existing_accounts:
            # Skip if existing_acct is not a string (NaN, etc.)
            if not isinstance(existing_acct, str):
                continue
            ratio = similar(missing_name, existing_acct)
            if ratio > best_ratio and ratio > 0.7:  # 70% similarity threshold
                best_ratio = ratio
                best_match = existing_acct

        if best_match:
            fuzzy_matches.append({
                'missing': missing_name,
                'possible_match': best_match,
                'similarity': best_ratio
            })

    if fuzzy_matches:
        print(f"Found {len(fuzzy_matches)} potential name variations:")
        for i, match in enumerate(fuzzy_matches[:10], 1):
            print(f"\n{i}. MWD: '{match['missing']}'")
            print(f"   Existing: '{match['possible_match']}'")
            print(f"   Similarity: {match['similarity']:.1%}")
        if len(fuzzy_matches) > 10:
            print(f"\n... and {len(fuzzy_matches) - 10} more possible matches")
    else:
        print("No fuzzy matches found (accounts are genuinely different)")

    # Summary
    print(f"\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    non_suspicious = len(likely_real) - len(fuzzy_matches)

    print(f"\nOf 208 missing accounts:")
    print(f"  • {len(test_accounts)} are test/demo accounts (exclude)")
    print(f"  • {len(restore_accounts)} are restore/backup accounts (exclude)")
    print(f"  • {len(suspicious_names)} have suspicious naming patterns (review)")
    print(f"  • {len(fuzzy_matches)} may be renamed versions (reconcile)")
    print(f"  • ~{non_suspicious} appear to be genuinely new accounts (investigate)")

    print(f"\n📋 RECOMMENDATIONS:")
    print(f"  1. Exclude {len(test_accounts) + len(restore_accounts)} test/restore accounts from analysis")
    print(f"  2. Manually review {len(suspicious_names)} suspicious names")
    print(f"  3. Reconcile {len(fuzzy_matches)} potential name variations")
    print(f"  4. Investigate remaining ~{non_suspicious} accounts:")
    print(f"     - Check if they're active customers")
    print(f"     - Verify they weren't added after 01-07-2026")
    print(f"     - Consider adding to your primary dataset if active")

    # Export findings
    output_path = Path('results/missing_accounts_analysis.csv')
    output_path.parent.mkdir(exist_ok=True)

    missing_df.to_csv(output_path, index=False)
    print(f"\n✅ Full missing accounts data exported to: {output_path}")

if __name__ == '__main__':
    main()
