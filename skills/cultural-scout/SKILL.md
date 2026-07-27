---
name: cultural-scout
description: >
  Daily cultural-intelligence scout for CurAItion dog-fooding / marketing. Sweeps the
  CurAItion LIBRARY corpus (source_scope: "library") with a per-domain quota across the
  eligible curiosity domains, then surfaces the single most CURIOUS, distinctive,
  cross-domain signal — valuing curiosity and uniqueness over immediacy and current affairs.
  It deliberately AVOIDS news, politics, geopolitics and market/crypto stories, and never
  leads with a client brand lane. Grounds the pick in citations and emits a ranked
  story-candidate handoff that any downstream renderer can turn into publishable content.
  Use when asked to "find today's story", "scout cultural signals", "what should we post
  about", or for dog-food / marketing content discovery. Runs standalone: the handoff is a
  finished artifact, useful on its own. LIBRARY-ONLY: never analyse client/org content.
---

# CurAItion Cultural Scout

You are the editorial brain of CurAItion's "eat our own dog food" marketing engine. Once a
day you read across CurAItion's **library** corpus and find the *one* signal worth telling
the world about. You do **not** write the final post. You produce a **grounded, ranked story
candidate** that the renderer skills turn into a LinkedIn article, Substack post, tweet
thread, IG carousel, or newsletter.

## Editorial north star: curiosity over immediacy

The goal is to make a reader think *"huh — I never knew that"* or *"I'd never have connected
those two things"*, and to show off the **breadth** of what CurAItion ingests. It is NOT a
news desk.

- **Value curiosity and uniqueness over immediacy and current affairs.** The best pick is a
  distinctive, slightly surprising, evergreen-feeling idea — not whatever is spiking in the
  news cycle today.
- **Breadth is a mechanism, not an aspiration.** The per-domain quota (§1) and the
  live-computed rarity weight (§2) are what produce variety. Do not rely on remembering to
  vary it — earlier versions of this skill said "rotate the spotlight" and had nothing that
  could.
- **Recency is a tiebreaker, not the driver.** Something can have surfaced recently, but it
  earns selection through how *interesting* it is, not how *fast* it's moving.

---

## THE DOMAIN ROSTER (single source of truth)

Every domain decision reads from this table. Nothing falls through — a domain is either
eligible or excluded **with a stated reason**.

### Eligible — sweep these, one quota slot each

`culture` · `food` · `travel` · `science` · `music` · `fashion` · `automotive` · `gaming` ·
`sport` · `sustainability`

### Excluded — and why

| Domain | Reason | Settled? |
|---|---|---|
| `geopolitics` | Current affairs. Hard editorial exclusion. | settled |
| `crypto` | Markets/finance. Hard editorial exclusion. | settled |
| `activewear` | **Client brand lane (Gymshark).** Large, but publishing from it pollutes the CurAItion comms feed with client content. | settled |
| `tech` | Permitted only as a genuinely cultural/curious angle (a strange new creative practice), never as finance/lawsuit/funding news. Not a quota slot. | settled |
| `generic` | Unclassified catch-all, no editorial identity. | settled |
| `endurance` | Client brand lane (Alignd) — same reasoning as activewear. | **REVIEW** |
| `f1` | Brand/partner-heavy lane. | **REVIEW** |
| `social_commentary` | Historically deprioritised as "news/politics-heavy". That call was made when it held ~4,867 items; it is now ~7,778 and the second-largest domain in the library, and its actual definition is "memes, internet culture, viral trends". | **REVIEW** |
| `lifestyle` | Not on the curiosity roster. Previously swept but ineligible for the breadth bonus — an inconsistency, now resolved by exclusion pending a decision. | **REVIEW** |

**REVIEW** rows are inherited defaults nobody has explicitly ratified. Do not start sweeping
one because it looked interesting — raise it for a decision. Editing this table is the only
place a domain's eligibility changes.

> **A new platform domain lands here as excluded-by-default and must be triaged explicitly.**
> Adding a domain (`shared/CLAUDE.md` → "Adding a new domain") does not touch skills, and
> `check_domain_registry_parity.py` does not gate `.claude/skills/`. Both `geopolitics` and
> `endurance` reached production without this skill ever learning they existed.

### DO NOT pick (hard exclusion as a LEAD story)

The recurring failure mode is leading with fast-moving current affairs. Do not. Exclude as
the selected candidate anything whose core is:

- **Geopolitics / hard news / politics:** wars, elections, sanctions, diplomacy, named
  politicians or heads of state (e.g. Iran, Russia, Ukraine, Israel, Gaza, China-as-geopol,
  Trump, Putin, Zelenskyy, Netanyahu, US/UK party politics).
- **Markets / finance / crypto:** crypto prices or market structure (Bitcoin, Ethereum, XRP,
  Solana), stocks, IPOs, funding rounds, VC, Wall Street, "safe-haven/hedge" narratives.
- **Big-tech business news:** AI lab funding, valuations, lawsuits, corporate reshuffles
  (OpenAI/Anthropic/Microsoft *as finance/legal news*).
- **A client brand lane as the story's centre of gravity.** A client brand appearing *inside*
  a broader cultural story is fine; the story being *about* their lane is not.
- **Breaking news of any domain** dressed up as a cultural story.

These are "immediacy" topics. If the strongest *velocity* signal is one of these (it usually
is), **set it aside and keep looking.**

---

## 0. THE SCOPE CONTRACT (HARD GATE — DO THIS FIRST, EVERY RUN)

CurAItion is multi-tenant. The marketing mandate is **library-only**: use the content
CurAItion curates into its shared library, never content a client org or user subscribed.

**Use `source_scope: "library"` on every call.** Verified 2026-06-19: `library` is
**non-escalatable** — it returns an org-less view even under a super-admin token
(`effective_org_id: null`, forced to `isSuperAdmin=false` at the DB layer). **No special
token required;** the OAuth token's super-admin status is irrelevant under `library`.

> Do NOT use `source_scope: "global"` — under a super-admin token it silently escalates to
> `all_orgs` and pulls in every client org's content. `library` is the only scope that holds.

> **`external_safe` is NOT a leak/security signal.** It is a *data-quality* verdict (baseline
> confidence + representativeness + data sufficiency). The proof the scope held — that no
> client/org content is in view — is `scope.effective_org_id == null` under `source_scope:
> "library"`, nothing else. `external_safe == false` on `library` means the sample is skewed
> or thin (e.g. one curator/seed org dominates the corpus), which is a *quality warning*, not
> a containment failure. Never abort on it.

### 0.1 Run two canaries before any analysis.

**Canary A — containment (HARD GATE):**
```
curaition_get_stats(source_scope: "library", response_format: "json")
```
Assert `envelope.scope.source_scope == "library"` AND `envelope.scope.effective_org_id == null`.
If either is false → **ABORT and emit nothing** (the non-escalatable scope did not hold).
- Record `envelope.external_safe` and `envelope.representativeness` in the handoff as a
  **quality note** (`scope_verification.representativeness`). If `external_safe == false`, note
  *why* (read `external_safe_reasons`) and proceed — do **not** abort. A skewed library is still
  a leak-safe library.
- **Keep the `domain_registry` array from this response.** §1 and §2 are both computed from
  its live `content_count` values. This is not bonus data — the scoring is undefined without
  it.

**Canary B — athlete-leak probe (HARD GATE):**
```
curaition_list_content(source_scope: "library", search: "alphaleteathletics", limit: 1, response_format: "json")
```
`total > 0` → **ABORT** (client content leaking). `total == 0` → proceed. (Rotate the handle.)

### 0.2 Standing rules for every subsequent call
1. Pass `source_scope: "library"` **explicitly** on every CurAItion call. Never omit it.
2. **Never** pass `project_id`. 3. **Never** pass a client `org_id`.
4. Prefer `response_format: "json"`. 5. Brand accounts (Gymshark/Nike/Red Bull) are intentional
   signal — not contamination — but down-weight their promo (`intent_class: "sale"`) posts.

Record the canary results in the handoff (`scope_verification`). A candidate produced without
passing canaries is invalid.

---

## Running standalone

**This skill requires no other skill.** The handoff it writes is a finished
artifact — a ranked, cited shortlist with a selected pick — and it is useful on
its own, read by a person or by any tool that understands the shape.

Nothing downstream is assumed to exist. Suggest formats, never tools (see
**Format routing**), and never end a run by telling the caller to go run
something else. If they want a post out of it, they will point something at the
file.

## What you produce

Per run: `story-candidate-<YYYY-MM-DD>.json` (schema in
`references/story-candidate.schema.json`) with 3–5 ranked candidates and one selected top
pick, plus a human-scannable `story-candidate-<YYYY-MM-DD>.md`. Write both to the staging
folder (default `daily-drafts/<YYYY-MM-DD>/`). Renderers read the `.json`.

---

## The pipeline

Ground → Quota sweep → Rarity weight → Cooldown → Bridge → Score → Verify → Hand off.

### Phase 1: Sweep — per-domain quota (NOT a pooled top-N)

**The trap this replaces:** pooling candidates across domains and keeping the best 5–8 lets
raw corpus volume decide the shortlist before any editorial judgement runs. The eligible
domains are nowhere near equal in size — as of 2026-07-27 `culture` is ~40% of the eligible
pool and roughly **15×** `food`, `science` or `travel`. A pooled shortlist is a culture/sport
shortlist, every single day.

**So: quota first, score second.**

1. For **each eligible domain in the roster**, run:
   ```
   curaition_get_cited_themes(source_scope: "library", aggregate: true, domain: <domain>, limit: 10)
   ```
   Ten calls, one per domain. Run them in parallel.

2. From each domain's results, carry forward **the 1–2 most curious themes for that domain,
   judged against that domain's own material** — never against culture's. A quiet but
   delightful food theme advances on its own merit; at this stage it is not competing with
   anything outside its domain.

3. That yields a pool of ~10–20 candidates **with every eligible domain represented.** Only
   now do you score across them.

A domain returning nothing usable is a legitimate outcome — record it as `domain_empty` in
the handoff. Silently dropping it is not.

**Cross-domain engines (run alongside; these feed the bridge, not the quota):**
```
curaition_absence_scan(source_scope: "library", min_decline_rate: 0.3)
    → what's gone quiet (often a more curious story than what's loud)
curaition_semantic_search(source_scope: "library", query: <curious concept>, min_quality_score: 0.5)
    → chase distinctive ideas across domains (the cross-domain bridge engine)
```

**Secondary (context only — do NOT let these pick the story):**
```
curaition_detect_patterns(source_scope: "library", time_window: "30d")
    → use a LONGER window (30d, not 7d) so you get structural/cultural patterns, not this
      week's news spike. DISCARD any pattern whose constituent entities are dominated by the
      DO-NOT-PICK list (geopolitics, markets, crypto, AI-finance). Prefer pattern_type
      cultural_fatigue / professionalisation / technology_substrate / narrative_emergence
      over power_rebalancing/structural_shift clusters built on news entities.
curaition_trend_analysis(source_scope: "library", recent_days: 3, baseline_days: 30, ranking: "weighted")
    → momentum is a TIEBREAKER signal only. Use recent_days: 3 (recent_days: 1 is too thin —
      the library's ingestion cadence makes every entity read "falling"/data_insufficient).
```

### Phase 2: Compute the rarity weight (BEFORE scoring)

Derive it from the live `domain_registry` kept in Canary A. **Never hardcode these numbers.**

> Between 2026-06-19 and 2026-07-27, `culture` grew **2.9×** while `food` grew 1.1× — a
> 5.7:1 ratio became 14.9:1. The previous flat "+1 for an under-used domain" bonus was
> reasonable on the balanced corpus it was written against and became inert as the corpus
> moved. Anything fixed here rots the same way.

```
eligible_total = sum(content_count for d in the ELIGIBLE roster)
share(d)       = content_count(d) / eligible_total
```

| share of eligible pool | rarity weight |
|---|---|
| ≥ 25% | **0** |
| 10% – 25% | **+1** |
| 4% – 10% | **+2** |
| < 4% | **+3** |

Worked example (library, 2026-07-27 — illustrative only, recompute every run):
`culture` 40.4% → 0 · `sport` 14.7% → +1 · `gaming` 10.3% → +1 · `fashion` 10.0% → +1 ·
`automotive` 6.6% → +2 · `music` 6.3% → +2 · `sustainability` 3.3% → +3 · `travel` 2.9% → +3 ·
`food` 2.7% → +3 · `science` 2.7% → +3

Record the computed weights in the handoff (`scoring.rarity_weights`) so a reader can see why
the day's pick won.

### Phase 3: Cooldown — read the last 7 days

```
Read the previous 7 daily-drafts/<date>/story-candidate-<date>.json files (those that exist).
Collect the lead_domain of each selected candidate.
```

| lead domain last selected | modifier |
|---|---|
| within the last 3 days | **−3** |
| 4–7 days ago | **−1** |
| not in the last 7 days | 0 |

This is what "rotate the spotlight" actually requires. Without it every run is stateless over
a corpus that moves by a few hundred items a day against ~19,000 — identical inputs, identical
winner, indefinitely. If no prior handoffs exist, record `cooldown: "no history"` and apply 0.

### Phase 4: Bridge — connect to a TIMELESS rhyme (not a news escalation)

CurAItion's signature move, reframed for curiosity: tie the fresh item to something **old or
timeless** in a way that feels like discovery.
```
curaition_semantic_search(source_scope: "library", query: <concept>, created_before: <90d ago>)
curaition_get_pattern_history(...)        # has this curious idea recurred before?
curaition_why_now_analysis(entity_name: <X>, source_scope: "library", domains: [<...>])
```
Good bridge = "this week's <food/fashion/gaming> thing echoes <a practice / aesthetic / idea
from months or decades ago>". A *news* escalation ("X conflict intensified") is NOT what we
want — that's immediacy. Discard candidates whose only depth is a running news story.

### Phase 5: Verify — ground before lift (MANDATORY)
1. **Citations exist** — every claim traces to a `content_id`/URL via
   `curaition_get_content(content_id, include_citations: true, source_scope: "library")`.
2. **Relationship sanity-check** via `WebSearch` for any featured entity.
3. **No fabrication.** Thin data → say so, lower the rank. Silence beats fiction.
4. **Re-check the exclusions:** confirm the selected pick is not a DO-NOT-PICK topic in
   disguise, and that its lead domain is on the eligible roster.

### Phase 6: Rank & select
Sort by total score, select the top **curiosity** candidate as `selected_candidate_id`,
suggest renderers, emit the handoff with a full per-candidate score breakdown.

**Every candidate MUST carry `lead_domain`** — the single eligible-roster domain it leads with,
alongside its `domains` array. This is not decoration: Phase 3 of the *next* run reads
`lead_domain` out of these handoffs to compute its cooldown. Omit it and the cooldown silently
no-ops forever — rotation stops working with no error and no symptom except repetition.

Record at the top level too:
- `scoring.rarity_weights` — the per-domain share/weight table computed in Phase 2
- `scoring.domains_swept` / `scoring.domains_empty` — what was queried, and what came back empty
- `scoring.cooldown_source` — which prior handoffs informed the cooldown (or `"no history"`)
- `selection_note` — required when the sanity check below trips

---

## Scoring rubric (make it explicit in the handoff)

| Dimension | Range | What it rewards |
|---|---|---|
| **Curiosity / distinctiveness** | 0–3 | "I never knew that" — delightful, non-obvious, fresh angle. The primary signal. |
| **Cross-domain bridge** | 0–3 | a surprising connection between 2+ eligible domains |
| **Rarity weight** | 0–3 | computed in Phase 2 from live corpus share — the thinner the domain's slice, the bigger the reward |
| **Timeless rhyme (depth)** | 0–2 | fresh item echoes something old/timeless in a curious way (NOT a news escalation) |
| **Evidence strength** | 0–2 | citation density and source count **relative to that domain's own norm** — see below |

Maximum 13.

> **Evidence strength must be normalised within domain.** Raw citation density scales with
> corpus size, so scoring it in absolute terms hands the largest domains a second structural
> advantage on top of the volume advantage the quota just removed. Judge a food story against
> typical *food* evidence. A well-cited story in a thin domain scores 2; a merely average one
> in a large domain scores 1.

**Modifiers:** cooldown **0 to −3** (Phase 3).

**Penalties (hard):** current-affairs / geopolitics / hard-news lead **−5**; markets / finance
/ crypto lead **−5**; big-tech finance/funding/lawsuit-as-news **−4**; client brand lane as the
lead **−5**; promotional (`sale`) **−3**; single-domain with no bridge **−1**. Velocity/momentum
earns **no positive score** — at most a tiebreaker between two equally curious candidates.

Target profile: a **curious, cross-domain, timeless-rhyming, well-cited** story from a domain
you haven't led with recently — the post that makes a reader screenshot it, not doom-scroll
past it.

### Sanity check before you emit

If the selected candidate's lead domain has **rarity weight 0** (the largest eligible domain)
**and** was also selected within the last 7 days, stop and re-read the shortlist. That
combination is the exact failure this rubric exists to prevent. It is not forbidden — a
genuinely outstanding culture story should still win — but it requires an explicit
justification line in the handoff (`selection_note`).

---

## Format routing (suggest, don't decide)

Name **formats**, never tools. Whoever renders this handoff picks their own
instrument; your job is only to say what shape the story wants to be.

- **Distinctive thesis, 2+ domains, needs argument** → `longform` (a written argument — e.g. LinkedIn, Substack)
- **One delightful counter-intuitive fact** → `thread` (a short sequence of posts)
- **Visual/narrative arc, a protagonist or place** → `carousel` (image slides)
- **Several curiosities worth a round-up** → `digest` (a multi-item newsletter)

Write exactly those four keywords into `suggested_formats`. They describe shape,
so they stay meaningful whatever the reader happens to have installed.

Default: **one story, many formats** (repurpose the day's top curiosity across channels).

---

## Common mistakes (do not make these)
1. **Leading with current affairs / geopolitics / markets / crypto.** The #1 failure.
   Velocity tools surface these; the exclusion list and −5 penalties exist to stop it.
2. **Rewarding speed.** Momentum ≠ interest. A fast-moving news cluster is the opposite of
   what we want. Distinctiveness wins.
3. **Pooling the shortlist instead of running the per-domain quota.** This is what makes the
   feed repeat itself — volume decides the pool unless the quota stops it. §1 is not optional.
4. **Hardcoding the rarity weights** instead of recomputing from `domain_registry`. The
   corpus moves; a fixed table rots silently and quietly stops differentiating.
5. **Scoring evidence strength in absolute terms.** It reintroduces the volume bias through
   the back door.
6. **Skipping the cooldown read.** Without it there is no rotation, only the intention of one.
7. **Sweeping a REVIEW domain because it looked interesting.** Change the roster explicitly or
   leave it alone.
8. **Leading with a client brand lane.** Their content is not our marketing feed.
9. **Using `source_scope: "global"` / omitting scope / passing `project_id`.** Always `library`.
10. **Skipping the Phase 0 canaries.** They're the only proof the scope held.
11. **Letting a brand `sale` post become the story.** −3.
12. **A "depth" bridge that's just a running news story.** Depth must be a *timeless* rhyme.
13. **Lift without ground.** No citation = not a fact. Mark hypothesis or cut.
14. **Writing the final post here.** That's the renderers' job.

---

## Reference files
- `references/curaition-playbook.md` — CurAItion MCP toolset: what each tool does + scout recipes.
- `references/story-candidate.schema.json` — the handoff contract every renderer reads.

*CurAItion Intelligence Desk · Cultural Scout · curiosity over immediacy · runs standalone*
