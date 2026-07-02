# Click-Bait Scout Playbook (WebSearch-first)

How to run the live-web fan-out, score virality, and (optionally) cross-reference CurAItion
for depth. The editorial rules live in `SKILL.md`; this is the tool reference. North star:
**immediacy + headline-grab over curiosity — but corroborate before you amplify.** Every
primary fact comes from a real web result; nothing is invented.

## Source-of-truth split

- **WebSearch / web_fetch = PRIMARY.** Discovery and all 24h citations. `WebSearch` to find
  what's spiking; `mcp__workspace__web_fetch` to open the article, confirm the timestamp is
  inside the window, and lift exact quotes/figures. If `web_fetch` returns a JS-shell with no
  body, the page is client-rendered — escalate to the Claude-in-Chrome tools
  (`navigate` → `get_page_text`); do NOT guess from the shell or fetch by other means.
- **CurAItion = OPTIONAL cross-reference.** Only to answer "do we already track this / what's
  the slow build behind the spike?". Never a blocker; the run completes without it.

## The 24h window

Get the real current date/time from the environment first. Compute `window_start = now − 24h`
(`fresh_hours`), absolute max `now − 48h` (`fresh_hours_max`) and ONLY for a story still
visibly accelerating. A published_at outside the window = stale = drop (−3). Resurfaced old
stories masquerading as new are the classic trap — check the original publish date, not just
the latest aggregator repost.

## Phase 1 — Live web fan-out (PRIMARY, batch the searches)

Run a wide spread of `WebSearch` calls in a single batch. Mix three query types:

1. **Generic "what's hot" probes:** `"trending today <date>"`, `"what's going viral right
   now"`, `"top story today"`, `"most shared article today"`, `"trending on X today"`,
   `"Reddit front page today"`.
2. **Per-domain breaking probes** (cover the whole map — this scout excludes nothing):
   politics · world/geopolitics · business & markets · crypto · tech · AI · sport ·
   football/F1 · entertainment/celebrity · music · gaming · internet culture / memes ·
   science · health. Query e.g. `"<domain> news today"`, `"<domain> breaking <date>"`.
3. **Entity confirmation probes** once a candidate emerges: the specific name + "today" /
   "latest" to find corroborating outlets and the exact figures.

Then `web_fetch` the 3–6 strongest hits. Confirm timestamp ∈ window; capture outlet, headline,
publish time, the key quote/number, and the URL for citations.

## Phase 3 — CurAItion cross-reference recipes (OPTIONAL depth)

If CurAItion is up, these add a take competitors don't have. **Every call passes
`source_scope: "library"`; never pass `project_id` or a client `org_id`.**

| Tool | Use | Key params |
|---|---|---|
| `curaition_semantic_search` | does the library already see these entities/this theme? | `query:<entity/theme>, source_scope:"library", include_citations:true` |
| `curaition_get_cited_themes` | what slow themes sit behind the hot story? | `domain:<domain>, source_scope:"library", aggregate:true` |
| `curaition_why_now_analysis` | web-grounded "why is this spiking now" | `entity_name:<X>, source_scope:"library"` |
| `curaition_detect_patterns` | is today's spike part of a longer structural pattern? | `time_window:"30d", source_scope:"library"` |

Put what you find in `the_depth_90d` (with a `connection_type`, usually `slow-build` or
`escalation`) and `curaition_crossref`. If CurAItion has nothing, set
`curaition_crossref.library_sees_it:false` and move on. If CurAItion errors/times out, omit
the block, set `scope_verification.curaition_used:false`, and proceed — the candidate is still
valid on web evidence alone.

### Why `library` scope even here
Under a super-admin token, `global`/`my_sources` silently escalate to `all_orgs` and pull in
client content; `library` is the only non-escalatable, externally-safe view
(`effective_org_id:null`, `external_safe:true`). Marketing output must never touch client data,
so if you call CurAItion at all, it's `library` only.

## Phase 4 — Corroboration & credibility tiers

The selected pick needs **2+ independent, reputable outlets** inside the window.

**Source tiers (for judging corroboration & credibility):**
- **Tier 1 — wires & established outlets:** Reuters, AP, AFP, Bloomberg, FT, BBC, Guardian,
  NYT, WaPo, and domain-authoritative trade press. Two Tier-1s on the same claim = solid.
- **Tier 2 — reputable digital/specialist:** established vertical outlets (e.g. The Verge,
  ESPN, Billboard, CoinDesk). Good corroboration, ideally paired with a Tier-1.
- **Tier 3 — social / aggregators / blogs / anonymous:** X posts, Reddit, Telegram,
  screenshots, single-author blogs. **Signal of spread, NOT proof of fact.** Use them to gauge
  virality; never as the sole basis for a claim.

Rules of thumb:
- Two Tier-3 sources ≠ corroboration. Need independent Tier-1/2 confirmation.
- If only Tier-3 carries it → `corroboration:"single-source"` or `"unverified"`, flag, don't
  select. The *spread itself* can be a media-criticism angle, attributed as such.
- If Tier-1 outlets are actively debunking it → it's a hoax; the debunk is the story, the claim
  is not.

## Virality scoring how-to

- **virality_signal (0–3):** 0 = isolated; 1 = a few outlets; 2 = broad pickup across outlets
  OR strong single-platform surge; 3 = wall-to-wall across outlets AND trending on 2+
  platforms.
- **headline_grab (0–3):** 0 = flat/worthy; 1 = mild interest; 2 = clear hook (number,
  reversal, conflict); 3 = irresistible "wait, what?" that screenshots itself.
- **source_velocity (string):** describe the spread concretely, e.g. "8+ outlets in ~6h, top
  of r/all, trending #2 on X UK". Numbers > adjectives.
- **freshness_hours:** hours since break/spike; must be ≤ `fresh_hours_max`.

Total score = velocity_spread + headline_grab + freshness + cross_domain_reach +
curaition_depth + evidence − penalties (see SKILL.md rubric). Velocity is the engine here, but
the Phase-4 gate (corroboration + brand_safety) can veto any pick regardless of score.

## Brand-safety flags
- `safe` — ordinary topical story, fine to amplify.
- `sensitive` — tragedy, ongoing crisis, named victims, private individuals, health/grief.
  Handle soberly; prefer a responsible angle; often better to pick a different candidate.
- `unsafe` — hoax, scam, defamation, fabrication, exploitative engagement-bait. **Cannot be
  the selected pick.** May appear lower-ranked as a "what NOT to touch" note.

## Failure handling
- All `WebSearch` results stale/thin → widen queries, try adjacent domains, or report "nothing
  clears the bar today" rather than forcing a weak pick. A null day is an acceptable output.
- `web_fetch` blocked/restricted → inform, don't route around it; find another source.
- `web_fetch` returns a JS shell → escalate to Claude-in-Chrome (`navigate` →
  `get_page_text`).
- CurAItion down → omit cross-ref, proceed on web evidence (run still valid).
- Can't reach 2 independent reputable sources → do not select; flag `single-source`.
