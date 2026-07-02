# Mandatory Tool Protocols — Detailed Reference

This file contains the detailed protocols for CurAItion tools that are MANDATORY in digest production. The SKILL.md references this file from Phase 1. Read it during research to ensure you use the full intelligence toolkit.

## Table of Contents

1. Aggregated Theme Synthesis (curaition_get_cited_themes)
2. Absence Scanning (curaition_absence_scan)
3. Implication Mapping (curaition_implication_map)
4. Editorial Imagery (curaition_asset_registry)
5. Entity Universe Mapping (curaition_search_entities)
6. Content Fetching with Full Embed Data (curaition_get_content)

---

## 1. Aggregated Theme Synthesis (MANDATORY — Phase 1, Step 2.5)

### Why This Matters

`curaition_get_cited_themes` with `aggregate=true` is the tool that transforms CurAItion from "a database you queried" into "an intelligence platform that synthesised patterns across dozens of sources." It produces cross-content thematic synthesis — e.g., "the theme 'weaponization of chokepoints' appears across 8 content items with average weight 0.92." This is what makes CurAItion intelligence distinctive and what should power the editorial voice.

Without it, you're relying on per-source theme data from `get_content`, which tells you what ONE source covered. The aggregated view tells you what the ENTIRE content landscape is saying — and that's the editorial difference between a book report and an intelligence briefing.

### How to Use

After identifying 3-5 compelling signals in Step 2, run:

```
curaition_get_cited_themes
  → aggregate: true
  → theme_query: "[your signal]"  (e.g., "economic warfare", "energy transition", "crypto as infrastructure")
  → domain: [relevant domain(s)]
```

Run one call per major signal. Each returns themes ranked by cross-content evidence strength, with full citation chains.

### What to Do with the Results

- Use the highest-evidenced themes as section anchors — they represent the strongest signals in the content landscape
- Quote the evidence breadth in your editorial: "Across 14 pieces analysed, the dominant theme is X, appearing with an average weight of 0.9"
- Themes that appear in many sources with high weight are consensus; themes that appear in few sources with very high weight are emerging signals worth spotlighting
- If a theme you expected to be strong has weak aggregate evidence, that's an editorial finding worth noting

### Common Mistake

Skipping this tool and relying solely on `get_content` per-source themes. The difference: `get_content` gives you "this video discussed economic warfare." `get_cited_themes` with `aggregate=true` gives you "economic warfare is the #1 theme across the intelligence landscape, evidenced in 8 of 14 sources." The latter is what CurAItion uniquely provides.

---

## 2. Absence Scanning (MANDATORY — Phase 1, Step 7)

### Why This Matters

`curaition_absence_scan` tells you what's NOT being talked about — who's gone quiet, what topics have been displaced, which entities have dropped off the radar. This is the most unique capability CurAItion offers. No other platform systematically tracks attention absence. In a crisis digest, absence data reveals what the crisis displaced; in a domain digest, it reveals contrarian signals and overlooked stories.

### How to Use

Run for each domain in the digest:

```
curaition_absence_scan
  → domain: [domain]
  → min_decline_rate: 0.3  (start here, adjust if too many/few results)
```

For crisis or event-driven digests, also run for adjacent domains to find displacement effects (e.g., a geopolitical crisis may displace fashion or lifestyle attention).

### What to Do with the Results

The results power one of two editorial approaches:

**Option A: Dedicated "What's Been Displaced" section.** When absence data is dramatic (e.g., "Ukraine attention down 45% since the Hormuz crisis began"), create a standalone section that names the displacement pattern. This is high-value editorial content that no other newsletter can provide.

**Option B: Editorial colour in the introduction or opinion section.** When absence data is subtler, weave it into your editorial analysis: "While the world watches Hormuz, the content landscape reveals a quieter shift — normal Bitcoin DeFi narratives have been almost entirely displaced by war-barometer coverage."

### Common Mistake

Treating absence scan as optional or "nice to have." It should run alongside your positive signal research. The story of what's disappeared is often as important as what's appeared.

---

## 3. Implication Mapping (MANDATORY — Phase 2, Recommendations Section)

### Why This Matters

`curaition_implication_map` generates audience-specific strategic implications with scenario analysis (continues/accelerates/reverses). Without it, the Recommendations section relies on editorial guesswork. With it, recommendations are grounded in systematic analysis of what different outcomes mean for different audiences.

### How to Use

Run after Phase 1 research is complete, before writing the Recommendations section:

```
curaition_implication_map
  → entity_name: [primary entity or pattern from the digest]
  → audiences: [relevant to the digest's readership — e.g., "investors", "content creators", "brands", "policymakers"]
```

### What to Do with the Results

- Select the 2-3 most actionable implications per audience
- Use the scenario analysis (continues/accelerates/reverses) to frame recommendations as conditional: "If X continues, then Y; if it reverses, then Z"
- The tool's output makes Recommendations data-driven rather than purely editorial — it's the difference between "we think brands should..." and "CurAItion's analysis suggests that if this pattern continues, brands should..."

### When to Skip

If the digest is purely retrospective (e.g., "what happened this week") with no forward-looking Recommendations section, you can skip this tool. But most digests benefit from at least a brief implications paragraph.

---

## 4. Editorial Imagery (CONDITIONAL — Phase 3)

### Why This Matters

`curaition_asset_registry` with action `generate_backfill` calls Replicate (Flux Schnell) to generate custom editorial imagery. This fills a gap when source content is text-heavy and lacks usable thumbnails.

### How to Use

```
curaition_asset_registry
  → action: "generate_backfill"
  → [prompt grounded in the digest's content analysis]
```

### When to Use

- A section has no CurAItion content items with usable thumbnails
- The digest topic is text-heavy (articles, reports, analysis pieces)
- You want a custom section header that captures the editorial theme

### When NOT to Use

- When real source thumbnails exist — always prefer authentic content imagery
- For every section — use sparingly (1-2 per digest max)
- The goal is editorial illustration, not decoration

See `references/visual-card-patterns.md` section 5 for the full card template.

---

## 5. Entity Universe Mapping (RECOMMENDED — Phase 1, Step 2)

### Why This Matters

`curaition_search_entities` maps the full entity universe around a topic — every person, brand, event, and concept that CurAItion has tracked, with content counts and domain spread. This surfaces entities you didn't think to search for, preventing the "known unknowns" problem where you only find what you already knew to look for.

### How to Use

```
curaition_search_entities
  → query: [topic or primary entity]
  → entity_type: [optional — filter to people, brands, events, etc.]
  → domain: [optional — filter to specific domain]
```

Run early in Phase 1 alongside `discover` and `trend_analysis`. Use the results to expand your search space: if entity search reveals "QatarEnergy" and "Kharg Island" as high-content entities you hadn't considered, add them to your semantic search queries.

---

## 6. Content Fetching — Thumbnail Priority (MANDATORY — Phase 1, Step 3)

### The Key Parameter

When calling `curaition_get_content`, always pass `include_citations: true`. This returns `citations.embed.thumbnail_url` — the real image URL you need for visual citation cards.

For YouTube content, `thumbnail_url` is ALWAYS available (format: `https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg`). This means every YouTube video in CurAItion can produce a real image card. There is no reason to produce a digest without at least 3 visual cards when the content landscape includes YouTube videos.

**Only for Instagram/TikTok content**, also pass `include_embed_html: true` to get pre-formatted iframe/blockquote markup. Do NOT rely on `embed_html` for YouTube — it returns a generic gradient card without the actual thumbnail image.

### Thumbnail Priority Order
1. `citations.embed.thumbnail_url` — use this first, always. Build an `<img>` card.
2. `embed_html` — use ONLY for Instagram/TikTok where `thumbnail_url` is absent.
3. Native iframe embed — last resort for Instagram legacy content.

### Common Mistake

Passing only `include_citations=true` and missing `include_embed_html=true`. For YouTube-heavy digests this makes no practical difference, but for Instagram/TikTok-heavy digests you'll end up manually constructing embed markup that the tool would have given you for free.

### Card Dedup Rule

Visual card HTML must use exactly ONE `href` per source URL (the image `<a>` wrapper). The title inside the card must be a plain `<div>`, NOT a second `<a>` tag. This is the #1 cause of dedup violations — a card with two `<a>` tags immediately consumes 2 of the source's max-2 href budget, and the Sources section pushes it to 3.
