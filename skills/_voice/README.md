# Voice profiles

**One voice guide, shared by the whole editorial chain.** `cultural-scout`,
`user-needs-classifier`, `story-packager`, `linkedin-writer` and
`substack-writer` all resolve their voice from here. None of them carries its
own copy — a per-skill copy is how a house voice quietly forks into five
dialects.

```
_voice/
  curaition-tone-of-voice.md   ← the default house voice
  voice_lint.py                ← the mechanical gate (British English, em dashes, filler openers)
  <your-profile>.md            ← add more here
```

Not in scope: the Gymshark skills (`gymshark-partner-pulse`,
`gymshark-market-pulse`) and `digest` speak in a client/product voice of their
own and deliberately do not resolve from here.

## Adding a different voice

Drop a new `.md` beside `curaition-tone-of-voice.md`. Match its section
structure — **How we write**, **Voice principles**, **Voice in practice** (paired
use-this/not-this examples), **Channel calibration**, **Sign-off convention** —
because the writers read those sections by name.

Then select it, by either route:

- **Per run:** name it when you invoke the skill — *"write the LinkedIn post
  using `_voice/acme-house.md`"*.
- **Per story:** set `voice_profile` on the artifact. `cultural-scout` and
  `click-bait-scout` write it onto the story-candidate handoff, `story-packager`
  carries it into the story-package, and the writers read it from there. The
  choice then travels the whole chain without any skill having to know which
  other skills exist.

`voice_profile` holds a path or a bare profile name (`acme-house` resolves to
`_voice/acme-house.md`). Absent, the default applies.

## Finding this directory

`_voice/` sits **beside** each skill's folder, not inside it:

```
skills/
  _voice/            ← here
  cultural-scout/
  linkedin-writer/
  …
```

So from a `SKILL.md`, the guide is `../_voice/curaition-tone-of-voice.md`. Do not
look for `_voice/` under the current working directory — when a skill runs, cwd is
usually the user's project or a staging folder, nowhere near the skills root.
Resolve the absolute path once and reuse it, including for `voice_lint.py`, which
is invoked from the staging folder where the draft lives.

## Resolution order

Every chain skill resolves voice the same way, most specific first:

1. A guide the caller names explicitly in the request.
2. `voice_profile` carried on the artifact being read.
3. `_voice/curaition-tone-of-voice.md` — the default.
4. **Nothing resolvable** → fall back to the inline essentials in the skill's own
   Voice section, and say so in the delivery note.

Step 4 is what keeps every skill runnable on its own. A skill copied out of this
repo on its own has no `_voice/` directory; it still produces on-voice work from
the handful of rules it carries inline, it just says the full guide wasn't
available. That is the same rule the rest of the repo follows: **a missing input
lowers confidence, it never blocks the run** (see the root `README.md`).

## The lint

`voice_lint.py` is the mechanical half — it catches what a rule can catch
(Americanisms, em dashes, filler openers, sentence length). It is one copy for
the same reason the guide is: two copies drift, and a lint that disagrees with
itself between channels is worse than no lint.

It checks the mechanical rules, not the voice. Passing the lint is necessary,
never sufficient.
