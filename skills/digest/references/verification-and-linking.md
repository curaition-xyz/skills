# Verification and Linking Rules — Detailed Reference

This file contains the detailed procedures for contextual verification, URL/linking standards, and hallucination prevention that every digest must follow. The SKILL.md references this file; read it during Phase 1.5 (Contextual Verification) and Phase 3 (Render).

## Table of Contents

1. Contextual Verification Procedures
2. URL and Linking Rules
3. Brand/Entity Profile Linking
4. Hallucination Prevention
5. WebSearch Fallback Procedures
6. Common Mistakes and Examples

---

## 1. Contextual Verification Procedures

### Why Verification Exists

CurAItion co-occurrence data shows entities appearing together — it says nothing about the nature of the relationship. A previous Gymshark Partner Pulse edition misidentified "Alive App" (Whitney Simmons' own company) as a third-party platform because co-occurrence data was taken at face value. This class of error applies to ALL digest types.

### Entity Ownership Checks

For every non-obvious brand or product that co-occurs with 3+ entities:

```
WebSearch: "[brand name] founder" OR "[brand name] co-founder" OR "[brand name] CEO"
```

Run in parallel for all key brands. If an entity OWNS a brand, that fundamentally changes the editorial angle — it's not a competitor, it's an extension of the entity's ecosystem.

### Person/Creator Business Venture Checks

For every person you plan to feature in a spotlight or lead story:

```
WebSearch: "[person name] brand" OR "[person name] business" OR "[person name] app" OR "[person name] company"
```

Discover businesses they own that might appear as separate entities in CurAItion data.

### Event/Campaign Context Checks

For entities showing content spikes:

```
WebSearch: "[entity name] tour 2026" OR "[event name] 2026" OR "[entity name] launch"
```

Understand what's driving the spike before editorializing about "momentum" or "cultural velocity."

### Market Data Verification

For any specific statistic, market share figure, or industry data point:

1. Find the original source (industry report, company filing, research firm)
2. Cross-reference with at least one additional source
3. If the figure cannot be verified from two sources, use hedging: "approximately", "estimated at", "reported to be"
4. Always hyperlink to the original data source in the digest

### Verification Log Format

Before proceeding to editorial writing, build this mental log:

```
Entity → Relationship Type → Evidence
--------------------------------------------------
[Brand X] → OWNS [Product Y] → [source URL]
[Person A] → SPONSORED_BY [Brand Z] → [source URL]
[Event E] → HOSTED_BY [Org O] → [source URL]
```

Any entity where the relationship type is OWNS requires completely different editorial treatment than SPONSORED_BY or COMPETES.

---

## 2. URL and Linking Rules

### The Cardinal Rule

Every factual claim in the digest must be traceable to a source with one click. The reader should never have to take your word for anything — every data point, quote, statistic, and observation must hyperlink to its origin.

### Citation Hierarchy

1. **CurAItion source content** (highest priority): Direct links to the TikTok, Instagram, YouTube, or article that CurAItion analysed. These come from `source_url` fields in `curaition_semantic_search`, `curaition_list_content`, and `curaition_get_content` results.

2. **Official sources**: Company websites, press releases, SEC filings, industry reports. Use when making market claims or citing official figures.

3. **Verified news sources**: Reputable publications covering the domain. Use when providing real-world context from Phase 0 (Ground).

4. **WebSearch results**: Direct links to search result articles. Use as fallback when CurAItion content and official sources don't cover the claim.

### Minimum Citation Requirements

- **Every section** must contain at least 2 hyperlinked citations
- **The full digest** must contain at least 3 embedded visual citation cards (YouTube thumbnails, Instagram embeds, or article cards)
- **Every data point** (percentage, count, market figure) must hyperlink to its source
- **Every person/brand** should hyperlink to a verified profile on first mention

### Inline Citation Format

Use the `citation-link` class for inline references:

```html
<a href="{URL}" target="_blank" class="citation-link" style="color: {ACCENT_COLOR}; text-decoration: none; border-bottom: 1px solid {ACCENT_COLOR};">{link text}</a>
```

### Footer Sources Section

Every digest must end with a numbered sources section listing all references used:

```html
<div class="sources-section">
  <h3>Sources</h3>
  <ol>
    <li><a href="{URL}">{Source description}</a></li>
    ...
  </ol>
</div>
```

---

## 3. Brand/Entity Profile Linking

### Process for Linking to Profiles

1. **Pull the actual URL from CurAItion data.** Run `curaition_list_content` or `curaition_semantic_search` filtered by entity name. The source URLs in the results reveal the REAL handles.

2. **Never guess or construct URLs from entity names.** If CurAItion shows content from `@dfyne.official`, the link is `https://www.instagram.com/dfyne.official/` — not `https://www.instagram.com/dfyne/` (which may be a different or private account).

3. **Link to the most active platform, or ideally all major ones.** Format: "Entity Name ([IG](url) · [TT](url) · [YT](url))". Include follower counts when available.

4. **Verify every URL before including it.** A 404 link destroys credibility instantly. If you cannot verify a URL from CurAItion data, use WebSearch to find the correct one.

5. **Extract handles from CurAItion content URLs.** If content appears at `https://www.tiktok.com/@brand.official/video/123`, the handle is `@brand.official` and the profile URL is `https://www.tiktok.com/@brand.official`.

---

## 4. Hallucination Prevention

### URL Hallucination — Zero Tolerance

- NEVER construct a URL from a brand name alone. Always derive it from CurAItion content URLs or verified WebSearch.
- NEVER add dots, underscores, or formatting to handles that don't appear in the source data. If CurAItion shows `@setactive`, the handle is `@setactive` — NOT `@set.active`, NOT `@set_active`.
- When cross-platform linking (e.g., TikTok handle → Instagram profile), assume handles match UNLESS verified otherwise via WebSearch.
- If a URL cannot be verified, DO NOT include it. Better to omit a link than to link to a 404.

### Data Hallucination Prevention

- NEVER invent percentages, follower counts, or market statistics. Every number must come from CurAItion data or a verified web source.
- NEVER present CurAItion trend percentages as absolute truth when the data window is short (less than 30 days). State what you have: "In the 14-day window analysed, X showed a +200% increase" rather than "X is growing rapidly."
- NEVER attribute quotes to real people unless the quote comes from a verified source (CurAItion citation, published interview, or official statement).

### Editorial Hallucination Prevention

- NEVER editorialize about entity relationships without web verification. CurAItion co-occurrence is not causation.
- NEVER assume a trend will continue. CurAItion shows what IS happening, not what WILL happen. Forward-looking statements must be clearly labelled as editorial interpretation.
- NEVER present your editorial interpretation as CurAItion's analysis. The platform provides data; you provide the editorial layer.

---

## 5. WebSearch Fallback Procedures

When CurAItion tools are unavailable, WebSearch becomes the primary research tool. The quality and citation standards remain identical.

### Research Substitutions

| CurAItion Tool | WebSearch Equivalent |
|---|---|
| `curaition_discover` | Domain-specific news searches: `"[domain] trends [month] [year]"` |
| `curaition_trend_analysis` | `"[domain] trending [month] [year]"`, Google Trends |
| `curaition_entity_cooccurrence` | `"[entity name] partnership" OR "[entity name] collaboration"` |
| `curaition_semantic_search` | Targeted searches for specific content by creator or topic |
| `curaition_get_cited_themes` | `"[domain] themes [year]"`, industry analysis articles |
| `curaition_detect_patterns` | Cross-referencing multiple domain searches for common threads |

### WebSearch Citation Requirements

When using WebSearch as a fallback:
- Every claim must hyperlink to the specific article or page that sourced it
- Influencer/creator profiles must be verified by visiting the actual platform URL
- Market statistics must link to the original research report or data source
- Never cite a search results page — always cite the underlying article

---

## 6. Common Mistakes and Examples

### Mistake: Unlinked claims
**Bad:** "IQOS has 69% market share in Japan's heated tobacco market."
**Good:** "IQOS holds [approximately 69% market share](https://tobaccoinsider.com/pmi-japan-2026) in Japan's heated tobacco market, according to PMI's latest disclosure."

### Mistake: Guessed profile URLs
**Bad:** Linking to `https://instagram.com/drift_king` when the actual handle is `@driftkingofficial`
**Good:** Verifying via CurAItion source URLs or WebSearch that the handle is `@driftkingofficial` before linking

### Mistake: Unverified entity relationships
**Bad:** "Brand X is competing directly with Brand Y" (based solely on co-occurrence data)
**Good:** "Brand X and Brand Y appear together in 15 content items. WebSearch confirms they are direct competitors in the same market segment."

### Mistake: Campaign spikes treated as trends
**Bad:** "Brand X is surging with a +500% increase in content volume" (during a product launch week)
**Good:** "Brand X's content spiked during their March product launch. Excluding the campaign window, their baseline output is steady at 3 items/week."
