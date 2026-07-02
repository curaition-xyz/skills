# Gymshark CurAItion Configuration

This file is the single source of truth for CurAItion scoping across all Gymshark digest skills. Every CurAItion tool call in every Gymshark digest MUST use one of these three tiers.

## Organisation

- **org_id:** `297e242a-4f5b-4012-8f82-10f717eeade7`
- **Organisation:** Gymshark (CurAItion)

## Three-Tier Scoping (MANDATORY)

### Tier 1: Partner Ecosystem (athletes)

```
org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
project_id: "83472bde-a285-42cd-bba0-f7b92728e728"
source_scope: "my_sources"
```

**Use for:** Partner Pulse athlete data, roster, content analysis, theme extraction, co-occurrences within the athlete ecosystem.

**Returns:** ~170 athlete sources, content from TikTok, Instagram, YouTube across the Gymshark partner network.

---

### Tier 2: Competitive Landscape (brands)

```
org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
source_scope: "my_sources"
(DO NOT pass project_id — omitting it returns evergreen/non-project content)
```

**Use for:** Market Pulse competitor data, brand teardowns, format innovations, competitive benchmarking.

**Returns:** ~1,200+ items from ~40+ competitor and adjacent brand accounts (YoungLA, DFYNE, Nike, Halara, TALA, Adanola, etc.).

**Important:** When project_id is omitted, results may include project content in matching domains. Filter by source handle/URL to exclude known Partner Ecosystem athletes if needed.

---

### Tier 3: Cross-Domain Intelligence (global)

```
org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
source_scope: "all"    (or "global" for CurAItion baseline only)
(DO NOT pass project_id)
```

**Use for:** Cross-domain signals in BOTH digests. Patterns from crypto, tech, gaming, F1, culture, food, music, etc. that have implications for Gymshark's strategy.

**Returns:** 9,200+ items across 16 domains from CurAItion's global cultural intelligence baseline.

**ALWAYS label cross-domain signals clearly** in the digest HTML (e.g., "Cross-Domain Signal" header, different visual treatment).

---

## When to Use Each Tier

| Digest Section | Tier |
|---|---|
| Partner Pulse — Big Story, Spotlight, Roster, Quotes | Tier 1 |
| Partner Pulse — Signal 1 (cross-domain, mandatory) | Tier 3 |
| Partner Pulse — Signals 2-3 | Tier 1 or Tier 2 |
| Partner Pulse — Who to Watch (verify existing partners) | Tier 1 |
| Market Pulse — Competitive Landscape, Brand Teardowns | Tier 2 |
| Market Pulse — Cross-Domain Signals | Tier 3 |
| Market Pulse — The Watchlist (verify existing tracking) | Tier 2 |
| Either Digest — "What We're Watching Next" prompts | All tiers (label which) |
