---
name: quality-check
description: Simple quality check for processed restaurant research files. Verifies category placement, numerical integrity, formula accuracy, original currency preservation, claims vs facts distinction, and concise Markdown format without product bloat.
---

# Quality Check

## Purpose

Verify that a processed research file accurately and concisely captures restaurant operational knowledge without errors, bloat, or product distortion.

---

# 1. Quality Checklist

For each reviewed research file, verify:

1. **Correct Category**: File is placed in the best matching folder among the 16 standard categories under `knowledge/`.
2. **Useful Information Preserved**: Key operational insights, methods, and practical takeaways were retained.
3. **Numbers & Calculations Accurate**: Percentages, costs, margins, and formulas match the source exactly.
4. **Original Currency Preserved**: Currencies (e.g. $, £, €) are kept intact without silent conversions.
5. **Examples vs Facts**: Hypothetical or creator-specific examples are not presented as universal industry facts or benchmarks.
6. **Claims vs Facts**: Creator opinions and assertions are clearly labeled as claims, not verified universal truths.
7. **Concise Markdown**: File is small (10–30 lines), uses bullet points, contains no filler or full transcript dumps.
8. **No Product Bloat**: No feature proposals, backlog recommendations, feasibility scores, or "Qavyo should build this" commentary.
9. **No Duplicates**: File is not a redundant duplicate of an existing topic file in that category.

---

# 2. Review Result

Use one of these outcomes:

- **PASS**: Meets all standards.
- **PASS-WITH-CORRECTIONS**: Minor corrections made (formatting, typo in number, label corrected).
- **NEEDS-REVIEW**: Ambiguity in source requires human review.

Report format:
```
Quality check: [PASS / PASS-WITH-CORRECTIONS / NEEDS-REVIEW]
File: [path]
Corrections: [none or list]
```
