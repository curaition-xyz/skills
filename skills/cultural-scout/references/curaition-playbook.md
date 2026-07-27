# CurAItion MCP Playbook (for the Cultural Scout)

How the CurAItion tools combine for daily **curiosity-led, library-only** discovery. Load
this when you need tool detail mid-run. **Every call assumes `source_scope: "library"`.**
The editorial rules live in `SKILL.md`; this is the tool reference. Remember the north star:
**curiosity over immediacy** — never lead with news/politics/markets/crypto.

## Scope mechanics (read once, internalise)

- `source_scope`: always **`"library"`** = CurAItion's curated, externally-safe corpus.
- **Why `library` and not `global`:** under a super-admin token, `global`/`my_sources`
  silently escalate to `all_orgs` (proven: `global` returned 18,790 client activewear items).
  `library` is **non-escalatable** — `effective_org_id:null`, forced non-super-admin at the DB
  layer, even for a super-admin token. Verified live 2026-06-19. NOTE: `external_safe` is a
  data-quality verdict, NOT proof of containment — it can read `false` on a leak-safe library
  when one curator/seed org dominates. The containment proof is `effective_org_id:null` +
  `source_scope:"library"`; treat `external_safe:false` as a quality note, never a gate.
- `project_id`: client investigation layers. Never pass it.
- Brand accounts (Gymshark, Nike, Red Bull) are intentionally library-flagged — signal, not
  contamination. Down-weight their `intent_class:"sale"` promo posts.

## The library, as measured (2026-07-27)

286 sources, 19,289 items, 19 domains.

> ⚠️ **These numbers are a snapshot for orientation only. Never score against them.** The
> scout's rarity weight is computed at run time from the live `domain_registry` returned by
> Canary A, precisely because this table goes stale fast — see the drift note below.

Eligible-roster domains: culture 10,141 · sport 3,704 · gaming 2,591 · fashion 2,523 ·
automotive 1,647 · music 1,585 · sustainability 836 · travel 732 · food 682 · science 677.

Excluded: social_commentary 7,778 · tech 4,608 · f1 2,322 · geopolitics 2,294 · generic 514 ·
crypto 304 · activewear 212 · endurance 138 · lifestyle 2,155. Reasons live in the SKILL.md
domain roster — that table, not this file, is the source of truth for eligibility.

### The corpus is NOT balanced any more — and that is why scoring must be dynamic

The previous revision of this file (2026-06-19) recorded *"well balanced
(`domain_balance 0.893`)"* and listed culture at 3,547. Since then:

| domain | 2026-06-19 | 2026-07-27 | growth |
|---|---|---|---|
| culture | 3,547 | 10,141 | **2.9×** |
| sport | 2,848 | 3,704 | 1.3× |
| food | 625 | 682 | 1.1× |
| science | 727 | 677 | 1.0× |

culture:food was **5.7:1**; it is now **14.9:1**. `culture` alone is ~40% of the eligible
pool. Any fixed weighting calibrated on the old distribution silently stops discriminating —
which is exactly what happened to the old flat "+1 breadth bonus".

**Two takeaways for anyone editing the scout:** compute domain weights from live counts, and
re-measure this table (don't trust it) whenever a selection starts looking repetitive.

### Standing judgements to revisit

`social_commentary` was marked "news/politics-heavy — treat with suspicion" when it held
**4,867** items. It now holds **7,778** and is the second-largest domain in the library,
described in the registry as *"memes, internet culture, viral trends, and social media
analysis"*. That judgement has not been re-examined against current material and is flagged
**REVIEW** in the SKILL.md roster.

Crypto (304 here, video-heavy) remains excluded as a lead topic on editorial grounds, not
volume.

## Server status (2026-06-19, post-hardening)
All tools green: `get_stats` (rollup-backed), `detect_patterns`, `semantic_search`
(embeddings fixed), `why_now_analysis` (web-grounded), `trend_analysis` (balanced **and**
per-domain; `domain_priorities` now library-scoped), `absence_scan`, `get_cited_themes`,
`get_content`, `list_content`, `list_sources`.

## CURRENT-AFFAIRS EXCLUSION (apply to every candidate)
Discard as a LEAD story anything whose core entities are: geopolitics / hard news / named
politicians (Iran, Russia, Ukraine, Israel, Trump, Putin, Zelenskyy, China-as-geopol, US/UK
party politics); markets/finance/crypto (Bitcoin, Ethereum, IPOs, funding, Wall Street);
big-tech-as-finance/lawsuit news (OpenAI/Anthropic funding/legal). Velocity tools surface
these constantly — that's expected; exclude them and keep looking.

## Tool catalogue by scout phase

### Phase 0 — Canaries
| Tool | Use | Assert |
|---|---|---|
| `curaition_get_stats` | containment proof + live domain registry | GATE: `source_scope=="library"` AND `effective_org_id==null`. Record `external_safe` as a quality note (do NOT gate on it). |
| `curaition_list_content` | athlete-leak probe | `search:"<athlete handle>"` → `total==0` |

### Phase 1 — Curiosity-led discovery (PRIMARY — lead with these)
| Tool | Use | Key params |
|---|---|---|
| `curaition_get_cited_themes` | evergreen, distinctive themes per domain — the richest curiosity source | `domain:<curiosity domain>, aggregate:true, min_weight:0.4` |
| `curaition_semantic_search` | chase a distinctive concept across domains (cross-domain bridge engine) | `query:<curious concept>, min_quality_score:0.5, include_citations:true` |
| `curaition_absence_scan` | what's gone quiet (often the better, quieter story) | `min_decline_rate:0.3` |

### Phase 1 — Velocity tools (SECONDARY — context only, never let them pick)
| Tool | Use | Key params |
|---|---|---|
| `curaition_detect_patterns` | structural/cultural patterns — **use 30d, not 7d**; DISCARD news/markets clusters; prefer `pattern_type` cultural_fatigue / professionalisation / technology_substrate / narrative_emergence | `time_window:"30d", min_confidence:0.5` |
| `curaition_trend_analysis` | momentum as a **tiebreaker only** | `recent_days:3` (NOT 1 — too thin), `baseline_days:30, ranking:"weighted"` |

### Phase 3 — Timeless-rhyme bridge (depth, NOT news escalation)
| Tool | Use | Key params |
|---|---|---|
| `curaition_semantic_search` | find 90d+ old content that rhymes with today's curiosity | `query`, `created_before:<90d ago>` |
| `curaition_get_pattern_history` | has this curious idea recurred before? | pattern ref |
| `curaition_why_now_analysis` | web-grounded "why now" (optional for evergreen picks) | `entity_name`, `domains:[...]` |

### Phase 4 — Verify / ground
| Tool | Use |
|---|---|
| `curaition_get_content` (`include_citations:true`) | citations + timestamped deep links + thumbnails |
| `WebSearch` | relationship sanity-check; confirm any real-world claim |

## Recipes (curiosity-first)

**Find the day's curiosity:** `get_cited_themes(domain:<food/science/travel/culture/…>,
aggregate:true)` across 3–4 broad domains → scan for the "I never knew that" theme (e.g.
"Unreasonable Hospitality", "the Dutch gave land back to the river", "McDonald's is a real-
estate empire"). This is the lead, not whatever `detect_patterns` says is fastest.

**Build a cross-domain bridge:** take the curious concept → `semantic_search` it across
domains → if it recurs in 2+ broad domains (food↔retail, travel↔engineering, science↔food),
that's the strong candidate.

**Build the timeless depth:** `semantic_search(query, created_before:<90d ago>)` → a rhyme
with older library content, OR a connection to a historical/timeless idea (ground via
WebSearch). Depth must be *timeless*, not a running news story.

**Screen out marketing & news:** drop `intent_class:"sale"` brand posts (−3) and anything on
the current-affairs exclusion list (−5/−4). Velocity is not a positive signal.

## Failure handling
- `get_cited_themes` without `theme_query` returns the domain's top aggregated themes — ideal
  for open-ended curiosity discovery.
- If `semantic_search` ever returns an embeddings error, retry once, then fall back to
  `list_content(search:...)` keyword search.
- If Phase 0 canaries fail, abort the whole run.
