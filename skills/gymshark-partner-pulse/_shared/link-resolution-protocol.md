# Link Resolution Protocol — Zero Guessed URLs

This protocol is MANDATORY for all Gymshark digest skills. Every hyperlink in the output HTML must be resolved from CurAItion data or verified via WebSearch. No URL may be constructed by guessing a handle from an entity name.

## Why This Exists

CurAItion entity names do not map 1:1 to social media handles. "Chris Williamson" the Modern Wisdom podcast host is `@ChrisWillx` on YouTube — not `@ChrisWilliamson` (which is a freelance filmmaker). Guessing handles produces wrong links that destroy credibility with the audience.

## The LINK_REGISTRY

Before writing ANY HTML, build a LINK_REGISTRY — a lookup table mapping every entity you plan to reference to its verified profile URLs.

### Step 1: Identify all entities to be linked

From your Batch 1 data collection, compile a list of every person and organisation that will appear in the digest. For Partner Pulse, this is typically 20-30 entities (top-20 roster + spotlight + signal subjects). For Market Pulse, this is 10-15 brands.

### Step 2: Resolve each entity via CurAItion content URLs

For each entity, run:
```
curaition_semantic_search(
  query="[entity name]",
  org_id="297e242a-4f5b-4012-8f82-10f717eeade7",
  project_id="83472bde-a285-42cd-bba0-f7b92728e728",  // omit for Market Pulse
  source_scope="my_sources",
  limit=5,
  response_format="json"
)
```

From the results, extract the `url` or `source_url` field. Parse the profile handle:
- `https://www.tiktok.com/@fitnessnojo/video/123` → handle: `@fitnessnojo`, profile: `https://www.tiktok.com/@fitnessnojo`
- `https://www.youtube.com/watch?v=abc&channel=ChrisWillx` → handle: `@ChrisWillx`, profile: `https://www.youtube.com/@ChrisWillx`
- `https://www.instagram.com/p/ABC123/` → requires additional step (see below)

For Instagram, the post URL doesn't contain the handle. Use `curaition_list_content` with `search="[entity name]"` and check the source metadata, OR run a targeted WebSearch: `"[entity name] Gymshark Instagram"`.

### Step 3: Batch resolution (efficiency)

To avoid N+1 queries, use `curaition_list_content` with `limit=100` sorted by `created_at desc` and extract unique base URLs across all results. This gives you most profile links in 1-2 calls.

Alternatively, if the MCP server supports `curaition_batch_resolve_links` (see Phase 2 PRD), use that for a single-call resolution.

### Step 4: Fill gaps via WebSearch

For any entity without a CurAItion-sourced URL, run:
```
WebSearch("[entity name] [platform] official account")
```

Verify the result is the correct person/brand (not a namesake).

### Step 5: Build the registry

Format:
```json
{
  "Chris Williamson": {
    "youtube": "https://www.youtube.com/@ChrisWillx",
    "instagram": "https://www.instagram.com/chriswillx/"
  },
  "Whitney Simmons": {
    "youtube": "https://www.youtube.com/@whitneysimmons",
    "instagram": "https://www.instagram.com/whitneyysimmons/",
    "tiktok": "https://www.tiktok.com/@whitneysimmons"
  }
}
```

### Step 6: Validate before writing HTML

Before writing any `<a href="...">` tag:
1. Look up the entity in the LINK_REGISTRY
2. If found → use the registry URL
3. If NOT found → STOP. Resolve the link before proceeding.
4. NEVER fall back to constructing a URL from the entity name

## Content Source Links

Every editorial claim that references specific content must hyperlink to the original post/video. These URLs come from:
- `curaition_semantic_search` results → `url` field
- `curaition_list_content` results → `url` field
- `curaition_get_content` results → `url` field

If you reference "Kyanfitt's running-as-therapy TikTok," the href must point to the actual TikTok video URL from CurAItion — not a general profile link.

## Cross-Reference Rule for Creator Scouting

Before including ANY creator in "Who to Watch" or "The Watchlist":

1. Run: `curaition_search_entities(query="[creator name]", org_id=..., project_id=..., source_scope="my_sources")`
2. If entity appears → they are ALREADY in the ecosystem → DO NOT include
3. Run: `curaition_entity_cooccurrence(entity_name="[creator name]", org_id=..., project_id=...)`
4. If they co-occur with Gymshark → they are likely already affiliated → VERIFY via WebSearch before including
5. Only include creators confirmed to be genuinely external to the current ecosystem
