# skills

CurAItion Agent Skills — editorial workflows, scouts, digest generators, and content production pipelines.

## The design rule: every skill runs alone

**A skill must run without any other skill installed.** Skills chain — the
scouts feed the classifier, which feeds the packager, which feeds the writers —
but the chain is the *caller's* choice, never a precondition baked into a skill.

Coupling goes to **artifacts**, never to skills:

| Do | Don't |
|---|---|
| Describe the *shape* you accept (`story-candidate`, `story-package`) | Name the skill that produces it |
| Bundle your own copy of any schema you read | Path-reference a sibling's `references/` folder |
| Degrade explicitly on thin input, and say what you inferred | Stop and tell the caller to go run something first |
| Suggest **formats** — `longform`, `thread`, `carousel`, `digest` | Suggest tools — `linkedin-writer`, `carousel-producer` |
| Key `channel_plan` by channel — `linkedin`, `substack`, `thread` | Key it by renderer skill name |

Two consequences worth stating outright:

- **Read a documented subset, ignore the rest.** A consumer names the fields it
  actually uses and tolerates everything else. Producers can then add fields
  without breaking anyone, and nothing has to be installed alongside anything.
- **A missing input lowers confidence, never blocks the run.** Emit the work,
  flag what you inferred, let the caller decide whether to enrich and re-run.
  The one thing that never degrades is citation: no skill may manufacture a
  source.

Why it matters: an installed set is not a fixed thing. Skills get added, split,
renamed and removed. A skill that names its neighbours breaks silently the day
that happens — and `tweet-thread`, referenced by six skills, never existed at
all. Naming formats and shapes instead means a handoff written today is still
readable by a renderer written next year.

Each `SKILL.md` in a chain carries a **Running standalone** section stating its
contract. Keep it there, and keep it true.

## One voice guide, not one per skill

House voice is the exception that proves the rule above — it is genuinely shared
data, so it lives in exactly one place: **`skills/_voice/`**.

Every skill in the editorial chain — `cultural-scout`, `click-bait-scout`,
`user-needs-classifier`, `story-packager`, `linkedin-writer`, `substack-writer` —
resolves from there. **None carries its own copy.** Two copies stay identical
right up until the day someone edits one, and then the house voice has quietly
forked into dialects that nobody notices because every individual skill still
looks self-consistent.

This does not break standalone-ness, because voice resolves like any other input
and degrades the same way: name a guide → read `voice_profile` off the artifact →
fall back to `_voice/curaition-tone-of-voice.md` → fall back to the handful of
essentials each skill carries inline, and say so. A skill lifted out of this repo
on its own still writes on-voice; it just flags that the full guide was
unreachable.

**Swapping voice is supported.** Add `<name>.md` to `_voice/`, then either name it
per run or set `voice_profile` on the artifact — every stage carries that field
forward, so the choice travels the chain without any skill knowing another
exists. See `_voice/README.md`.

Out of scope: `gymshark-partner-pulse`, `gymshark-market-pulse` and `digest`
speak in a client/product voice of their own and deliberately do not resolve from
`_voice/`.
