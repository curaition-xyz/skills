# Data Collection Reference — Market Pulse CurAItion + Apify Tool Call Patterns

All CurAItion calls must include:
- `org_id`: `297e242a-4f5b-4012-8f82-10f717eeade7`
- `source_scope`: `my_sources` (for competitor data)
- **DO NOT pass `project_id`** — this returns evergreen/non-project content

See `../_shared/gymshark-config.md` for the full three-tier scoping strategy.

## Batch 1: Competitive Landscape Overview (run in parallel)

### Content Stats
```
curaition_get_stats
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  // NO project_id
```
Returns: total content items, format breakdown, domain distribution, source count.

**Warning:** the format breakdown returned here is the WHOLE-ORG aggregate. To get the windowed (e.g. last 14d) format mix, use Batch 5 below — `list_content` with `created_after` filter — and compute the mix yourself.

### Organization Entities (Brands)
```
curaition_search_entities
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  entity_type: "organization"
  limit: 200
  created_after: "[14d ago]"
```
Returns: brand/organisation entities with content counts within the window.

### Source Inventory (for TRACKED_BRANDS registry — Phase 2)
```
curaition_source_inventory
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
```
Returns: every evergreen (non-project) source currently in CurAItion. **This is the ground truth for Phase 2.5d Watchlist Pre-Flight.** Persist the result as `TRACKED_BRANDS` and check every Watchlist candidate against it.

Fallback if `curaition_source_inventory` is unavailable:
```
curaition_list_sources
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  limit: 200
```

### Cited Themes (Competitor Content)
```
curaition_get_cited_themes
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  aggregate: true
  min_weight: 0.5
  limit: 30
  created_after: "[14d ago]"
```

### Gymshark Co-occurrences in Competitive Landscape
```
curaition_entity_cooccurrence
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  entity_name: "Gymshark"
  limit: 50
  created_after: "[14d ago]"
```

## Batch 2: Brand-Level Deep Dives (run after Batch 1 review)

For each of the top 8-10 competitor brands:

### Brand Co-occurrences
```
curaition_entity_cooccurrence
  entity_name: "[Brand Name]"
  limit: 20
  created_after: "[14d ago]"
```

### Brand Content List (for content count, format mix, posting cadence)
```
curaition_list_content
  search: "[Brand Name]"
  limit: 100
  created_after: "[14d ago]"
```
**Use this output to compute (programmatically, not by eyeballing):**
- Exact item count for the brand in the window
- Daily posting rate (count / 14)
- Format mix (count by `content_type`)
- Posting time-of-day distribution
- For brands with creator-code strategies: extract unique discount codes from captions and count

These computed values are inputs to the `CLAIMS_REGISTER` (Phase 2.6). Do NOT cite numbers from a sample of 20-30 items as if they were full-window counts.

### Brand Semantic Search
```
curaition_semantic_search
  query: "[Brand name] content strategy campaign"
  limit: 10
```

## Batch 3: Competitive Patterns & Trends

### Pattern Detection
```
curaition_detect_patterns
  source_scope: "my_sources"
  time_window: "14d"
```

### Trend Analysis
```
curaition_trend_analysis
  source_scope: "my_sources"
  recent_days: 14
  baseline_days: 30
  entity_type: "organization"
```

**Warning:** check `baseline_quality` and `data_insufficient` fields in the response. If `baseline_quality: 0` or `data_insufficient: true`, label the deltas as **directional, not absolute** in the digest. Phase 2.6 enforces this — quantitative trend claims with unreliable baselines must be flagged in the CLAIMS_REGISTER as `extrapolated` or `speculative`.

## Batch 4: Cross-Domain Intelligence (Tier 3 — MANDATORY)

These calls use `source_scope: "all"` to access CurAItion's global baseline.

### Cross-Domain Patterns
```
curaition_detect_patterns
  source_scope: "all"
  time_window: "14d"
```

### Cross-Domain Themes
```
curaition_get_cited_themes
  source_scope: "all"
  aggregate: true
  min_weight: 0.6
  limit: 20
```

### Targeted Cross-Domain Searches
Run 2-3 semantic searches across global data for topics relevant to Gymshark:
```
curaition_semantic_search
  source_scope: "all"
  query: "[topic from competitive data that has cross-domain implications]"
  limit: 10
```

## Batch 5: Source URLs for Linking and Embedding

```
curaition_list_content
  source_scope: "my_sources"
  limit: 100
  created_after: "[14d ago]"
  // sorted by created_at desc
```
Use to harvest source URLs for the LINK_REGISTRY and embed preparation.

## Batch 6: Apify Profile Verification & Discovery (MANDATORY for Watchlist + follower counts)

Apify is the primary-source layer for **profile metadata, follower counts, engagement metrics, and new-account discovery**. CurAItion is the source of truth for *what content has been ingested into our tracking*. Apify is the source of truth for *what exists on Instagram and TikTok right now*. Both are needed.

### When to use Apify (not optional):

| Use case | Apify Actor | When |
|---|---|---|
| Verify Watchlist candidate handle exists & pull follower count | `apify/instagram-profile-scraper`, `clockworks/tiktok-scraper` | Phase 2.5d Gate 4 |
| Verify follower count for any brand cited numerically in the digest | same actors | Phase 2.6 CLAIMS_REGISTER |
| Backfill engagement metrics for posts cited as evidence (likes, views, saves, comments) | `clockworks/tiktok-scraper`, `apify/instagram-post-scraper` | When CurAItion `engagement: null` |
| Discover new accounts in fitness/athleisure not yet in CurAItion | `apify/instagram-hashtag-scraper`, `clockworks/tiktok-scraper` (hashtag mode) | Phase 2.5d Watchlist candidate generation |
| Verify a TikTok handle exists when only Instagram is in CurAItion | `clockworks/tiktok-scraper` (profile mode) | LINK_REGISTRY construction |

### Apify call patterns

**Profile verification (Instagram):**
```
call_actor("apify/instagram-profile-scraper", input={
  "usernames": ["banditrunning", "halara_official", "cieleathletics"]
})
```
Returns per-username: `followersCount`, `followsCount`, `postsCount`, `biography`, `verified`, `private`, `profilePicUrl`, last 12 posts. This is the ONLY acceptable source for follower counts cited in the digest.

**Profile verification (TikTok):**
```
call_actor("clockworks/tiktok-scraper", input={
  "profiles": ["banditrunning", "halara_official", "cieleathletics"],
  "resultsPerPage": 1
})
```
Returns `fans`, `followingCount`, `videoCount`, `verified`, recent video metadata.

**Post engagement backfill (when CurAItion engagement is null):**
```
call_actor("apify/instagram-post-scraper", input={
  "directUrls": [
    "https://www.instagram.com/p/DY7tfPRiA8z/",
    "https://www.instagram.com/p/DY7a7PqDJZz/"
  ]
})
```
Returns likes, views, comments, saves, shares per post.

**Hashtag discovery (for Watchlist candidate generation):**
```
call_actor("apify/instagram-hashtag-scraper", input={
  "hashtags": ["hyroxapparel", "runclub", "gymtok", "femaleathleisure"],
  "resultsLimit": 50
})
```
Returns recent top posts per hashtag. Extract unique account handles. Filter against `TRACKED_BRANDS`. Remaining handles are Watchlist candidates — feed them into Phase 2.5d gates.

```
call_actor("clockworks/tiktok-scraper", input={
  "hashtags": ["hyroxapparel", "runclub", "gymtok"],
  "resultsPerPage": 100
})
```
Same pattern on TikTok.

### Apify rate-limit and cost notes

- Profile scrapers cost ~$0.01 per profile. Budget for 10-20 lookups per digest is trivial.
- Hashtag scrapers cost more per run (~$0.50 per hashtag, 50 results). Limit to 3-5 hashtags per digest in the discovery phase.
- Cache results in HTML comments at the top of the relevant section so they can be audited and rerunning the same digest doesn't duplicate spend.
- Verify exact actor names and pricing via the Apify MCP `search-actors` / `fetch-actor-details` before relying on a specific actor — names occasionally change.

### What NOT to use Apify for in this digest

- Do NOT use Apify to replace CurAItion source ingestion. CurAItion is the ongoing tracker; Apify is the point-in-time verifier.
- Do NOT scrape full content libraries via Apify — that's an ingestion task, not a digest task. If a brand should be tracked continuously, the answer is to add it to CurAItion (and let the Watchlist recommendation drive that).
- Do NOT cite an Apify-discovered post as a digest source unless you also link to its primary URL. Apify gives you the data; the digest's hyperlinks must point at the original Instagram/TikTok URL.

## Summary: Which tool for which job

| Question | Tool |
|---|---|
| What's in our competitive tracking? | `curaition_source_inventory` / `curaition_list_sources` |
| What did our tracked brands post in the last 14d? | `curaition_list_content`, `curaition_search_entities` |
| What's the structural pattern across the dataset? | `curaition_detect_patterns`, `curaition_entity_cooccurrence`, `curaition_get_cited_themes` |
| Is this Watchlist candidate already tracked? | `curaition_search_entities` + `curaition_list_content` (gates 2-3 of Phase 2.5d) |
| Does this candidate's handle exist? How many followers? | Apify profile scraper (gate 4 of Phase 2.5d) |
| What are the engagement numbers for this specific post? | Apify post scraper (if CurAItion engagement is null) |
| What new accounts are emerging in [hashtag]? | Apify hashtag scraper |
