# Story Package — National Identity in Sportswear

`pkg-2026-07-02-national-identity-sportswear` · built 2026-07-02 · from `story-candidate-2026-07-02.json` (candidate `national-identity-sportswear`, mode **cultural**)

**Thesis.** The 2026 World Cup kit has quietly become a text: brands are stitching national mythology into shirts that most fans only ever decode through slowed-down social content.

> Scope receipt carried through: `source_scope: library`, `effective_org_id: null`, `external_safe: true`. Brand safety: **safe**. Promotional: **no**.

---

## Facts (ground truth — frozen, every claim cited)

Writers may reorder, select by importance, and rephrase these. They may **not** assert anything not on this list.

| id | ★ | layer | claim | citations |
|----|---|-------|-------|-----------|
| **f1** | 3 | signal_24h | England's Nike 2026 home shirt hides "Happy and Glorious" (from "God Save the King") inside the collar, with the Three Lions, the World Cup star and a Saint George's Cross woven throughout. | [Instagram](https://www.instagram.com/p/DWHbrNDDERP/) · [Dezeen](https://www.dezeen.com/2026/03/20/england-world-cup-kit-2026-nike-all-white/) |
| **f2** | 2 | signal_24h | Canada's home/away kits use the maple leaf and a "black ice" pattern tied to the country's winter landscape and a "stealthily dangerous" identity. | [Instagram](https://www.instagram.com/p/DV84O2jjFbG/) |
| **f3** | 1 | verification | The England shirt also carries a jacquard lion pattern and Nike "Aero-Fit" fabric tech. | [Dezeen](https://www.dezeen.com/2026/03/20/england-world-cup-kit-2026-nike-all-white/) |
| **f4** | 2 | why_now | 2026 World Cup federation kit reveals are rolling out through June–July 2026, ahead of the tournament. | [Dezeen](https://www.dezeen.com/2026/03/20/england-world-cup-kit-2026-nike-all-white/) |

---

## Editorial (craft — malleable, seeded from the candidate)

**Headline pool** (writers select + adapt; they don't originate):

1. World Cup Kits Are Heraldry With a Swoosh
2. The Anthem Is Hidden in the Collar
3. Nobody Reads the Shirt — Until Someone Points a Camera at It
4. Your Country's Kit Is a Coat of Arms Now

**Dek.** Nike and Adidas are encoding anthem lyrics, saints' crosses and winter landscapes into 2026 World Cup shirts — turning kit design into a national literacy test.

**Hooks.** "You've worn the shirt. Have you ever actually read it?" · "There's a line from the national anthem hidden inside England's collar. Almost nobody has noticed." · "A World Cup kit is now a coat of arms you can buy in a size medium."

**Pull-quotes.** "'Happy and Glorious' — the anthem, printed where only the player can see it." · "Kit design has become a literacy test." · "Heraldry with a design studio instead of a herald's office."

### Narrative spine (the reuse engine — one spine, every channel maps it)

| # | beat | type | point | rests on |
|---|------|------|-------|----------|
| 1 | hook | grounded | An anthem lyric is hidden in England's collar that most fans never notice. | f1 |
| 2 | context | grounded | What's actually woven in: anthem line, Three Lions, St George's Cross; maple leaf and "black ice". | f1, f2 |
| 3 | depth | **lift** | Heraldry by another name — cloth has encoded national identity for centuries; a collar quoting the anthem is the same logic via a kit studio. | *interpretive — uncited* |
| 4 | why_now | grounded | Kit-reveal season is peaking now, ahead of the 2026 tournament. | f4 |
| 5 | so_what | grounded | Kit design is now a literacy test — identity transmitted via close-read content, not just the badge. | f1, f2 |
| 6 | cta | structural | Ask readers what's hidden in their own team's kit. | — |

**Tone.** evergreen-curious · primary need **give me perspective** (understand axis) · reframe-the-familiar register; defer to `my-writing-style` for house voice.

---

## Assets (media manifest — the QA hub)

| id | role | kind | provider | durable | source |
|----|------|------|----------|---------|--------|
| a1_england_ig | inline | embed | instagram | ✅ | [IG post](https://www.instagram.com/p/DWHbrNDDERP/) |
| a2_canada_ig | inline | embed | instagram | ✅ | [IG post](https://www.instagram.com/p/DV84O2jjFbG/) |

Both are Instagram oEmbeds — a writer emits the bare URL and the platform renders it (Substack supports basic IG embeds). **Gap:** no generated hero image exists yet; the carousel channel must supply one downstream, and it will land as a Replicate asset flagged `rehost_required` at that point.

---

## Channel plan (late-divergence steering — not rendered copy)

- **substack** → lead with the hook, longform, use both IG embeds, all six beats.
- **carousel** → lead with the hook, 7 slides, use both IG embeds, beats 1–3 + 5–6.

---

## Backfilled by the packager (transparent gap-filling)

No user-needs file was supplied, so the packager derived the following rather than carrying them. Nothing here is silently invented — each is traceable and reversible.

| field | method | from | conf. | note |
|-------|--------|------|-------|------|
| tone.primary_need | inferred | why_it_matters, surprise_factor | med | Reframes a familiar object, not breaking news → give me perspective. |
| tone.primary_axis | inferred | why_it_matters | med | Understanding, not know/do/feel. |
| headline_options | generated | headline_hypothesis, surprise_factor | high | Seeded from the candidate's hypothesis; classifier options unavailable. |
| narrative_spine | generated | signal_24h, depth_90d, why_now, why_it_matters | high | depth_90d carried as **lift** — explicitly uncited interpretation. |
| facts | carried-transformed | signal_24h.summary, relationship_verifications, why_now | high | Summary split into atomic facts; corroboration folded into f1. |
| assets | carried-transformed | signal_24h.citations | high | Two IG citations promoted to oEmbed assets. |

---
*CurAItion · story-packager (draft) · validates against `story-package.schema.json` v1*
