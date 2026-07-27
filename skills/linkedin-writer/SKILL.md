---
name: linkedin-writer
description: >-
  Render a committed CurAItion Story Package into one on-voice LinkedIn post.
  Consumes a story-package.json (a committed story with a frozen facts layer)
  plus the shared CurAItion tone-of-voice, and emits a single dry,
  argument-led, 150-250 word LinkedIn post that ends on a provocation. Facts
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

  **Where it is:** `_voice/` sits *beside this skill's own directory*, not inside
  it — so `../_voice/curaition-tone-of-voice.md` relative to this SKILL.md, and
  `<skills-root>/_voice/…` absolute. Resolve it that way rather than looking for
  `_voice/` under the current working directory, which is usually somewhere else
  entirely. See `_voice/README.md` to add a different profile.

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

LinkedIn calibration: **dry, argument-led, no product pitch, 150-250 words, end
with a question or provocation.** No sign-off (the "Ben + Rick" sign-off is for
DMs and email, not posts).

## Structure (the shape that works)

Derived from the calibrated reference post (`examples/`). Map the package's spine
onto it; don't pad to fill it.

1. **Reframe hook** (1-3 short lines). Flip the obvious read. State the headline
   fact, then undercut it. *"Bitcoin went up while tech went down. That's the
   headline. It's the least interesting thing that happened."*
2. **What actually happened** — the core grounded facts, compressed. Cited facts
   only; lead with specifics and numbers.
3. **The part the coverage skips** — the `lift` beat. The CurAItion angle that
   reframes the news (the depth layer, the pattern). Framed as interpretation.
4. **The tension** — the `so_what`. Often a counter-fact that complicates the
   easy read (price vs flows).
5. **Provocation close** — one question that hands the argument to the reader.
   *"Which one are you trading?"*
6. **CTA** — `Full breakdown in the comments.` (drives to the longform / source;
   this is the `structural` beat).

## Rules (the guardrails)

1. **Facts-only.** Every claim traces to `facts[]`. No new numbers, names, or
   sources. If the post needs a fact the package lacks, stop and say so.
2. **Lift stays interpretation.** Never state a `lift` beat as a flat fact.
3. **150-250 words.** If it won't fit, cut, don't shrink the idea.
4. **End on a question or provocation.** Never a summary, never a pitch.
5. **British English, no em dashes, no filler opener.** Enforced by the lint.
6. **No product pitch.** The intelligence is the case. Let it stand.
7. **Hashtags:** none, or at most 1-3 tasteful. Never a stack.

## Output, then validate

Write the post to the package's staging folder as
`<slug>-linkedin.md` — the post body only, no descriptive H1 (a LinkedIn post
has no headline). Then run the gate:

```
python <skills-root>/_voice/voice_lint.py <slug>-linkedin.md --channel linkedin \
  --package story-package-<date>.json
```

`<skills-root>` is the directory this skill's own folder sits in — the lint lives
beside the skill, but you run it from the **staging folder** where the draft is,
so a bare `../_voice/…` will not find it. Use the absolute path you resolved for
the voice guide.


It must exit 0 (no hard failures) before you present the draft. Hard failures:
em dashes, US spelling, filler openers, word count outside 140-260. Warnings
(numbers not traceable to `facts[]`, over-long sentences) are for review — read
them; a warned number usually means a fact-fidelity slip to fix.

## Reference files

- `_voice/curaition-tone-of-voice.md` — the shared voice authority (one copy,
  used by the whole chain; see `_voice/README.md`).
- `_voice/voice_lint.py` — the "validate, don't hope" gate. Run every time.
- `examples/` — a golden input/output pair: the source package
  (`story-package-clickbait-withneeds-2026-07-02.json`) and the rendered post
  (`linkedin-bitcoin-decoupling.md`) it produces. The post passes the lint with
  zero warnings; use it as the calibration target.

This skill does not define the story-package format — it reads a documented
subset of it (see **Inputs**) and ignores the rest. That is deliberate: a
producer can add fields without breaking this renderer, and this renderer needs
nothing installed alongside it to work.

---

*CurAItion Intelligence Desk · LinkedIn Writer · one package, one post, facts frozen · runs standalone*
