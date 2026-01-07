#!/usr/bin/env python3
"""
Product-Based Cluster Validation Script
Analyzes actual sold items to validate industry classifications.
Uses same approach as validate_general_wd_subclusters.py

Author: Evidence-Based Analysis
Date: January 7, 2026
"""

import pandas as pd
import re
from typing import Dict, List, Tuple

# Product keyword patterns for each cluster
# Based on what customers actually sell (not what they say they do)
CLUSTER_PRODUCT_KEYWORDS = {
    'Medical Equipment & Supplies': {
        'keywords': ['medical', 'surgical', 'hospital', 'patient', 'diagnostic', 'healthcare',
                    'dental', 'therapy', 'pharmaceutical', 'clinical', 'laboratory', 'exam',
                    'stretcher', 'wheelchair', 'iv', 'catheter', 'bandage', 'syringe'],
        'exclude': ['veterinary', 'vet', 'equine', 'animal', 'pet']  # Exclude vet products
    },
    'Food & Beverage Dist/Mfg': {
        'keywords': ['food', 'beverage', 'produce', 'meat', 'dairy', 'bakery', 'grocery',
                    'organic', 'fresh', 'frozen', 'canned', 'snack', 'drink', 'coffee', 'tea',
                    'bread', 'cheese', 'milk', 'juice', 'wine', 'beer', ' ale ', 'fruit', 'vegetable',
                    'tortilla', 'salsa', 'sauce', 'spice', 'ingredient'],
        'exclude': []
    },
    'Building Materials & Construction': {
        'keywords': ['lumber', 'wood', 'concrete', 'brick', 'stone', 'flooring', 'tile',
                    'roofing', 'siding', 'drywall', 'insulation', 'door', 'window', 'molding',
                    'trim', 'cabinet', 'countertop', 'shingle', 'gutter', 'decking',
                    'plywood', 'beam', 'joist', 'railing'],
        'exclude': []
    },
    'Industrial Equipment & Machinery': {
        'keywords': ['valve', 'pump', 'bearing', 'motor', 'machinery', 'equipment',
                    'industrial', 'hydraulic', 'pneumatic', 'compressor', 'gearbox',
                    'conveyor', 'actuator', 'sensor', 'controller', 'regulator'],
        'exclude': []
    },
    'Chemicals, Plastics & Rubber': {
        'keywords': ['chemical', 'plastic', 'rubber', 'polymer', 'resin', 'compound',
                    'coating', 'adhesive', 'sealant', 'lubricant', 'solvent', 'cleaner',
                    'acid', 'alkali', 'catalyst', 'additive'],
        'exclude': []
    },
    'Electronics & Technology': {
        'keywords': ['electronics', 'computer', 'laptop', 'monitor', 'keyboard', 'mouse',
                    'tablet', 'phone', 'router', 'switch', 'cable', 'circuit', 'chip',
                    'semiconductor', 'LED', 'display', 'battery', 'charger'],
        'exclude': []
    },
    'Furniture & Home Furnishings': {
        'keywords': ['furniture', 'chair', 'table', 'desk', 'sofa', 'couch', 'bed',
                    'dresser', 'bookshelf', 'cabinet', 'lamp', 'rug', 'curtain',
                    'cushion', 'mattress', 'frame', 'seat', 'bench'],
        'exclude': ['kitchen cabinet']  # Kitchen cabinets may belong in Building Materials
    },
    'Apparel & Textiles': {
        'keywords': ['clothing', 'apparel', 'shirt', 'pants', 'dress', 'jacket', 'coat',
                    'uniform', 'shoe', 'boot', 'hat', 'glove', 'fabric', 'textile',
                    'garment', 'fashion', 'footwear', 'accessories'],
        'exclude': ['metal', 'steel', 'fabrication', 'welding', 'machining']  # Exclude metal fab
    },
    'Automotive & Transportation': {
        'keywords': ['auto', 'automotive', 'car', 'truck', 'vehicle', 'tire', 'brake',
                    'engine', 'transmission', 'oil', 'filter', 'battery', 'spark plug',
                    'belt', 'hose', 'muffler', 'exhaust'],
        'exclude': []
    },
    'Metal Fabrication & Steel': {
        'keywords': ['metal', 'steel', 'aluminum', 'iron', 'stainless', 'fabrication',
                    'welding', 'machining', 'sheet metal', 'plate', 'tube', 'pipe',
                    'angle', 'channel', 'beam', 'bar', 'rod', 'wire', 'mesh'],
        'exclude': []
    },
    'Electrical & Lighting Equipment': {
        'keywords': ['electrical', 'lighting', 'light', 'lamp', 'fixture', 'LED',
                    'bulb', 'switch', 'outlet', 'panel', 'breaker', 'wire', 'conduit',
                    'transformer', 'ballast', 'dimmer'],
        'exclude': []
    },
    'Packaging & Printing': {
        'keywords': ['packaging', 'box', 'carton', 'container', 'bag', 'wrap', 'label',
                    'printing', 'print', 'ink', 'paper', 'envelope', 'tape', 'stretch wrap',
                    'shrink wrap', 'pallet wrap'],
        'exclude': []
    },
    'Office Supplies & Equipment': {
        'keywords': ['office', 'paper', 'pen', 'pencil', 'notebook', 'folder', 'binder',
                    'stapler', 'clip', 'toner', 'ink', 'printer', 'copier', 'desk',
                    'file', 'organizer'],
        'exclude': []
    },
    'Safety & Security Equipment': {
        'keywords': ['safety', 'PPE', 'glove', 'goggle', 'helmet', 'vest', 'harness',
                    'respirator', 'mask', 'ear plug', 'security', 'camera', 'alarm',
                    'lock', 'badge', 'access', 'fire extinguisher'],
        'exclude': []
    },
    'Sporting Goods & Fitness Equipment': {
        'keywords': ['sport', 'fitness', 'athletic', 'gym', 'exercise', 'weight',
                    'treadmill', 'bike', 'ball', 'golf', 'tennis', 'baseball', 'basketball',
                    'soccer', 'hockey', 'camping', 'outdoor'],
        'exclude': []
    },
    'Signs, Graphics & Displays': {
        'keywords': ['sign', 'banner', 'display', 'graphic', 'vinyl', 'decal',
                    'lettering', 'billboard', 'poster', 'flag', 'awning'],
        'exclude': []
    },
    'Agriculture & Greenhouse/Nursery': {
        'keywords': ['agriculture', 'farm', 'crop', 'seed', 'fertilizer', 'pesticide',
                    'greenhouse', 'nursery', 'plant', 'tree', 'flower', 'soil', 'mulch',
                    'irrigation', 'tractor', 'harvest', 'landscaping'],
        'exclude': []
    },
    'Wood Products & Lumber': {
        'keywords': ['wood', 'lumber', 'hardwood', 'plywood', 'timber', 'sawdust',
                    'veneer', 'millwork', 'woodworking', 'oak', 'maple', 'pine',
                    'cedar', 'mahogany'],
        'exclude': []
    },
    'HVAC & Refrigeration Equipment': {
        'keywords': ['HVAC', 'heating', 'cooling', 'air conditioning', 'refrigeration',
                    'furnace', 'boiler', 'chiller', 'compressor', 'evaporator', 'condenser',
                    'thermostat', 'ductwork', 'vent'],
        'exclude': []
    },
    'Manufacturer Representatives': {
        'keywords': ['commission', 'sales rep', 'agency fee', 'representative fee'],
        'exclude': []
    },
}


def classify_product_item(item_name: str, cluster_definitions: Dict) -> Dict[str, float]:
    """
    Classify a single product item against cluster definitions.
    Returns dict of cluster -> confidence score (0-1).
    """
    item_lower = item_name.lower()
    cluster_scores = {}

    for cluster, definition in cluster_definitions.items():
        keywords = definition['keywords']
        exclude_keywords = definition.get('exclude', [])

        # Check for exclusion keywords first
        exclude_match = False
        for exclude_kw in exclude_keywords:
            if exclude_kw in item_lower:
                exclude_match = True
                break

        if exclude_match:
            cluster_scores[cluster] = 0.0
            continue

        # Count keyword matches
        matches = 0
        for keyword in keywords:
            if keyword in item_lower:
                matches += 1

        # Confidence score: % of keywords matched (with minimum threshold)
        confidence = min(matches / max(len(keywords), 1), 1.0)
        cluster_scores[cluster] = confidence

    return cluster_scores


def classify_account_products(products: List[str]) -> Dict[str, any]:
    """
    Classify an account based on its product mix.
    Returns best matching cluster with confidence score.
    """
    if not products:
        return {
            'Classification': 'Unknown (No Products)',
            'Confidence': 0.0,
            'Item_Match_Count': 0,
            'Item_Match_Pct': 0.0,
            'Top_3_Clusters': []
        }

    # Classify each product
    cluster_item_counts = {cluster: 0 for cluster in CLUSTER_PRODUCT_KEYWORDS.keys()}

    for product in products:
        scores = classify_product_item(product, CLUSTER_PRODUCT_KEYWORDS)

        # Assign to cluster with highest score (if > 0)
        if scores:
            best_cluster = max(scores, key=scores.get)
            if scores[best_cluster] > 0:
                cluster_item_counts[best_cluster] += 1

    # Calculate percentages
    total_items = len(products)
    cluster_percentages = {
        cluster: (count / total_items * 100)
        for cluster, count in cluster_item_counts.items()
    }

    # Get top cluster
    best_cluster = max(cluster_percentages, key=cluster_percentages.get)
    best_percentage = cluster_percentages[best_cluster]

    # Get top 3 clusters
    top_3 = sorted(cluster_percentages.items(), key=lambda x: x[1], reverse=True)[:3]
    top_3_str = ', '.join([f"{c}: {p:.1f}%" for c, p in top_3 if p > 0])

    # Confidence based on percentage match
    # 40%+ = high confidence, 20-40% = medium, <20% = low
    confidence = best_percentage

    return {
        'Classification': best_cluster if best_percentage >= 20 else 'General Wholesale/Distribution',
        'Confidence': confidence,
        'Item_Match_Count': cluster_item_counts[best_cluster],
        'Item_Match_Pct': best_percentage,
        'Top_3_Clusters': top_3_str
    }


def validate_cluster_products(cluster_name: str = None,
                                sample_size: int = None,
                                output_file: str = 'product_validation_results.csv'):
    """
    Validate accounts via product data analysis.

    Args:
        cluster_name: If specified, only validate this cluster
        sample_size: If specified, limit to N accounts per cluster
        output_file: Output CSV filename
    """
    print("="*80)
    print("PRODUCT-BASED CLUSTER VALIDATION")
    print("="*80)

    # Load main dataset
    print("\nLoading datasets...")
    df = pd.read_csv('data/customermethodaccount_01-07-2026_RECLUSTERED_V2_WITH_PRODUCT_TYPES.csv')
    active = df[df['Active?'] == True].copy()

    # Load product data
    products_df = pd.read_csv('customer_product_offerings_with_type.csv')

    print(f"Total active accounts: {len(active)}")
    print(f"Product data available: {products_df['Account'].nunique()} accounts")

    # Filter by cluster if specified
    if cluster_name:
        active = active[active['Industry_Cluster_Enhanced_V2'] == cluster_name]
        print(f"\nFiltering to cluster: {cluster_name}")
        print(f"Accounts in cluster: {len(active)}")

    # Filter to accounts with product data
    accounts_with_products = active[
        active['Account Name'].isin(products_df['Account'].unique())
    ].copy()

    print(f"Accounts with product data: {len(accounts_with_products)} "
          f"({len(accounts_with_products)/len(active)*100:.1f}%)")

    # Sample if specified
    if sample_size and len(accounts_with_products) > sample_size:
        accounts_with_products = accounts_with_products.sample(n=sample_size, random_state=42)
        print(f"\nSampling {sample_size} accounts for validation")

    # Validate each account
    print("\n" + "="*80)
    print("VALIDATION PROCESS")
    print("="*80)

    results = []
    for idx, row in accounts_with_products.iterrows():
        account = row['Account Name']
        expected_cluster = row['Industry_Cluster_Enhanced_V2']
        sample_products = row.get('Sample_Products', '')

        # Get product list for this account
        account_products = products_df[products_df['Account'] == account]['Item'].tolist()

        if not account_products:
            continue

        # Classify based on products
        classification = classify_account_products(account_products)

        # Check if matches expected cluster
        matches_expected = (classification['Classification'] == expected_cluster)
        product_confidence = classification['Confidence']

        result = {
            'Account_Name': account,
            'Expected_Cluster': expected_cluster,
            'Product_Classification': classification['Classification'],
            'Product_Confidence': round(product_confidence, 1),
            'Items_Analyzed': len(account_products),
            'Items_Matching_Expected': classification['Item_Match_Count'] if matches_expected else 0,
            'Items_Matching_Pct': round(classification['Item_Match_Pct'], 1) if matches_expected else 0,
            'Matches_Expected': matches_expected,
            'Top_3_Clusters': classification['Top_3_Clusters'],
            'Sample_Products': sample_products[:200] if pd.notna(sample_products) else '',  # First 200 chars
            'Notes': ''
        }

        # Add notes for conflicts
        if not matches_expected and product_confidence >= 40:
            result['Notes'] = f"HIGH CONFIDENCE CONFLICT: Products suggest {classification['Classification']} " \
                              f"({product_confidence:.1f}%) but classified as {expected_cluster}"
        elif not matches_expected and product_confidence >= 20:
            result['Notes'] = f"POSSIBLE CONFLICT: Products suggest {classification['Classification']} " \
                              f"({product_confidence:.1f}%)"
        elif not matches_expected:
            result['Notes'] = f"General/Mixed: No strong cluster match ({product_confidence:.1f}%)"

        results.append(result)

        if (idx + 1) % 50 == 0:
            print(f"Processed {idx + 1} accounts...")

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Save results
    results_df.to_csv(output_file, index=False)
    print(f"\nSaved validation results to: {output_file}")

    # Summary statistics
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)

    total_validated = len(results_df)
    matches = results_df['Matches_Expected'].sum()
    accuracy = matches / total_validated * 100 if total_validated > 0 else 0

    print(f"\nTotal accounts validated: {total_validated}")
    print(f"Matches expected cluster: {matches} ({accuracy:.1f}%)")
    print(f"Conflicts detected: {total_validated - matches} ({100-accuracy:.1f}%)")

    # High confidence conflicts
    high_conf_conflicts = results_df[
        (~results_df['Matches_Expected']) &
        (results_df['Product_Confidence'] >= 40)
    ]

    if len(high_conf_conflicts) > 0:
        print(f"\nHIGH CONFIDENCE CONFLICTS: {len(high_conf_conflicts)}")
        print("-"*80)
        for _, row in high_conf_conflicts.iterrows():
            print(f"  {row['Account_Name']}")
            print(f"    Expected: {row['Expected_Cluster']}")
            print(f"    Products suggest: {row['Product_Classification']} ({row['Product_Confidence']:.1f}%)")
            print()

    return results_df


if __name__ == '__main__':
    # Example: Validate Building Materials cluster (for pilot testing)
    print("\nPILOT TEST MODE: Building Materials & Construction")
    print("This will validate the cluster known to have 100% accuracy")
    print("-"*80)

    results = validate_cluster_products(
        cluster_name='Building Materials & Construction',
        output_file='product_validation_pilot_test.csv'
    )

    print("\n" + "="*80)
    print("Pilot test complete! Review results in product_validation_pilot_test.csv")
    print("="*80)
