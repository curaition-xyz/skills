# Source Coverage & Deduplication Protocol — Detailed Reference

This file contains the protocol for auditing source coverage and creating a deduplication allocation plan BEFORE rendering. The SKILL.md references this file from Phase 1.75 (Source Coverage Audit). Read it after completing Phase 1 research and before starting Phase 2 curation.

## Table of Contents

1. Source Coverage Report
2. Source Allocation Plan
3. Coverage Targets
4. Worked Example

---

## 1. Source Coverage Report (MANDATORY — between Phase 1 and Phase 2)

### Why This Exists

The Hormuz crisis digest had 34 relevant CurAItion sources available but only used 7 (20%). This wasn't a deliberate editorial choice — it was an accidental gap caused by not auditing coverage before curation. The Source Coverage Report prevents this by making the gap visible before you commit to a narrative structure.

### How to Build It

After completing all Phase 1 research, compile a source inventory:

**Step 1: List all discovered CurAItion content items**

Run these two queries and merge the results (deduplicate by content_id):

```
curaition_list_content → title search for [topic keywords]
curaition_semantic_search → conceptual search for [topic + adjacent concepts]
```

If you ran additional semantic searches during Phase 1, include those results too.

**Step 2: Count and categorise**

For each discovered item, note:
- `content_id`
- `title`
- `source_url`
- `content_type` (video, short, article, reel, etc.)
- `relevance` (high / medium / low — based on how central it is to the digest's theme)

**Step 3: Select and document**

Select 5-8 items for the digest. For each item NOT selected, write a one-line reason:
- "Too tangential — covers Iran but not Hormuz specifically"
- "Duplicate angle — same topic as [other selected item] but weaker"
- "Low quality score"
- "Would exceed section source budget"

### What This Produces

A mental model (and optionally a written note) of:
- **Total available**: how many CurAItion sources exist for this topic
- **Selected**: which ones you're using and where
- **Excluded**: which ones you skipped and why
- **Coverage rate**: selected / total available

---

## 2. Source Allocation Plan (MANDATORY — before starting Phase 3 HTML)

### Why This Exists

The Content Deduplication Rules in SKILL.md say "audit before rendering" — but by Phase 3 you've already committed to a narrative structure and restructuring is expensive. The Source Allocation Plan moves the dedup audit to Phase 2, before any HTML is written.

### Format

Build a simple allocation map before writing any HTML:

```
content_id | title (short)         | section           | format
-----------|----------------------|-------------------|--------
abc123     | Atlantic Oil Analysis | I. The Chokepoint | card
def456     | Graeme Wood Dispatch  | II. Dispatches    | card
ghi789     | Fertilizer Crisis    | III. From Field   | card
jkl012     | $200 Oil Scenario    | III. From Field   | inline
mno345     | Crypto Outflows      | IV. Crypto Front  | card
pqr678     | Trump Ultimatum      | I. The Chokepoint | inline
stu901     | Iran Speedboats      | V. Overheard      | inline
```

Format types:
- **card** = visual citation card (thumbnail, embed, or article card) — MAX ONE per content item across entire digest
- **inline** = text hyperlink citation — allowed after a card exists elsewhere, or as standalone
- **skip** = in the coverage report but not used in the digest

### Validation Rules

Before proceeding to HTML:
1. No content_id appears as "card" more than once
2. No content_id appears more than twice total (1 card + 1 inline, or 2 inline)
3. Each section draws from at least 2 different source content items
4. No two consecutive sections share the same primary card source
5. Total unique sources used ≥ 5

If any rule is violated, redistribute before writing HTML.

---

## 3. Coverage Targets

| Metric | Target | Red Flag |
|--------|--------|----------|
| Unique CurAItion sources used | ≥ 5 | < 4 |
| Coverage rate (used / available) | ≥ 30% | < 20% |
| Max appearances per source | 2 | 3+ |
| Sections with visual cards | ≥ 3 | < 2 |
| Sources per section (unique) | ≥ 2 | 1 |

If available sources for the topic are fewer than 10, flag to the user that CurAItion coverage may be thin and consider supplementing with WebSearch-sourced content (following the WebSearch fallback procedures in `verification-and-linking.md`).

---

## 4. Worked Example

**Hormuz Crisis Digest — what should have happened:**

Available sources: 34 (14 title matches + ~20 semantic matches)
Target coverage: 30% = ~10 sources
Actually used: 7 (20%) — below target

The missing step was the Source Coverage Report. Had it been run, it would have surfaced 34 available sources and the 30% target would have pushed selection to 10-11 items. The extra 3-4 sources would have either added new visual cards to thin sections or provided denser inline citation, making the editorial voice feel more grounded in a broad intelligence scan rather than a narrow selection.

The Source Allocation Plan would have caught that The Atlantic's oil analysis video appeared as both a card in Section I and a card in Section II (violating the one-card-per-source rule) before any HTML was written, rather than requiring a post-render fix.

---

## 5. Post-Render Dedup Verification

Even with a Source Allocation Plan, dedup violations slip through during HTML generation because the agent loses track of URL counts across a long output. This step is a mandatory final gate.

### Procedure

After generating the full HTML, before saving:

1. Scan the HTML for all `href="https://..."` values
2. Build a frequency count: `{ url: count }`
3. Check: is any count ≥ 3? If yes, find and remove or replace the excess reference
4. Check: does any source URL appear as both a visual card `<img>` AND an `<iframe>`? If yes, remove one
5. Check: are there ≥ 5 unique source URLs? If no, add inline citations from your coverage report's unused sources

### Why This Exists

In eval testing, dedup compliance failed in 100% of runs (4 of 4) despite the Source Allocation Plan existing. The root cause is that agents correctly plan dedup at Phase 1.75, then lose track during the long Phase 3 HTML generation. This post-render check catches the drift.
