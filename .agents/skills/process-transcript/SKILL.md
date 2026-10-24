---
name: process-transcript
description: Processes a restaurant-related transcript into a single structured research file. Extracts all useful restaurant operational knowledge, preserves numbers, calculations, claims, examples, context, and the full transcript into the appropriate knowledge category.
---

# Process Transcript

## Purpose

Process one restaurant-related transcript into a single structured Markdown research file.

The goal is simple:

Save all useful restaurant operational knowledge permanently.

Each useful source produces ONE Markdown research file under the appropriate category in `knowledge/`.

Do NOT split one transcript into many knowledge files.
Do NOT create product features or backlogs.
Do NOT make product decisions or score opportunities.

---

# 1. Processing Workflow

Follow these steps for each transcript:

1. Read the transcript from `inbox/transcripts/`.
2. Read `config/QAVYO-PRODUCT-CONTEXT.md` only for general domain understanding (never filter out useful knowledge because it doesn't match a Qavyo module).
3. Identify the primary category from the 14 standard categories in `knowledge/`.
4. Identify useful tags for secondary concepts.
5. Remove obvious transcript noise (intros, outros, subscribe requests, sponsor reads, filler, repeated transcription glitches).
6. Preserve all useful restaurant information.
7. Preserve numbers, metrics, benchmarks, and statistics with original currency and units.
8. Preserve calculations, formulas, inputs, outputs, and explanations exactly.
9. Preserve useful examples and case studies (distinguish from facts or benchmarks).
10. Preserve important creator claims (without assuming they are verified facts).
11. Preserve context and limitations (e.g., US/UK, restaurant type, service model).
12. Include the complete transcript at the bottom of the file.
13. Create ONE clean Markdown research file using the standard research file format.
14. Place the file in the best-matching category folder under `knowledge/<category>/`.
15. Remove the inbox copy from `inbox/transcripts/` only after the file is successfully saved.

---

# 2. Categories

Place the research file into one of these 14 main category folders:

- `knowledge/finance/`
- `knowledge/food-cost/`
- `knowledge/labour/`
- `knowledge/inventory/`
- `knowledge/menu/`
- `knowledge/kitchen/`
- `knowledge/operations/`
- `knowledge/purchasing/`
- `knowledge/customers/`
- `knowledge/delivery/`
- `knowledge/payments/`
- `knowledge/forecasting/`
- `knowledge/marketing/`
- `knowledge/other/`

Do not create subfolders. Use tags in the front matter for secondary topics.

---

# 3. File Naming Convention

Use lowercase kebab-case:

- When date is known:
  `YYYY-MM-DD-[source]-[short-topic].md`
  Example: `2026-10-20-ownercom-food-cost-control.md`

- When date is unknown:
  `[source]-[short-topic].md`
  Example: `ownercom-food-cost-control.md`

Avoid unnecessarily long filenames.

---

# 4. Research File Structure

Every processed research file must use this format:

```markdown
---
title:
source:
creator:
url:
platform:
date:
category:
tags: []
---

# Summary

Short explanation of what the content teaches.

# Important Information

Save all useful restaurant information.

Do not remove information simply because it does not immediately relate to Qavyo.

# Numbers & Statistics

Save all useful:
* percentages
* costs
* margins
* averages
* ranges
* benchmarks
* quantities
* dates

Preserve original currency and context.

If none:
None.

# Calculations & Formulas

Save formulas and calculation methods exactly when available.

Include:
* formula
* inputs
* output
* explanation

If none:
None.

# Operational Methods

Save useful processes, systems, workflows, rules and management methods.

If none:
None.

# Useful Examples

Preserve useful examples from the source.

Clearly distinguish examples from facts or benchmarks.

# Important Claims

Save meaningful claims made by the creator.

Do not automatically treat creator claims as verified facts.

# Context / Limitations

Record things such as:
* US-specific
* UK-specific
* restaurant type
* hypothetical example
* creator opinion
* unclear evidence

# Full Transcript

Preserve the complete transcript.
```

---

# 5. Extraction Principles

- **Save Everything Useful**: If content teaches something meaningful about restaurants, operations, finance, costs, customers, staff, inventory, menus, marketing, profitability, management, delivery, forecasting, payments, or restaurant business, save it.
- **Do Not Filter for Qavyo**: Do NOT reject information because it is not currently a Qavyo feature or software capability.
- **Numerical Integrity**: Preserve exact numbers, currencies ($ vs £), units, and ranges. Never convert currencies or generalize local benchmarks without evidence.
- **Distinguish Claims from Facts**: State creator claims as claims. Do not turn personal opinions or anecdotal examples into universal industry facts.
- **No Product Decisions**: Do NOT write feature proposals, product recommendations, backlog items, or feasibility scores.

---

# 6. Prohibited Actions

Do NOT:
- create feature files or entries in `feature-opportunities/`
- decide what Qavyo should build
- split one transcript into multiple knowledge files
- merge unrelated source files
- create product scores or feasibility ratings
- create complex evidence matrices
- update product indexes
- commit or push to Git
