# CurAItion MCP Playbook (for the Cultural Scout)

How the CurAItion tools combine for daily **curiosity-led, library-only** discovery. Load
this when you need tool detail mid-run. **Every call assumes `source_scope: "library"`.**
The editorial rules live in `SKILL.md`; this is the tool reference. Remember the north star:
**curiosity over immediacy** — never lead with news/politics/markets/crypto.

## Scope mechanics (read once, internalise)

- `source_scope`: always **`"library"`** = CurAItion's curated, externally-safe corpus.
- **Why `library` and not `global`:** under a super-admin token, `global`/`my_sources`
  silently escalate to `all_orgs` (proven: `global` returned 18,790 client activewear items).
  `library` is **non-escalatable** — `effective_org_id:null`, `external_safe:true`, even for a
  super-admin token. Verified live 2026-06-19.
- `project_id`: client investigation layers. Never pass it.
- Brand accounts (Gymshark, Nike, Red Bull) are intentionally library-flagged — signal, not
  contamination. Down-weight their `intent_class:"sale"` promo posts.

## The library, as measured (2026-06-19)

233 sources, ~14,587 items, all 17 domains, well balanced (`domain_balance 0.893`). The
curiosity-rich domains to favour: culture 3,547 · sport 2,848 · automotive 2,413 · fashion
2,041 · gaming 1,868 · music 1,440 · sustainability 975 · travel 741 · science 727 · food
625. Tech (4,631) and social_commentary (4,867) are large but **news/politics-heavy — treat
with suspicion** (most current-affairs pollution lives there). Crypto (1,018) is video-only
(0 articles) and excluded as a lead topic.

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
| `curaition_get_stats` | envelope safety + live domain registry | `effective_org_id==null` AND `external_safe==true` |
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
