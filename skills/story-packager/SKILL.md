---
name: story-packager
description: >-
  Consolidate a story-candidate handoff (and, when present, a user-needs
  classification) into a single, self-contained, channel-agnostic Story Package
  that any writer or renderer consumes unchanged. It COMMITS to one story,
  CONSOLIDATES candidate + classification into one artifact so no writer
  re-derives, and SEPARATES a frozen, cited facts layer from a malleable craft
  layer (thesis, spine, hooks, headlines) plus an asset manifest and per-channel
  plan. Use for "package this story", "build a story package", "prep this
  candidate for the writers", "turn this scout output into a brief the channels
  can share", or any request to assemble one grounded, reusable source-of-truth
  for multi-channel content. Runs standalone: it needs only a cited candidate,
  and degrades explicitly when the optional classification is absent.
---

# CurAItion Story Packager

A story arrives as *what* (a grounded, cited candidate) and, sometimes, as a
*need* (the psychological job it does for a reader). Format — Substack,
LinkedIn, a thread, a carousel — is decided later, by whoever renders it. This
skill sits between framing and rendering and does the **commit**: it takes the
many-candidate handoff plus any need classification and produces one **Story
Package** — the single, self-contained source of truth every channel writer
builds from.

Its three moves:

1. **Commit** — collapse the scout's `candidates[]` down to the one
   `selected_candidate_id` (or a candidate you name). The package is always about
   one story; it never carries an array of candidates.
2. **Consolidate** — fold the story-candidate and the user-needs classification
   into one artifact so no downstream writer has to call back upstream or
   re-derive anything.
3. **Separate** — keep a **frozen, cited `facts[]` layer** distinct from a
   **malleable `editorial` craft layer**. This mirrors the CurAItion "grounded
   facts vs interpretive lift" rule and is what makes the no-fabrication
   guarantee enforceable: a writer may rephrase facts and elaborate editorial,
   but may never assert a claim that isn't in `facts[]`.

## Why this exists

Without a shared package, each channel writer re-derives the story from the raw
handoff — and four writers produce four subtly different takes: the LinkedIn post
cites a stat the tweet thread doesn't, the carousel's thesis drifts from the
Substack piece. For a studio whose product is signal-vs-noise and
no-fabrication, that fact-drift across channels is the thing to design out. One
package, one spine, one set of cited facts → every channel provably tells the
same story.

## What you produce

Per run, in the **same staging folder as the source story-candidate file**
(the scouts' default is `daily-drafts/<YYYY-MM-DD>/`, but treat that as a
convention, not a guarantee — the file may sit anywhere):

- `story-package-<YYYY-MM-DD>.json` — the machine artifact
  (schema: `references/story-package.schema.json`).
- `story-package-<YYYY-MM-DD>.md` — a human-scannable twin for review.

The `.json` **must** pass `scripts/validate_package.py` before you emit it.

## Running standalone

**This skill requires no other skill.** It consumes *artifacts*, not a pipeline
position, and both inputs below can come from anywhere — another skill, a
colleague, a hand-written file.

Only the candidate is required, and even that degrades: given a cited brief or
a topic with links rather than a formal handoff, build the candidate structure
yourself from the material and proceed. The one thing you may never manufacture
is a citation — see rule 2 under **Non-negotiables**.

The need classification is genuinely optional and the fallback is built in
(step 3). Never stop and tell the caller to go run something else first;
produce the package, flag what you inferred, and let them decide whether to
enrich it and re-run.

## Inputs

- **Required:** a story-candidate handoff — `story-candidate-<date>.json` or
  `clickbait-candidate-<date>.json`. Read its `selected_candidate_id` and commit
  to that one candidate (or a specific `candidate_id` if the caller names one).
  `examples/story-candidate-2026-07-02.json` is a worked instance of the shape.
- **Optional:** a user-needs classification — `user-needs-<date>.json`. When
  present, the need, axis, angle guidance and headline options are **carried as
  source of truth** — do not re-derive them. When absent, infer a provisional
  need as a **flagged, low-confidence fallback** (see step 3) and record
  `source: "backfill"` so a later pass can tell what was inferred from what was
  classified.

## Workflow

### 1. Load and commit

Read the story-candidate handoff. Take the `selected_candidate_id` (or the named
candidate). Carry into `source`: the `mode` discriminator, `scope_verification`
(the library-scope compliance receipt), and — for click-bait — the `virality`
block including `brand_safety`. **If `brand_safety` is `unsafe`, stop and refuse
to package.** Set `source.candidate_id`, `source.story_candidate_file`, and (if
used) `source.user_needs_file`.

### 2. Build `facts[]` — the ground-truth layer

Split `the_signal_24h.summary` (and corroborated detail from
`relationship_verifications`, `why_now`) into **atomic** facts — one claim each,
never bundled. For every fact:

- attach **≥1 citation drawn only from the handoff** (citation fidelity: the
  packager consolidates, it never researches or invents a new URL/`content_id`);
- set `importance` 0–3 (lets short formats keep only the top facts) and `layer`
  (`signal_24h` / `depth_90d` / `why_now` / `verification`);
- set `source` to the originating research tool (`CurAItion` / `WebSearch` /
  `WebFetch`) — **facts may never be sourced to a pipeline stage.**

**Depth handling (the important branch):** look at `the_depth_90d`.
- If it **has citations** (e.g. a CurAItion library item), it becomes a normal
  **grounded fact** with the right `source`.
- If it is **explicitly uncited interpretation** (the CurAItion "lift" — a
  historical rhyme, an analytical bridge), it is **NOT a fact**. It survives only
  as a `beat_type: lift` beat in the spine (step 4). Never launder uncited lift
  into `facts[]`.

### 3. Consolidate need and tone

- **If a user-needs file is present:** carry `primary_need`, `primary_axis`,
  `angle_guidance` and `headline_options` for the selected candidate into
  `editorial.tone` and `editorial.headline_options`. Do **not** put these in
  `backfill` — they are carried, not derived. Add a `provenance` entry with
  `source: "user-needs-classifier"`.
- **If absent:** infer a provisional `primary_need`/`primary_axis` from
  `why_it_matters` and `surprise_factor`, mark it **low confidence in
  `backfill`** with `source: "story-packager"`, and note in `tone.voice_notes`
  that a portfolio-balance check was not possible. Ship the package regardless —
  a flagged inference is the designed behaviour here, not a blocked run.

Set `tone.register` from `source.mode` (`click-bait` → `urgent-topical`,
`cultural` → `evergreen-curious`).

### 4. Write `editorial` — the craft layer

Generate the malleable layer, seeded from the candidate (`headline_hypothesis`,
`why_it_matters`, `surprise_factor`) and, if present, the classifier's
`angle_guidance`:

- `thesis` — the one-sentence argument the whole story makes.
- `headline_options` — a **pool** (writers select + adapt; they don't
  originate). Seed from the classifier's `headline_options` when present, else
  from `headline_hypothesis`.
- `dek`, `hooks` (from `surprise_factor`), `pull_quotes` (consistent with
  `facts[]`).
- `narrative_spine` — one ordered set of beats; this is the **reuse engine**
  (longform → sections, thread → posts, carousel → slides). Each beat has
  a `beat_type`:
  - **grounded** — rests on cited facts; `supports` is required and every id must
    exist in `facts[]`.
  - **lift** — interpretive bridge, no citation; `supports` must be empty. Marked
    so a writer never states it as flat fact.
  - **structural** — mechanical, no claim (e.g. `cta`); no `supports`.
  - **Beat vocabulary is hybrid:** prefer the core set
    (`hook / context / tension / depth / why_now / so_what / cta`) so writers can
    rely on it, but a story may define its own beat. The validator *warns*
    (doesn't fail) on off-core beats.

### 5. Build `assets[]` — the media manifest

This is the single source of truth for every image, animation, video and
embeddable URL, and the manifest a publisher/QA gate diffs the rendered output
against.

- Promote embeddable source citations (Instagram, TikTok, YouTube, X…) to
  `kind: embed` assets with the right `embed_provider` — a writer emits the bare
  URL for the platform to oEmbed.
- For any generated or non-hosted asset (Replicate output, etc.), set
  `origin` accordingly and flag `durable: false`, `rehost_required: true` — the
  Replicate-URL-expiry guard. **The packager only flags durability; it does not
  rehost — that is the publisher's job.**
- For content a target platform can't embed (Replicate video, custom iframe),
  name a `fallback_asset_id` (a static poster/still). Enforce "a fallback exists"
  rather than a silent drop.
- **Do not fabricate assets.** If the story has no hero image, leave `assets`
  without one and record the gap in `format_readiness` — never invent a
  Replicate URL that doesn't exist.

### 6. Channel plan

From the candidate's `suggested_formats`, emit per-channel steering in
`channel_plan`: `lead_with`, `length`, a `beats` subset of the spine,
`use_assets` ids, and `need_emphasis`. **This is steering, never rendered copy.**

**Key by channel, never by tool** — `linkedin`, `substack`, `thread`,
`carousel`, `digest`. You do not know, and must not care, what will render this
package: a renderer looks up its own channel, and a channel nobody renders is
simply unread. Naming a tool here would bake your installed set into the
artifact and strand it the day that set changes. New channels need no schema
change.

### 7. `format_readiness`

Score each target format `ready` / not, and name what's missing — so a writer
acts on the ceiling instead of discovering it mid-draft. Typical calls: text
formats ready immediately; a carousel `needs` generated hero + charts when
`assets` has no visual; longform `ready: false` when the evidence base is thin
(few facts / few primary sources), with an `enrichment` list.

### 8. Compliance, provenance, backfill

- `compliance` — set `brand_safety`, `promotional_flag`, and a
  `fabrication_guard` statement of the invariants asserted.
- `provenance` — carry the handoff's provenance and add packager/classifier
  entries.
- `backfill` — log **every field the packager derived rather than carried**
  (method, `derived_from`, confidence, note). When the pipeline is complete
  (scout + classifier both present), backfill should be small — mostly generated
  craft (spine, hooks). A large backfill is a signal the classifier was skipped.

### 9. Validate, then emit

Run `python scripts/validate_package.py <package.json> --handoff <candidate.json>
[--user-needs <user-needs.json>]`. It must pass (exit 0) before you write the
files. Then write the `.json` and the `.md` twin to the staging folder.

## Rules (the guardrails)

1. **Facts are frozen and cited.** Writers may reorder, select by importance, and
   rephrase — never add a claim not in `facts[]`.
2. **Citation fidelity.** Only reuse URLs/`content_id`s already in the handoff.
   The packager consolidates; it does not research.
3. **Ground before lift.** Uncited interpretation is `beat_type: lift`, never a
   fact. `facts[].source` is restricted to real research tools.
4. **Need is owned by the classification, not by you.** Carry it when present; infer only
   as a flagged, low-confidence fallback, and say so.
5. **Flag durability, don't rehost.** The packager marks `rehost_required`; the
   publisher acts on it.
6. **Emit a plan, never rendered copy.** No channel gets finished prose from here.
7. **`brand_safety: unsafe` is never packaged.**

## Common mistakes to avoid

1. **Re-deriving the story** or adding facts not in the handoff. The packager
   consolidates a decided story; it is not a second scout.
2. **Laundering uncited lift into `facts[]`.** If it has no citation from the
   handoff, it is a `lift` beat, not a fact.
3. **Guessing the need when a user-needs file exists** — or failing to flag the
   guess when it doesn't. Lean on the classifier.
4. **Fabricating a hero/visual asset** that the story doesn't have. Record the
   gap in `format_readiness` instead.
5. **Putting rendered copy in `channel_plan`.** It is steering only.
6. **Carrying all candidates.** Commit to one.

## Reference files

- `references/story-package.schema.json` — the output contract (draft-07).
- `scripts/validate_package.py` — the invariant checks JSON Schema can't express
  (spine⊆facts, beat-type/supports, citation fidelity, click-bait two-source,
  carry-through, `facts[].source` restriction). Run it every time.
- `examples/` — three golden fixtures covering the branches:
  - `story-package-2026-07-02.*` — cultural mode, **uncited-lift** depth, IG
    embeds, **inferred** need.
  - `story-package-clickbait-2026-07-02.*` — click-bait mode, **cited** depth, no
    embeddable assets, need **inferred + flagged**.
  - `story-package-clickbait-withneeds-2026-07-02.*` — the **carry-through**
    path: need carried from `user-needs-2026-07-02.json`, backfill collapses.

## Scope (v1)

This is the story-packager foundation: one committed story, one shared package.
The **need-aware `framings[]` extension** (multiple need-conditioned framings of
one story, plus portfolio-balance-driven lead selection — the "user-needs-package"
idea) is deliberately **deferred to v2** and is not built here.

*CurAItion Intelligence Desk · Story Packager · commit → consolidate → separate · runs standalone*
