# Qavyo Restaurant Intelligence — Knowledge Schema

## 1. Purpose

This file defines the required structure for reusable restaurant knowledge entries.

The goal is to ensure that knowledge collected from hundreds or thousands of sources remains:

- consistent
- traceable
- searchable
- machine-readable
- understandable by humans
- useful for future AI analysis
- useful for Qavyo product research
- resistant to source distortion

Every knowledge entry should describe a reusable restaurant operational concept.

A knowledge entry is NOT simply a transcript summary.

---

# 2. Core Principle

The system should transform:

SOURCE CONTENT

into:

STRUCTURED RESTAURANT KNOWLEDGE

while preserving:

- meaning
- evidence
- context
- numbers
- assumptions
- uncertainty
- provenance

The structured entry should make sense even when read independently from the original transcript.

However, it must remain traceable back to the original source.

---

# 3. Canonical Knowledge Entry

Each reusable concept should normally have one canonical knowledge file.

Example:

knowledge/finance/contribution-margin.md

Additional sources discussing contribution margin should generally strengthen, challenge or expand the existing canonical entry rather than automatically creating duplicate files.

Do NOT create:

contribution-margin-owner-com.md

contribution-margin-video-2.md

contribution-margin-new.md

contribution-margin-explained.md

when all of them describe substantially the same operational concept.

---

# 4. File Naming

Use lowercase kebab-case.

Examples:

contribution-margin.md

labour-cost-percentage.md

inventory-variance.md

theoretical-food-cost.md

sales-per-labour-hour.md

supplier-price-variance.md

Files should be named after the knowledge concept, not the creator or source.

---

# 5. Required Front Matter

Every structured knowledge file must begin with YAML front matter.

Use this structure:

---
title:
slug:
category:
subcategory:
knowledge_types: []
evidence_types: []
geographic_applicability: []
restaurant_applicability: []
qavyo_product_areas: []
source_ids: []
confidence:
status:
last_updated:
---

Do not invent additional metadata fields casually.

If a new metadata field appears repeatedly necessary, recommend a schema review rather than modifying the schema during ordinary processing.

---

# 6. Front Matter Rules

## title

Human-readable concept name.

Example:

Contribution Margin

---

## slug

Lowercase kebab-case canonical identifier.

Example:

contribution-margin

Normally matches the filename.

---

## category

Must use a valid top-level category from:

config/TAXONOMY.md

Example:

finance

---

## subcategory

Must use a valid relevant subcategory from:

config/TAXONOMY.md

Example:

contribution-margin

---

## knowledge_types

Use one or more allowed knowledge types from TAXONOMY.md.

Examples:

- formula
- metric
- kpi
- operational-rule
- cause-effect

Only include types that genuinely apply.

---

## evidence_types

Use valid evidence types from TAXONOMY.md.

Examples:

- source-claim
- calculation
- benchmark
- illustrative-example
- multi-source-consensus

More than one may apply.

---

## geographic_applicability

Use controlled values defined in TAXONOMY.md.

Examples:

- global-principle
- uk
- us
- geography-sensitive

Do not assume global applicability.

---

## restaurant_applicability

Use controlled applicability values.

Examples:

- all-restaurants
- full-service
- quick-service
- delivery-heavy

Use:

unknown

when the source does not establish applicability.

---

## qavyo_product_areas

Use only approved Qavyo product-area tags from TAXONOMY.md.

Example:

- pos
- inventory
- menu
- analytics
- ai-intelligence

These indicate relevant Qavyo areas.

They do NOT mean Qavyo already implements the capability.

---

## source_ids

List every source record that materially supports this knowledge entry.

Example:

- SRC-ownercom-menu-profitability-001
- SRC-restaurant365-menu-engineering-004

Source IDs must point to real source records.

Never invent provenance.

---

## confidence

Allowed values:

- low
- medium
- high

Confidence refers to confidence in the structured knowledge entry as written.

It is influenced by:

- source quality
- evidence quality
- clarity
- consistency
- number of supporting sources
- conflicting evidence
- context

Do not automatically assign high confidence because a creator sounds confident.

---

## status

Allowed values:

- draft
- reviewed
- established
- disputed
- needs-verification

During automatic ingestion, new entries should normally begin as:

draft

unless a workflow explicitly defines otherwise.

---

## last_updated

Use ISO date format:

YYYY-MM-DD

This records when the structured knowledge file was materially updated.

---

# 7. Required Body Structure

Every knowledge entry should use the following structure where applicable.

Not every section must contain large amounts of content.

Do not fill sections with invented material merely to make the document look complete.

Required structure:

# [Knowledge Title]

## Definition

## Why It Matters

## Core Logic

## Formula

## Variables

## Worked Example

## Interpretation

## Operational Use

## Required Data

## Relationships

## Qavyo Relevance

## Conditions and Limitations

## Evidence

## Conflicting Evidence

## Related Knowledge

## Verification Notes

---

# 8. Definition

Provide a concise explanation of the operational concept.

The definition should describe what the concept means.

Do not include unnecessary source commentary.

Example:

Contribution margin measures how much revenue remains from a sale after subtracting costs that vary directly with that sale.

Do not state uncertain claims as universal definitions.

---

# 9. Why It Matters

Explain why a restaurant operator may care about the concept.

Focus on practical operational value.

Examples:

- profitability
- cost control
- staffing
- purchasing
- pricing
- waste
- forecasting
- operational decision-making

Avoid generic statements such as:

"This metric is very important for restaurants."

Explain why.

---

# 10. Core Logic

Explain the operational relationship behind the concept.

Example:

Selling more of a high-revenue item does not necessarily improve profitability if its variable costs are also high.

This section is useful when the knowledge is more than a simple formula.

---

# 11. Formula

When a formula exists, preserve it clearly.

Example:

Contribution Margin =
Selling Price
− Variable Costs

Contribution Margin % =
Contribution Margin
÷ Selling Price
× 100

Never create a formula merely because a topic sounds measurable.

If no established formula exists, write:

Not applicable.

---

# 12. Variables

Where calculations exist, explain each variable.

Preferred format:

| Variable | Meaning | Example Data Source |
|---|---|---|
| Selling Price | Amount charged to the customer | POS / Menu |
| Ingredient Cost | Cost of ingredients used | Inventory / Recipe |
| Packaging Cost | Variable packaging cost | Inventory / Purchasing |

Do not claim Qavyo currently provides a data source unless PRODUCT-CONTEXT supports that claim.

The "Example Data Source" column describes where the data could logically originate.

---

# 13. Worked Example

Use a worked example only when:

- the source provides one
- multiple sources establish the calculation clearly
- or the agent creates an explicitly labelled illustrative example

Source examples must preserve the source numbers.

If an example is created by the agent, clearly label it:

Illustrative example created to demonstrate the formula.

Never present an invented example as source evidence.

Example:

Selling price: £15.00
Variable cost: £6.00

Contribution margin:

£15.00 − £6.00 = £9.00

Contribution margin percentage:

£9.00 ÷ £15.00 × 100 = 60%

---

# 14. Interpretation

Explain how to read the result.

Example:

A £9 contribution margin means each sale contributes £9 toward covering fixed costs and eventual profit after the specified variable costs.

Be careful with language.

Do not imply that contribution margin equals net profit.

---

# 15. Operational Use

Describe how the concept may actually be used.

Examples:

- compare menu items
- monitor trends
- detect cost changes
- investigate variance
- make scheduling decisions
- compare locations
- review supplier pricing

Focus on decisions and actions rather than theoretical explanation.

---

# 16. Required Data

List the information required to calculate or apply the concept.

Example:

- menu selling price
- ingredient quantities
- ingredient unit costs
- packaging costs
- relevant transaction costs

Separate:

required data

from:

helpful additional data.

If useful, structure as:

### Required

### Optional / Enhancing

---

# 17. Relationships

Record meaningful connections to other restaurant concepts.

Example:

Contribution margin relates to:

- food cost
- recipe costing
- menu pricing
- sales mix
- channel fees
- menu engineering

Where meaningful, explain the relationship.

Do not create connections merely to increase cross-linking.

---

# 18. Qavyo Relevance

This section explains how the knowledge relates to Qavyo.

It should NOT automatically propose a feature.

Use the following structure:

### Relevant Product Areas

List applicable Qavyo areas.

### Potential Data Connections

Example:

POS sales
+
menu prices
+
recipe cost
+
inventory costs

### Possible Intelligence Use

Describe only plausible uses supported by the knowledge.

Examples:

- automated calculation
- trend monitoring
- anomaly detection
- comparison
- recommendation support

### Feature Status

Choose one:

- no-direct-feature-identified
- supports-existing-area
- existing-capability-improvement-opportunity
- potential-feature-opportunity
- requires-further-research

Do not create a feature proposal inside this section.

Formal feature proposals belong under:

feature-opportunities/

---

# 19. Conditions and Limitations

This is a high-priority section.

Record anything that limits interpretation.

Examples:

- restaurant type
- geography
- time period
- accounting method
- included/excluded costs
- tax treatment
- delivery commissions
- discounts
- service model
- data accuracy

Example:

A contribution-margin calculation can vary depending on which variable costs are included.

This context must not be discarded.

---

# 20. Evidence

For each materially important source, summarize what it actually supports.

Preferred format:

### SRC-example-001

Supports:

- definition of contribution margin
- calculation method
- worked example

Evidence type:

source-claim / calculation

Source context:

US restaurant educational video.

Do not copy unnecessarily large portions of transcripts.

Use concise evidence summaries.

---

# 21. Conflicting Evidence

If sources disagree, preserve the disagreement.

Example:

Source A recommends treating payment-processing fees as part of item-level variable cost.

Source B discusses contribution margin without including payment-processing fees.

Do not silently merge incompatible definitions.

When no conflict is currently known, write:

No material conflicting evidence currently recorded.

---

# 22. Related Knowledge

Link only to actual existing knowledge files.

Preferred format:

- [Food Cost Percentage](../food-cost/food-cost-percentage.md)
- [Recipe Costing](../food-cost/recipe-costing.md)
- [Menu Item Profitability](../menu-engineering/item-profitability.md)

Never create links to files that do not exist.

If related files have not yet been created, leave the section empty or note:

Related entries not yet created.

---

# 23. Verification Notes

Use this section for research-quality notes.

Examples:

- benchmark needs UK validation
- source uses US labour economics
- calculation appears consistent across three sources
- definition varies depending on accounting convention
- source provides no supporting data
- additional primary source needed

This is not a general notes section.

Use it specifically for knowledge quality and validation.

---

# 24. Source Claims vs Synthesized Knowledge

A knowledge file may combine multiple sources.

When doing so, distinguish between:

## Direct Source Claim

A claim explicitly made by a source.

## Derived Calculation

A result calculated directly from supplied source data.

## Synthesis

A conclusion supported by multiple sources.

## Agent Interpretation

An interpretation added by the research system.

Agent interpretation must never be disguised as source evidence.

---

# 25. Benchmark Handling

When storing benchmarks, always preserve relevant context.

A benchmark should include:

- metric
- value or range
- unit
- source
- publication date when available
- geography
- restaurant type
- business model where known
- sample context where known

Example:

Weak:

Good food cost is 30%.

Better:

Source X states that food cost of approximately X–Y% is commonly discussed for [restaurant context], based on [source context].

Benchmark applicability must remain explicit.

---

# 26. Calculation Handling

For calculations, preserve:

- formula
- inputs
- units
- output
- assumptions
- rounding
- exclusions

If the source's calculation appears mathematically incorrect:

1. preserve the source claim
2. flag the discrepancy
3. do not silently correct the source and present the corrected number as though the source said it

---

# 27. Cause-and-Effect Knowledge

For causal or operational relationships, structure clearly.

Example:

Observed condition:

Ingredient purchase price increases.

Direct effect:

Recipe cost increases.

Possible downstream effect:

Contribution margin decreases if menu price and other variables remain unchanged.

Important:

Do not convert correlation into causation without evidence.

Use language such as:

- may contribute to
- can result in
- is associated with
- possible cause

when causality is not established.

---

# 28. Operational Rules

Rules should be written in a structured form when possible.

Example:

Condition:

Actual ingredient usage materially exceeds theoretical usage.

Investigate:

- waste
- portion control
- recipe configuration
- stock counting
- receiving discrepancies
- unrecorded consumption
- shrinkage

Do not state that one cause definitely exists merely because a variance exists.

Operational rules often define what should be investigated rather than automatically declaring a diagnosis.

---

# 29. Knowledge Updating

When new evidence arrives:

Do not automatically create another knowledge file.

First determine whether the new source:

- confirms existing knowledge
- adds important context
- adds another example
- introduces a new formula
- changes applicability
- conflicts with existing knowledge
- provides stronger evidence
- actually describes a different concept

Then update appropriately.

---

# 30. Duplicate Detection

Before creating a new entry:

1. search filenames
2. search titles
3. search slugs
4. search concept wording
5. review related categories

If an existing canonical entry covers the concept, update it instead.

Examples of likely duplicates:

food-cost-percent.md
food-cost-percentage.md

employee-labour-cost.md
labour-cost.md

menu-profit.md
menu-item-profitability.md

Use the established canonical concept.

---

# 31. Splitting Knowledge

Split one source into multiple entries when the concepts can be independently reused.

Example source discusses:

- food cost percentage
- labour percentage
- prime cost
- break-even

These may warrant separate canonical entries.

Do not create one document called:

restaurant-finance-video-notes.md

---

# 32. Combining Knowledge

Do not unnecessarily split concepts that are inherently part of one calculation.

Example:

Contribution margin formula
+
contribution margin interpretation

should normally remain in one canonical knowledge entry.

---

# 33. Knowledge Quality Levels

Use confidence and status together.

Example:

New creator claim:

confidence: low
status: needs-verification

Clear calculation confirmed by multiple independent sources:

confidence: high
status: established

Do not promote entries automatically based purely on source count.

Source independence and quality matter.

---

# 34. No Empty Boilerplate

The schema is meant to improve consistency, not generate useless text.

Do not write meaningless filler such as:

## Relationships

There may be relationships to other areas.

If there is no meaningful content, use:

None identified yet.

or:

Not applicable.

---

# 35. Example Skeleton

A knowledge file should generally resemble:

---
title: Contribution Margin
slug: contribution-margin
category: finance
subcategory: contribution-margin
knowledge_types:
  - formula
  - metric
evidence_types:
  - calculation
  - source-claim
geographic_applicability:
  - global-principle
restaurant_applicability:
  - all-restaurants
qavyo_product_areas:
  - pos
  - inventory
  - menu
  - analytics
  - ai-intelligence
source_ids:
  - SRC-example-001
confidence: medium
status: draft
last_updated: YYYY-MM-DD
---

# Contribution Margin

## Definition

[Structured definition]

## Why It Matters

[Operational value]

## Core Logic

[Underlying relationship]

## Formula

[Formula or Not applicable]

## Variables

[Variable table]

## Worked Example

[Source example, illustrative example, or Not applicable]

## Interpretation

[How to understand the result]

## Operational Use

[Practical uses]

## Required Data

### Required

- ...

### Optional / Enhancing

- ...

## Relationships

- ...

## Qavyo Relevance

### Relevant Product Areas

- ...

### Potential Data Connections

...

### Possible Intelligence Use

...

### Feature Status

...

## Conditions and Limitations

- ...

## Evidence

### SOURCE-ID

Supports:

- ...

Evidence type:

...

Source context:

...

## Conflicting Evidence

...

## Related Knowledge

...

## Verification Notes

...

---

# 36. Final Rule

A strong knowledge entry should answer:

WHAT is this?

WHY does it matter?

HOW does it work?

HOW is it calculated?

WHAT data is required?

WHEN is it useful?

WHEN is it misleading?

WHAT evidence supports it?

WHERE does it apply?

HOW does it connect to other restaurant operations?

HOW could Qavyo potentially use the knowledge?

If those questions can be answered reliably, the knowledge is likely useful.
