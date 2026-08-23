---
name: substack-writer
description: >-
  Render a committed CurAItion Story Package into one on-voice Substack "The
  Drop" article. Consumes a story-package.json (a committed story with a frozen
  facts layer) plus the shared CurAItion tone-of-voice, and emits a single dry,
  evidence-led Drop essay of 1,000 words max — a gap-opening title, a mandatory
  subtitle that hints without resolving, sectioned beats, and sources carried
  as INLINE hyperlinks in the body (never a sources block). It is the premium,
  deeper version of the LinkedIn post, and its subtitle becomes the LinkedIn
  post's first line. Facts are frozen (it may only assert claims present in
  the package's facts[]); voice and framing are malleable. Ships a voice-lint
  gate. Use when the user asks to "write the Drop", "render this package for
  Substack", "turn this story package into a Drop article", or names
  Substack/The Drop as the target channel. Runs standalone: given a thinner
  brief it commits the story itself and says so. Scope: The Drop only (not the
  longform essay).
---

# CurAItion Substack Writer (The Drop)

This skill renders a committed story into one Substack **Drop** article: the
deeper, evidenced sibling of the LinkedIn post, same facts, more room. It
writes prose; it never re-derives the story or invents a fact.

Governing rule, inherited from the package: **facts are frozen, craft is
malleable.** Reorder, select, expand and rephrase freely. Never assert a claim
absent from the package's `facts[]`.

The Drop is *"more depth, more evidence, still dry — the premium version of the
LinkedIn post"* (tone-of-voice guide). Same argument as the post; it earns its
length with evidence and sequencing, not adjectives.

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

The Drop's length makes this more consequential than for a short post: with
more room, an uncommitted story drifts further. Keep the thin-input version
shorter rather than padding to the usual depth.

The only hard floor is citation: every claim you assert must be traceable to
something in the material you were given. Thin input lowers confidence, never
the sourcing bar.

## Inputs

- **Preferred:** `story-package-<date>.json`. The fields below are the whole
  contract — anything else in the file is ignored, and any producer that emits
  them will work. `examples/story-package-clickbait-withneeds-2026-07-02.json`
  is a complete worked instance; read it if the shape is unclear. Read:
  - `editorial.thesis` — the argument the essay must land, and the seed of the
    headline.
  - `editorial.headline_options` — the pool for the title (adapt, don't
    originate). The Drop title is usually two short declaratives ("The
    Decoupling Is Real. The Buyers Aren't.").
  - `editorial.narrative_spine` — the ordered beats; each becomes a section or a
    move within one. `beat_type` governs use: `grounded` states cited fact;
    `lift` is framed as a read, never flat fact; `structural` is mechanical.
  - `editorial.dek`, `editorial.pull_quotes` — supporting craft.
  - `editorial.tone` — `primary_need`, `primary_axis`, `register`. The need
    steers which section leads.
  - `facts[]` — the frozen ground truth with `importance` and `layer`. The Drop
    can carry more of the mid-importance facts than the post; still lead with
    the importance-3 signal.
  - `channel_plan["substack"]` — per-channel steering when present
    (`lead_with`, `length`, `beats`, `use_assets`, `need_emphasis`). Steering,
    not copy. Packages written before 2026-07-27 key this by writer name
    instead; if `["substack"]` is absent, fall back to `["substack-writer"]`.
    If neither exists, proceed — the plan is optional steering, never a
    precondition.
  - `provenance` / `facts[].citations` — the only sources the closing line may
    name.
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

## Voice

Dry, precise, direct; authority without arrogance; peer-to-peer. Short
sentences, one idea each. No filler openers. **British English. No em dashes.**
Self-aware, not cringe. The Drop is still dry — depth is added evidence and
structure, not enthusiasm or ornament.

## Structure (The Drop)

Canonical spec: GBrain `curaition/daily-publishing-prompt` (pull it at run
time when GBrain is available; it wins over this file on any conflict). The
issue log `curaition/the-drop` holds every published title, subtitle and
caption — the calibration corpus. Sections are guided by the spine; use the
beats you have, not a fixed count.

1. **Title** — must create a tension or reversal. Never resolve the argument
   in the title itself: the title opens the gap. Obeys the voice rules (no em
   dash, no double hyphen, British English). Published references: *"The
   Batman Problem"*, *"It exists only for pleasure"*, *"Unexpected items in
   the bagging area"*, *"The stink of excellence"*.
2. **Subtitle** — mandatory, every issue. It hints at the answer without
   resolving it, and it does double duty: it becomes the LinkedIn post's
   first line verbatim. Published reference: title *"The clicks that weren't
   real."* / subtitle *"A trillion-dollar industry. Forty percent of it was
   bots."*
3. **Lede** — opens on the specific object, never the announcement of it.
   State the obvious read, then pivot to what the coverage skips. Cited
   facts only.
4. **Sections** (`## …`, ~3-4), each one beat of the spine:
   - the catalyst (what actually moved it),
   - the prior thesis (the CurAItion depth layer — the `lift`, framed as a
     read with its honest caveat),
   - the counter-evidence (the `so_what`),
   - **one thing worth watching** — the conditions that would turn the story
     into a signal.
   Structure the argument on the Veritasium engagement formula: a
   misconception challenged, a question opened then explained, an A plot
   carrying a B plot. Before writing, answer: what does this add up to? What
   does the reader leave with that they didn't arrive with?
5. **Close** — restate the sharpest number or tension. Land the thesis.
6. **Sources are inline.** Every source is a markdown hyperlink in the body,
   at the claim it supports, using only URLs present in the package
   citations. **No sources block at the bottom — the lint fails it.** Never
   introduce a source the package doesn't carry.

## Rules (the guardrails)

1. **Facts-only.** Every claim traces to `facts[]`. No new numbers, names, or
   sources anywhere, including inline links.
2. **Lift stays interpretation.** A thesis that "has been about to happen" is a
   read, and carries its own caveat. Never launder it into fact.
3. **British English, no em dashes, no double hyphens, no filler opener.**
   Enforced by the lint.
4. **Still dry.** No hype, no build-up language, no pitch. The evidence is the
   essay.
5. **Length: 1,000 words max.** Target ~600-900 (lint band 400-1000). If it
   wants to run longer, that is the longform format, which is out of scope
   here.
6. **One argument.** The Drop deepens the post's single thesis; it does not add
   a second.
7. **Reads as discovered, not constructed.** Argument worked out on the page,
   uneven rhythm, no parallel short-sentence structures, no tidy three-beat
   builds, never explain the observation after making it. See the shared
   voice guide's "Reads as discovered, not constructed" section.
8. **Verified links only.** When a verification manifest is present in the
   staging folder (`verification-<date>.json`, produced by the daily-drop
   fact gate), link only to URLs it marks verified. A fact whose citation
   failed verification does not appear in the article at all.

## Output, then validate

Write to the package's staging folder as `<slug>-substack-drop.md`, headline
first. Then produce the paste-ready HTML twin:

```
python <path-to-this-skill>/scripts/drop_to_html.py <slug>-substack-drop.md
```

This exists because pasting raw markdown into Substack's editor loses every
element (links included), while pasting rendered HTML keeps them. The script
strips the title and subtitle (those go into Substack's own fields — it
prints them for copying) and converts the body via pandoc. The publisher
opens the `.html` in a browser, selects all, copies, and pastes into the
Substack body. Both files ship together.

Then run the gate:

```
python <path-to>/_voice/voice_lint.py <slug>-substack-drop.md --channel substack-drop \
  --package story-package-<date>.json
```

Use the **absolute** path to `voice_lint.py` you resolved above (inside this
skill's folder, or beside it). You run the lint from the staging folder where the
draft is, so any relative `_voice/…` path will miss it.


Must exit 0 (no hard failures) before presenting. Hard failures: em dashes, US
spelling, filler openers, word count outside 400-1000. Warnings (numbers not
traceable to `facts[]`, over-long sentences) are for review — a warned number
usually means a source line or stat to re-check against the package.

## Reference files

- `_voice/curaition-tone-of-voice.md` — the shared voice authority (one copy,
  used by the whole chain; see `_voice/README.md`).
- `_voice/voice_lint.py` — the gate. Run every time.
- `examples/` — an input/output pair: the source package
  (`story-package-clickbait-withneeds-2026-07-02.json`) and the rendered Drop
  (`substack-thedrop-bitcoin-decoupling.md`). **The rendered example predates
  the 16 Aug 2026 spec** (it carries a sources line and no subtitle, both of
  which now fail the lint) — use it for the shape of a package-to-prose
  render, never for format. The calibration corpus for format is the
  published archive: GBrain `curaition/the-drop` (titles, subtitles,
  captions, 51+ issues) and curaition.substack.com for full articles.

This skill does not define the story-package format — it reads a documented
subset of it (see **Inputs**) and ignores the rest. That is deliberate: a
producer can add fields without breaking this renderer, and this renderer needs
nothing installed alongside it to work.

---

*CurAItion Intelligence Desk · Substack Writer (The Drop) · one package, one essay, facts frozen · runs standalone*
