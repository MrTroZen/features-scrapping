# Qavyo Restaurant Intelligence — Agent Instructions

## 1. Mission

This repository is a structured restaurant operations knowledge system for Qavyo.

Its purpose is to:

- collect useful restaurant operational knowledge
- preserve source evidence
- extract calculations, formulas, KPIs, benchmarks and operational methods
- organize knowledge consistently
- identify relationships between restaurant operational data
- identify potential Qavyo product opportunities when justified by evidence
- create a long-term AI-readable restaurant intelligence library

This repository is NOT a general note-taking system.

Information must be structured for later use by AI systems, product research and software development.

---

## 2. Repository Priority

Before performing substantial knowledge-processing work, read the relevant configuration files.

The intended configuration files are:

- config/QAVYO-PRODUCT-CONTEXT.md
- config/RESEARCH-SCOPE.md
- config/TAXONOMY.md
- config/KNOWLEDGE-SCHEMA.md
- config/SOURCE-POLICY.md
- config/FEATURE-RULES.md

Do not assume missing information.

If a configuration file has not yet been completed, do not invent its contents.

---

## 3. Source Fidelity

Never change the meaning of source material.

Always distinguish between:

- FACT
- SOURCE CLAIM
- BENCHMARK
- FORMULA
- EXAMPLE
- OPINION
- RECOMMENDATION
- ESTIMATE

A statement made confidently by a creator does not automatically become a verified fact.

Do not convert:

"restaurants should target 30%"

into:

"the correct target is 30%"

unless appropriate evidence supports that conclusion.

Preserve uncertainty.

---

## 4. Numerical Integrity

Numbers are high-priority information.

When processing source material:

- preserve percentages
- preserve currencies
- preserve units
- preserve formulas
- preserve thresholds
- preserve calculation inputs
- preserve example outputs
- preserve relevant conditions and assumptions

Never silently modify numbers.

Never create missing numbers.

Never complete a formula using assumptions unless explicitly identified as an example created by the agent.

---

## 5. No Hallucinated Restaurant Knowledge

Do not invent:

- restaurant benchmarks
- industry averages
- profit margins
- labour percentages
- food-cost targets
- operational statistics
- formulas
- regulations
- Qavyo capabilities
- source claims

When something is unknown, record it as unknown rather than filling the gap.

---

## 6. Separate Source From Knowledge

Raw source material and structured knowledge are different things.

Raw transcripts belong under:

raw-transcripts/

Processed knowledge belongs under:

knowledge/

Never rewrite the raw transcript simply to make it cleaner.

The raw source should remain available as evidence.

---

## 7. One Source Can Produce Multiple Knowledge Entries

Do not assume:

one video = one knowledge file.

A source may contain:

- zero useful insights
- one useful insight
- many independent useful insights

Split materially different concepts into separate knowledge entries when appropriate.

Example:

One transcript may contain information about:

- food cost percentage
- contribution margin
- delivery commission
- menu pricing

These should not automatically become one giant knowledge document.

---

## 8. Do Not Force Knowledge Extraction

Not every transcript deserves a knowledge entry.

If a source contains only:

- marketing
- branding
- promotion
- motivational content
- sponsorship
- repetitive generic advice
- irrelevant material

it is acceptable to extract zero knowledge entries.

Do not manufacture value just because a transcript was supplied.

---

## 9. Controlled Taxonomy

Use the taxonomy defined in:

config/TAXONOMY.md

Do not casually create new top-level categories.

Do not create near-duplicate categories such as:

- profitability
- restaurant-profit
- profit-management
- restaurant-economics

when an existing category already represents the concept.

If existing taxonomy is genuinely insufficient, flag the issue rather than automatically changing the taxonomy.

---

## 10. Knowledge Granularity

A knowledge entry should represent a reusable operational concept.

Examples:

- contribution margin
- labour cost percentage
- inventory variance
- recipe costing
- menu item profitability
- waste tracking
- break-even sales
- staff productivity
- purchasing variance

Avoid extremely broad documents containing unrelated concepts.

Avoid extremely tiny documents containing no independently useful knowledge.

---

## 11. Qavyo Product Separation

Restaurant knowledge and Qavyo product ideas are not the same thing.

Restaurant knowledge belongs under:

knowledge/

Potential product concepts belong under:

feature-opportunities/

Never rewrite factual restaurant knowledge to make it fit a desired Qavyo feature.

Evidence comes first.

Product interpretation comes second.

---

## 12. No Automatic Feature Creation

Do not create a Qavyo feature simply because an interesting insight exists.

A potential feature should have a defensible relationship between:

1. a real restaurant problem
2. useful operational knowledge
3. relevant data
4. an action, decision or outcome
5. Qavyo's product capabilities

Weak or speculative opportunities should remain observations rather than becoming feature proposals.

---

## 13. Existing vs Proposed Qavyo Capabilities

Never describe a potential feature as though Qavyo already has it.

Clearly distinguish:

- existing Qavyo capability
- improvement to an existing capability
- proposed capability
- research opportunity
- speculative idea

Use config/QAVYO-PRODUCT-CONTEXT.md as the authority for existing Qavyo capabilities once that file is completed.

---

## 14. Duplicate Detection

Before creating a new knowledge file, check whether substantially equivalent knowledge already exists.

If related knowledge already exists:

- update it when appropriate
- enrich it with another source
- cross-reference it
- or create a separate entry only when there is a meaningful distinction

Do not create unnecessary duplicate files.

---

## 15. Contradictory Sources

Do not delete or hide disagreement between sources.

If two credible sources disagree:

- preserve both claims
- identify the disagreement
- preserve each source
- record applicable context
- avoid choosing a winner without adequate evidence

Conflicting information can itself be useful knowledge.

---

## 16. Source Traceability

Structured knowledge must remain traceable to its originating source.

Where applicable preserve:

- creator/source
- source title
- source URL
- publication date if known
- processing date if needed
- source identifier
- relevant transcript reference

Never create a knowledge claim with fake provenance.

---

## 17. Evidence Strength

Do not treat every source equally.

Where required, distinguish concepts such as:

- single-source claim
- multi-source agreement
- verified calculation
- industry benchmark
- illustrative example
- personal opinion
- unclear evidence

Do not inflate confidence.

---

## 18. Preserve Context

Do not extract numbers or advice while removing conditions that change their meaning.

For example, a margin discussed specifically for:

- quick-service restaurants
- full-service restaurants
- delivery
- dine-in
- a particular country
- a particular business model

must not automatically be generalized to every restaurant.

---

## 19. UK Context

Qavyo's initial commercial focus is the UK.

However:

Do not discard useful information from US or international sources.

Instead, distinguish between:

- universally useful operational principles
- geography-sensitive benchmarks
- geography-sensitive regulation
- geography-sensitive labour economics
- geography-sensitive taxes
- geography-sensitive payment economics
- geography-sensitive customer behaviour

Never assume a US benchmark automatically applies to the UK.

---

## 20. File Naming

Use clear lowercase kebab-case filenames.

Good:

contribution-margin.md

food-cost-percentage.md

inventory-variance.md

Bad:

NewFile1.md

OwnerVideoInterestingThing.md

restaurant_stuff_final2.md

Names should describe the knowledge concept rather than the creator who mentioned it.

---

## 21. Repository Cleanliness

Do not create unnecessary:

- scratch files
- duplicate files
- temporary Markdown documents
- random directories
- test output
- generated summaries

Use the established repository structure.

Temporary processing material should be removed when no longer needed.

---

## 22. Do Not Modify System Files Casually

The following files control repository behaviour:

- AGENTS.md
- config/*
- templates/*
- .agents/skills/*
- .agents/workflows/*

Do not modify these while processing ordinary transcripts unless the user explicitly requests a system change.

Knowledge ingestion must not silently change its own rules.

---

## 23. Skills and Workflows

When relevant repository skills or workflows exist under `.agents/`, use them instead of improvising a completely new process.

Follow their instructions together with AGENTS.md.

AGENTS.md establishes repository-wide principles.

Configuration defines domain rules.

Skills define specialized procedures.

Workflows define repeatable user-triggered operations.

---

## 24. Index Integrity

When knowledge files are added, removed, renamed or materially changed, update the relevant indexes when required by the configured workflow.

Indexes must point to real files.

Do not leave knowingly broken references.

---

## 25. Destructive Actions

Do not:

- delete large groups of files
- restructure major folders
- rewrite raw sources
- rewrite repository rules
- overwrite large portions of knowledge
- remove provenance

unless explicitly required.

Prefer targeted changes.

---

## 26. Git Behaviour

Never automatically push changes merely because files were modified.

Follow the active workflow.

During initial system development:

- inspect changes
- keep commits focused
- do not push unless explicitly instructed

Do not commit unrelated files together.

Never commit secrets, API keys, credentials or private tokens.

---

## 27. GitHub Is Not the Authority for Source Truth

Git history provides version history.

It does not replace source provenance.

A knowledge claim must still identify where the restaurant information originated.

---

## 28. Quality Over Volume

The goal is not to create the largest possible knowledge base.

The goal is to create a reliable, searchable and reusable restaurant intelligence system.

Prefer:

one strong structured entry

over:

five weak repetitive entries.

---

## 29. When Unsure

When a decision is uncertain:

1. preserve the source
2. avoid inventing facts
3. avoid destructive changes
4. use the existing taxonomy where reasonable
5. mark uncertainty
6. leave enough provenance for later review

---

## 30. Current Setup State

This repository is currently being constructed.

Do not interpret placeholder configuration files as completed policies.

The system should only begin production transcript processing after the required configuration, templates, skills and workflows have been completed and tested.
