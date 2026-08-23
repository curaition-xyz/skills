---
name: carousel-producer
description: "Produce brand-locked carousels from CurAItion cultural intelligence — deterministic, typographic, image-free. Pulls the most compelling narrative thread via CurAItion MCP tools, writes an editorial script, then renders 8 content slides + 1 final brand slide in TWO formats from one carousel.json: Instagram 1080x1350 PNGs and a LinkedIn 1080x1350 PNG set compiled to a PDF for document upload (olive-on-cream Geist Medium typography, 66px, max 3 lines per slide, mycelium watermark, one story-specific SVG data chart, N/9 slide numbers) via a bundled Chromium (Playwright) renderer, gated by a density lint. No AI image generation — visual richness comes from copy, data, and brand system. Use when the user asks to create a carousel, Instagram post series, LinkedIn carousel, visual story, or slide-based content from CurAItion data. Also trigger for 'make a carousel from this episode', 'turn this into slides', 'create an Instagram series', 'regen slide N', 'tweak slide N', 'change the chart', or any request combining CurAItion content analysis with brand-rendered carousel production or editorial iteration on a previously-produced carousel."
---

# CurAItion Carousel Producer (Brand Render)

You produce Instagram carousels that turn CurAItion cultural intelligence into scroll-stopping **typographic** narratives, rendered in the CurAItion brand system. Each carousel is a text-first editorial sequence grounded in real data — themes, entities, relationships, citations — and rendered as pixel-deterministic PNGs.

This skill is deliberately **image-free**. Content slides are pure typography; the only graphic slide is one story-specific data chart. AI image generation is a **separate concern** handled by a future companion skill — see *Boundary With Image Generation* at the end. Do not generate, fetch, or place photographic/AI imagery behind this typography; the brand is anti-image on content slides (clean cream, olive text, no scrim).

The pipeline has six layers. Layers 1–2 are editorial intelligence (unchanged in spirit from prior versions). Layer 3 is deterministic brand rendering. Layer 4 packages and (optionally) ingests via the prerendered endpoint. Layer 5 is cheap single-slide iteration. Layer 6 is the publishing boundary — this skill does not publish, but it documents the gate its output must pass and the sequencing the publisher follows.

---

## Carousel Shape (default, overridable)

**Default: 8 content slides + 1 final brand slide = 9 total.** Exactly one of the content slides (position **3–5**) is a data chart.

This is a default, not a hard rule:
- Flex the content-slide count (6–10) when the arc genuinely needs it. The final brand slide is always last and always present.
- Drop the chart slide when the story has **no honest quantitative angle** — never invent numbers to fill it. If you drop it, say so and keep all content slides typographic.
- The chart earns its slot only if there is a citable figure worth seeing. One chart maximum.

---

## Layer 1: CurAItion Analytical Substrate

Before any creative work, extract the intelligence layer from CurAItion. This is the foundation everything sits on.

### Step 1: Source Selection

If the user specifies a content source, use it. If they say "pick something interesting," run discovery:

```
curaition_list_content        → recent content in the target domain(s)
curaition_get_content (include_citations: true) → full analysis for 2–3 candidates
```

**Selection criteria** (rank candidates by these, in order):
1. **Narrative arc potential** — setup, tension, resolution.
2. **A single stop-the-scroll detail** — one fact, number, or reversal.
3. **A quantitative spine** — is there a citable figure that could carry the chart slide? (Nice-to-have, not required.)
4. **Theme weight** — prefer themes with CurAItion weight ≥ 0.80.
5. **Citation density** — more timestamped citations = more material.

### Step 2: Deep Analysis Pull

For the chosen source, extract everything:

```
curaition_get_content (content_id, include_citations: true)
```

Harvest: **themes** (with weights — the narrative spine), **entities** (with significance — the characters), **relationships** (the plot points), **cultural references** (contextual bridges), **timestamped citations** (evidence), **domain trends** (the "why now"), **embed data** (source_url for provenance), and any **quantitative signals** (counts, percentages, deltas — candidate chart data).

### Step 3: Supplementary Research

CurAItion is the analytical substrate; carousels need narrative and numeric detail that goes beyond content analysis. Use `WebSearch` to fill gaps: biographical facts, historical context, specific numbers/quotes from primary sources, and — critically for the chart slide — **verifiable data points with a citable source**.

**Label everything.** Every data point is tagged `CurAItion analysis` or `Supplementary` (web research). Non-negotiable — it's the provenance chain. Never fabricate a figure for the chart; if you cannot cite it, drop the chart.

---

## Layer 2: Editorial Intelligence

Raw analysis becomes a story here. You write a production script — a creative brief specifying every slide's copy, the chart's data, and production notes.

### The Production Script Format

```markdown
# CAROUSEL PRODUCTION SCRIPT

## [Title]
*[Subtitle — the narrative angle in one line]*

## THE SIGNAL
**Source:** [title] — [creator/channel]
**Content ID:** [UUID]
**CurAItion Domain:** [domain]
[All extracted themes, relationships, references, domain trends]
**Narrative angle:** [2–3 sentences: WHAT this is about and WHY it isn't just a summary]

## SLIDES
### SLIDE N — [FUNCTION]
**Copy:**
> [The exact text, with hard line breaks marked]
**Production note:** [Why this slide exists, which CurAItion data it draws from]

### SLIDE k — CHART — [FUNCTION]
**Title:** [chart title]
**Data:** [{label, value}, ...]  **Unit:** [% / count / etc.]
**Source:** [citable source string]
**Production note:** [Why this figure matters to the arc]

## OVERARCHING POST / CAPTION
> [Instagram caption with hashtags and source credit]

## DATA PROVENANCE
| Data Point | Source | Tool |
|---|---|---|
| [item] | [CurAItion analysis / Supplementary] | [tool] |
```

### Narrative Architecture

Every carousel follows a dramatic arc. Three structures:

- **LINEAR-HERO** — one protagonist's journey: Person → Action → Consequence → Legacy.
- **LINEAR-HERO (dual protagonist)** — two protagonists split the arc: A instigates act 1, B inherits act 2; the irony is B gets exactly what A wanted and finds it hollow. Use when the power is in the gap between wanting and getting.
- **CONVERGENT-OPPOSITION** — two forces on a collision course: Force A → Force B → the gap → collision → aftermath. Tension comes from the audience seeing what neither side can.

Choose by the material: one protagonist → LINEAR-HERO; instigator/executor handoff → dual-protagonist; two colliding forces → CONVERGENT-OPPOSITION.

**Slide functions** (not every carousel uses all):

| Function | Purpose |
|----------|---------|
| **HOOK** | Stop the scroll. One striking detail, number, or reversal. Slide 1. |
| **PROTAGONIST** | Introduce the main character in staccato fragments. |
| **ANTAGONIST** | Introduce the opposing force with hard metrics (CONVERGENT-OPPOSITION). |
| **CONTEXT / CHART** | The "wait, what?" reframe. Often the best home for the data chart. |
| **DECISION** | The fateful choice that sets dominoes falling. |
| **ESCALATION** | Stack details, raise stakes. |
| **PIVOT** | The moment everything changes. |
| **CLIMAX** | Peak of action or revelation. |
| **LEGACY** | Connect the specific story to a universal pattern. |
| **CLOSE** | Mirror the hook. Land the theme. Last **content** slide. |
| **FINAL** | Brand sign-off (mark + wordmark). Always the true last slide. Not narrative. |

### Slide Copy Rules (brand-specific)

The copy is the entire visual. Canonical authority: GBrain
`curaition/carousel-slide-density` (reach-data-backed; pull at run time when
GBrain is available) and `curaition/daily-publishing-prompt`. These rules are
tuned for 66px centred Geist Medium on cream:

1. **Maximum 3 lines per slide. Ideally 2.** The best slides are 1-2 lines.
   The gap between two lines is where the interest lives. A slide that needs
   a fourth line is two slides.
2. **Slide 1 is the hook, and the sparest slide in the deck.** 1-2 lines
   only. Specific fact + reframe/withhold. The canonical reach-ranked hooks:
   - *"England are in the World Cup semifinal. / They left their best right
     back at home."* (fact + reframe, nothing explained)
   - *"Jannik Sinner just won Wimbledon. / Again."* (the pause is everything)
   - *"Yesterday, Ariana Grande's rep issued a statement. / One word in it is
     doing all the work."* (states the fact, withholds the punchline)
   - *"China's Gen Z stopped buying status."* (one line; the statement IS the
     argument)
   The pattern: a short first line stating a specific fact or naming the
   specific object; a second line that reframes, contradicts, withholds, or
   delivers a flat verdict. What kills it: explaining the observation after
   making it, a third line that summarises the first two, parallel sentence
   structures, opening with a question (reads as an ad).
3. **One idea per slide.** Each slide delivers exactly one beat. Never two.
4. **Hard line breaks, and you own every one.** Write copy with explicit
   `\n`. Keep every line **≤ 24 characters** so the authored break IS the
   rendered break at 66px — a longer line wraps and the visual line count
   drifts off-spec. Do not lower `font_size` to cram a long line in; cut the
   line.
5. **No widows.** A last line of 6 characters or fewer fails the lint (the
   renderer would merge it, but rebalance the copy instead).
6. **Sentence case, not caps.** Geist on cream reads as calm editorial.
7. **Numbers do the work.** "168 vs 80,000" beats any adjective.
8. **Staccato for character.** "Illiterate. Illegitimate. Nearly 60."
9. **Primary-source quotes cut through.** Verbatim, source in the production
   note.
10. **End on a mirror or a verdict.** The last content slide (CLOSE) echoes
    the hook with the weight of the whole story behind it.
11. **Gate before rendering:** `python scripts/slide_lint.py carousel.json`
    must exit 0. It enforces the density rules, the hook rules, widows, line
    length, and the no-em-dash / no-double-hyphen rule mechanically.

### The Chart Slide

One chart, positioned 3–5, only if there's a citable figure. Keep it honest and sparse:
- 3–6 bars maximum. More than 6 and the labels crowd.
- Values are real and cited. Put the citation in the `source` field (renders small at the bottom) **and** in provenance.
- Title is a short declarative phrase (≤ 2 lines), not a caption.
- The renderer handles all styling (olive bars, sparse grid, ghosted mark). You supply only title, `{label, value}` pairs, unit, and source.

### Caption Writing

The IG caption is **one line, declarative, ending with a relevant emoji**.
It states the hook's fact and withholds the rest — the carousel does the
work. Published references (from the issue log): *"A CEO cited Batman to
justify his surveillance cameras. Batman ends with the surveillance system
being shut down. 🦇"*, *"She played a girl who couldn't be hurt. She was
thirty-six. 🖤"*. Validate with
`voice_lint.py <file> --channel ig-caption`. No hashtag stack in the
caption; discovery hashtags belong to the LinkedIn first comment, not here.

---

## Layer 3: Brand Rendering

This layer is deterministic. Given a `carousel.json`, the bundled renderer produces identical PNGs every time. No model-in-the-loop image decisions.

### The Brand Spec (authoritative)

Canonical source: GBrain `curaition/daily-publishing-prompt` § Carousel
technical spec (16 Aug 2026, from Issue 44 production). On any conflict, the
GBrain page wins; update this file and the renderer to match it.

| Token | Value |
|-------|-------|
| IG canvas | **1080 × 1350px** PNG (4:5 — the tallest ratio Instagram's API accepts) |
| LinkedIn canvas | **1080 × 1350px** PNG per slide, compiled to a **PDF** (uploaded via the document icon, not the image icon) |
| Renderer | headless Chromium (Playwright); vertical geometry expressed as fractions of slide height, against a `SPEC_BASELINE_H` of 1440 — the height the spec's absolute values were authored at, deliberately kept separate from the canvas |
| Text / mark / values | Olive **#6B7A3F** — never dark ink on content slides |
| Chart bars | Sage **#9CAF7A** |
| Background | Cream **#F1EFE8** throughout |
| Slide numbers, axis, source lines | Stone **#C8C3B4** |
| Content type | **Geist Medium (500)**, 66px, line-height 1.31, centred |
| Slide numbers | **Geist Light (300)**, 28px, top-right, format **N/9** (N/total) |

**Content slide:** olive copy on cream, centred, **66px / 1.31 line-height,
max 3 lines**. Slide number top-right `N/9`. Mycelium watermark **32×32px,
horizontally centred, bottom edge at 96.9% of slide height** (y=1412 at the
spec's 1440 authoring baseline → y=1324 on the 1350 canvas), rendered as an
`<img>`-equivalent CSS mask, never SVG `<image>`.

**Chart slide:** vertical bars only, as **SVG `<rect>` elements** (HTML divs
are silently dropped by some rasterisers; rects are also what the spec
mandates). Bars anchor to a **1px stone axis baseline at 86.5% of slide
height** (y=1246 at the 1440 authoring baseline → y=1168 on the 1350
canvas); the tallest bar is **396px** at that baseline, scaled
proportionally to **371px** on the 1350 canvas. Title **left-aligned at y=110**, Geist
Medium olive. Generous empty space above the bars. Value labels above bars
(Medium, olive), category labels below the baseline (Light, olive), source
line **anchored to that same baseline** — 68px below it, Light, stone — so
the caption tracks the labels it sits under instead of the canvas bottom. This is the moment the question
becomes concrete in numbers — the Q→E beat of the Veritasium formula.

**Final slide (slide 9):** mycelium mark **40px tall** + **"curAItion"**
wordmark (**42px, Geist Medium**) as a horizontal lockup, truly centred,
**both entirely in olive — the AI is NOT contrasted in a different colour**.
CTA **"Read the full story at curaition.substack.com"** bottom-centre, Geist
Medium 26px olive. **No watermark and no slide number on the final slide.**
**LinkedIn variant:** the same lockup plus **"Follow curAItion for daily
cultural intelligence"** in Geist Light 300 below the wordmark, CTA at the
bottom.

> **Font note:** fonts are embedded as base64 **WOFF2** per spec — Chromium decodes WOFF2 data-URIs natively (verified). (History: an earlier wkhtmltoimage/Qt-WebKit renderer could not decode WOFF2 and needed a TTF fallback; the move to Chromium removed that compromise.)

### Instagram media spec (the hard gate the render must satisfy)

From `publishing/instagram/media_spec.py` in the platform repo — these are
Meta's limits, enforced by CurAItion **at ingest only** (the publish path
never re-validates geometry, confirmed by inspection). A successful
`POST /api/assets/prerendered` is the compliance proof; never assume the
publish step will catch a bad canvas.

| Constraint | Value |
|---|---|
| Aspect ratio | 0.8 (4:5) – 1.91 (1.91:1) |
| Width | 320 – 1440 px |
| File size | 8 MB, **after JPEG conversion** |
| Carousel items | 2 – 10 |

**1080×1350 is 0.8000 exactly** — compliant with zero margin below. The old
1080×1440 canvas (0.75) sat below Meta's floor; that is what v3.1 fixed, and
`media_spec.py` names the daily-drop sets in its own docstring. Never
restore 1440.

### carousel.json

```json
{
  "slug": "mycelium-mind",
  "slides": [
    {"type": "content", "copy": "Line one\nLine two"},
    {"type": "content", "copy": "A shorter beat.", "font_size": 100},
    {"type": "chart",
     "title": "Share of forest carbon routed\nthrough fungal networks",
     "unit": "%",
     "source": "Source: Nature 2023 (CurAItion cited)",
     "bars": [
       {"label": "Boreal", "value": 58},
       {"label": "Temperate", "value": 41},
       {"label": "Tropical", "value": 33}
     ]},
    {"type": "content", "copy": "..."},
    {"type": "content", "copy": "..."},
    {"type": "content", "copy": "..."},
    {"type": "content", "copy": "..."},
    {"type": "content", "copy": "The close line."},
    {"type": "final"}
  ]
}
```

Field notes:
- `type`: `content` | `chart` | `final`.
- Slide numbers auto-fill as `N/total` by position for `content`/`chart`. Override with `n` if needed. `final` has no number.
- `font_size` (content) overrides the 66px default for a single slide. Prefer cutting the line to shrinking the type — the spec is 66px.
- `bars[].display` (optional) overrides the value label text (e.g. `"58%"`, `"1.2M"`); otherwise it's `value` + `unit`.
- `final` accepts optional `wordmark` (default `"curAItion"`) and `url` (default `"curaition.xyz"`).
- `background` (optional, any slide) — the image-composite layer. **Brand content slides omit it.** See *Image slides — renderer contract* below.

### Image slides — renderer contract (for the image-gen companion skill)

The renderer is Chromium, so it can composite brand typography over a full-bleed image with real CSS legibility treatments. This is the seam the future image-gen skill fills: it supplies a `background` block on a slide; **this** renderer and **this** `carousel.json` schema stay the single source of truth. Brand content/chart/final slides never carry a background.

```json
{"type": "content", "copy": "Text over imagery.",
 "background": {
   "image": "file:///abs/path.png",   // or https:// — the generated image
   "fit": "cover",                     // cover | contain (default cover)
   "focal": "50% 40%",                 // background-position (default 50% 50%)
   "treatments": ["duotone", "scrim-bottom", "dim:0.2", "blur:4"],
   "text_color": "#F1EFE8"             // optional; defaults to cream over images
 }}
```

Treatment tokens (listed bottom-to-top paint order): `duotone` (desaturate + olive/cream grade — keeps the brand palette over any photo), `grayscale`, `blur:<px>`, `dim:<0..1>` (flat dark overlay), `scrim-bottom` (gradient for bottom-set copy), `scrim-full` (even wash). Copy defaults to cream over imagery for legibility, and the **mycelium mark auto-switches to cream** over images too (the mark renders as a recolourable CSS mask, so one asset tints per context; override with `background.mark_color`). The slide number still renders. See `examples/demo-image-slide.json`. **Boundary:** only the image-gen skill emits `background`; the brand's own eight content cards remain image-free by design.

### Rendering

```
python scripts/slide_lint.py carousel.json          # must exit 0 first
python scripts/render_carousel.py carousel.json --out-dir out/ \
    [--format ig|linkedin|both] [--chromium /path/to/chrome]
```

Outputs, per format: `out/<slug>-ig-slide-01.png` … `-09.png` and
`out/<slug>-linkedin-slide-01.png` … `-09.png`, both at 1080×1350, plus
`out/<slug>-linkedin.pdf` (the slides compiled via Pillow, ready for
LinkedIn's document upload). Fonts and the mycelium mark are embedded as
base64 in each slide's HTML (self-contained); one Chromium instance renders
both decks. The renderer applies the widow gate automatically (merges a
last line of ≤6 characters) and reports when it does.

**Prerequisite — Playwright + Chromium:** `pip install playwright` then `playwright install chromium`. On a server also install the browser's system libraries once: `sudo playwright install-deps chromium` (or `playwright install --with-deps chromium`). If you can't use root (sandboxed), the browser still runs once the shared libs are on `LD_LIBRARY_PATH`. Point `--chromium` at a specific Chrome/Chromium build if you don't want Playwright's bundled one. Chromium is chosen deliberately: it renders the spec's WOFF2 natively and provides the CSS compositing the image layer needs.

### Bundled assets

```
assets/Geist-Medium.woff2        # Geist 500, OFL — content copy, wordmark, CTA
assets/Geist-Regular.woff2       # Geist 400, OFL
assets/Geist-Light.woff2         # Geist 300, OFL — slide numbers, labels
assets/mycelium-mark-olive.png   # transparent PNG, mark mapped to #6B7A3F
scripts/render_carousel.py       # the renderer (single source of truth for the brand spec)
scripts/slide_lint.py            # the density gate — run before every render
examples/carousel.example.json   # a complete 9-slide reference
examples/demo-image-slide.json   # image-background compositing demo
```

If `Geist-Medium.woff2` is missing: `npm pack geist && tar -xzf geist-*.tgz
&& cp package/dist/fonts/geist-sans/Geist-Medium.woff2 assets/`.

The mark asset was produced from `curAItion_Logo_Image.jpg` by stripping light pixels to transparent and mapping dark pixels to olive #6B7A3F. To regenerate it, see *Regenerating the mark* below.

---

## Layer 4: Packaging and Ingestion

### HTML Preview (review artefact)

Generate a single-file `carousel-[slug]-preview.html` that shows the nine PNGs as a horizontal strip with snap points, at mobile scale, so the carousel can be reviewed before publishing. Reference the PNGs by relative path. This is for editorial review only — the PNGs are the deliverable.

### Asset JSON (local provenance)

Save `carousel-[slug]-asset.json` capturing the full record: title, subtitle, source_content_id, domain, narrative_structure, the caption, and per-slide `{position, slide_function, type, copy | chart_data, png_file, production_note}`, plus a `provenance[]` array of `{data_point, supplementary}`. This is the source of truth for iteration (Layer 5) — never regen from memory.

### LinkedIn is a manual upload

The LinkedIn PDF this skill produces has **no automated publish path**:
`output_platforms` carries a placeholder `linkedin` row (`publisher_class`
NULL, inactive, zero channels), the publishing package contains only
`instagram/`, and every produced asset on record is `instagram_carousel`.
A human uploads the PDF via LinkedIn's document icon. Package it, hand it
over, and say so — do not imply an automated post is coming.

### CurAItion Ingestion (optional) — prerendered endpoint ONLY

If publishing through CurAItion, ingest via multipart
**`POST /api/assets/prerendered`** on the CurAItion API. This is the only
correct route for finished artwork, and the reason is structural: the
publish renderer preserves slides untouched **only** when
`metadata.prerendered is True` (a strict identity check in
`renderer.py`, symbol `PRERENDERED_METADATA_KEY`); every other branch
composites overlay text onto a background photo, i.e. **redraws the deck**.
The generic asset path (`POST /api/assets`, or any
`curaition_asset_catalog` create) does not set that flag, so a deck
ingested that way is silently redesigned at publish time with no error.
There is no MCP tool for the prerendered endpoint today — call the API
directly.

Contract (verified against `web/routers/api/assets.py`):

| Field | Type | Notes |
|---|---|---|
| `files` | list of files | **Slide 1 first.** 2–10 slides |
| `caption` | form string | The post caption |
| `hashtags_json` | form string | JSON **array** string; leading `#` stripped server-side |
| `title` | form string | Display title |
| `cta_url` | form string | Appended to the caption at publish (`🔗 <url>`); lands on the **last slide only**. See the sequencing rule in Layer 6 |
| `created_by` | form string | Defaults `prerendered-ingest` |

- **Requires organization context**: API-key callers send
  `X-Organization-ID` (CurAItion org:
  `00000000-0000-4000-a000-000000000001`) or the call 400s.
- Everything is validated through `prepare_carousel_images` **before
  anything is written** — a bad slide leaves no half-built asset behind.
- On success the asset lands in **`review` status** with
  `metadata.prerendered = true` and waits indefinitely for a human.
- ORM/DB naming split: the Python attribute is `asset_metadata`, the
  physical column is `metadata`. Raw SQL against `asset_metadata` throws.

The endpoint's own docstring explains the design and belongs in your head:
Instagram's API has no draft — its only unpublished state is a media
container that expires after 24 hours and is invisible in the app. So the
review gate lives in CurAItion, and the asset waits there until a human
calls the publish endpoint.

For a purely local deliverable, skip ingestion.

---

## Layer 5: Editorial Iteration — Single-Slide Re-render

After the first pass the user will want to tweak a slide. This is now **cheap and deterministic** — no Replicate, no spend. A re-render is just running the renderer again for the affected slide(s).

### Triggers

"Regen/tweak/fix slide N", "punchier copy on slide 1", "change the chart to X", "slide 4 is clipping", "make the close line …", "reorder slides", "drop the chart".

### Procedure

1. **Load `carousel-[slug]-asset.json`** — the source of truth.
2. **Edit the target slide** in `carousel.json`: change `copy`, `font_size`, chart `bars`/`title`/`source`, or slide order. Preserve every other slide verbatim.
3. **Re-render.** Either re-run the whole deck (it's fast and guarantees consistency) or render a single slide by passing a one-slide JSON and copying the PNG into place. Prefer whole-deck re-render unless the deck is large.
4. **Update artefacts in lockstep:** the `carousel.json`, the asset JSON (update the slide's `copy`/`chart_data`/`png_file`; append a provenance entry `"Slide N re-rendered: <delta>"`), and the preview HTML (swap the `<img>` for that slide). If already ingested and still in `review`, re-ingest the full deck via `POST /api/assets/prerendered` (a fresh asset) rather than patching slides in place — the prerendered flag and validation only apply at ingest.
5. **Show the user** the re-rendered slide and confirm before the next change.

### Guardrails

- **No widows and no clipping** — after any copy change, re-check line breaks and longest-line length. Lower `font_size` before letting a line clip.
- **Never fabricate chart data** on a tweak. If the user asks for a number you can't cite, say so.
- **Never introduce imagery** to a content slide. If the user wants a picture, that's the image-gen skill's job (see below), and it produces its own separate slides.
- **Keep the arc coherent** — if a copy change breaks the one-idea-per-slide rule, split or rebalance.
- **Preserve provenance** — append, never delete.

---

## Layer 6: Publishing — the skill's downstream boundary

The skill's output ends at render + ingest. What happens next matters
because the ingest call is the last gate. The chain, verified live on
Issue 52 (23 Aug 2026):

```
render (this skill)
  → POST /api/assets/prerendered      → status: review        [human gate]
  → POST /api/assets/{id}/publish     → Celery publish_carousel
      dry_run=true   → validate only, status stays review, no trace
      dry_run=false  → live, IRREVERSIBLE
  → status: published + published_url
```

- Publishable statuses: `review`, `approved`, `failed`, `publishing`.
- The Instagram `media_publish` call carries **`max_retries=0`**,
  deliberately — a media container may expire during backoff. Never add
  retries.
- **Know what the dry run does and does not prove.** For a prerendered
  asset it only confirms S3 reachability and slide count (the renderer
  short-circuits and returns stored URLs). It does NOT re-validate the
  media spec (that ran at ingest only) and does NOT touch Instagram, so it
  never exercises the token. Real pre-flight assurance is two extra steps:
  `prepare_carousel_images(raw)` against the bytes in S3, and
  `InstagramPublisher().test_connection()` (read-only token/account check).

### Sequencing — Substack first

`cta_url` is baked into the Instagram caption at publish and the Substack
slug is not knowable until that post is live. Order: publish Substack →
set `cta_url` from the minted slug → publish Instagram. If ingesting
before the Substack post exists, leave `cta_url` **null** — a wrong link
is worse than a missing one, and a placeholder is easy to forget.

### Ops facts (runbook)

- **Substack publication split (live misconfiguration, flagged to Rick,
  not fixed):** `curaition-api-staging` has `SUBSTACK_PUBLICATION_URL =
  curaitedcrypto.substack.com`, but The Drop is `curaition.substack.com`.
  A default-client call 404s with `Draft not found`; pass
  `get_substack_client(publication_url="https://curaition.substack.com")`
  explicitly.
- **Instagram token:** a PAGE token (never expires) — but
  `data_access_expires_at` is a separate ~90-day clock (next lapse
  **2026-11-21**), and a token can show `expires_at: 0` yet stop working
  when it lapses. Both clocks are monitored (log-only alerting).

---

## Design Principles (Codified)

1. **The copy is the image.** With no photography, every slide's impact is the sentence and its breaks. Cut ruthlessly; one idea per slide.
2. **Restraint is the brand.** On the eight content cards: cream, olive, Geist, one mark. No gradients, no grain, no scrims, no drop shadows. (Scrims/duotone exist only in the optional image layer, which the brand cards never use.) If a slide feels busy, remove something.
3. **Centre and breathe.** Text sits just below centre with generous padding. Whitespace is a feature, not waste.
4. **Determinism over vibes.** The renderer owns the spec. Don't hand-tune CSS per carousel; change copy and data, not the brand system.
5. **The chart must earn its slot.** One chart, real numbers, cited. No decorative data.
6. **Slide 1 is a thumbnail.** On the grid it's the only slide visible — it must work standalone and open the story.
7. **The final slide is a signature, not a CTA dump.** Mark + wordmark, centred, calm. One URL. Nothing else.
8. **No widows, ever.** The single most common quality failure. Own your line breaks.
9. **`SPEC_BASELINE_H` is a denominator, not a canvas.** It equals `H_IG` today (1440 vs the 1350 canvas is the point: the spec's absolute values — watermark y=1412, chart baseline y=1246, tallest bar 396px — are authored against 1440). Folding it into `H_IG` silently re-scales every chart.
10. **Anchor chart furniture to the chart baseline, never the canvas bottom.** Half-proportional, half-absolute positions are the v3.1/v3.2 bug class.
11. **Never restore 1080×1440.** Below Meta's 4:5 floor; every deck at that canvas was un-postable.
12. **Prerendered artwork goes through `/api/assets/prerendered` only.** Any other create path omits the `prerendered` flag and the publish renderer silently redraws the deck (Layer 4).
13. **Measure, don't compute.** To check a layout relationship, render with and without the element and diff the ink rows, with a difference threshold above 100 — below ~24, antialiasing spread reads as ink and shifts band edges by several px.

---

## Regenerating the mark

If `assets/mycelium-mark-olive.png` is ever lost, recreate it from the brand source `curAItion_Logo_Image.jpg` (Drive) with PIL: convert to luminance, treat the light background as transparent (alpha = 255 − luminance, zero below ~8%), set every pixel's RGB to olive #6B7A3F, autocrop to the alpha bounding box, and downscale to ~600px wide. The mark is dark-on-white in the source, so no inversion is needed.

## Boundary With Image Generation

Image generation is a **separate companion skill**. The seam is intentional and now concrete: this skill owns the deterministic renderer *and* the `carousel.json` schema, including the optional `background` image layer (see *Image slides — renderer contract*). The image-gen skill's only job is to (a) generate an image and (b) emit a slide with a `background` block pointing at it — this renderer composites it. That keeps one renderer, one schema, and one brand system across both skills, whether they run in Cowork or self-hosted (e.g. Hermes-Agent, whose Tool Gateway can supply the generated images and whose Chromium already backs Playwright).

The brand's own **eight content cards stay image-free by design** — never place generated imagery behind them. Image-led slides are additional, distinct slides.

---

## File Naming Convention

```
carousel-[slug]-script.md       # Layer 2 production script
carousel-[slug].json            # Layer 3 render input (carousel.json)
carousel-[slug]-asset.json      # Layer 4 provenance record
carousel-[slug]-preview.html    # Layer 4 review strip
out/[slug]-slide-01.png …       # Layer 3 exported slides
```

## Quick Reference: Tools by Layer

| Layer | Tool | Purpose |
|-------|------|---------|
| 1 | `curaition_list_content` | Find candidate source content |
| 1 | `curaition_get_content` | Deep analysis with citations |
| 1 | `curaition_get_cited_themes` | Timestamped evidence |
| 1 | `curaition_trend_analysis` | Domain trend context |
| 1 | `WebSearch` | Supplementary research + citable chart data |
| 3 | `scripts/render_carousel.py` | Render carousel.json → 1080×1350 PNGs |
| 3 | Playwright + Chromium | Headless browser the renderer drives (WOFF2 + image compositing) |
| 4 | `POST /api/assets/prerendered` (CurAItion API, no MCP tool) | Ingest finished artwork for review — the ONLY route that preserves it |
| 5 | `scripts/render_carousel.py` | Re-render tweaked slide(s) |
| 6 | `POST /api/assets/{id}/publish` (human-invoked) | Publish from review; `dry_run=false` is irreversible |

---

*CurAItion Intelligence Desk · Carousel Producer · brand-rendered typography · renderer stage of the daily publishing chain · v3.3*
*Changelog v3.3: Documentation only — the renderer is untouched. Corrected the ingestion section, which named a tool that does not exist (`curaition_asset_registry`) and pointed at the generic asset path: the publish renderer preserves finished artwork ONLY when `metadata.prerendered is True`, a flag the generic path never sets, so a deck ingested as previously documented would have been silently redrawn at publish. The only correct route is multipart `POST /api/assets/prerendered` (full contract now in Layer 4, verified against the live endpoint and the Issue 52 publish). Added: the Instagram media-spec table (enforced at ingest ONLY — the publish path never re-validates geometry); Layer 6 covering the review gate, the dry run's blind spots, `max_retries=0` on `media_publish`, and the Substack-first `cta_url` sequencing; the LinkedIn manual-upload reality (no automated LinkedIn publish exists — placeholder platform row, no publisher class); ops runbook facts (staging Substack publication-URL split, Instagram token's separate `data_access_expires_at` clock, next lapse 2026-11-21); and five new design principles folding in the guardrails (SPEC_BASELINE_H is a denominator, baseline-anchored chart furniture, never 1440, prerendered-only ingest, measure-don't-compute).*
*Changelog v3.2: Fixed the chart source caption's anchor. It was positioned from the canvas bottom by `round(70 * scale) + 40` — a mixed anchor whose `+ 40` did not scale — while the category labels above it are anchored proportionally to the chart baseline. Shrinking the canvas 1440 → 1350 in v3.1 therefore moved the labels down toward a caption that barely moved, cutting the clearance between them from **15px to 7px** (measured, not computed: rendered with and without the `source` field and diffed, so the caption rows are isolated exactly). It never actually overlapped — the earlier report of a collision was wrong, from approximate arithmetic that guessed at descender and line-height. The caption is now anchored to the chart baseline like the labels (`CHART_SOURCE_DY = 68`), restoring **25px** of clearance and making it canvas-height independent; `line-height` is pinned at 1.2 because the UA default is font-dependent and left the box height unassertable. Blast radius verified: of the 9-slide example deck only the chart slide changes, and a chart with no `source` renders byte-identical. Same bug class as v3.1's `SPEC_BASELINE_H` split — a layout value that is half proportional and half absolute.*
*Changelog v3.1: The Instagram canvas moved 1080×1440 → **1080×1350**. Instagram's Content Publishing API accepts aspect ratios between 4:5 (0.800) and 1.91:1 only, and the old 3:4 (0.750) canvas sat below that floor — every IG deck this skill has ever produced was un-postable through the API, and would have been cropped by Instagram had it gone through. The two formats now share a canvas and differ only in the final slide's follow line and the LinkedIn PDF compile. **No redesign:** geometry is fraction-based, so the IG slides now render byte-identical to the already-approved LinkedIn slides (verified: 9/9 identical, slide 9 excepted). Internally `SPEC_BASELINE_H = 1440` was split out of `H_IG` — the spec's absolute values (watermark y=1412, chart baseline y=1246, tallest bar 396px) are authored against 1440 and are the *denominator*, not a canvas. They were the same number until now; folding them back together silently re-scales every chart. GBrain `curaition/daily-publishing-prompt` is canonical and carries this change.*
*Changelog v3.0: Synchronised with the canonical publishing spec (GBrain `curaition/daily-publishing-prompt` 16 Aug 2026 + `curaition/carousel-slide-density` 15 Aug 2026). Content type is now Geist Medium 500 at 66px / 1.31 (was Regular 108px / 1.08); max 3 lines per slide with the hook capped at 2; slide numbers are N/9 at 28px; watermark is 32px at 96.9% height; chart is SVG rects in sage #9CAF7A on a stone baseline at 86.5% with a left-aligned title; final slide is the 40px mark + 42px Geist Medium wordmark, all olive, with the Substack CTA, plus a LinkedIn variant with the follow line. Added the LinkedIn 1080×1350 PNG + PDF output, the density lint (`slide_lint.py`), the automatic widow gate, and the one-line IG caption spec. GBrain is canonical for all of the above; this file mirrors it.*
*Changelog v2.1: Renderer moved from wkhtmltoimage to Playwright/Chromium — restores base64 WOFF2 per spec (no TTF fallback) and adds an optional `background` image-composite layer (cover/focal/duotone/scrim/blur/dim + text-colour override) so the future image-gen skill integrates through the same carousel.json. One browser renders the whole deck. Runtime-agnostic: identical output under Cowork or self-hosted (Hermes-Agent).*
*Changelog v2.0: Replaced the AI-imagery pipeline (Flux/Wan, frame extraction, gradient overlays, Bebas Neue) with a deterministic olive-on-cream Geist brand renderer. Added bundled Geist + mycelium mark, a data-chart slide, and a final brand lockup slide.*
