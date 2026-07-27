---
name: user-needs-classifier
description: >
  Classifies a CurAItion story-candidate handoff against the smartocto /
  Dmitry Shishkin "User Needs Model 2.0" (built on BBC news user-needs
  research): the eight needs Update me, Keep me engaged, Give me
  perspective, Educate me, Inspire me, Divert me, Help me, Connect me.
  Produces primary/secondary need scores, story-specific angle and
  headline guidance, and a portfolio-balance check against recent editions
  so output doesn't lopsidedly over-serve one need (esp. overproduced,
  underperforming "Update me" pieces). Applies to a story-candidate handoff
  from any source, and to a story described in prose when no handoff exists.
  Also trigger for "classify by user need", "what need does this story
  serve", "apply the user needs framework/model", "run this through
  smartocto/BBC user needs", or any request for editorial framing/angle
  guidance on a story idea, even without naming the framework. Runs
  standalone: it needs nothing but a story to classify.
---

# User Needs Classifier

Editorial framing sits on top of facts and format. Something else finds the
*what* (a grounded, cited story candidate). Something else decides the
*format* (a long-form essay, a thread, a carousel, a digest). This skill
decides the *need* — the psychological reason a reader engages with the
piece — and hands whoever writes it concrete guidance for hitting it.

## Running standalone

**This skill requires no other skill.** It classifies whatever story it is
given. A `story-candidate-<date>.json` is the richest input, but a story
described in a paragraph, a headline plus a few links, or a rough pitch all
work — the eight needs apply to any story, not to a file format.

With thinner input the classification is thinner too: say so in the
rationale and hold the secondary need loosely. What you must not do is
refuse, or send the caller away to produce a handoff first.

Read `references/user-needs-model.md` before classifying anything — it has
the full framework, all eight need definitions, and the question banks this
skill draws its angle guidance from. Don't rely on memory of the model; the
nuances (which need sits on which axis, the format-vs-need pitfall, the two
needs that are genuinely new in 2.0) matter for getting classification right.

## Why this exists

A story can be reported as pure fact (Update me), or the same story can be
explained (Educate me), analysed for what it means (Give me perspective),
made to feel something (Inspire me / Divert me), or turned into something
the reader can act on (Help me / Connect me). None of these is "more
correct" — they're different jobs a piece of content can do for a reader.
Studios that don't think about this default to Update me for everything,
because it's the easiest to write. The research behind this model
(smartocto, in collaboration with former BBC user-needs lead Dmitry
Shishkin) found that's a mistake: in one dataset, 57% of published articles
were Update me pieces but they earned only 8.5% of reads, while Educate me
and Give me perspective pieces were comparatively under-produced and
over-performed. Classifying and rotating needs deliberately is what this
skill is for.

## Workflow

### 1. Load the story candidates

Read the `story-candidate-<YYYY-MM-DD>.json`, wherever it actually lives
(`daily-drafts/<YYYY-MM-DD>/` is the usual convention, not a guarantee — the
file may sit anywhere, including flat in a working directory). It does not
matter what produced it; only its shape matters. If no such file exists,
work from whatever description of the story you were given and skip to
step 2. You need the full `candidates` array, not just the
`selected_candidate_id` — classify every candidate the scout ranked, not
only the top pick, since the portfolio-balance step (below) benefits from
seeing the full spread of options that were available that day.

### 2. Classify each candidate against the eight needs

For each candidate, read `the_signal_24h.summary`, `the_depth_90d.summary`,
`why_it_matters`, and `surprise_factor` — the classification must be
grounded in what's actually in the candidate, not a generic guess at the
topic. Ask, in order:

1. **Which axis does the core hook sit on?** Is the reader's primary payoff
   a new fact (know), a clearer picture of why/how (understand), a feeling
   (feel), or something to do (do)? Most stories have a dominant axis even
   if they touch others. Each need belongs to exactly one axis — use this
   lookup so `primary_need` and `primary_axis` never disagree:

   | Axis | Needs |
   |---|---|
   | know | update_me, keep_me_engaged |
   | understand | give_me_perspective, educate_me |
   | feel | inspire_me, divert_me |
   | do | help_me, connect_me |

2. **Within that axis, which of the two needs fits tighter?** Use the
   definitions and question bank in `references/user-needs-model.md` to
   decide — e.g. on the "understand" axis, is this explaining a mechanism
   the reader didn't know existed (Educate me), or analysing/interpreting
   something they already partly know about (Give me perspective)?
3. **Is there a secondary need worth naming?** Stories often straddle two
   needs — the whitepaper's own example is that "Connect me" and "Inspire
   me" sit next to each other in the model because the pull to feel
   connected to a cause borders on the pull to feel motivated by it, even
   though they're driven by different axes (do vs. feel). Name a secondary
   need only if it's genuinely present in the cited facts, not to hedge.

Score all eight needs 0-3 (0 = absent, 3 = strong fit) so the classification
is auditable rather than a single unexplained label, then take the top two
as primary/secondary. Write a one-line rationale for each that names the
specific fact it's grounded in.

If the source candidate itself flags its evidence as thin, contaminated, or
inconclusive (a `why_now` signal marked contaminated, or a candidate
carrying only one or two citations), say so
explicitly in the rationale and hold any secondary need loosely rather than
scoring it with the same confidence as a well-evidenced candidate. A
low-confidence classification honestly labelled is more useful downstream
than a confident-sounding one built on thin material.

**Watch for the format-vs-need trap** (this is the single most common
mistake newsrooms make with this model, per the source material): a format
like "analysis" or "explainer" is not itself a need. An analysis piece can
serve Give me perspective (interpreting what something means) or Educate me
(explaining how something works) depending on what it's actually doing for
the reader — don't let the candidate's `suggested_formats` field
(longform, thread, carousel, digest) bleed into or substitute for the
need classification. They're independent axes: format is the container,
need is the psychological job. This is also why the classification never
names a renderer — it describes the job, and whoever renders picks the
container.

## Voice

This skill writes text a reader will see — the example headline you produce for each need, and the angle questions a
writer will work from — so it resolves the **shared**
house voice, the same one the writers use. There is one guide for the whole
editorial chain; this skill does not carry its own copy.

Resolve most specific first:

1. a voice guide named in the request;
2. `voice_profile` on the artifact you are reading (a path, or a bare name
   resolving to `_voice/<name>.md`);
3. the default `_voice/curaition-tone-of-voice.md`;
4. nothing resolvable → the essentials below, and say so in your output.

**Carry `voice_profile` forward onto everything you emit.** That is what lets a
non-default voice travel the chain without any skill needing to know which other
skills exist. If you resolved the default, write `voice_profile` anyway so the
choice stays explicit rather than implied.

Essentials, if the guide is unreachable: dry, not earnest. Short sentences, one
idea each. No filler openers. **British English. No em dashes.** Peer-to-peer,
never a vendor pitching. See `_voice/README.md` to add a different profile.

### 3. Generate angle guidance for the top need(s)

For the primary need (and secondary if named), produce 3-4 concrete
questions a writer should ask about *this specific story* to hit that need,
plus one example headline. Base the question style on the patterns in
`references/user-needs-model.md` §Question bank, but write them against the
actual facts of the candidate — generic questions ("is there anything to
learn here?") are not useful; specific ones ("is there a precedent for this
exact illegal-release-then-legalise pattern in another country?") are.

Two optional fields exist for extra sharpness, and both should be used
sparingly rather than filled by default: `brand_specific_flavour` (a
sharper, story-specific naming of the need, in the style of the
publisher-specific needs the source material documents — e.g. "give me an
edge") is worth adding only when it genuinely sharpens the framing beyond
the core need label; most candidates won't need one. `format_vs_need_note`
is worth adding whenever the candidate's `suggested_formats` could
plausibly be mistaken for the need itself (this is common, so expect to use
it on most candidates), but skip it if there's no real risk of confusion.

### 4. Portfolio-balance check

Scan the same directory the source story-candidate file lives in (and
dated sibling directories if it follows the `daily-drafts/<date>/`
convention) for prior `user-needs-<date>.json` outputs, looking back over
the last 7 available editions (fewer if history is shorter — say so
plainly, and if this is the first-ever run, report zero editions found
rather than guessing at history).

The tally that drives `skew_flag` is **the `primary_need` of the
`selected_candidate_id` only, one data point per edition** — this is what
actually got published, so it's what portfolio balance is about. Flag it
if:
- any single need accounts for more than half of that tally, or
- any need hasn't appeared at all across the window.

Separately, you can note the broader spread of primary needs across *all*
ranked candidates (not just the selected one) as supporting colour — e.g.
"today's runners-up would have served Update me and Connect me, so the
studio had options beyond what got picked" — but this broader spread is
context, not part of the skew calculation itself.

This isn't a hard rule to force diversity for its own sake — a genuine run
of "Give me perspective" stories is fine if that's what the material
supports. It's a check against the default-to-Update-me drift the research
warns about. Say what you found plainly; don't manufacture a false balance
recommendation if the data doesn't support one (an n=1 window has nothing
to balance against — say so instead of speculating).

### 5. Write the handoff

Produce `user-needs-<YYYY-MM-DD>.json` (schema in
`references/user-needs-handoff.schema.json`) and a human-scannable
`user-needs-<YYYY-MM-DD>.md`, both in the same staging folder as the source
story-candidate file. Carry over the `selected_candidate_id` from the
source file unchanged — this skill adds framing, it doesn't re-rank the
scout's pick.

Tell renderer skills (or whoever picks this up next) to read the
`angle_guidance` for the candidate they're rendering and use it to shape the
opening hook and structure, not just the topic.

## Common mistakes to avoid

1. **Classifying the topic, not the story.** Two pieces about the same
   underlying event can serve completely different needs depending on
   what's foregrounded. Classify what the candidate's cited facts actually
   emphasise.
2. **Treating format as need.** See the format-vs-need trap above — it's
   the single most-cited pitfall in the source material.
3. **Forcing a secondary need that isn't there.** Most stories have one
   dominant need; only name a second if it's grounded in a distinct cited
   fact, not to seem thorough.
4. **Defaulting to Update me.** It's the easiest need to assign to any
   factual story and the one the research explicitly warns is
   overproduced. If a candidate genuinely is a fact-driven update with no
   deeper angle, say so — but check whether Give me perspective or Educate
   me is actually the better fit first.
5. **Skipping the portfolio check because history is thin.** Even one or
   two prior editions are worth noting ("no prior editions to compare" is a
   valid, honest finding — don't skip the step silently).

---

*CurAItion Intelligence Desk · User Needs Classifier · classify the need before you render · runs standalone*
