# Quality Gates — Market Pulse Pre-Delivery Checklist

Run this checklist BEFORE delivering the HTML file. Every item must pass.

## Phase 2 Gates — Runtime Tier Map (NEW in v0.2.0)

- [ ] **TRACKED_BRANDS registry built at runtime** — `curaition_source_inventory` (or fallback `curaition_list_sources`) was called this run and the result was persisted as `TRACKED_BRANDS`. **Did NOT rely on a static brand list in SKILL.md.**
- [ ] **Tier map computed from live data** — Tier 1/2/3/4 buckets populated from the entity search + source inventory, not from a hardcoded list.
- [ ] **Tier map appears in the digest's Landscape section** — with actual item counts per tier from this window.

## Phase 2.5a Gates — Contextual Verification (before ANY editorial analysis)

- [ ] **Brand ownership verified** — For every brand to be featured, WebSearched `"[brand] founder"` to confirm it's an independent competitor, not athlete-owned or a Gymshark ecosystem entity. (Alive App incident: was listed as Tier 3 competitor, is actually Whitney Simmons' company.)
- [ ] **Brand status confirmed** — Every featured brand verified as currently active via WebSearch. No defunct, acquired, or pivoted brands presented as competitors.
- [ ] **Partner ecosystem cross-referenced** — No athlete-owned businesses from the Gymshark partner ecosystem appearing as competitors.

## Phase 2.5b Gates — Campaign Spike Detection

- [ ] **Campaign spikes computed programmatically** — For any brand with >20 items, daily posting rate computed and compared to baseline. Spike multiplier quantified, not eyeballed.
- [ ] **CAMPAIGN_SPIKES list cited in Landscape section** — If any brand is spiked, the digest discloses it (e.g., "DFYNE 232 items, +5.8x baseline — campaign push, treated directionally").
- [ ] **Spiked brands NOT used as lead stories** — Big Move and primary teardown subjects are NOT campaign-spiked brands.

## Phase 2.5c Gates — Obviousness Filter & Editorial Selection

- [ ] **Obviousness filter applied to Big Move** — The Big Move is NOT a single brand's campaign or known strategy. It's a cross-brand pattern or structural shift only visible at scale.
- [ ] **Every section passes "Would the team already know this?"** — Each lead story, teardown angle, and signal has been tested against what the Gymshark social team can see from their own feeds.
- [ ] **Every section has a specific "So What?" callout** — Not "consider leveraging this trend" but specific names, actions, and timing.
- [ ] **Surprise-first selection applied** — Lead stories prioritise convergence without coordination, competitive white space, punching-above-weight signals, network anomalies, and format arbitrage over volume-based selection.

## Phase 2.5d Gates — Watchlist Pre-Flight (NEW in v0.2.0 — non-skippable)

This phase exists because Issue #6 (June 2026) shipped a Watchlist where all 3 brands (Bandit Running, Halara, Ciele Athletics) were already tracked. Every candidate must pass ALL 4 gates.

- [ ] **Gate 1 — Source-inventory check** — Every candidate handle checked against `TRACKED_BRANDS` (from Phase 2). Matched candidates REMOVED.
- [ ] **Gate 2 — Entity-search check** — `curaition_search_entities(query="[candidate name]")` run for every remaining candidate. Any result with `content_count >= 1` = REMOVE.
- [ ] **Gate 3 — Content-search check** — `curaition_list_content(search="[candidate name]", limit=5)` run for every remaining candidate. Any source URL containing the candidate's handle = REMOVE.
- [ ] **Gate 4 — Apify primary-source verification** — Every surviving candidate verified via `apify/instagram-profile-scraper` and/or `clockworks/tiktok-scraper`. Follower count, last-post date, and verification status come from Apify, NOT WebSearch snippets.
- [ ] **WATCHLIST_VERIFICATION_LOG present** — HTML comment at the top of the Watchlist section showing all 4 gate results for every candidate. This is the audit trail.
- [ ] **No padding** — If fewer than 3 candidates pass all gates, the Watchlist section is shorter. Never add a candidate to fill space.

## Phase 2.6 Gates — Quantitative Claims Register (NEW in v0.2.0 — non-skippable)

This phase exists because Issue #6 shipped claims like "100+ unique DFYNE codes" (extrapolated from 30 of 139 items), "Adanola carousels average 27 entities" (one data point), and whole-org format-mix percentages cited as if they were windowed metrics.

- [ ] **CLAIMS_REGISTER built** — Every numeric claim that will appear in the digest has a row in CLAIMS_REGISTER with: claim text, data source query, computation method, result, confidence label (`exact`/`sampled`/`extrapolated`/`speculative`).
- [ ] **No `speculative` quantitative claims in the digest** — Speculative numbers reframed qualitatively or removed.
- [ ] **`sampled` and `extrapolated` claims explicitly labelled in digest text** — Use "~", "estimated", "based on N-item sample" wording. Reader can see the confidence level.
- [ ] **CurAItion `baseline_quality` warnings disclosed** — Any trend delta from a `baseline_quality: 0` or `data_insufficient: true` response is labelled as directional, not absolute.
- [ ] **Format-mix percentages are windowed, not whole-org** — If a format-mix percentage appears in the digest, it was computed from `curaition_list_content` filtered by `created_after`, NOT pulled from `curaition_get_stats` (which is whole-org aggregate).
- [ ] **"Average" claims actually average across the brand's full windowed content list** — One data point is not an average. Either compute the real average or drop the claim.
- [ ] **"Higher sentiment / engagement" comparisons have N ≥ 20 per cohort** — Or are explicitly framed as "in the sample we looked at" with the N stated.
- [ ] **CLAIMS_REGISTER persisted in the digest** — HTML comment at the top of the Landscape section. Audit trail.

## Phase 2.75 Gates (before writing HTML)

- [ ] **LINK_REGISTRY built** — Verified profile URLs for ALL brands to be featured. Source: CurAItion content URLs, NOT guessed from brand names. Handles match exactly what appears in content URLs (e.g., `@dfyne.official` not `@dfyne`).
- [ ] **Cross-domain data collected** — Batch 4 (Tier 3 scoping) completed. At least one `detect_patterns` or `get_cited_themes` call with `source_scope: "all"`.
- [ ] **Embed content identified** — At least 5 content items with source URLs suitable for embedding. Instagram shortcodes extracted.
- [ ] **Editorial breadth verified** — No single brand appears as the focus of more than 2 sections.
- [ ] **All Phase 2 / 2.5b / 2.5d / 2.6 registries are persisted** — TRACKED_BRANDS, CAMPAIGN_SPIKES, WATCHLIST_VERIFICATION_LOG, CLAIMS_REGISTER all built before writing HTML.

## HTML Content Gates (after writing HTML)

### Audit Trail Comments
- [ ] **CLAIMS_REGISTER HTML comment** is at the top of the Landscape section
- [ ] **WATCHLIST_VERIFICATION_LOG HTML comment** is at the top of the Watchlist section
- [ ] **CAMPAIGN_SPIKES** cited in Landscape section if any spikes detected

### Links
- [ ] Every `<a href="...">` points to a URL sourced from CurAItion data, verified WebSearch, or Apify
- [ ] Every brand name on first mention links to verified profile(s) — ideally all three platforms
- [ ] Handles match exactly what appears in CurAItion content URLs (no prettified or guessed variants)
- [ ] Every content reference links to the specific content URL, not just a profile
- [ ] No 404s — spot-check at least 5 links

### Embeds
- [ ] Minimum 3 real embeds across the digest
- [ ] Zero emoji placeholder divs
- [ ] Zero YouTube iframes (use visual cards instead)
- [ ] Each embed sourced from a verified CurAItion content URL

### The Big Move
- [ ] Subject is a cross-brand pattern, NOT a single brand mid-campaign
- [ ] Analysis reveals a STRATEGIC insight, not just volume or theme concentration
- [ ] Includes at least 1 real content embed
- [ ] Includes a specific "So What?" callout

### Brand Teardowns
- [ ] 4-5 DIFFERENT brands from The Big Move subject
- [ ] Each includes: content volume, format mix, dominant themes, notable content with hyperlink, "What This Means" callout
- [ ] At least 2 real content embeds across all teardowns
- [ ] All quantitative claims trace to CLAIMS_REGISTER rows

### Cross-Domain Signals
- [ ] 2-3 signals from Tier 3 (global) data
- [ ] Each signal hyperlinks to specific CurAItion content that surfaced it
- [ ] Each signal explains why Gymshark should care, with actionable implication

### The Watchlist
- [ ] WATCHLIST_VERIFICATION_LOG HTML comment present at top of section
- [ ] Every brand passed all 4 Phase 2.5d gates
- [ ] Every brand has Apify-verified handles and follower counts (NOT WebSearch snippets)
- [ ] Each recommendation grounded in a specific data pattern from the competitive set
- [ ] If fewer than 3 candidates passed, the section is shorter — NOT padded

### What We're Tracking Next
- [ ] Each signal follows three-part format: Signal → Prompt → Brief starter (per `../_shared/activation-format.md`)
- [ ] Each signal includes a copy-paste CurAItion query
- [ ] Each signal includes a brief starter with format, talent, timing, hook
- [ ] Zero passive "we'll continue to monitor" language

## Final Check
- [ ] Read the digest as a Gymshark social media manager. Would any section make you think "I already knew that"? If yes, rewrite it.
- [ ] Does the digest cover at least 8 different brands across all sections? If not, broaden.
- [ ] For every `<strong>N</strong>`, every `N%`, every "X times", every "Y items" in the HTML — does it trace to a CLAIMS_REGISTER row? If any number does NOT, stop and fix.
- [ ] Read the WATCHLIST_VERIFICATION_LOG. Are the gate results actually filled in, or are there placeholders? If placeholders, the verification didn't happen.
