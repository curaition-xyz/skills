# Gymshark CurAItion Configuration

This file is the single source of truth for CurAItion scoping across all Gymshark digest skills. Every CurAItion tool call in every Gymshark digest MUST use one of these three tiers.

## Organisation

- **org_id:** `297e242a-4f5b-4012-8f82-10f717eeade7`
- **Organisation:** Gymshark (CurAItion)

## Three-Tier Scoping (MANDATORY)

### Tier 1: Gymshark Creator Dashboard (the roster — athletes AND creators)

```
org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
project_id: "0bdbc3d2-1360-4430-b634-dea95841c9ba"
source_scope: "my_sources"
```

**Use for:** Partner Pulse roster data, content analysis, theme extraction, co-occurrences. This is Gymshark's SINGLE roster project — signed athletes, ambassadors and discovery-pool creators all live here. It is not a discovery pool sitting next to a roster; treat the mix as a property of the corpus and say which kind of creator a story is about.

**Returns:** 1,560 source rows across TikTok, Instagram and YouTube (~39,000 content items). That is a **channel** count, not a person count — most creators hold two or three rows, one per platform. Distinct handles number roughly **1,172**, which is the closest cheap proxy for headcount; there is no canonical-person field on a source, so any "N creators" claim has to be deduped by hand (see Phase 2 in SKILL.md).

**All 1,560 rows are live as of 2026-08-25.** The 124 rows carried over from `Partner Ecosystem` had been PAUSED since 2026-07-30 — archiving that project cascaded a pause onto every source exclusive to it (by design, CUR-1018). Once they were linked here that precondition no longer held, so 123 were resumed; the 1 exception is a source separately flagged `NEEDS_REVIEW` for no-yield. Content published between 2026-07-30 and 2026-08-25 was never ingested for those channels, so **expect a ~4-week hole in their history** — a creator can look quiet in that window and not have been. Check `min(published_at)` after 08-25 before calling a lull real.

**Domain scoping caveat.** This project's `domains` array is `["activewear", "lifestyle"]` (recomputed from its sources on 2026-08-25; it had been empty). A project-scoped CurAItion read returns project-source content **plus evergreen content in matching domains** — currently ~379 non-project items in those two domains. That is small against ~39,000 roster items, but it is not roster content. If a Tier 1 result names a source you cannot find in `curaition_list_sources(project_id=...)`, that is why: it came in through the domain match, and it does not belong in a roster claim.

> **Changed 2026-08-25 (superseded the same day — read the second note).** Tier 1
> previously pointed at `Partner Ecosystem`
> (`83472bde-a285-42cd-bba0-f7b92728e728`). Every Partner Pulse edition before
> this date was scoped to that project.
>
> **Correction, 2026-08-25 (evening).** The first version of this note said the
> archived project had "170 sources, none of them still syncing". That was
> wrong, and it was wrong in a way worth recording: 46 of its 170 rows were
> ALSO linked to this Creator Dashboard project, and those 46 were ACTIVE and
> syncing hourly — the archived project's apparent liveness was entirely
> borrowed from Creator Dashboard membership. The remaining 124 rows were
> PAUSED, stopping at 2026-07-30. A `last_sync desc` page of the first 15 rows
> showed only the live 46 and read as "all of them are current"; the sort order
> hid the split. Check a status histogram, never the head of a sorted page.
>
> The same note claimed 129 of the 170 rows were duplicates of people already
> here, leaving a real gap of ~16-18. At the CHANNEL level that was also wrong:
> 124 rows were genuinely unlinked, and NONE of them was a same-platform
> duplicate of an existing row (`handle × platform` overlap was exactly zero).
> 48 matched an existing handle on a *different* platform — the same person's
> other channel, e.g. Whitney Simmons, whose Instagram row was here while her
> TikTok and YouTube rows were not. 73 matched nothing at all.
>
> **Resolved 2026-08-25.** All 124 were linked into this project. Partner
> Ecosystem is now fully contained here and this is Gymshark's SINGLE roster
> project — there is no second roster to consult, and nothing should be scoped
> to `83472bde` again.

---

### Tier 1 Alt: Gymshark Owned Channels (optional — for own-channel audits)

```
org_id: "297e242a-4f5b-4012-8f82-10f717eeade7"
project_id: "<gymshark_owned_channels_project_id>"   # set up separately; not yet provisioned
source_scope: "my_sources"
```

**Use for:** `curaition_compare(dimension="themes", project_id_a=<owned>, project_id_b=<roster>)` — Prompt 4 "audit the brand's own channels against the partner ecosystem." Surfaces which themes the brand under/over-indexes on its owned feed vs the athletes.

**Setup path:** The owned-channels project is created separately via the admin dashboard (Sources → Add Project) or by a super-admin operator using `curaition_queue_source_ingest(platform, handle, project_id)`. Until that project is provisioned, skip the own-channel section of the digest — do not fabricate a comparison from a single-tier read.

**When to skip:** If the owned-channels project does not exist or has fewer than 20 recent content items, the log-odds-ratio comparison will be statistically noisy. State the gap exists in the digest narrative; do not quote a metric.

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
| Partner Pulse — Own-Channel Gap (Prompt 4, optional) | Tier 1 + Tier 1 Alt via `curaition_compare` |
| Market Pulse — Competitive Landscape, Brand Teardowns | Tier 2 |
| Market Pulse — Cross-Domain Signals | Tier 3 |
| Market Pulse — The Watchlist (verify existing tracking) | Tier 2 |
| Either Digest — "What We're Watching Next" prompts | All tiers (label which) |
