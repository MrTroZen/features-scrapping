# Qavyo Restaurant Intelligence — Source Policy

## 1. Purpose

This file defines how research sources are:

- recorded
- identified
- evaluated
- preserved
- cited
- compared
- processed
- linked to structured knowledge

The goal is to ensure that every important knowledge claim remains traceable to its original source.

A source can provide useful knowledge without automatically being treated as authoritative.

---

# 2. Source vs Knowledge

A source record describes:

WHERE the information came from.

A knowledge entry describes:

WHAT reusable restaurant knowledge was extracted.

These must remain separate.

Example:

Source:

Owner.com short-form video about menu profitability.

Knowledge extracted:

- contribution margin
- menu item profitability
- pricing relationship

One source may support multiple knowledge entries.

One knowledge entry may be supported by multiple sources.

---

# 3. Supported Source Types

The system may collect useful restaurant knowledge from:

- short-form video
- long-form video
- podcast
- interview
- article
- blog post
- industry report
- research report
- documentation
- webinar
- presentation
- social-media post
- restaurant operator discussion
- forum discussion
- Reddit discussion
- software company education content
- consultant content
- accounting content
- hospitality training content
- government or regulatory material
- academic material
- other relevant sources

The source type does not determine usefulness by itself.

---

# 4. Source Record Requirement

Every processed source must have a source record.

Source records should eventually be stored in a dedicated source-record location defined by the repository workflow.

Every source record should have a stable Source ID.

Knowledge entries must reference Source IDs rather than relying only on URLs.

---

# 5. Source ID Format

Use a stable Source ID format.

Recommended structure:

SRC-[source]-[topic]-[number]

Examples:

SRC-ownercom-food-cost-001

SRC-ownercom-menu-profitability-002

SRC-restaurant365-inventory-001

SRC-7shifts-labour-001

SRC-reddit-restaurantowners-labour-001

Use lowercase after the SRC prefix when practical.

Do not change an existing Source ID simply because the source title later changes.

The Source ID is an internal stable reference.

---

# 6. Source Metadata

Every source record should preserve as much of the following as is actually known:

- source_id
- creator
- organisation
- platform
- source_type
- title
- source_url
- publication_date
- date_accessed
- geography
- language
- transcript_available
- transcript_location
- processing_status
- primary_topics
- notes

Do not invent missing metadata.

Use:

unknown

when necessary.

---

# 7. Source URL

Preserve the direct source URL whenever available.

Prefer the original source.

Examples:

Prefer:

original YouTube video

over:

a reposted clip

Prefer:

original Owner.com page or social post

over:

a third-party copy

If only a repost exists, record that fact.

---

# 8. Creator and Organisation

Where possible, distinguish:

Creator:
individual person

Organisation:
company or entity publishing the content

Example:

Creator:
[person]

Organisation:
Owner.com

Do not assume the speaker personally represents every claim made by the organisation unless the source establishes that.

---

# 9. Publication Date

Preserve publication date when known.

This is especially important for:

- costs
- labour benchmarks
- software economics
- payment fees
- inflation-sensitive numbers
- regulations
- wage information
- consumer behaviour
- industry benchmarks

If publication date is unknown:

publication_date: unknown

Never fabricate a date from upload order or filename.

---

# 10. Geography

Preserve source geography when relevant.

Examples:

- uk
- us
- europe
- global
- unknown

Also record more specific geographic context when materially relevant.

Example:

A labour-cost claim based on California should not automatically be represented merely as:

US restaurant labour benchmark.

Preserve specificity when it matters.

---

# 11. Raw Transcript Preservation

When a transcript is available, preserve the raw transcript separately from structured knowledge.

Raw transcripts must not be rewritten to improve grammar or readability.

Minor technical cleanup may be performed only if necessary for storage, such as:

- removing duplicated transcription artifacts
- fixing obvious timestamp formatting
- removing accidental repeated lines

Do not change substantive meaning.

When uncertain, preserve the original.

---

# 12. Transcript Types

Where possible, identify transcript origin.

Examples:

- platform-generated
- manually transcribed
- AI-generated
- creator-provided
- unknown

AI-generated transcripts may contain errors.

Important numbers, names, percentages and formulas should be treated carefully when transcript accuracy is uncertain.

---

# 13. Transcript Confidence

If a transcript appears unclear, mark issues such as:

- uncertain number
- uncertain speaker wording
- incomplete sentence
- inaudible section
- suspected transcription error

Do not silently guess.

Example:

If transcript says:

"food cost should be twenty... maybe thirty percent"

do not rewrite it as:

Food cost should be 30%.

Mark the ambiguity.

---

# 14. Source Quality Is Multi-Dimensional

Do not assign credibility solely based on:

- follower count
- production quality
- company size
- popularity
- confidence of speaker

Evaluate sources based on factors such as:

- expertise
- transparency
- evidence
- specificity
- methodology
- context
- consistency
- recency
- independence
- primary vs secondary sourcing

---

# 15. Source Reliability Levels

When required, a source may be assigned a rough reliability level:

- low
- medium
- high
- unknown

This rating applies to the source for the relevant topic.

It is not a permanent judgement of the creator.

Example:

A restaurant software company may be:

high reliability for explaining its own software behaviour

but only:

medium reliability for broad industry profitability claims

unless evidence is provided.

---

# 16. Primary Sources

Prefer primary evidence where available.

Examples:

- government regulations
- official tax guidance
- official wage data
- financial statements
- original research
- original surveys
- first-party documentation
- direct operator data

Secondary educational content can still be valuable, especially for explaining operational methods.

---

# 17. Promotional Sources

Restaurant software companies, consultants and creators may produce excellent educational content while also promoting a product or service.

Do not automatically reject promotional sources.

Instead separate:

Useful restaurant knowledge

from:

Product promotion

Example:

A software company may accurately explain:

theoretical vs actual food cost

while then claiming:

"our software is the only way to solve this."

Extract the operational concept.

Ignore unsupported promotional superiority claims.

---

# 18. Competitor Sources

Competitor educational material is valid research input.

Examples may include:

- Owner.com
- Toast
- Square
- Lightspeed
- Restaurant365
- 7shifts
- MarginEdge
- Deliverect
- other restaurant technology companies

Do not treat competitor content as product requirements.

Separate:

underlying restaurant problem

from:

competitor implementation

and from:

competitor marketing.

---

# 19. Owner.com Specific Policy

Owner.com is expected to be an important initial research source, especially for short-form restaurant education content.

When processing Owner.com content:

Prioritise:

- calculations
- profitability logic
- margins
- restaurant economics
- cost control
- menu economics
- direct-order economics
- customer economics
- management processes
- operational decision rules
- practical restaurant examples

Deprioritise:

- Owner.com product promotion
- branding messages
- sales messaging
- founder promotion
- generic marketing content
- generic growth claims
- calls to action

Do not automatically reject useful knowledge merely because the source promotes Owner.com.

---

# 20. Source Claim Classification

Claims extracted from a source should be distinguished when possible.

Examples:

### Factual Claim

A statement presented as fact.

### Benchmark Claim

A recommended or observed numerical range.

### Personal Experience

Based on the speaker's own restaurant or clients.

### Example

Used to demonstrate a concept.

### Recommendation

What the creator suggests doing.

### Opinion

A judgement or viewpoint.

### Promotional Claim

A claim intended to promote a product or service.

### Derived Calculation

A value that can be mathematically calculated from provided data.

Do not merge these categories.

---

# 21. Benchmarks Require Extra Caution

Claims such as:

"restaurants should spend 30% on labour"

must retain context.

Capture:

- exact claim
- source
- geography
- restaurant type
- date
- whether a range was given
- whether evidence was provided
- whether it is a recommendation or observed average

Do not transform a benchmark recommendation into a universal standard.

---

# 22. Examples Are Not Benchmarks

If a creator says:

"Imagine a restaurant doing £100,000 in monthly sales with £30,000 in labour."

This is an example.

It does NOT establish:

Restaurants should have 30% labour cost.

Classify examples correctly.

---

# 23. Creator Case Studies

Case studies may provide valuable operational knowledge.

Record whether the case describes:

- one restaurant
- several restaurants
- an anonymised client
- a hypothetical restaurant
- an industry dataset

Do not generalise single-business results into industry benchmarks automatically.

---

# 24. Numbers and Currency

Always preserve currency.

Example:

$50,000

must not silently become:

£50,000

When knowledge principles are reusable across currencies, the principle may be generalised while the original example remains preserved.

---

# 25. US to UK Translation

Do not automatically convert US numbers into UK numbers.

For example:

- wages
- taxes
- delivery fees
- card processing
- rent
- menu prices
- labour benchmarks

must remain in their original context unless a deliberate UK validation step occurs.

General formulas may still be applicable.

---

# 26. Duplicate Sources

The same video or piece of content may appear on:

- TikTok
- Instagram
- YouTube Shorts
- LinkedIn
- Facebook

These should normally be treated as one underlying source if the content is materially identical.

Do not create five independent evidence sources from one piece of content.

Record alternate URLs when useful.

---

# 27. Reposted Content

If content is reposted by another account:

identify the original creator when reasonably known.

Do not count a repost as independent corroboration.

---

# 28. Repeated Creator Claims

If one creator repeats the same claim across ten videos:

this does not equal ten independent sources.

The knowledge system should recognise source dependence.

Repeated claims may demonstrate consistency from that creator, but not independent consensus.

---

# 29. Independent Corroboration

Multi-source support is stronger when sources are genuinely independent.

Examples:

Stronger:

Owner.com
+
restaurant accountant
+
government industry data

Weaker:

three Owner.com videos repeating the same claim.

Do not inflate evidence strength.

---

# 30. Conflicting Sources

When sources disagree:

Do not delete either source.

Record:

- source A claim
- source B claim
- contextual differences
- possible reasons for disagreement
- whether additional verification is required

Conflicting evidence should improve understanding rather than be hidden.

---

# 31. Source Correction

If a source appears factually or mathematically wrong:

Do not rewrite history.

Preserve:

what the source claimed

and separately record:

identified discrepancy.

Example:

Source calculation:

£20 ÷ £100 = 25%

Actual calculation:

£20 ÷ £100 = 20%

Record the source error.

Do not present the corrected result as if the creator originally stated it.

---

# 32. Claim Extraction

Do not extract every sentence as knowledge.

Extract only claims that are:

- operationally useful
- reusable
- measurable
- decision-relevant
- explanatory
- part of a valid calculation
- important for restaurant management

Avoid filling the repository with trivial statements.

---

# 33. Evidence Summary

Knowledge files should contain concise evidence summaries.

Do not paste full transcripts into knowledge entries.

Example:

Good:

Source explains that contribution margin should account for item selling price and relevant variable costs.

Bad:

Copying the entire 90-second transcript into the knowledge file.

The raw transcript already preserves full source context.

---

# 34. Direct Quotes

Direct quotations should be used sparingly.

Prefer structured paraphrase.

Use direct wording only when:

- exact phrasing materially matters
- ambiguity needs preservation
- the claim would otherwise lose meaning

Never replace evidence with unnecessarily long quotes.

---

# 35. Source Processing Status

Source records may use controlled processing statuses:

- inbox
- processing
- processed
- partially-processed
- rejected-no-useful-knowledge
- needs-review
- duplicate
- archived

Do not invent new statuses casually.

---

# 36. Rejected Sources

A source can be processed and produce zero knowledge entries.

Examples:

- purely promotional video
- repeated generic advice
- motivational content
- content already fully represented
- no operational substance

Mark:

rejected-no-useful-knowledge

This is a valid outcome.

---

# 37. Partially Useful Sources

A video may contain:

80% marketing
20% valuable operational knowledge

Extract only the useful 20%.

Do not summarise the entire source simply because it was submitted.

---

# 38. Source Topic Tags

Source records may contain several primary topics.

Examples:

- food-cost
- menu-engineering
- labour
- inventory
- finance

These topic tags help discovery.

They do not replace the formal taxonomy of knowledge entries.

---

# 39. Source Record Must Not Become Analysis

The source record should remain primarily factual.

It records:

- identity
- provenance
- metadata
- transcript
- processing outcome

Detailed restaurant knowledge belongs in knowledge files.

Detailed product ideas belong in feature-opportunities.

---

# 40. Source Archival

Once processed:

the original transcript should remain available unless deliberately removed for legal, storage or policy reasons.

Processing should not destroy the source.

---

# 41. Missing Original Content

If only a transcript is available and the original URL is missing:

record:

source_url: unknown

Do not fabricate one.

The transcript can still be processed if useful.

---

# 42. Deleted Content

If a source later disappears online:

do not remove structured knowledge automatically.

Preserve the recorded provenance and note:

source no longer accessible

when this becomes known.

---

# 43. Updated Sources

If a source is materially revised or replaced:

preserve enough information to distinguish versions when the difference matters.

Do not overwrite meaningful historical evidence without noting the change.

---

# 44. Source Independence

When evaluating consensus, consider ownership and derivation.

For example:

An article quoting another article is not necessarily independent evidence.

A creator repeating a statistic from a report should ideally link back to the original report when possible.

Prefer the upstream source for validation.

---

# 45. Source Escalation

When a source provides a highly valuable but uncertain claim, mark it for further verification.

Examples:

- strong benchmark
- unusual margin claim
- regulatory claim
- tax claim
- major profitability number
- surprising industry statistic

Use:

needs-verification

rather than discarding potentially useful information.

---

# 46. Regulation and Legal Content

Legal, tax, wage, employment and compliance information can materially change over time.

For these topics:

- preserve jurisdiction
- preserve date
- prefer authoritative sources
- avoid treating old content as current law
- flag information requiring current verification

The restaurant intelligence system is not a substitute for professional legal or tax advice.

---

# 47. Source Priority

When multiple sources describe the same concept, prefer stronger evidence for the canonical knowledge entry.

A rough preference may be:

authoritative primary source
↓
research/data
↓
experienced practitioner with methodology
↓
industry specialist
↓
educational company content
↓
single operator experience
↓
unverified social media claim

This is not absolute.

Context matters.

---

# 48. Source Diversity

Over time, avoid building the entire knowledge base from one company or creator.

The system should deliberately accumulate diverse perspectives.

Important concepts should ideally be validated across different source types.

Example:

Contribution margin:

software educator
+
restaurant accountant
+
operator
+
industry documentation

This reduces dependence on one source's worldview.

---

# 49. Processing Date

Record when the source was processed when useful.

This helps identify:

- outdated benchmarks
- research age
- validation needs
- processing history

Use ISO format:

YYYY-MM-DD

---

# 50. Source Provenance Rule

Every material knowledge claim must be traceable.

The chain should be:

Knowledge statement
↓
Source ID
↓
Source record
↓
Original source / transcript

If this chain is broken, provenance is incomplete.

---

# 51. No Fake Evidence

Never create:

- fake URLs
- fake creators
- fake titles
- fake publication dates
- fake quotes
- fake statistics
- fake citations
- fake reports
- fake source IDs pointing to nonexistent records

Unknown information must remain unknown.

---

# 52. Final Source Test

Before marking a source as processed, ask:

1. Do we know where it came from?
2. Is the original transcript preserved when available?
3. Did we separate useful knowledge from promotion?
4. Did we preserve important numbers accurately?
5. Did we preserve geography and context?
6. Did we distinguish examples from benchmarks?
7. Did we identify source claims rather than presenting everything as fact?
8. Did we avoid counting duplicates as independent evidence?
9. Can every extracted knowledge entry trace back to this source?
10. Is the processing status correct?

If yes, the source is ready to be considered processed.
