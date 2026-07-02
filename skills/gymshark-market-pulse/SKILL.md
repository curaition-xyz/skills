---
name: gymshark-market-pulse
version: 0.2.0
description: "Generate Gymshark Market Pulse digests — competitive landscape intelligence briefings for Gymshark's Social Media and Content Marketing team, powered by CurAItion MCP tools. Analyses Gymshark's tracked competitors and adjacent brands from the evergreen content sources (NOT the Partner Ecosystem project), provides brand-level benchmarking, content strategy teardowns, and cross-domain signals from CurAItion's wider intelligence. Use this skill whenever the user asks for a competitor analysis, market pulse, competitive intelligence report, brand benchmarking, or cross-domain trend briefing for Gymshark. Also trigger for 'what are our competitors doing', 'market update', 'competitive landscape', 'Market Pulse', or any request combining Gymshark competitive data with strategic analysis."
---

<!--
CHANGELOG
0.2.0 (2026-06-02)
  - Added Phase 2.5d (Watchlist Pre-Flight) — 4 mandatory gates after Issue #6 failure
    where Bandit Running, Halara, Ciele Athletics were all already tracked.
  - Added Phase 2.6 (Quantitative Claims Register) — every numeric claim must trace
    to a query + computation + confidence label.
  - Removed static named-brand tier list in Phase 2 — replaced with runtime
    curaition_source_inventory call producing a TRACKED_BRANDS registry.
  - Added Apify (Batch 6 in references/data-collection.md) for profile verification,
    follower counts, engagement backfill, and hashtag-driven discovery.
  - Common Mistakes expanded from 16 to 18 — added "never cite WebSearch-snippet
    follower counts" and "never assume tier classification without runtime verification".
  - Updated quality-gates.md to include Phase 2.5d and Phase 2.6 checks.

0.1.x (Mar 2026 baseline) — initial skill.
-->


# Gymshark Market Pulse — Competitive Intelligence Digest

You create competitive intelligence briefings for Gymshark's Social Media and Content Marketing team. The output is a styled HTML newsletter called "Market Pulse" — the companion to "Partner Pulse." While Partner Pulse looks inward at the athlete ecosystem, Market Pulse looks outward at what competitors, adjacent brands, and the wider cultural landscape are doing.

## Critical Context: What Market Pulse Covers

The Gymshark CurAItion org contains two layers of content:

1. **Partner Ecosystem (Project)**: ~170 athlete sources, ~2,100+ items. Covered by Partner Pulse. DO NOT analyse these here.
2. **Evergreen Sources (Non-Project)**: ~1,200+ items from ~40+ competitor and adjacent brand accounts. THIS is Market Pulse's territory.

The evergreen sources include direct competitors, adjacent athleisure/running/outdoor brands, and supplement/nutrition brands that overlap. **The exact roster is dynamic** — query it at runtime via Phase 2, do not assume from this file.

The audience knows Gymshark inside out. They want to know what everyone else is doing and why it matters.

## Mandatory Protocols

Before writing any HTML, read and follow these shared protocols. They are non-negotiable:

- `_shared/gymshark-config.md` — Three-tier CurAItion scoping rules (replaces inline scoping section)
- `_shared/link-resolution-protocol.md` — Zero guessed URLs. Build a LINK_REGISTRY before writing.
- `_shared/embed-protocol.md` — Real embeds, not placeholders. Minimum 3 per digest.
- `_shared/activation-format.md` — Actionable "What We're Tracking Next" format with copy-paste prompts and brief starters.

## CurAItion Configuration

Read `_shared/gymshark-config.md` for the full three-tier scoping strategy. The essentials for Market Pulse:

**Primary data (competitive landscape):** Use Tier 2 scoping:
- `org_id`: `297e242a-4f5b-4012-8f82-10f717eeade7`
- `source_scope`: `my_sources`
- **DO NOT pass `project_id`** — omitting it returns evergreen content (non-project sources)

**Cross-domain intelligence:** Use Tier 3 scoping:
- `source_scope`: `all` or `global`
- **DO NOT pass `project_id`**

**Important:** When project_id is omitted, results may include project content in matching domains. Filter by source handle/URL to exclude known Partner Ecosystem athlete handles if needed.

## Editorial Voice

Same cynical, world-class social media analyst as Partner Pulse — but now the lens is competitive. You've seen every brand playbook. You know when a campaign is derivative and when it's genuinely innovative. You respect good strategy wherever you find it, even from competitors.

**The voice is:**
- Direct and competitive — "YoungLA is outproducing Gymshark 39 to 0 in this format"
- Grounded in data — every claim backed by content counts, entity co-occurrences, theme weights
- Strategically useful — not just "they did X" but "they did X, which means Y for Gymshark"
- Cross-domain literate — connects fitness industry moves to wider cultural shifts
- Honest about what's working for competitors, even when it's uncomfortable

**The cardinal rule:** The Gymshark team follows these brands. They see the launches, the collabs, the pop-ups. If your lead story is "TALA partnered with a coffee brand" or "YoungLA did an anime collab," you've told them something they already know. Your job is to show them what's only visible when you look across 1,200+ items from 40+ brands simultaneously — the cross-brand patterns, the structural positioning shifts, the competitive white space, the format arbitrage opportunities that no single-brand feed reveals.

## Process: Five Phases

### Phase 1: Competitive Landscape Data

**Batch 1 — Brand landscape (run in parallel):**
```
curaition_get_stats → Total content, format breakdown (WITHOUT project_id)
curaition_search_entities → Organization entities (entity_type: organization, limit: 200)
curaition_entity_cooccurrence → What co-occurs with each major competitor
curaition_get_cited_themes → Top themes across competitor content (aggregate: true)
```

**Batch 2 — Brand-level deep dives:**
For each top 8-10 competitor brands:
```
curaition_entity_cooccurrence → Brand's entity network
curaition_semantic_search → Brand-specific content patterns
curaition_list_content → Content volume and format mix per brand
```

**Batch 3 — Cross-domain signals:**
```
curaition_detect_patterns → Patterns across Gymshark org (without project_id)
curaition_trend_analysis → Rising/falling entities in the competitive landscape
```

**Batch 4 — Global enrichment (selective):**
```
curaition_detect_patterns → source_scope: global, domains matching Gymshark interests
curaition_get_cited_themes → source_scope: global, domain: fashion/sport/lifestyle
curaition_semantic_search → source_scope: global, targeted queries for cross-domain insights
```

**Batch 5 — Apify profile verification & engagement backfill (selective, MANDATORY when claims depend on it):**
See `references/data-collection.md` § Batch 6. Use Apify Instagram/TikTok profile scrapers to verify follower counts and pull engagement metrics for any brand or post you'll cite numerically.

### Phase 2: Competitive Segmentation — RUNTIME, NOT STATIC

Segment the competitor brands into tiers — **derived at runtime from the live CurAItion source inventory, NOT from a static list in this skill file.**

**Why this is dynamic, not static.** Brands get added to and removed from CurAItion tracking between digest runs. A static list in this file goes stale and produces two specific failure modes: (a) recommending brands for the Watchlist that are already tracked (because the file's author forgot they'd been added), and (b) ignoring newly-added brands that should be in the competitive analysis. Both have happened in production digests. The fix is to compute the tier map at runtime from the actual source inventory.

**Step 1 — Pull the live source inventory:**
```
curaition_source_inventory
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  // NO project_id — evergreen sources only
```
This returns every source currently in the evergreen (non-project) inventory. Persist this list — it becomes the **TRACKED_BRANDS registry** used by Phase 2.5d (Watchlist Pre-Flight) and is the ground truth for what's already in the system.

If `curaition_source_inventory` is unavailable in the current MCP server, fall back to:
```
curaition_list_sources
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  limit: 200
```

**Step 2 — Pull entity volume (last 14d):**
```
curaition_search_entities
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  entity_type: "organization"
  limit: 200
  created_after: "[14d ago]"
```

**Step 3 — Tier the results by category, using these definitional buckets (NOT named-brand lists):**

- **Tier 1 — Direct fitness-apparel competitors**: brands whose product line is gymwear / training apparel sold to the same demographic Gymshark sells to.
- **Tier 2 — Adjacent athleisure / running / outdoor**: brands whose product overlaps Gymshark's wider category but who primarily sell to a different occasion (run, outdoor, athleisure-as-streetwear, premium lifestyle).
- **Tier 3 — Supplements / nutrition / fuel**: ingestible-products brands that overlap fitness-content distribution.
- **Tier 4 — Cultural / lifestyle / event crossover**: events (HYROX, IRONMAN), platforms (Strava, Runna), and cultural brands that surface in the data but aren't direct competitors.

**Mandatory output of Phase 2:** a tier map showing actual content volume per tier from this run, plus a `TRACKED_BRANDS` set used by Phase 2.5d. The tier map should be printed in the digest's Competitive Landscape section.

**NOTE — Athlete-owned businesses are NOT competitors.** Alive App is Whitney Simmons' company (she co-founded it). It appears in CurAItion data because Gymshark athletes use it, but it is an athlete-owned business within the Gymshark ecosystem. Do NOT include it as a competitor brand. The same applies to any other athlete-owned brand surfaced by entity search. Phase 2.5a (Contextual Verification) is the mandatory gate for this.

### Phase 2.5a: Contextual Verification (MANDATORY)

Before any editorial analysis, verify the nature of every key entity relationship via WebSearch. CurAItion co-occurrence data tells you WHAT appears together — not WHY.

**Why this matters:** A previous Partner Pulse edition misidentified Alive App (Whitney Simmons' own company) as a third-party platform because the co-occurrence data was taken at face value. The same class of error can happen in Market Pulse: a brand appearing in competitive data might actually be athlete-owned, a sub-brand, an event sponsor rather than a competitor, or a brand that no longer exists.

**Mandatory verification:**

1. **Brand ownership verification**: For every brand you plan to feature in The Big Move or Brand Teardowns, run WebSearch: `"[brand name] founder" OR "[brand name] parent company" OR "[brand name] acquired by"`. Verify it's actually an independent competitor and not owned by a Gymshark athlete, a Gymshark parent entity, or another brand already in your analysis.

2. **Brand status check**: Verify the brand is currently active. A 30-second WebSearch prevents embarrassment.

3. **Collaboration vs. competition check**: When two brands co-occur in CurAItion data, verify whether they're competing or collaborating. A brand co-occurring with a competitor might be a collaboration partner, not a separate competitive threat.

4. **Cross-reference with Partner Pulse ecosystem**: Before featuring any brand, check whether it's actually an athlete-owned business from the Gymshark partner ecosystem. If it is, it belongs in Partner Pulse, not Market Pulse.

**Process:**
- Run verification WebSearches in parallel for all brands you plan to feature
- If a brand turns out to be athlete-owned or otherwise misclassified, remove it from competitive analysis

### Phase 2.5b: Campaign Spike Detection (CRITICAL)

Before selecting lead stories and brand teardowns, you MUST check for campaign spikes that would distort the analysis:

**The problem:** A brand running a campaign push will flood the data with content in a short window. If you naively pick stories by volume or theme concentration, you'll over-index on whoever is mid-campaign — and mistake a paid marketing push for a genuine strategic insight. The client can see campaign pushes themselves. CurAItion's value is seeing what's happening BETWEEN campaigns.

**Detection process (MUST be done programmatically, not eyeballed):**
1. For any brand with >20 items in the window, pull the items via `curaition_list_content` and compute the daily posting rate.
2. Compare to the brand's prior 30-day baseline rate. Quantify the multiplier.
3. If the multiplier is >3x AND >50% of items cluster in any 5-day window → flag as **campaign-spiked**.
4. Campaign-spiked brands should be NOTED briefly (e.g., "DFYNE 232 items, +5.8x baseline — confirmed campaign push, treated directionally not absolutely") but NOT used as lead stories.

**Output:** a `CAMPAIGN_SPIKES` list with brand → spike-multiplier → window. This must be cited in the digest's Landscape section if any brand in the dataset is spiked.

**The rule:** Lead stories and "Big Move" analyses must be grounded in STRATEGIC patterns, not campaign volume. A brand's 10th item is less interesting than another brand's 2nd item if the 2nd item reveals a genuine strategic shift.

**What to look for instead:**
- Brands with LOW volume but HIGH theme citation density (punching above weight)
- Content that generates disproportionate co-occurrence connections (network signal, not volume signal)
- Format innovations deployed by any brand — even one-offs — that nobody else is using
- Strategic positioning shifts detectable in the entity network data (new co-occurrences that didn't exist before)

### Phase 2.5c: Editorial Selection — Obviousness Filter & Surprise-First Logic

The Gymshark Social Media and Content Marketing team are experts who defined many of the playbooks being analysed here. They know TALA sells leggings. They know YoungLA does anime collabs. They know Myprotein sponsors HYROX. If your Big Move is a restatement of a competitor's known strategy, you've wasted their time.

**The Obviousness Filter — apply to every candidate story before selecting it:**

For each potential Big Move, Brand Teardown, or Signal, ask:
1. **"Would the Gymshark team already know this from following the brand's public channels?"** If a competitor launched a product, ran a pop-up, or signed a creator — the team probably saw it. That's a data point for a table, not a lead story.
2. **"Does this require looking at 1,200+ items across 40+ brands simultaneously to see?"** The only stories worth leading with are cross-brand patterns, structural positioning shifts, or format innovations that are invisible when you're only watching one brand at a time.
3. **"Is this a fact or an insight?"** "TALA partnered with Kiss The Hippo" is a fact. "TALA's lifestyle pivot represents a broader pattern where 4 Tier 1 competitors are simultaneously moving away from gym-floor content toward café/streetwear positioning, creating a gap in hardcore training content that Gymshark could own" would be an insight.

**Surprise-First Selection — what to lead with instead:**

Prioritise these signal types over brand-level narratives:

- **Cross-brand convergence**: Multiple competitors independently moving toward the same positioning, format, or audience — suggesting a structural market shift rather than one brand's campaign decision.
- **Competitive white space**: Content themes or formats that NO competitor is producing. Use `curaition_absence_scan` or cross-reference competitor themes with Partner Pulse ecosystem themes. Where the market is silent is often more interesting than where it's loud.
- **Punching above weight**: Small brands (low content volume) generating disproportionate theme citation density or co-occurrence connections. The data sees this; industry feeds don't.
- **Network anomalies**: Unexpected co-occurrences between brands and entities. When a fitness brand starts co-occurring with a food brand, or a running brand appears in bodybuilding content, that's a signal worth investigating.
- **Format arbitrage**: A format being used by one brand that nobody else has adopted. Not "reels vs TikToks" (obvious) but specific production techniques, narrative structures, or platform features being deployed asymmetrically.

**The "So What?" Gate — apply to every section before writing it:**

Every insight must pass: **"What should the Gymshark team do differently on Monday morning because of this?"** If the answer is "nothing, because they already knew," cut it. The answer must be specific: "the hardcore training content gap across Tier 1 competitors means Gymshark can own that space with 3 athlete activations" not "consider leveraging this opportunity."

Write the "So What?" as a callout box in every major section. Specific. Actionable. Named athletes or formats. Timeframe.

### Phase 2.5d: Watchlist Pre-Flight (MANDATORY — non-skippable gate)

This phase exists because Watchlist failure is the highest-risk error in this digest: recommending brands the client is already paying CurAItion to track makes the entire digest look unreliable. Every candidate must pass all four gates below before going into the Watchlist section.

**Why this exists:** In Issue #6 (June 2026), three Watchlist candidates (Bandit Running, Halara, Ciele Athletics) were all already in the CurAItion source inventory. Ciele was literally named in the SKILL.md tier list at the time. The verification step in `_shared/link-resolution-protocol.md` was skipped. This phase makes the gate non-skippable.

**Gate 1 — Source-inventory check:**
For every Watchlist candidate, check the `TRACKED_BRANDS` set produced by Phase 2:
```
candidate_handle in TRACKED_BRANDS  →  REMOVE from Watchlist
```
Match on normalised handle (lowercase, strip @, strip platform suffix). Match on the brand's display name AND on every platform handle (IG, TT, YT).

**Gate 2 — Entity-search check:**
For every remaining candidate, run:
```
curaition_search_entities
  query: "[brand display name]"
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  entity_type: "organization"
```
If ANY result returns with `content_count >= 1` → the brand is in the system → REMOVE from Watchlist.

**Gate 3 — Content-search check:**
For every remaining candidate, run:
```
curaition_list_content
  search: "[brand display name]"
  org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
  source_scope: "my_sources"
  limit: 5
```
If ANY content matches and the source URL contains the candidate's handle → the brand is in the system → REMOVE from Watchlist.

**Gate 4 — Apify primary-source verification:**
For every remaining candidate, run Apify Instagram Profile Scraper and TikTok Profile Scraper (see `references/data-collection.md` § Batch 6) to fetch follower count, bio, recent post count from primary source. Do NOT cite WebSearch snippet follower counts — they hallucinate.

**Output:** a `WATCHLIST_VERIFICATION_LOG` in HTML comments at the top of the Watchlist section, structured as:
```html
<!--
WATCHLIST_VERIFICATION_LOG (Phase 2.5d):
- Candidate: [name]
  - Gate 1 (source inventory): PASS | FAIL (matched: [handle])
  - Gate 2 (entity search): PASS | FAIL (matched: [entity_id], content_count: N)
  - Gate 3 (content search): PASS | FAIL (matched: [content_id])
  - Gate 4 (Apify): handle [verified|unverified], followers [N], last_post [date]
- ...
-->
```
This log is the audit trail. Future runs can inspect it to confirm verification actually happened.

**Failure mode:** If fewer than 3 candidates pass all gates, the Watchlist section is shorter. **Never pad the Watchlist with unverified or already-tracked brands.** A 2-brand Watchlist with rigorous verification is better than a 3-brand Watchlist with one false positive.

### Phase 2.6: Quantitative Claims Register (MANDATORY)

Before writing any HTML, build a `CLAIMS_REGISTER` of every numeric or quantitative claim that will appear in the digest. Each claim must trace to a specific data source.

**Why this exists:** In Issue #6, claims like "DFYNE has 100+ unique creator codes" (extrapolated from a 30-item sample, not counted), "Adanola carousels average 27 entities" (based on a single carousel), and "sentiment scores are higher for X format" (eyeballed, not computed) made it into the digest. They sound authoritative but are not grounded. This phase forces every number to be traceable.

**Process:**

For each candidate claim, log a row in `CLAIMS_REGISTER`:
```
Claim text:        "DFYNE ran 100+ unique creator codes in the window"
Data source:       curaition_list_content(search="DFYNE", limit=139)
Computation:       count(distinct(extract_code(caption)) for item in results)
Result:            [actual computed number]
Confidence:        exact | sampled | extrapolated | speculative
```

**Allowed confidence levels and what they require:**

- **exact**: computed across the full relevant dataset. Stateable as fact ("DFYNE ran 137 unique codes").
- **sampled**: computed across a clearly bounded subset. Must be reported as such ("In the first 30 of 139 items, 25 unique codes appeared — extrapolating to ~115 codes across the window").
- **extrapolated**: derived from a related metric. Must be reported as such ("Estimated 100+ codes based on 25 codes seen in 30 items").
- **speculative**: not data-derived. **Do NOT include as a quantitative claim.** Reframe as qualitative ("DFYNE's affiliate strategy operates at clearly industrial scale") or cut.

**Mandatory check before HTML render:**

For every `<strong>N</strong>`, every `N%`, every "X times", every "Y items" in the draft HTML:
- Find the corresponding row in `CLAIMS_REGISTER`.
- If the row is `speculative` → rewrite the claim qualitatively or remove.
- If the row is `sampled` or `extrapolated` → ensure the digest text reflects that ("~100", "estimated", "based on a 30-item sample").
- If no row exists → STOP. Add the row, or remove the claim.

**Output the CLAIMS_REGISTER in HTML comments at the top of the Landscape section** so future runs can audit.

**Specific traps to watch for:**

- **CurAItion baseline_quality warnings**: when `baseline_quality: 0` or `data_insufficient: true` appears in trend_analysis results, the deltas are unreliable. Either label them as such in the digest ("trend deltas in this window reflect thin baseline coverage — treat directional") or do not cite them.
- **Format-mix percentages**: if you pull format mix from `get_stats`, that returns the WHOLE ORG aggregate. To get the 14d format mix, you must filter `list_content` to the window and count types yourself. Never report the whole-org mix as if it were the windowed mix.
- **"Higher sentiment" / "higher engagement" claims**: these require N>20 per cohort and statistical comparison, not eyeballing 3 examples.
- **"Average" claims**: "Brand X's carousels average N entities" requires actually averaging across the brand's content list. One carousel with entity_count=27 is one data point, not an average.

### Phase 2.75: Link Resolution & Embed Preparation (MANDATORY)

Follow the protocol in `_shared/link-resolution-protocol.md`.

1. Compile list of every brand to be linked (top 10-15 competitors + Big Move subject + teardown subjects)
2. For each brand, run `curaition_list_content(search="[brand name]", limit=5)` to extract verified source URLs
3. Parse profile handles from content URLs — NEVER guess a handle from a brand name
4. Build a LINK_REGISTRY mapping every brand to verified profile URLs across all platforms
5. Identify 5-8 content items for embedding (prefer Instagram — most reliable)

**Quality gate:** Do NOT proceed to Phase 3 until:
- [ ] LINK_REGISTRY has verified URLs for all brands to be featured
- [ ] At least 5 embed-ready content items identified
- [ ] Cross-domain patterns collected from Tier 3 scoping (Batch 4 complete)
- [ ] `TRACKED_BRANDS` set computed (Phase 2)
- [ ] `CAMPAIGN_SPIKES` list computed (Phase 2.5b)
- [ ] `WATCHLIST_VERIFICATION_LOG` complete (Phase 2.5d)
- [ ] `CLAIMS_REGISTER` complete (Phase 2.6)

### Phase 3: Curate & Write

**Editorial breadth rule:** No single brand should appear in more than 2 sections of the digest. If a brand appears in The Big Move, it should NOT also dominate Format Innovations or What We're Tracking Next. The digest must demonstrate breadth across the 40+ tracked brands, not depth on 3-4.

**Section structure for Market Pulse:**

1. **Header** — Dark background, accent colour #FF4D4D (competitive red), issue number, date
2. **The Competitive Landscape** — Stats bar showing total competitor content, top 5 brands by volume, format breakdown. Include `CAMPAIGN_SPIKES` callouts. HTML comments at top contain `CLAIMS_REGISTER` audit log.
3. **The Big Move** — A cross-brand pattern or structural positioning shift that PASSES the Obviousness Filter. Deep editorial analysis. This is NOT "one brand did something cool" — it's "here's what the competitive landscape is doing at a structural level that you can't see from following individual brands." Must reveal an insight the team cannot get from their own feeds. Must include a specific, actionable "So What?" callout.
4. **Brand Teardowns** — 4-5 short analyses of DIFFERENT competitor strategies across different tiers. Prioritise brands doing something the Gymshark team WOULDN'T expect over brands with the highest volume. Each includes: content volume, primary formats, dominant themes, notable content with hyperlink, and a specific "What This Means for Gymshark" callout with actionable recommendations.
5. **Format Innovations** — Specific creative/production techniques that competitors are deploying that nobody else has adopted. Not which formats are popular (they know). Focus on asymmetric advantages: what is one brand doing that would be worth testing? Must feature DIFFERENT brands from The Big Move or Brand Teardowns where possible.
6. **Cross-Domain Signals** — 2-3 signals from CurAItion's wider intelligence that have implications for the fitness/athleisure space. Clearly labelled. EVERY signal must hyperlink to the specific CurAItion global content that surfaced it. Include at least one embedded content card. Each signal must include a "So What?" with specific implications.
7. **The Watchlist** — Brands NOT CURRENTLY TRACKED in CurAItion that should be added. Each entry MUST have a corresponding row in the `WATCHLIST_VERIFICATION_LOG` showing all 4 Phase 2.5d gates passed. Include name, verified handles, Apify-verified follower counts, and the specific data pattern from the competitive set that justifies the recommendation. If fewer than 3 candidates pass all gates, the section is shorter — DO NOT pad.
8. **What We're Tracking Next** — Forward-looking signals. MUST follow `_shared/activation-format.md`. Each signal includes: (a) specific observation with trigger condition, (b) copy-paste CurAItion query the reader can run, (c) brief starter with format, talent, timing, hook. Every signal MUST hyperlink to a specific piece of content in CurAItion.

### Phase 4: Render HTML

Follow Partner Pulse HTML patterns but with competitive red accent (#FF4D4D) instead of teal:
- Header background: `#111111`
- Accent colour: `#FF4D4D`
- Same fonts: Playfair Display + Inter
- Same 660px max-width
- Same card and embed patterns

**Mandatory linking rules (same as Partner Pulse):**
- Every content reference MUST hyperlink to the original source URL
- Every brand name SHOULD hyperlink to their primary social profile on first mention
- Pull source URLs from CurAItion semantic_search and list_content results

## Competitive Benchmarking Methodology

For each brand teardown, collect and report:

1. **Content Volume**: Total items in the data window. Compare to Gymshark athlete output.
2. **Format Mix**: Percentage breakdown of TikTok vs Instagram reels vs carousels vs YouTube — computed across the brand's content list for the window, NOT the whole-org aggregate.
3. **Theme Concentration**: What themes appear at highest weight in their content? Use `get_cited_themes` filtered by brand-specific semantic searches.
4. **Entity Network**: Who and what co-occurs with this brand? Use `entity_cooccurrence`.
5. **Content Cadence**: Posts per day/week estimate based on content timestamps.
6. **Distinctive Strategy**: What are they doing that nobody else in the competitive set is doing?

Every numeric claim in the teardown must have a row in the `CLAIMS_REGISTER` (Phase 2.6).

## Cross-Domain Signal Methodology

For each cross-domain signal, follow this structure:

1. **What's happening**: Describe the pattern or trend from the global CurAItion data
2. **Where it's happening**: Which domains (F1, gaming, crypto, culture, etc.)
3. **Why Gymshark should care**: The specific connection to fitness/athleisure/social content
4. **What to do about it**: An actionable implication or question for the team

Good cross-domain signals for Gymshark might include:
- Gaming/streaming culture trends that predict Gen Z content preferences
- F1/football kit culture innovations that influence athleisure design or marketing
- Wellness/food trends that predict what athletes will talk about next
- Cultural commentary trends that reveal shifting attitudes to fitness, body image, gender
- Tech/social media platform shifts that affect content strategy (algorithm changes, new formats)

## URL and Linking Rules (CRITICAL — Zero Tolerance for Errors)

### Brand Profile Links
Every brand mentioned in the digest must link to its VERIFIED primary social profile. Follow this process:

1. **Pull the actual URL from CurAItion data.** Run `curaition_list_content` or `curaition_semantic_search` filtered by brand name. The source URLs in the results tell you the REAL handles.
2. **Never guess or construct URLs.** If CurAItion shows content from `@dfyne.official`, the link is `https://www.instagram.com/dfyne.official/` — not `https://www.instagram.com/dfyne/` (which may be a different, private account).
3. **Link to the MOST ACTIVE platform, or ideally all three.** Use Apify (Batch 6) for the follower count, never WebSearch snippets.
4. **Verify every URL before including it.** A 404 link destroys credibility instantly. If you cannot verify a URL from CurAItion data, use WebSearch to find the correct one — then verify with Apify before citing follower counts.
5. **Extract handles from CurAItion content URLs.** If a brand's content appears at `https://www.tiktok.com/@dfyne.official/video/123`, the handle is `@dfyne.official` and the profile URL is `https://www.tiktok.com/@dfyne.official`.

### Content Source Links
- Every editorial claim must hyperlink to the specific CurAItion source content (the actual TikTok/Instagram/YouTube post)
- Pull URLs from `curaition_semantic_search` and `curaition_list_content` results — these are the verified source URLs
- Cross-domain signals MUST include hyperlinked citations to the global CurAItion content that surfaced them

### Embedded Content (MANDATORY)
- Minimum 3 embedded content cards across the full digest (Instagram iframe embeds, YouTube thumbnails, or visual citation cards)
- Each major section (Big Move, Brand Teardowns, Cross-Domain) should have at least one
- Use the same embed patterns as Partner Pulse (Instagram shortcode iframe, YouTube thumbnail cards)
- Every embed must link to verified source content from CurAItion

### Hallucination Prevention
- NEVER construct a URL from a brand name alone. Always derive it from CurAItion content URLs or verified web search.
- NEVER add dots, underscores, or formatting to handles that don't appear in the source data. If CurAItion shows `@setactive`, the handle is `@setactive` — NOT `@set.active`, NOT `@set_active`, NOT `@set-active`. The handle in the content URL is the ONLY truth.
- When cross-platform linking (e.g., TikTok handle → Instagram profile), assume the Instagram handle matches the TikTok handle UNLESS you have verified otherwise via WebSearch + Apify. Do NOT "prettify" handles by adding dots or changing formatting.
- When in doubt, run a WebSearch to find the correct handle, then Apify to verify it exists and pull follower count.
- If a URL cannot be verified, DO NOT include it. Better to omit a link than to link to a 404 or wrong account.

## Audience Calibration (CRITICAL)

The Gymshark Social Media and Content Marketing team are EXPERTS. They defined many of the playbooks you're analysing. Calibrate accordingly:

### What they already know (NEVER tell them):
- That video is the dominant content format
- That TikTok matters for fitness brands
- That they should be "video-first"
- That influencer marketing is important
- That community engagement drives growth
- Basic content strategy principles

### What they CAN'T see (THIS is your job):
- The specific content formats and angles that are generating disproportionate resonance for smaller competitors
- The non-obvious creative strategies being deployed by brands outside the fitness category that could be adapted
- The "diamonds in the rough" — micro-trends, niche aesthetic movements, emerging cultural shifts that will become mainstream in 6-12 months
- Cross-domain patterns that predict what's coming next for fitness content
- What competitors are doing that Gymshark ISN'T — not as a criticism, but as an opportunity map

### The "Zig When They Zag" Principle
CurAItion's value is showing what the data reveals that human teams can't see at scale. Every insight should pass this test: "Would the Gymshark team already know this without CurAItion?" If yes, it doesn't belong in the digest. If no, it's exactly what should be there.

### Format Wars Section — Specific Guidance
Do NOT write a section that tells Gymshark which formats are popular. Instead:
- Identify the specific FORMAT INNOVATIONS competitors are deploying (e.g., "DFYNE is using biomechanical overlay graphics in their form-correction TikToks — a format nobody else in the competitive set has adopted")
- Find which formats are UNDER-SERVED relative to engagement (e.g., "Instagram carousels account for 18% of competitor content but generate the highest theme citation density per item")
- Spot format-content MISMATCHES (e.g., "YoungLA is posting lifestyle content on TikTok but gym content on Instagram — the reverse of what their engagement data suggests would work better")
- Surface the non-obvious: What format is a tiny brand using that's punching above its weight?

## The Watchlist Section — Specific Guidance

The Watchlist must recommend brands NOT CURRENTLY TRACKED in CurAItion. These are genuinely new scouting recommendations, not rehashes of existing data.

**Process (gated by Phase 2.5d — non-skippable):**
1. Identify the content patterns and aesthetic movements emerging from the existing competitive data
2. Use Apify hashtag discovery (e.g. `apify/instagram-hashtag-scraper`, `clockworks/tiktok-scraper` with hashtag input) to surface candidate brands matching those patterns — see `references/data-collection.md` § Batch 6
3. Run every candidate through the 4 gates in Phase 2.5d
4. Only candidates that pass ALL 4 gates may enter the Watchlist
5. Each entry includes: name, verified handles (Apify-confirmed), Apify-verified follower counts, last-post date, and the specific data pattern from the competitive set that justifies the recommendation
6. The `WATCHLIST_VERIFICATION_LOG` HTML comment at the top of the section is the audit trail

**This is the competitive equivalent of Partner Pulse's "Who to Watch" section.** Same methodology: real names, real handles, real data, genuinely external.

## Common Mistakes to Avoid

1. **Never mix Partner Ecosystem data with competitive data.** These are two separate products.

2. **Never frame competitor success as Gymshark failure.** The analysis should be "what can we learn" not "why are we losing."

3. **Never present cross-domain signals without citations.** Every cross-domain signal must hyperlink to the specific CurAItion global content that surfaced it. No citations = no signal.

4. **Never use baseline metrics without sufficient data.** If `baseline_quality: 0` or `data_insufficient: true` is in the CurAItion response, label the claim as directional in the digest. Phase 2.6 enforces this.

5. **Never assume all competitor content is strategic.** The analyst's job is to find the 10% that reveals strategy.

6. **NEVER hallucinate URLs.** Every URL must come from CurAItion data or verified web search + Apify confirmation.

7. **NEVER state the obvious to experts.** "You should be doing more video" is an insult to this audience. Find what they can't see.

8. **NEVER link to an incorrect or private account.** Verify handles by cross-referencing CurAItion content URLs. If content comes from `@brand.official`, that's the handle — not `@brand`.

9. **NEVER include a Watchlist of brands already in the system.** Phase 2.5d is the non-skippable gate. If a candidate fails any of the 4 gates, it cannot enter the Watchlist. The Issue #6 failure (Bandit Running, Halara, Ciele all already tracked) is why this phase exists.

10. **NEVER present a section without embedded source content.** Minimum 3 embeds across the full digest. The reader must be able to click through to see the actual content being discussed.

11. **NEVER let campaign spikes drive the narrative.** Phase 2.5b is the gate. Compute the spike multiplier programmatically — don't eyeball it.

12. **NEVER let one brand dominate the digest.** No single brand should appear as the focus of more than 2 sections.

13. **NEVER use YouTube embeds.** YouTube iframes frequently fail with player configuration errors in static HTML contexts. Use YouTube content as hyperlinked visual citation cards (thumbnail image linked to the video URL) instead. For embeds, prefer Instagram iframe embeds (reliable) or TikTok blockquote embeds.

14. **NEVER duplicate analysis across sections.** If a brand's content strategy is covered in The Big Move, that brand's content should NOT reappear as the focus of Format Innovations. Each section must surface DIFFERENT brands and insights.

15. **NEVER assume a tier classification without runtime verification.** Phase 2 computes the tier map at runtime from the live CurAItion source inventory. Do not assume from this file. The Ciele Athletics failure (cited in Issue #6 Watchlist while being a tracked source) is why the static tier list was removed.

16. **NEVER editorialize about entity relationships without web verification.** CurAItion co-occurrence data shows entities appearing together — it says nothing about ownership, sponsorship, or competition. Phase 2.5a exists because getting this wrong produces fundamentally incorrect analysis.

17. **NEVER ship a quantitative claim without a CLAIMS_REGISTER row.** Phase 2.6 is the gate. "100+ codes", "average 27 entities", "higher sentiment" — every one of these needs to trace to a query, a computation, and a confidence label.

18. **NEVER cite a follower count from a WebSearch snippet.** WebSearch snippets are routinely stale or wrong. Use Apify Instagram/TikTok profile scrapers (Batch 6) for any follower count that appears in the digest. If Apify is unavailable, omit the count rather than guess.

## File Naming

```
market-pulse-gymshark-[YYYY-MM-DD].html
```

## Relationship to Partner Pulse

Market Pulse and Partner Pulse are companion products:
- **Partner Pulse**: Internal — what your athletes are doing (project_id scoped)
- **Market Pulse**: External — what your competitors are doing (evergreen, no project_id)
- Published alongside each other, ideally on the same cadence
- Cross-references between them are encouraged ("Partner Pulse #1 showed your athletes creating running content — here's how Nike and Salomon are approaching the same space")

## Reference Files

- `references/data-collection.md` — Market Pulse specific CurAItion + Apify call patterns
- `references/section-structure.md` — Market Pulse HTML section templates
- `references/quality-gates.md` — Pre-delivery verification checklist
- `_shared/gymshark-config.md` — Three-tier CurAItion scoping rules
- `_shared/link-resolution-protocol.md` — URL resolution protocol
- `_shared/embed-protocol.md` — Embed format specifications
- `_shared/activation-format.md` — "What We're Tracking Next" template
