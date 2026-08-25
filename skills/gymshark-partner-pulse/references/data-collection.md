# Data Collection Reference — Partner Pulse CurAItion Tool Call Patterns

All calls must include:
- `org_id`: `297e242a-4f5b-4012-8f82-10f717eeade7`
- `project_id`: `0bdbc3d2-1360-4430-b634-dea95841c9ba`
- `source_scope`: `my_sources` (where applicable)

See `_shared/gymshark-config.md` for the full three-tier scoping strategy.

## Batch 1: Landscape Overview (run in parallel)

### Content Stats
```
curaition_get_stats
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
```
Returns: total content items, format breakdown (TikTok videos, IG reels, IG carousels, long-form, etc.), source count. Use the total from get_stats as the canonical content count — it may differ from list_content pagination totals.

### Cited Themes
```
curaition_get_cited_themes
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  aggregate: true
  min_weight: 0.5
  limit: 30
```
Returns: themes with citation counts and weights. Higher citation count = more evidence. Weight 1.0 = maximum confidence. These are your editorial building blocks — each theme is a potential story.

### Gymshark Co-occurrences
```
curaition_entity_cooccurrence
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  entity_name: "Gymshark"
  limit: 50
```
Returns: entities that co-occur with Gymshark in content, ranked by frequency. This tells you what concepts, people, and brands appear alongside Gymshark in the ecosystem. Key structural insight.

### Person Entities
```
curaition_search_entities
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  entity_type: "person"
  limit: 200
```
Returns: all person entities detected across content. WARNING: This will include duplicates (same person across platforms) and generic labels ("Speaker", "Woman", "Creator"). You must deduplicate manually. See Phase 2 in SKILL.md.

## Batch 2: Deep Dives (run after reviewing Batch 1)

### Individual Athlete Co-occurrences
For each athlete you want to feature, run:
```
curaition_entity_cooccurrence
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  entity_name: "[Athlete Name]"
  limit: 20
```
This reveals what brands, concepts, and other athletes cluster around each individual. Essential for the "Three Signals" and "Athlete Spotlight" sections.

### Semantic Search for Stories
```
curaition_semantic_search
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  query: "[specific topic or theme]"
  limit: 10
```
Use this to find specific content related to themes identified in Batch 1. Run multiple searches in parallel for different stories. Each result includes a source URL — collect these for hyperlinking.

### Pattern Detection
```
curaition_detect_patterns
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  time_window: "7d" or "14d"
```
Returns structural patterns forming across the ecosystem. Good for the "Three Signals" section.

### Trend Analysis (only with sufficient historical data)
```
curaition_trend_analysis
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  recent_days: 7
  entity_type: "person"
```
IMPORTANT: Only use trend/momentum metrics if there is at least 30 days of historical data. If the system was recently set up, trend percentages are meaningless. State what you have, not what you wish you had.

## Batch 2.5: Contextual Verification (MANDATORY — run before editorial writing)

CurAItion co-occurrence data shows entities appearing together but cannot distinguish ownership from sponsorship from casual mention. Before writing any editorial analysis, verify the nature of key entity relationships.

**Why this exists:** A previous edition's Big Story was entirely wrong because "Alive App" (which co-occurs with multiple Gymshark athletes) was treated as a third-party platform. It's actually Whitney Simmons' own company. This batch prevents that class of error.

### Brand/App Ownership Checks
For every non-Gymshark brand that co-occurs with 3+ athletes:
```
WebSearch: "[brand name] founder" OR "[brand name] co-founder" OR "[brand name] CEO"
```
Run in parallel for all key brands. If an athlete OWNS the brand, that fundamentally changes the editorial angle.

### Athlete Business Venture Checks
For every athlete you plan to feature in Big Story or Athlete Spotlight:
```
WebSearch: "[athlete name] brand" OR "[athlete name] business" OR "[athlete name] app" OR "[athlete name] company"
```
Discover businesses they own that might appear as separate entities in CurAItion data.

### Event/Tour Context Checks
For athletes showing content spikes:
```
WebSearch: "[athlete name] tour 2026" OR "[event name] 2026"
```
Understand what's driving the spike before editorializing about "momentum."

### Output
Create a mental VERIFICATION_LOG before proceeding:
- Entity → Relationship Type (OWNS / SPONSORED_BY / COLLABORATES / APPEARS_WITH) → Evidence
- Any entity where the relationship type is OWNS requires a completely different editorial treatment

## Batch 3: Source URLs for Linking (CRITICAL)

Every reference in the digest must hyperlink to the original content. Use semantic search results to collect URLs:

```
curaition_semantic_search
  query: "[athlete name] [topic]"
  limit: 5
```

Run targeted searches for every story you plan to reference. Collect the `source_url` from each result. If `curaition_get_content` returns "Content not found" for specific content_ids (this has happened), fall back to the URLs available in semantic_search and list_content results.

### Content List (for volume and URL harvesting)
```
curaition_list_content
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  source_scope: "my_sources"
  limit: 50
  sort_by: "created_at"
  sort_order: "desc"
```
Use to supplement URL collection when semantic search doesn't surface a specific piece of content.

## Batch 4: Own-Channel Gap Analysis (Optional — Prompt 4)

Run this only if a Gymshark Owned Channels project is provisioned. See `_shared/gymshark-config.md` → Tier 1 Alt. If the project does not yet exist, skip this batch.

### Compare Owned vs Ecosystem Themes

```
curaition_compare
  dimension: "themes"
  project_id_a: "<gymshark_owned_channels_project_id>"
  project_id_b: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  created_after: "YYYY-MM-DD"   # digest window start
  created_before: "YYYY-MM-DD"  # digest window end
  tz: "Europe/London"
  min_significance: 1.28         # 80% CI — relax from 1.96 default for smaller projects
  min_weight: 0.3
  limit: 30
```

Returns `{ shared[], only_in_a[], only_in_b[], metadata, significance_method: "log-odds-ratio" }`. Each theme carries `{ theme, count_a, count_b, log_odds_ratio, z_score, direction }`.

**What to feature in the digest:**
- `only_in_b` with high |z| — themes the ecosystem leads on that the brand's feed ignores. Strongest Big Story candidates.
- `only_in_a` with high |z| — themes the brand pushes that the athletes don't echo. Drift signal.
- `shared` with large log_odds_ratio magnitude — themes both sides cover, but with a pronounced skew.

**What to ignore:**
- Any theme with raw count <5 on either side — statistical noise.
- |z| < 1.28 when both sides have <50 items total — underpowered comparison.

### Queueing a Discovered Source (Super-Admin Only)

When "Who to Watch" surfaces a creator the team wants to track, the super-admin operator can queue them for CurAItion ingestion:

```
curaition_queue_source_ingest
  platform: "instagram" | "tiktok" | "youtube"
  handle: "@creator_handle"       # youtube requires channel_id (UC...)
  organization_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
  window_days: 30
  priority: "normal"
```

Returns `{ job_id, estimated_cost_usd, estimated_items, estimated_completion_at }`. Poll:

```
curaition_get_ingest_status(job_id: "<returned_id>")
```

Status progression: `queued → apify_running → apify_complete → writing → completed`. Typical completion: 5-20 minutes for Instagram / TikTok with window_days=30.

**Scope:** Super-admin only. Regular digest operators should capture the recommendation in the digest and flag it to the CurAItion team for queueing — do not attempt the call as a non-super-admin operator (returns 403).

## Known Issues and Workarounds

1. **get_content "Content not found"**: Some content_ids from other tool results may not resolve in get_content. Use the source URLs from semantic_search and list_content as primary link sources instead.

2. **Entity name variants**: Athletes may appear under multiple names (e.g., "Cranon Worford" vs "Cranonnn" vs "cranonnn"). If an entity search returns 0 results, try the handle without the @ symbol, or the display name variant.

3. **Content count discrepancy**: list_content pagination may show fewer items than get_stats reports. Always use get_stats as the canonical total.

4. **Generic person entities**: The entity system detects many generic person references ("Speaker", "Woman in gym", "Creator"). These inflate the person count. Filter them out during deduplication.

5. **YouTube handle format**: `curaition_queue_source_ingest` for YouTube currently requires a channel_id (e.g., `UCxxxxxxxxxxxxxxxxxxxxxx`) — `@handle` style is not accepted. Find the channel_id via the channel's About page → "Share channel" → "Copy channel ID". Handle-to-channel-id resolution is a follow-up capability.
