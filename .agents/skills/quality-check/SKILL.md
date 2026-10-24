---
name: quality-check
description: Reviews processed restaurant research files for accuracy, preserved transcript, numerical integrity, formula correctness, clean Markdown, and appropriate category placement.
---

# Quality Check

## Purpose

Review processed research files after transcript extraction to ensure quality, factual integrity, and completeness.

The quality check is simple and focused. It does NOT perform product-level checks, feature evaluations, or backlog reviews.

---

# 1. Quality Checklist

For each reviewed research file, verify:

1. **Transcript Preserved**: The complete transcript is included under `# Full Transcript`.
2. **Numbers & Statistics Accurate**: All material percentages, costs, currencies, units, and ranges match the source transcript exactly. Currencies were not silently converted.
3. **Formulas Accurate**: Mathematical formulas, inputs, and outputs are correctly recorded and explained. Discrepancies in the source are noted rather than silently rewritten.
4. **Source Metadata Correct**: Source URL, creator, platform, and publication date are recorded accurately when known. Unknown values are marked `unknown`, not fabricated.
5. **Category Reasonable**: The file is placed in the best matching folder among the 14 standard categories under `knowledge/`.
6. **No Important Information Lost**: Operational concepts, management methods, and practical insights were not omitted simply because they don't relate to software.
7. **Examples vs Facts**: Hypothetical or creator-specific examples are not presented as industry-wide facts or universal benchmarks.
8. **Claims vs Facts**: Creator opinions and assertions are clearly identified as claims, not verified universal truths.
9. **Clean Markdown**: Proper front matter, headings, bullet lists, and readable structure.
10. **No Product Creep**: No feature proposals, product backlogs, feasibility scores, or "Qavyo should build this" commentary.

---

# 2. Scope & Results

Review one research file or a recent batch of processed files.

Use one of these review outcomes:

- **PASS**: Meets all quality standards.
- **PASS-WITH-CORRECTIONS**: Minor, safe corrections made (e.g. formatting, labeling a claim, typo in numbers).
- **NEEDS-REVIEW**: Unclear source audio/text or ambiguous statement requires human review.

Keep reports concise:
```
Quality result: [PASS / PASS-WITH-CORRECTIONS / NEEDS-REVIEW]
File reviewed: [path]
Corrections made: [none or list]
Notes: [optional brief note]
```

---

# 3. Prohibited Actions

This skill must NOT:
- perform product feasibility or feature evaluations
- rewrite substantive source content
- commit or push to Git
