#!/usr/bin/env python3
"""
Investigate the 34 validation subset accounts missing from active dataset
CRITICAL: These accounts were in General W/D validation AND MWD_Enriched but NOT in active accounts
"""

import pandas as pd
from pathlib import Path

def main():
    print("="*100)
    print("CRITICAL: Investigating 34 Validation Subset Accounts Missing from Active Dataset")
    print("="*100)

    # Load all datasets
    print("\nLoading datasets...")
    validation_df = pd.read_csv('results/general_wd_validation_results.csv')
    mwd_df = pd.read_csv('data/MWD_Enriched_Accounts.csv')
    main_df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv',
                          dtype={'Active?': str}, low_memory=False)

    # Identify the 34 missing accounts
    validation_accounts = set(validation_df['Account_Name'].str.lower().str.strip())
    main_accounts = set(main_df['Account'].str.lower().str.strip())
    missing_accounts = validation_accounts - main_accounts

    print(f"✓ Validation subset: {len(validation_accounts):,} accounts")
    print(f"✓ Main dataset: {len(main_accounts):,} unique accounts")
    print(f"⚠️  Missing: {len(missing_accounts):,} accounts\n")

    # Check if they exist in main dataset but with different active status
    print("="*100)
    print("STEP 1: Checking if accounts exist in FULL main dataset (not just active)")
    print("="*100)

    all_main_accounts = set(main_df['Account'].str.lower().str.strip())
    missing_but_in_full = missing_accounts & all_main_accounts

    if len(missing_but_in_full) > 0:
        print(f"\n✓ Found {len(missing_but_in_full)} accounts in full main dataset!")
        print("   These accounts exist but may be marked as inactive.\n")

        for acct in sorted(missing_but_in_full)[:10]:
            main_row = main_df[main_df['Account'].str.lower().str.strip() == acct].iloc[0]
            print(f"   • {acct}")
            print(f"     Active?: {main_row.get('Active?', 'N/A')}")
            print(f"     Users: {main_row.get('Users', 'N/A')}")
            print(f"     MRR: ${main_row.get('MRR_Calculated', 0):.2f}")
            print()
    else:
        print("\n⚠️  None of the 34 accounts found in full main dataset")
        print("   They are completely missing, not just inactive.\n")

    # Get full details from MWD_Enriched
    print("="*100)
    print("STEP 2: Full Details from MWD_Enriched")
    print("="*100)

    missing_details = []
    for acct in missing_accounts:
        mwd_row = mwd_df[mwd_df['Account Name'].str.lower().str.strip() == acct]
        if len(mwd_row) > 0:
            mwd_row = mwd_row.iloc[0]
            missing_details.append({
                'account': acct,
                'company_name_qb': mwd_row.get('Company Name in QB', 'N/A'),
                'users': mwd_row.get('Users', 0),
                'invoice': mwd_row.get('Last Invoice $', 0),
                'sign_up_date': mwd_row.get('Sign Up Date', 'Unknown'),
                'health_score': mwd_row.get('Health Score', 'N/A'),
                'industry': mwd_row.get('Industry (Research)', 'Unknown'),
                'workflow_type': mwd_row.get('Workflow Type', 'Unknown'),
                'vertical': mwd_row.get('Vertical', 'Unknown'),
                'website': mwd_row.get('Website', 'N/A')
            })

    missing_df = pd.DataFrame(missing_details)
    missing_df['users'] = pd.to_numeric(missing_df['users'], errors='coerce')
    missing_df['invoice'] = pd.to_numeric(missing_df['invoice'], errors='coerce')
    missing_df = missing_df.sort_values(['users', 'invoice'], ascending=[False, False])

    # Priority 1: Enterprise accounts (>5 users)
    print("\n🚨 PRIORITY 1: Enterprise Accounts (>5 users)")
    print("-"*100)
    enterprise = missing_df[missing_df['users'] > 5]

    if len(enterprise) > 0:
        for i, row in enterprise.iterrows():
            print(f"\n{row['account'].upper()}")
            print(f"  Company Name (QB): {row['company_name_qb']}")
            print(f"  Users: {row['users']:.0f} | Invoice: ${row['invoice']:.0f} | Health Score: {row['health_score']}")
            print(f"  Sign-Up: {row['sign_up_date']}")
            print(f"  Industry: {row['industry']}")
            print(f"  Workflow: {row['workflow_type']}")
            print(f"  Website: {row['website']}")
            print(f"\n  🔍 ACTION REQUIRED:")
            print(f"     1. Search CRM for: '{row['company_name_qb']}'")
            print(f"     2. Check for account name variations")
            print(f"     3. Verify current active status")
            print(f"     4. If active: WHY is it missing from analysis?")
    else:
        print("  None found")

    # Priority 2: Multi-user accounts (2-5 users)
    print("\n\n🟡 PRIORITY 2: Multi-User Accounts (2-5 users)")
    print("-"*100)
    multi_user = missing_df[(missing_df['users'] >= 2) & (missing_df['users'] <= 5)]

    if len(multi_user) > 0:
        for i, row in multi_user.iterrows():
            print(f"\n{row['account']}")
            print(f"  Company: {row['company_name_qb']} | Users: {row['users']:.0f} | Invoice: ${row['invoice']:.0f}")
            print(f"  Sign-Up: {row['sign_up_date']} | Industry: {row['industry'][:60]}")
    else:
        print("  None found")

    # Priority 3: Recent sign-ups (2025-2026)
    print("\n\n📅 PRIORITY 3: Recent Sign-Ups (2025-2026)")
    print("-"*100)
    missing_df['sign_up_date'] = pd.to_datetime(missing_df['sign_up_date'], errors='coerce')
    recent = missing_df[missing_df['sign_up_date'] >= '2025-01-01'].sort_values('sign_up_date', ascending=False)

    if len(recent) > 0:
        print(f"\n  Found {len(recent)} accounts signed up in 2025-2026:")
        for i, row in recent.head(10).iterrows():
            print(f"\n  {row['account']}")
            print(f"    Sign-Up: {row['sign_up_date'].strftime('%Y-%m-%d')} | Users: {row['users']:.0f} | Invoice: ${row['invoice']:.0f}")
            print(f"    Company: {row['company_name_qb']}")
            print(f"    Industry: {row['industry'][:70]}")

        print(f"\n  🔍 HYPOTHESIS: These may be post-01-07-2026 additions")
        print(f"     Your dataset export: 01-07-2026")
        print(f"     Latest sign-up in missing accounts: {recent['sign_up_date'].max().strftime('%Y-%m-%d')}")
        print(f"     If sign-ups are BEFORE 01-07-2026: Data integrity issue")
        print(f"     If sign-ups are AFTER 01-07-2026: Expected (not in export yet)")

    # Priority 4: High invoice amounts
    print("\n\n💰 PRIORITY 4: High Invoice Amounts (>$150)")
    print("-"*100)
    high_invoice = missing_df[missing_df['invoice'] > 150].sort_values('invoice', ascending=False)

    if len(high_invoice) > 0:
        for i, row in high_invoice.head(10).iterrows():
            print(f"\n  {row['account']}")
            print(f"    Invoice: ${row['invoice']:.0f} | Users: {row['users']:.0f} | Sign-Up: {row['sign_up_date']}")
            print(f"    Company: {row['company_name_qb']}")

    # Summary and recommendations
    print("\n\n" + "="*100)
    print("SUMMARY & RECOMMENDATIONS")
    print("="*100)

    print(f"\n📊 Statistics:")
    print(f"   Total missing: {len(missing_df)}")
    print(f"   Enterprise (>5 users): {len(enterprise)}")
    print(f"   Multi-user (2-5 users): {len(multi_user)}")
    print(f"   Single user: {len(missing_df[missing_df['users'] == 1])}")
    print(f"   Recent sign-ups (2025-2026): {len(recent)}")
    print(f"   High invoice (>$150): {len(high_invoice)}")

    print(f"\n📋 Immediate Actions:")
    print(f"   1. Investigate enterprise accounts: {', '.join(enterprise['account'].tolist()) if len(enterprise) > 0 else 'None'}")
    print(f"   2. Check CRM for accounts by Company Name (QB) - may be named differently")
    print(f"   3. Verify sign-up dates - if before 01-07-2026, should be in dataset")
    print(f"   4. Review recent sign-ups - may be expected if after export date")

    print(f"\n❓ Questions to Answer:")
    print(f"   1. Are these accounts marked as 'Active?' = FALSE in your system?")
    print(f"   2. Were they filtered out intentionally (e.g., test accounts, churned)?")
    print(f"   3. Do they exist under different account names?")
    print(f"   4. Were they added after 01-07-2026 export date?")

    # Export results
    output_path = Path('results/validation_missing_34_accounts_detailed.csv')
    missing_df.to_csv(output_path, index=False)
    print(f"\n✅ Full details exported to: {output_path}")

    # Create action items CSV
    action_df = missing_df[['account', 'company_name_qb', 'users', 'invoice', 'sign_up_date', 'health_score']].copy()
    action_df['priority'] = action_df.apply(
        lambda x: 'P1-Enterprise' if x['users'] > 5
        else 'P2-Multi-User' if x['users'] > 1
        else 'P3-Recent' if pd.notna(x['sign_up_date']) and pd.to_datetime(x['sign_up_date']) >= pd.Timestamp('2025-01-01')
        else 'P4-Standard',
        axis=1
    )
    action_df['action_needed'] = 'Search CRM by company name and verify status'
    action_df['status'] = 'PENDING INVESTIGATION'

    action_path = Path('results/validation_missing_ACTION_ITEMS.csv')
    action_df.to_csv(action_path, index=False)
    print(f"✅ Action items exported to: {action_path}")

    print("\n" + "="*100)
    print("NEXT STEPS")
    print("="*100)
    print("\n1. Open results/validation_missing_ACTION_ITEMS.csv")
    print("2. For each P1-Enterprise account, search CRM by 'company_name_qb'")
    print("3. Document findings in 'status' column")
    print("4. Determine: Add to active dataset, confirm inactive, or reconcile name")

if __name__ == '__main__':
    main()
