#!/usr/bin/env python3
"""
Website-Based Cluster Validation Script
Uses WebFetch tool to retrieve website content and validate industry classifications.

Author: Evidence-Based Analysis
Date: January 7, 2026
"""

import pandas as pd
import re
from typing import Dict, List, Tuple

# Import cluster keyword definitions from recluster_analysis.py
# These are the same keywords used for initial clustering
CLUSTER_KEYWORDS = {
    'Medical Equipment & Supplies': [
        'medical', 'healthcare', 'hospital', 'clinic', 'surgical', 'diagnostic',
        'patient', 'pharmaceutical', 'laboratory', 'dental', 'therapy', 'rehabilitation'
    ],
    'Food & Beverage Dist/Mfg': [
        'food', 'beverage', 'bakery', 'dairy', 'meat', 'produce', 'grocery',
        'restaurant', 'catering', 'brewery', 'distillery', 'wine', 'coffee', 'organic'
    ],
    'Building Materials & Construction': [
        'lumber', 'concrete', 'brick', 'stone', 'flooring', 'roofing', 'siding',
        'drywall', 'insulation', 'construction', 'contractor', 'building materials'
    ],
    'Industrial Equipment & Machinery': [
        'valve', 'pump', 'bearing', 'motor', 'equipment', 'machinery', 'industrial',
        'hydraulic', 'pneumatic', 'automation', 'manufacturing equipment'
    ],
    'Chemicals, Plastics & Rubber': [
        'chemical', 'plastic', 'rubber', 'polymer', 'resin', 'compound', 'coating',
        'adhesive', 'sealant', 'lubricant', 'solvent'
    ],
    'Electronics & Technology': [
        'electronics', 'technology', 'computer', 'software', 'hardware', 'IT',
        'networking', 'telecommunications', 'semiconductor', 'circuit'
    ],
    'Furniture & Home Furnishings': [
        'furniture', 'furnishing', 'interior design', 'home decor', 'upholstery',
        'cabinet', 'seating', 'table', 'desk', 'bedroom', 'living room'
    ],
    'Apparel & Textiles': [
        'clothing', 'apparel', 'textile', 'fabric', 'garment', 'fashion',
        'footwear', 'accessories', 'uniform', 'workwear'
    ],
    'Automotive & Transportation': [
        'automotive', 'vehicle', 'truck', 'car', 'auto parts', 'transportation',
        'fleet', 'tire', 'brake', 'engine', 'transmission'
    ],
    'Metal Fabrication & Steel': [
        'metal', 'steel', 'fabrication', 'welding', 'machining', 'sheet metal',
        'aluminum', 'iron', 'stainless', 'fabricator', 'metalworking'
    ],
    'Electrical & Lighting Equipment': [
        'electrical', 'lighting', 'illumination', 'fixture', 'lamp', 'LED',
        'wiring', 'switch', 'outlet', 'panel', 'electrician'
    ],
    'Packaging & Printing': [
        'packaging', 'printing', 'label', 'box', 'container', 'carton',
        'corrugated', 'flexographic', 'lithographic', 'graphic design'
    ],
    'Office Supplies & Equipment': [
        'office supplies', 'stationery', 'paper', 'printer', 'toner', 'ink',
        'desk', 'chair', 'file', 'office furniture', 'workspace'
    ],
    'Safety & Security Equipment': [
        'safety', 'security', 'protection', 'PPE', 'surveillance', 'alarm',
        'access control', 'fire', 'emergency', 'protective equipment'
    ],
    'Sporting Goods & Fitness Equipment': [
        'sporting goods', 'fitness', 'athletic', 'recreation', 'gym', 'exercise',
        'sports equipment', 'outdoor', 'camping', 'golf', 'tennis'
    ],
    'Signs, Graphics & Displays': [
        'signs', 'signage', 'graphics', 'display', 'banner', 'billboard',
        'vinyl', 'digital printing', 'visual communication', 'branding'
    ],
    'Agriculture & Greenhouse/Nursery': [
        'agriculture', 'farming', 'greenhouse', 'nursery', 'horticulture',
        'crop', 'irrigation', 'fertilizer', 'seed', 'plant', 'landscaping'
    ],
    'Wood Products & Lumber': [
        'wood', 'lumber', 'timber', 'hardwood', 'plywood', 'sawmill',
        'woodworking', 'flooring', 'millwork', 'veneer'
    ],
    'HVAC & Refrigeration Equipment': [
        'HVAC', 'heating', 'cooling', 'air conditioning', 'refrigeration',
        'ventilation', 'climate control', 'furnace', 'chiller', 'compressor'
    ],
    'Manufacturer Representatives': [
        'manufacturer rep', 'sales representative', 'agency', 'distribution rep',
        'independent rep', 'manufacturers agent'
    ],
    'General Retail': [
        'retail', 'store', 'shop', 'consumer', 'B2C', 'customer',
        'merchandise', 'ecommerce', 'online store'
    ],
    'General Wholesale/Distribution': [
        'wholesale', 'distributor', 'distribution', 'supply', 'supplier',
        'B2B', 'bulk', 'warehouse', 'logistics'
    ],
    'General/Specialty Manufacturing': [
        'manufacturing', 'manufacturer', 'production', 'assembly', 'factory',
        'fabrication', 'processing', 'custom manufacturing'
    ],
    'Services & Other': [
        'services', 'consulting', 'professional services', 'business services',
        'support services', 'management', 'advisory'
    ]
}


def extract_keywords_from_text(text: str, keywords: List[str]) -> Dict[str, int]:
    """
    Extract and count keyword matches from text.
    Returns dict of keyword -> count.
    """
    text_lower = text.lower()
    keyword_counts = {}

    for keyword in keywords:
        # Use word boundaries to avoid substring false positives
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        matches = len(re.findall(pattern, text_lower))
        if matches > 0:
            keyword_counts[keyword] = matches

    return keyword_counts


def calculate_cluster_confidence(keyword_counts: Dict[str, int],
                                  cluster_keywords: List[str]) -> float:
    """
    Calculate confidence score (0-100) that text matches a cluster.
    Based on:
    - Number of different keywords found
    - Total keyword frequency
    """
    if not keyword_counts:
        return 0.0

    # Count how many different cluster keywords were found
    keywords_found = len(keyword_counts)
    total_keywords = len(cluster_keywords)

    # Total frequency of keywords
    total_frequency = sum(keyword_counts.values())

    # Confidence score:
    # - 50% weight on keyword diversity (what % of cluster keywords found)
    # - 50% weight on keyword frequency (how many times they appear)
    diversity_score = (keywords_found / total_keywords) * 50
    frequency_score = min(total_frequency / 10, 1.0) * 50  # Cap at 10 occurrences

    confidence = diversity_score + frequency_score
    return min(confidence, 100.0)


def classify_website_content(website_content: str) -> Dict[str, float]:
    """
    Classify website content against all cluster definitions.
    Returns dict of cluster -> confidence score.
    """
    cluster_scores = {}

    for cluster, keywords in CLUSTER_KEYWORDS.items():
        keyword_counts = extract_keywords_from_text(website_content, keywords)
        confidence = calculate_cluster_confidence(keyword_counts, keywords)
        cluster_scores[cluster] = confidence

    return cluster_scores


def validate_account_website(account_name: str, website_url: str,
                               expected_cluster: str) -> Dict:
    """
    Validate a single account's website against expected cluster.

    NOTE: This is a placeholder that would use WebFetch tool in actual implementation.
    For now, returns a template result.
    """
    result = {
        'Account_Name': account_name,
        'Website_URL': website_url,
        'Expected_Cluster': expected_cluster,
        'Website_Accessible': None,  # True/False/Error
        'Website_Classification': None,
        'Website_Confidence': 0.0,
        'Expected_Confidence': 0.0,
        'Matches_Expected': None,  # True/False
        'Conflict_Cluster': None,
        'Conflict_Confidence': 0.0,
        'Keywords_Found': '',
        'Notes': ''
    }

    # In actual implementation, would use WebFetch here:
    # Example: content = webfetch(website_url, "Extract business description, products, services")
    # For now, mark as needs manual implementation
    result['Notes'] = 'PLACEHOLDER - Requires WebFetch tool integration'

    return result


def validate_cluster_websites(cluster_name: str = None,
                                sample_size: int = None,
                                output_file: str = 'website_validation_results.csv'):
    """
    Validate accounts via website content analysis.

    Args:
        cluster_name: If specified, only validate this cluster
        sample_size: If specified, limit to N accounts per cluster
        output_file: Output CSV filename
    """
    print("="*80)
    print("WEBSITE-BASED CLUSTER VALIDATION")
    print("="*80)

    # Load data
    print("\nLoading dataset...")
    df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')
    active = df[df['Active?'] == True].copy()

    # Filter to accounts with websites
    active_with_websites = active[
        active['Website'].notna() &
        (active['Website'] != '') &
        (active['Website'] != 'nan')
    ].copy()

    print(f"Total active accounts: {len(active)}")
    print(f"With website URLs: {len(active_with_websites)} ({len(active_with_websites)/len(active)*100:.1f}%)")

    # Filter by cluster if specified
    if cluster_name:
        active_with_websites = active_with_websites[
            active_with_websites['Industry_Cluster_Enhanced_V2'] == cluster_name
        ]
        print(f"\nFiltering to cluster: {cluster_name}")
        print(f"Accounts to validate: {len(active_with_websites)}")

    # Sample if specified
    if sample_size and len(active_with_websites) > sample_size:
        active_with_websites = active_with_websites.sample(n=sample_size, random_state=42)
        print(f"\nSampling {sample_size} accounts for validation")

    # Validate each account
    print("\n" + "="*80)
    print("VALIDATION PROCESS")
    print("="*80)
    print("\nNOTE: This is a template script. WebFetch integration required for actual validation.")
    print("The script structure is ready - you'll need to integrate WebFetch tool calls.")
    print("="*80)

    results = []
    for idx, row in active_with_websites.iterrows():
        account = row['Account Name']
        website = row['Website']
        cluster = row['Industry_Cluster_Enhanced_V2']

        # Validate (placeholder for now)
        result = validate_account_website(account, website, cluster)
        results.append(result)

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Save results
    results_df.to_csv(output_file, index=False)
    print(f"\nSaved validation results to: {output_file}")
    print(f"Total accounts processed: {len(results_df)}")

    # Summary statistics (when WebFetch is integrated)
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Integrate WebFetch tool to retrieve website content")
    print("2. Run validate_account_website() with actual content")
    print("3. Calculate cluster scores using classify_website_content()")
    print("4. Generate confidence scores and conflict detection")
    print("5. Re-run this script with real data")

    return results_df


if __name__ == '__main__':
    # Example: Validate Building Materials cluster (for pilot testing)
    print("\nPILOT TEST MODE: Building Materials & Construction")
    print("This will validate the cluster known to have 100% accuracy")
    print("-"*80)

    results = validate_cluster_websites(
        cluster_name='Building Materials & Construction',
        output_file='website_validation_pilot_test.csv'
    )

    print("\nPilot test template created!")
    print("Integrate WebFetch tool and re-run for actual validation.")
