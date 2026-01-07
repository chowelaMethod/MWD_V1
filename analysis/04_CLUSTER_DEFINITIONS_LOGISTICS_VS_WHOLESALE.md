# Cluster Definitions: Logistics & Fulfillment vs. General Wholesale/Distribution

**Purpose**: This document clarifies the distinction between two clusters currently lumped together in "General Wholesale/Distribution" (421 accounts).

---

## Summary Comparison

| Attribute | Logistics & Fulfillment Services | True General Wholesale/Distribution |
|-----------|----------------------------------|-------------------------------------|
| **Account Count** | 184 (43.7% of current cluster) | 146 (34.7% of current cluster) |
| **MRR** | $24,400 (48% of total MRR) | $15,600 (31% of total MRR) |
| **% of Cluster Revenue** | **70.3%** | 30.9% |
| **Business Model** | SERVICE-BASED (shipping, warehousing, fulfillment) | PRODUCT-BASED (buying & reselling physical goods) |
| **Revenue Source** | Fees for logistics services | Markup on product sales |
| **Core Activity** | Move goods for others | Own & sell inventory |
| **Inventory Ownership** | Customer-owned goods (in transit/storage) | Own inventory for resale |
| **Customer Type** | B2B (manufacturers, retailers, e-commerce) | B2B (retailers, contractors, end-users) |

---

## 1. Logistics & Fulfillment Services (184 accounts, $24.4K MRR)

### Definition

**Business Model**: Service companies that move, store, or fulfill goods on behalf of other businesses. They do NOT own the products they handle.

**Revenue Model**: Charge fees for services rendered (per shipment, per pallet stored, per order fulfilled, etc.)

**Core Services**:
- Shipping & courier services
- Freight forwarding
- Warehousing & storage
- Order fulfillment (pick, pack, ship)
- Last-mile delivery
- Cross-docking
- Industrial laundry services (textiles)

### Keywords (for clustering)

logistics, shipping, courier, freight, transport, delivery, warehouse, distribution services, fulfillment, laundry, storage, express, cross dock, forwarding, carrier, trucking, moving

### Example Companies (from Agent analysis)

**Type 1: Shipping & Courier**
- Express delivery services
- Regional freight carriers
- Package delivery companies

**Type 2: Warehousing & Fulfillment**
- 3PL (third-party logistics) providers
- E-commerce fulfillment centers
- Public warehousing companies

**Type 3: Specialized Logistics**
- Cold chain logistics (temperature-controlled)
- Industrial laundry services
- Cross-docking facilities

### Business Characteristics

**Inventory**: Customer-owned goods in transit or temporary storage
- They don't buy/resell products
- They move/store products for clients

**Revenue Streams**:
- Per-shipment fees
- Storage fees (per pallet, per sq ft)
- Fulfillment fees (per order processed)
- Subscription/retainer fees

**Customer Relationship**: Ongoing service contracts
- Monthly/annual agreements
- Volume-based pricing
- Long-term partnerships

### Why This Matters for Product Strategy

**Different Needs Than Wholesalers**:
1. **No traditional inventory management** - track customer-owned goods, not owned inventory
2. **Service billing** - charge for services rendered, not product markup
3. **Route optimization** - for delivery/transportation companies
4. **Warehouse space management** - track utilization, not stock levels
5. **SLA tracking** - on-time delivery, order accuracy metrics
6. **Multi-client management** - segregate goods by customer

**CRM Features Needed**:
- Service ticket tracking
- Route management
- Warehouse space allocation
- SLA/performance metrics
- Client-specific billing rates
- Proof of delivery tracking

---

## 2. True General Wholesale/Distribution (146 accounts, $15.6K MRR)

### Definition

**Business Model**: Companies that BUY products from manufacturers and RESELL them to retailers, contractors, or end-users. They OWN the inventory they distribute.

**Revenue Model**: Buy low, sell high - profit from markup on products sold

**Core Activities**:
- Purchase inventory from manufacturers
- Store inventory in own warehouses
- Sell to retailers, contractors, businesses
- Provide credit terms to customers
- Offer product expertise & recommendations

### Keywords (for clustering)

wholesale, merchant wholesale, distributor, trading company, import/export, general merchandise, multi-line distributor (EXCLUDING specific product keywords like "lumber", "medical", "food", etc.)

### Example Companies (from Agent analysis)

**Type 1: Multi-Line Distributors**
- Sell variety of unrelated products
- No dominant product category
- Serve multiple industries

**Type 2: General Merchandise Wholesalers**
- Wide assortment of consumer/business goods
- No specialized vertical focus
- Opportunistic buying & selling

**Type 3: Trading Companies**
- Import/export businesses
- Buy from overseas, sell domestically (or vice versa)
- Multi-product, multi-industry

### Business Characteristics

**Inventory**: OWN the products they sell
- Purchase inventory with capital
- Take on inventory risk
- Manage stock levels, SKUs, reorder points

**Revenue Streams**:
- Product sales (markup over cost)
- Volume discounts (buy bulk, sell smaller quantities)
- Sometimes: freight/delivery fees as add-on

**Customer Relationship**: Transactional with credit terms
- Purchase orders
- Net 30/60/90 payment terms
- Volume-based pricing tiers

### Why This Matters for Product Strategy

**Traditional Wholesale Needs**:
1. **Inventory management** - track owned stock, reorder points, cost/sell price
2. **Purchase orders** - buying from suppliers
3. **Sales orders** - selling to customers
4. **Pricing & quoting** - cost + markup calculations
5. **Credit management** - customer payment terms, AR tracking
6. **Product catalog** - manage SKUs, descriptions, pricing

**CRM Features Needed**:
- Inventory tracking (owned stock)
- Purchase order management
- Sales order processing
- Pricing/quoting tools
- Customer credit limits
- Vendor management

---

## Side-by-Side Example

### Logistics & Fulfillment Company

**Company**: ABC Fulfillment Services
**Business**: E-commerce order fulfillment for online retailers

**How it works**:
1. Online retailer ships inventory to ABC's warehouse
2. ABC stores products (charges monthly storage fee)
3. Customer orders from retailer's website
4. ABC picks, packs, ships order (charges per-order fee)
5. ABC sends invoice to retailer for services rendered

**Revenue**: $5,000/month in fulfillment fees (storage + pick/pack/ship)

**Inventory**: $0 (all goods are client-owned)

**CRM Needs**:
- Track which products belong to which client
- Calculate billing based on orders fulfilled
- Manage warehouse space utilization
- Track SLA metrics (order accuracy, ship time)

---

### General Wholesale/Distribution Company

**Company**: XYZ General Distributors
**Business**: Buy industrial supplies, resell to contractors & small businesses

**How it works**:
1. XYZ buys $50K worth of products from various manufacturers
2. Stores inventory in own warehouse
3. Contractors/businesses order products
4. XYZ sells products at 30% markup
5. Offers Net 30 payment terms

**Revenue**: $5,000/month in gross profit (20-30% margin on $20K sales)

**Inventory**: $50K owned stock (XYZ's capital at risk)

**CRM Needs**:
- Track inventory levels, costs, sell prices
- Purchase orders to suppliers
- Sales orders to customers
- Calculate profit margins
- Manage customer credit/payments
- Reorder alerts for low stock

---

## Why They're Currently Lumped Together

### Common Keyword: "Distribution"

**Problem**: Both business models use the word "distribution" in their industry descriptions:
- **Logistics**: "distribution services" (moving goods for others)
- **Wholesale**: "product distribution" (owning & reselling goods)

**Current Clustering Logic**:
```python
if 'wholesale' in vertical or any(x in combined for x in ['wholesale', 'distribution',
                                                            'merchant wholesale', 'distributor']):
    return 'General Wholesale/Distribution'
```

This catches BOTH types because they both contain "distribution" somewhere in their Sector/QBO fields.

---

## How to Separate Them (V3 Clustering)

### Step 1: Prioritize Logistics Keywords (Higher Precedence)

```python
# NEW: Extract Logistics & Fulfillment FIRST (before generic wholesale)
logistics_keywords = ['logistics', 'shipping', 'courier', 'freight', 'transport',
                      'delivery', 'warehouse', 'fulfillment', 'laundry', 'storage',
                      'express', 'cross dock', 'forwarding', 'carrier', 'trucking']

if any(x in combined for x in logistics_keywords):
    return 'Logistics & Fulfillment Services'

# THEN catch remaining wholesale (product distributors)
if 'wholesale' in vertical or any(x in combined for x in ['wholesale', 'distribution',
                                                            'merchant wholesale', 'distributor']):
    return 'General Wholesale/Distribution'
```

### Step 2: Validate with Sample Data

**Expected Result**:
- **Logistics & Fulfillment**: 184 accounts, $24.4K MRR (70% of current cluster revenue)
- **General Wholesale/Distribution**: 146 accounts, $15.6K MRR (30% of current cluster revenue)

**Validation Method**:
- Check top 10 accounts in each new cluster
- Verify business models via website
- Confirm revenue split is accurate

---

## Impact on Product Strategy

### Logistics & Fulfillment Services (184 accounts, $24.4K MRR)

**Strategic Importance**: 70% of General W/D cluster revenue!

**Product Features Needed** (Different from traditional wholesale):
1. **Service-based billing** (not product markup)
   - Bill for storage, fulfillment, shipping services
   - Time & materials pricing
   - Subscription/retainer models

2. **Client inventory segregation**
   - Track which goods belong to which client
   - Multi-client warehouse management
   - Client-specific reporting

3. **SLA & performance tracking**
   - On-time delivery metrics
   - Order accuracy rates
   - Customer satisfaction scores

4. **Route optimization** (for delivery/courier companies)
   - Delivery route planning
   - Driver scheduling
   - Fleet management

**Recommendation**: If inventory management MVP is being built, consider a **separate module for logistics/fulfillment** with different data model:
- Inventory = customer-owned (not owned stock)
- Transactions = services rendered (not product sales)
- Billing = fee-based (not cost + markup)

---

### General Wholesale/Distribution (146 accounts, $15.6K MRR)

**Strategic Importance**: 30% of cluster revenue, but more traditional wholesale model

**Product Features Needed** (Traditional wholesale):
1. **Inventory management** (owned stock)
   - Track cost, sell price, margin
   - Reorder points, safety stock
   - SKU management

2. **Purchase order management**
   - Buying from suppliers
   - Receiving goods
   - Vendor management

3. **Sales order processing**
   - Quoting & pricing
   - Order fulfillment
   - Invoicing

4. **Credit management**
   - Customer payment terms
   - AR tracking
   - Credit limits

**Recommendation**: Standard inventory management MVP applies to this cluster - traditional wholesale/distribution functionality.

---

## Recommended Next Steps

### 1. V3 Re-Clustering (Technical)
- Add Logistics keywords BEFORE wholesale keywords in clustering logic
- Extract 184 accounts to new "Logistics & Fulfillment Services" cluster
- Remaining 146 accounts stay in "General Wholesale/Distribution"

### 2. Customer Interviews (Validation)
- Interview 5-7 Logistics companies to understand their needs
- Interview 5-7 General Wholesale companies for comparison
- Validate that their product requirements are different

### 3. Inventory MVP Scoping (Product)
- **Question**: Does inventory MVP support service-based billing for logistics companies?
- **Question**: Or is it traditional wholesale (owned inventory, cost + markup)?
- **Recommendation**: Start with traditional wholesale (146 accounts), add logistics module later (184 accounts) if validated

### 4. Feature Prioritization (Strategic)
- **Option A**: Build for General Wholesale first (traditional, well-understood)
- **Option B**: Build for Logistics & Fulfillment (larger revenue opportunity, more complex)
- **Option C**: Build horizontal features that work for both (safest, but less differentiated)

---

## Summary Table

| Metric | Logistics & Fulfillment | General Wholesale/Distribution |
|--------|------------------------|-------------------------------|
| **Accounts** | 184 | 146 |
| **% of Current Cluster** | 43.7% | 34.7% |
| **MRR** | $24,400 | $15,600 |
| **% of Cluster Revenue** | **70.3%** (MAJORITY) | 30.9% |
| **Avg MRR** | $133 | $107 |
| **Business Model** | Service-based (fees) | Product-based (markup) |
| **Inventory** | Customer-owned | Own stock |
| **Complexity** | HIGH (multi-client, SLA) | MEDIUM (traditional wholesale) |
| **Strategic Priority** | **HIGH** (70% revenue) | MEDIUM (30% revenue) |

**Key Takeaway**: Logistics & Fulfillment represents 70% of the current General Wholesale/Distribution revenue despite being only 44% of the account count. This is the **higher-value segment** but also has **different product requirements** than traditional wholesale.

---

**Document Status**: ✅ Complete
**Version**: 1.0
**Date**: January 7, 2026
**Next Action**: V3 re-clustering to separate these two distinct business models
