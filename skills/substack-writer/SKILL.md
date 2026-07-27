---
name: substack-writer
description: >-
  Render a committed CurAItion Story Package into one on-voice Substack "The
  Drop" article. Consumes a story-package.json (a committed story with a frozen
  facts layer) plus the shared CurAItion tone-of-voice, and emits a single dry,
  evidence-led Drop essay — a headline, a "Cur(AI)tion · date" subhead, a few
  sectioned beats, and a sources line. It is the premium, deeper version of the
  LinkedIn post. Facts are frozen (it may only assert claims present in the
  package's facts[]); voice and framing are malleable. Ships a voice-lint gate.
  Use when the user asks to "write the Drop", "render this package for
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
  dialects. See `_voice/README.md` to add a different profile.

## Voice

Dry, precise, direct; authority without arrogance; peer-to-peer. Short
sentences, one idea each. No filler openers. **British English. No em dashes.**
Self-aware, not cringe. The Drop is still dry — depth is added evidence and
structure, not enthusiasm or ornament.

## Structure (The Drop)

From the calibrated reference (`examples/`). Sections are guided by the spine;
use the beats you have, not a fixed count.

1. **Title** — the argument as a headline. Usually two short declaratives. Obeys
   the voice rules (no em dash, British English).
2. **Subhead** — `*Cur(AI)tion · <DD Month YYYY>*`.
3. **Lede** — the setup in facts, then the pivot: state the obvious read, then
   *"None of that is the story. The story is…"*. Cited facts only.
4. **Sections** (`## …`, ~3-4), each one beat of the spine:
   - the catalyst (what actually moved it),
   - the prior thesis (the CurAItion depth layer — the `lift`, framed as a read
     with its honest caveat),
   - the counter-evidence (the `so_what`; e.g. flows vs price),
   - **one thing worth watching** — the conditions that would turn the story
     into a signal.
5. **Close** — restate the sharpest number or tension. Land the thesis.
6. **Sources line** — `*Sources: …*` naming only outlets/links present in the
   package citations. Never introduce a source the package doesn't carry.

## Rules (the guardrails)

1. **Facts-only.** Every claim traces to `facts[]`. No new numbers, names, or
   sources anywhere, including the sources line.
2. **Lift stays interpretation.** A thesis that "has been about to happen" is a
   read, and carries its own caveat. Never launder it into fact.
3. **British English, no em dashes, no filler opener.** Enforced by the lint.
4. **Still dry.** No hype, no build-up language, no pitch. The evidence is the
   essay.
5. **Length:** a Drop, not a longform. Target ~500-900 words (lint band
   400-1000). If it wants to run longer, that is the longform format, which is
   out of scope here.
6. **One argument.** The Drop deepens the post's single thesis; it does not add a
   second.

## Output, then validate

Write to the package's staging folder as `<slug>-substack-drop.md`, headline
first. Then run the gate:

```
python ../_voice/voice_lint.py <slug>-substack-drop.md --channel substack-drop \
  --package story-package-<date>.json
```

Must exit 0 (no hard failures) before presenting. Hard failures: em dashes, US
spelling, filler openers, word count outside 400-1000. Warnings (numbers not
traceable to `facts[]`, over-long sentences) are for review — a warned number
usually means a source line or stat to re-check against the package.

## Reference files

- `_voice/curaition-tone-of-voice.md` — the shared voice authority (one copy,
  used by the whole chain; see `_voice/README.md`).
- `_voice/voice_lint.py` — the gate. Run every time.
- `examples/` — a golden input/output pair: the source package
  (`story-package-clickbait-withneeds-2026-07-02.json`) and the rendered Drop
  (`substack-thedrop-bitcoin-decoupling.md`), which passes the lint with zero
  warnings. Use it as the calibration target.

This skill does not define the story-package format — it reads a documented
subset of it (see **Inputs**) and ignores the rest. That is deliberate: a
producer can add fields without breaking this renderer, and this renderer needs
nothing installed alongside it to work.

---

*CurAItion Intelligence Desk · Substack Writer (The Drop) · one package, one essay, facts frozen · runs standalone*
