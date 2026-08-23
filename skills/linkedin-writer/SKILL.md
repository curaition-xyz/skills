---
name: linkedin-writer
description: >-
  Render a committed CurAItion Story Package into one on-voice LinkedIn post
  plus its prepared first comment. Consumes a story-package.json (a committed
  story with a frozen facts layer) plus the shared CurAItion tone-of-voice,
  and — when the Drop draft exists — that draft, whose subtitle becomes the
  post's first line verbatim. Emits a single dry, argument-led, 150-250 word
  LinkedIn post that mirrors the Drop's opening object and register, ends
  "Full breakdown in the comments" with max 3 hashtags, and a separate
  first-comment file carrying the Substack link and remaining hashtags. Facts
  are frozen (it may only assert claims present in the package's facts[]);
  voice and framing are malleable. Ships a voice-lint gate. Use when the user
  asks to "write the LinkedIn post", "render this package for LinkedIn", "turn
  this story package into a LinkedIn post", or names LinkedIn as the target
  channel. Runs standalone: given a thinner brief it commits the story itself
  and says so.
---

# CurAItion LinkedIn Writer

This skill does one thing: render a committed story into a single LinkedIn post
in CurAItion's voice. It writes prose; it never re-derives the story or invents
a fact.

The governing rule, inherited from the package: **facts are frozen, craft is
malleable.** You may reorder, select by importance, compress and rephrase. You
may never assert a claim that is not in the package's `facts[]`.

## Running standalone

**This skill requires no other skill.** It consumes an *artifact*, not a
pipeline position. A story package may arrive from anywhere — another skill, a
colleague, a file you wrote by hand.

If you are handed something thinner than a story package (a scout handoff, a
cited brief, a topic plus links), do not stop and ask for one. Commit the story
yourself: pick the single candidate, extract the cited claims into a `facts[]`
of your own with `importance` and `layer`, derive a one-line thesis, and write.
Then open the delivery note with one line — *"Rendered from a raw handoff, not
a committed package: thesis and fact importance are mine."* — so the caller
knows the framing was not pre-agreed. A flagged inference beats a refusal.

The only hard floor is citation: every claim you assert must be traceable to
something in the material you were given. Thin input lowers confidence, never
the sourcing bar.

## Inputs

- **Preferred:** `story-package-<date>.json`. The fields below are the whole
  contract — anything else in the file is ignored, and any producer that emits
  them will work. `examples/story-package-clickbait-withneeds-2026-07-02.json`
  is a complete worked instance; read it if the shape is unclear. Read:
  - `editorial.thesis` — the one-sentence argument the post must land.
  - `editorial.hooks` — candidate opening reframes.
  - `editorial.narrative_spine` — the ordered beats. Each beat's `beat_type`
    governs how you may use it:
    - `grounded` — rests on cited facts; state it plainly, drawing only on the
      `supports` fact ids.
    - `lift` — interpretive bridge (the CurAItion "part the coverage skips").
      Frame it as a read, never as flat fact ("the argument sat there for a
      quarter" is analysis, not a datum).
    - `structural` — mechanical (e.g. the comments CTA).
  - `editorial.headline_options` — a pool to draw the hook's angle from (adapt,
    don't originate).
  - `editorial.tone` — `primary_need`, `primary_axis`, `register`. Let the need
    steer emphasis (e.g. "Give me perspective" → lead with the reframe).
  - `facts[]` — the frozen ground truth, each with `importance` (0-3) and a
    `layer`. For a 150-250 word post, keep only importance 2-3 facts.
  - `channel_plan["linkedin"]` — per-channel steering when present:
    `lead_with`, `length`, a `beats` subset of the spine, `use_assets`,
    `need_emphasis`. This is steering, not copy. Honour it. Packages written
    before 2026-07-27 key this by writer name instead; if `["linkedin"]` is
    absent, fall back to `["linkedin-writer"]`. If neither exists, proceed —
    the plan is optional steering, never a precondition.
- **Voice source:** resolved from the shared guide, most specific first:
  1. a voice guide named in the request;
  2. `voice_profile` carried on the package (a path, or a bare name resolving to
     `_voice/<name>.md`);
  3. the default `_voice/curaition-tone-of-voice.md`;
  4. nothing resolvable → the essentials below, and say so in the delivery note.

  There is **one** voice guide for the whole editorial chain and this skill does
  not carry its own — per-skill copies are how a house voice forks into
  dialects.

  **Where it is** depends on how this skill was installed. Check both, in order:

  1. `_voice/` **inside** this skill's folder — an installed bundle carries its
     own copy, because a packaged skill is a single folder with no siblings.
  2. `../_voice/` **beside** this skill's folder — a checkout of the skills repo,
     where one shared copy serves every skill.

  Either way, resolve it relative to *this SKILL.md*, never to the current
  working directory — when a skill runs, cwd is the user's project or a staging
  folder, nowhere near the skills root. See `_voice/README.md` to add a
  different profile.

  The essentials below are a summary of the default, never a substitute for it.

## Voice (from the tone-of-voice guide)

Dry, precise, direct. Authority without arrogance. One senior practitioner
writing to another, never a vendor pitching.

- **Short sentences.** One idea each. Split anything over two clauses.
- **No filler openers.** Never "We're excited to…", "In today's evolving…".
  Start with the thing.
- **British English.** Colour, realise, organisation. No exceptions.
- **No em dashes.** Use a full stop or a comma.
- **Self-aware, not cringe.** A point of view on ourselves, without preciousness.

LinkedIn calibration: **dry, argument-led, no product pitch, 150-250 words,
compressed not summarised.** No sign-off (the "Ben + Rick" sign-off is for DMs
and email, not posts).

Canonical spec: GBrain `curaition/daily-publishing-prompt` (pull it at run
time when GBrain is available; it wins over this file on any conflict).

## Structure (the shape that works)

The post is the Drop's compression, not its summary. Same argument, same
register, less room. Map the package's spine onto it; don't pad to fill it.

1. **First line = the Drop's subtitle, verbatim.** When a Drop draft exists in
   the staging folder (`<slug>-substack-drop.md`), its subtitle is your
   opening line, character for character. When there is no Drop draft, write
   the line that would be its subtitle: it hints at the answer without
   resolving it.
2. **Mirror the Drop's opening** — the same specific object, the same
   register, compressed. Open on the thing, never the announcement of it.
3. **What actually happened** — the core grounded facts, compressed. Cited
   facts only; lead with specifics and numbers.
4. **The part the coverage skips** — the `lift` beat, framed as
   interpretation.
5. **The tension** — the `so_what`. Often a counter-fact that complicates the
   easy read.
6. **Provocation** — one question that hands the argument to the reader.
7. **CTA** — the post's last sentence is `Full breakdown in the comments.`
   (the lint enforces the ending). Hashtags may follow it.
8. **Hashtags** — exactly this shape: `#CulturalIntelligence #BrandStrategy`
   plus at most one story-specific variable. Never more than 3.

## The first comment (second output)

The link lives in the comment, not the post. Alongside the post, write
`<slug>-linkedin-first-comment.md`:

- the Substack link for this issue (the only URL);
- hashtags: `#culturalintelligence #brandstrategy` + 2-3 topic-specific +
  `#curaition`.

Validate with `--channel first-comment`. If the Substack URL is not yet known
(the article publishes first), write the canonical placeholder
`https://curaition.substack.com/p/<slug>` and flag it in the delivery note for
the publisher to confirm. When the run creates the Substack draft through the
`curaition_publish_substack` MCP tool (daily-drop Stage 7), the tool returns
the slug Substack actually assigned: the first comment must use that real
slug, not the placeholder, and is re-linted after the swap. Without the tool,
the placeholder stands and the publisher confirms the live URL before
posting the comment.

## Rules (the guardrails)

1. **Facts-only.** Every claim traces to `facts[]`. No new numbers, names, or
   sources. If the post needs a fact the package lacks, stop and say so.
2. **Lift stays interpretation.** Never state a `lift` beat as a flat fact.
3. **150-250 words.** If it won't fit, cut, don't shrink the idea.
4. **British English, no em dashes, no double hyphens, no filler opener.**
   Enforced by the lint.
5. **No product pitch.** The intelligence is the case. Let it stand.
6. **No links in the post body.** The Substack link goes in the first
   comment. LinkedIn suppresses reach on body links; the canonical layout has
   always kept the link in the comment.
7. **Reads as discovered, not constructed.** Uneven rhythm, no parallel
   short-sentence structures, no tidy three-beat builds. See the shared voice
   guide's "Reads as discovered, not constructed" section.

## Output, then validate

Write the post to the package's staging folder as
`<slug>-linkedin.md` — the post body only, no descriptive H1 (a LinkedIn post
has no headline) — and the first comment as
`<slug>-linkedin-first-comment.md`. Then run the gates:

```
python <path-to>/_voice/voice_lint.py <slug>-linkedin.md --channel linkedin \
  --package story-package-<date>.json --drop <slug>-substack-drop.md
python <path-to>/_voice/voice_lint.py <slug>-linkedin-first-comment.md \
  --channel first-comment
```

`--drop` makes the lint verify the first-line/subtitle mirror mechanically;
omit it only when no Drop draft exists, and say so in the delivery note.

Use the **absolute** path to `voice_lint.py` you resolved above (inside this
skill's folder, or beside it). You run the lint from the staging folder where the
draft is, so any relative `_voice/…` path will miss it.


It must exit 0 (no hard failures) before you present the draft. Hard failures:
em dashes, US spelling, filler openers, word count outside 140-260. Warnings
(numbers not traceable to `facts[]`, over-long sentences) are for review — read
them; a warned number usually means a fact-fidelity slip to fix.

## Reference files

- `_voice/curaition-tone-of-voice.md` — the shared voice authority (one copy,
  used by the whole chain; see `_voice/README.md`).
- `_voice/voice_lint.py` — the "validate, don't hope" gate. Run every time.
- `examples/` — an input/output pair: the source package
  (`story-package-clickbait-withneeds-2026-07-02.json`) and the rendered post
  (`linkedin-bitcoin-decoupling.md`). **The rendered example predates the
  16 Aug 2026 spec** (it does not open with a Drop subtitle) — use it for the
  package-to-prose shape, never for format. Calibrate format against the
  published corpus: GBrain `curaition/the-drop` subtitles are the openers of
  the live posts.

This skill does not define the story-package format — it reads a documented
subset of it (see **Inputs**) and ignores the rest. That is deliberate: a
producer can add fields without breaking this renderer, and this renderer needs
nothing installed alongside it to work.

---

*CurAItion Intelligence Desk · LinkedIn Writer · one package, one post, facts frozen · runs standalone*
