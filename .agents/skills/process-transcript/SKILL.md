---
name: process-transcript
description: Quickly processes a restaurant-related transcript into a concise, structured Markdown research file. Accepts transcripts from inbox/transcripts or pasted directly into chat, extracts important information, numbers, methods, and context without full transcript duplication or product bloat, and saves directly to the appropriate knowledge category with the source link at the end.
---

# Process Transcript

## Purpose

Extract only the useful restaurant operational knowledge from a transcript into ONE small Markdown file and save it in the correct category under `knowledge/`.

Do NOT over-engineer this system.
Do NOT make product decisions or create feature backlogs.
Do NOT copy the full transcript into the research file.
Do NOT split one short transcript into multiple files.

---

# 1. Input Sources

The process-transcript skill accepts transcripts from BOTH:

1. **Direct Chat Input**:
   When a transcript is pasted directly into chat with a request to process/save/store/add it:
   - **Immediately process it.**
   - Do NOT ask whether the user wants to save it.
   - Do NOT ask whether it should go to the inbox.
   - Do NOT present Option A / Option B choices.
   - Do NOT ask whether process-transcript should run.
   - The transcript plus user request is complete authorization.

2. **Inbox Files (`inbox/transcripts/`)**:
   Plain-text or Markdown files placed in `inbox/transcripts/` (e.g. `ownercom-delivery-fees.txt`).
   When instructed to process inbox transcripts, process each file, save to `knowledge/`, and remove the inbox file only after the save succeeds.

---

# 2. Main Categories

Every transcript must be assigned to exactly ONE primary category folder:

- `knowledge/finance/`: Profit, margins, revenue, break-even, prime costs, unit economics
- `knowledge/food-cost/`: Food cost percentage, recipe costing, portion cost, ingredient cost
- `knowledge/labour/`: Staff, wages, hours, scheduling, productivity
- `knowledge/inventory/`: Stock levels, stock counts, waste, spoilage, shrinkage
- `knowledge/menu/`: Menu pricing, menu engineering, menu design, item profitability
- `knowledge/kitchen/`: Kitchen workflow, ticket times, prep planning, throughput
- `knowledge/operations/`: Operating procedures, daily management, opening/closing, table turnover
- `knowledge/purchasing/`: Supplier pricing, purchase orders, order quantities, receiving
- `knowledge/customers/`: Customer retention, repeat visits, frequency, customer lifetime value
- `knowledge/delivery/`: Delivery economics, third-party platforms, commissions, direct ordering
- `knowledge/payments/`: Transaction fees, payment processing methods, refunds, tips
- `knowledge/forecasting/`: Demand forecasting, covers prediction, sales forecasting
- `knowledge/marketing/`: General restaurant marketing, local branding, acquisition
- `knowledge/promotions/`: Discounts, special offers, promotional campaigns, happy hours
- `knowledge/social/`: Instagram, TikTok, Facebook, social media operational strategies
- `knowledge/other/`: Any valuable restaurant operational topic that does not clearly fit above

Rule: If a topic does not cleanly fit, fallback to `knowledge/other/`. Do not create new category folders. Tags in front matter handle secondary topics.

---

# 3. File Naming Convention

Use short, lowercase kebab-case filenames representing the concept:

- `knowledge/<category>/<short-topic>.md`
- Examples:
  - `knowledge/delivery/third-party-delivery-fees.md`
  - `knowledge/food-cost/food-cost-percentage.md`
  - `knowledge/customers/repeat-customer-value.md`
  - `knowledge/promotions/discount-profitability.md`
  - `knowledge/social/restaurant-instagram-content.md`

Avoid long filenames. Do not include creator names unless necessary to distinguish the topic.

---

# 4. Markdown File Structure

Keep files small (typically 10–30 lines for a short video). Use this structure:

```markdown
---
serial: "001"
title:
source:
category:
tags: []
---

# Key Information

- Main useful operational information from the transcript.
- Bullet points, concise, readable.
- Do not repeat the transcript or add filler.

# Numbers / Calculations

- Percentages, prices, costs, margins, benchmarks, formulas.
- Preserve original currencies ($ vs £). Never convert USD to GBP.
- (Only include this section if useful numbers or calculations exist).

# Useful Method / Takeaway

- Meaningful processes, strategies, rules, or operational techniques.
- (Only include this section if a meaningful method exists).

# Context

- Specific conditions: US-specific, UK-specific, restaurant type, hypothetical example, creator claim.
- (Only include this section if important context is required).

# Source

Video: [original URL]
```

---

# 5. Source Section Rules (REQUIRED)

At the very end of every processed Markdown research file, include the `# Source` section:

1. **Always the Final Section**: The `# Source` section must ALWAYS be the last section in the Markdown file.
2. **Visible Link**: Do not hide the URL only inside YAML/front matter. It must be visible at the bottom so a human can quickly click and open the original video or content later.
3. **Preserve Exact URL**: Preserve the supplied original URL exactly. Do not shorten it, alter tracking parameters unless obviously unnecessary, or invent a different URL.
4. **Fallback When Missing**: If no URL was provided with the transcript, write:
   ```markdown
   # Source

   Video: unknown
   ```
   Do NOT stop processing or ask the user for the URL.
5. **Universal Source Support**: The `# Source` section applies to all content sources (YouTube, YouTube Shorts, Instagram, TikTok, Facebook, LinkedIn, website/article URL, podcast URL). Even though the label is `Video:`, use the supplied original content link.
6. **Both Direct and Inbox**: Directly pasted transcripts and inbox transcripts must both adhere to this rule.

---

# 6. Extraction Rules

1. **Do NOT Include Full Transcripts**: Never paste the full transcript into the Markdown research file.
2. **Preserve Numbers & Currency**: Preserve exact numbers, percentages, and currencies ($ vs £).
3. **Distinguish Claims from Facts**: State creator claims as claims, not universal facts.
4. **Distinguish Examples from Benchmarks**: Hypothetical examples must not become universal benchmarks.
5. **No Product Bloat**: Never write feature opportunities, feasibility scores, backlog recommendations, or "Qavyo should build this".
6. **Check for Duplicates**: Check if a substantially identical file exists in the category. If so, enrich it instead of creating duplicates.
7. **Serial Number Traceability (Rule)**: When processing from an indexed source list (such as a CSV tracking file), always include the serial number in the front matter (e.g. `serial: "001"` formatted as a 3-digit zero-padded string) so it stays consistent with the resource tracking file.

---

# 7. Response Format

After processing, respond strictly with this concise confirmation:

```
Saved:
[path]

Category:
[category]

Tags:
[tag1, tag2, ...]

Captured:
[one short sentence]
```

Do not ask what to do next. Do not provide Option A / Option B choices.
