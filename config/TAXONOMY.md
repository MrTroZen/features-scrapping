# Qavyo Restaurant Intelligence — Taxonomy

## Purpose

This file defines the controlled knowledge taxonomy.

Agents must use these categories when organising structured research.

Do not create new top-level categories during ordinary transcript processing.

If a concept does not fit cleanly, use the closest valid category and flag the taxonomy issue for later review.

---

# 1. FINANCE

Folder:

knowledge/finance/

Subcategories:

- revenue
- profitability
- gross-profit
- contribution-margin
- net-profit
- break-even
- prime-cost
- cash-flow
- fixed-costs
- variable-costs
- unit-economics
- financial-controls
- financial-reporting

---

# 2. FOOD COST

Folder:

knowledge/food-cost/

Subcategories:

- food-cost-percentage
- theoretical-food-cost
- actual-food-cost
- recipe-costing
- ingredient-cost
- portion-cost
- food-cost-variance
- cost-trends
- cost-control

---

# 3. LABOUR

Folder:

knowledge/labour/

Subcategories:

- labour-cost
- labour-cost-percentage
- scheduling
- overtime
- staffing-levels
- productivity
- sales-per-labour-hour
- attendance
- shift-management
- demand-vs-staffing

---

# 4. INVENTORY

Folder:

knowledge/inventory/

Subcategories:

- stock-levels
- stock-counting
- inventory-valuation
- theoretical-usage
- actual-usage
- inventory-variance
- waste
- spoilage
- shrinkage
- receiving
- transfers
- stock-turnover
- replenishment

---

# 5. MENU ENGINEERING

Folder:

knowledge/menu-engineering/

Subcategories:

- item-profitability
- item-popularity
- contribution-margin
- sales-mix
- pricing
- recipe-cost
- menu-design
- category-performance
- menu-optimisation
- upselling

---

# 6. OPERATIONS

Folder:

knowledge/operations/

Subcategories:

- daily-operations
- opening
- closing
- management-process
- standard-operating-procedures
- operational-controls
- capacity
- bottlenecks
- service-flow
- operational-review

---

# 7. KITCHEN

Folder:

knowledge/kitchen/

Subcategories:

- ticket-time
- preparation-time
- kitchen-throughput
- kitchen-capacity
- production-planning
- prep-planning
- station-performance
- order-delays
- portion-control
- kitchen-waste

---

# 8. PURCHASING

Use:

knowledge/inventory/

with subcategory metadata:

- purchasing
- supplier-pricing
- supplier-comparison
- purchase-orders
- order-quantity
- purchase-variance
- purchasing-controls
- receiving-costs

Do NOT create a new top-level purchasing folder unless the taxonomy is deliberately revised later.

---

# 9. CUSTOMERS

Folder:

knowledge/customers/

Subcategories:

- retention
- repeat-rate
- visit-frequency
- customer-value
- lifetime-value
- segmentation
- ordering-behaviour
- loyalty
- churn
- customer-frequency

---

# 10. ORDERS / CHANNELS

Use:

knowledge/operations/

or:

knowledge/delivery/

depending on the primary topic.

Relevant subcategories:

- dine-in
- takeaway
- online-ordering
- qr-ordering
- kiosk
- channel-mix
- average-order-value
- order-volume
- fulfilment
- channel-profitability

---

# 11. DELIVERY

Folder:

knowledge/delivery/

Subcategories:

- delivery-economics
- commissions
- third-party-delivery
- direct-delivery
- delivery-profitability
- delivery-fees
- delivery-order-value
- channel-comparison

---

# 12. PAYMENTS

Folder:

knowledge/payments/

Subcategories:

- transaction-fees
- payment-methods
- refunds
- settlements
- tips
- payment-costs
- net-revenue-impact

---

# 13. FORECASTING

Folder:

knowledge/forecasting/

Subcategories:

- sales-forecasting
- demand-forecasting
- cover-forecasting
- labour-forecasting
- inventory-forecasting
- purchasing-forecasting
- seasonality
- trend-analysis

---

# 14. RESERVATIONS

Use:

knowledge/operations/

with relevant metadata.

Subcategories:

- reservations
- no-shows
- cancellations
- walk-ins
- waitlist
- covers
- occupancy
- table-utilisation
- table-turnover

---

# 15. MARKETING

Marketing is not currently a dedicated top-level knowledge folder.

If operationally valuable marketing research appears, store it under:

knowledge/customers/

or:

knowledge/operations/

depending on context.

Examples:

- retention
- customer-frequency
- promotion-profitability
- discount-economics
- customer-acquisition-economics

Generic marketing content should usually be ignored.

---

# 16. OTHER

Folder:

knowledge/other/

Use ONLY when:

- the information is genuinely valuable
- no existing taxonomy category fits
- forcing it into an existing category would be misleading

Use of "other" should be rare.

Repeated use of "other" may indicate the taxonomy needs deliberate revision.

---

# KNOWLEDGE TYPE

Every structured knowledge entry should also identify a Knowledge Type.

Allowed values:

- formula
- metric
- kpi
- benchmark
- operational-rule
- management-method
- workflow
- calculation
- cause-effect
- problem
- recommendation
- concept
- control
- forecasting-method
- comparison

Multiple types may apply when justified.

---

# EVIDENCE TYPE

Allowed evidence classifications:

- verified-fact
- source-claim
- benchmark
- illustrative-example
- opinion
- recommendation
- estimate
- calculation
- multi-source-consensus
- disputed

Do not classify something as verified-fact unless appropriate evidence supports it.

---

# GEOGRAPHIC APPLICABILITY

Allowed values:

- global-principle
- uk
- us
- europe
- country-specific
- geography-sensitive
- unknown

A piece of knowledge may use more than one when appropriate.

---

# RESTAURANT APPLICABILITY

When known, identify applicability such as:

- all-restaurants
- independent
- multi-location
- quick-service
- fast-casual
- full-service
- fine-dining
- cafe
- takeaway
- delivery-heavy
- bar
- other
- unknown

Do not assume applicability if the source does not establish it.

---

# QAVYO PRODUCT AREA TAGS

Knowledge may be tagged with relevant Qavyo product areas.

Allowed values:

- pos
- orders
- tables
- website
- online-ordering
- qr-ordering
- kiosk
- kitchen
- inventory
- menu
- payments
- staff
- scheduling
- reservations
- customers
- marketing
- analytics
- ai-intelligence
- hardware

Multiple product areas may apply.

Do not create new tags casually.

---

# CATEGORY DECISION RULE

Choose the category based on the primary operational concept.

Example:

If a source discusses:

"ingredient price increases reducing burger profitability"

Primary concept may be:

menu-engineering / item-profitability

Related tags may include:

- food-cost
- inventory
- menu
- finance

Do not duplicate the same knowledge into four folders merely because four product areas are involved.

Store one canonical knowledge entry and use metadata/cross-links.

---

# TAXONOMY GOVERNANCE

Ordinary research processing must NOT:

- create new top-level categories
- rename categories
- merge categories
- restructure folders
- create near-duplicate categories

If repeated useful knowledge does not fit this taxonomy, record a taxonomy-review recommendation rather than changing the structure automatically.
