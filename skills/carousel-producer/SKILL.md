---
name: carousel-producer
description: "Produce brand-locked Instagram carousels from CurAItion cultural intelligence — deterministic, typographic, image-free. Pulls the most compelling narrative thread via CurAItion MCP tools, writes an editorial script, then renders 8 content slides + 1 final brand slide as 1080x1440 PNGs (olive-on-cream Geist typography, mycelium watermark, one story-specific data chart) via a bundled Chromium (Playwright) renderer. No AI image generation — visual richness comes from copy, data, and brand system. Use when the user asks to create a carousel, Instagram post series, visual story, or slide-based content from CurAItion data. Also trigger for 'make a carousel from this episode', 'turn this into slides', 'create an Instagram series', 'regen slide N', 'tweak slide N', 'change the chart', or any request combining CurAItion content analysis with brand-rendered carousel production or editorial iteration on a previously-produced carousel."
---

# CurAItion Carousel Producer (Brand Render)

You produce Instagram carousels that turn CurAItion cultural intelligence into scroll-stopping **typographic** narratives, rendered in the CurAItion brand system. Each carousel is a text-first editorial sequence grounded in real data — themes, entities, relationships, citations — and rendered as pixel-deterministic PNGs.

This skill is deliberately **image-free**. Content slides are pure typography; the only graphic slide is one story-specific data chart. AI image generation is a **separate concern** handled by a future companion skill — see *Boundary With Image Generation* at the end. Do not generate, fetch, or place photographic/AI imagery behind this typography; the brand is anti-image on content slides (clean cream, olive text, no scrim).

The pipeline has four working layers plus an iteration layer. Layers 1–2 are editorial intelligence (unchanged in spirit from prior versions). Layer 3 is deterministic brand rendering. Layer 4 packages and (optionally) ingests. Layer 5 is cheap single-slide iteration.

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

The copy is the entire visual. These rules are tuned for large centred Geist on cream:

1. **One idea per slide.** Each slide delivers exactly one beat. Never two.
2. **Hard line breaks, and you own every one.** Write copy with explicit `\n`. The renderer breaks only where you tell it. Every break is a beat.
3. **No widows.** Never leave a lone short word on the last line. Because you control breaks, this is an editorial obligation — rebalance the lines. (Old-WebKit rendering has no auto-balance; the fix is your line breaks.)
4. **Fit the frame.** Default size is **108px**. At 108px, a line of ~16–18 characters fills the safe width (side padding is 104px). Keep the longest line under ~18 characters, or lower `font_size` for that slide (e.g. 92–100px) — never let a line clip. Aim for ≤ 6 lines.
5. **Sentence case, not caps.** Geist on cream reads as calm editorial, not shouty overlay. Do **not** uppercase. (This is a deliberate reversal of the old overlay aesthetic.)
6. **Numbers do the work.** "168 vs 80,000" beats any adjective. Lead with specifics.
7. **Staccato for character.** "Illiterate. Illegitimate. Nearly 60." Fragments build a person fast.
8. **Primary-source quotes cut through.** Use devastating period voice verbatim; label the source in the production note.
9. **End on a mirror or a question.** The last content slide (CLOSE) echoes the hook with the weight of the whole story behind it.

### The Chart Slide

One chart, positioned 3–5, only if there's a citable figure. Keep it honest and sparse:
- 3–6 bars maximum. More than 6 and the labels crowd.
- Values are real and cited. Put the citation in the `source` field (renders small at the bottom) **and** in provenance.
- Title is a short declarative phrase (≤ 2 lines), not a caption.
- The renderer handles all styling (olive bars, sparse grid, ghosted mark). You supply only title, `{label, value}` pairs, unit, and source.

### Caption Writing

The Instagram caption follows the same arc, compressed: **Hook** (restate the premise), **Build** (3–4 short paragraphs of specifics — names, numbers), **Land** (the thematic punchline, often the CLOSE line), **Credit** (@ mention the source creator), **Hashtags** (8–12, mixing broad and specific). Facts first, emotion second. The caption stands alone for non-swipers.

---

## Layer 3: Brand Rendering

This layer is deterministic. Given a `carousel.json`, the bundled renderer produces identical PNGs every time. No model-in-the-loop image decisions.

### The Brand Spec (authoritative)

| Token | Value |
|-------|-------|
| Canvas | **1080 × 1440px**, PNG, rendered by headless Chromium (Playwright) |
| Text / bars / mark | Olive **#6B7A3F** |
| Background | Cream **#F1EFE8** |
| Slide numbers, light labels | Stone **#C8C3B4** |
| Primary type | **Geist Regular (400)** — content copy, chart values, wordmark |
| Secondary type | **Geist Light (300)** — slide numbers, chart labels, curaition.xyz |

**Content slide:** olive copy on cream, centred, default **108px**, line-height 1.08. Text block sits **slightly below vertical centre** (padding 180px top / 130px bottom → optical centre ≈ 25px below middle). Slide number **top-right**, two digits (`01`…`08`), Geist Light 300, stone #C8C3B4. Mycelium mark **~62px wide, centred at the bottom**.

**Chart slide:** olive bars on cream, sparse horizontal grid (5 faint lines at 0/25/50/75/100%), Geist value labels above bars (Regular) and category labels below (Light), title top-centre (Regular olive), source line bottom (stone), slide number top-right. A **ghosted mycelium mark at 5% opacity** sits behind the plot area. **No decorative grain, no overlays, no bottom watermark** on this slide (the ghost mark is the brand cue).

**Final slide (slide 9):** the mark (~90px) and the **"curAItion"** wordmark (90px, Geist Regular 400) as a **horizontal inline lockup, truly centred** on the slide. **"curaition.xyz"** in Geist Light 300, small, centred at the bottom. Cream background, **no scrim, no dark background**.

> **Font note:** fonts are embedded as base64 **WOFF2** per spec — Chromium decodes WOFF2 data-URIs natively (verified). (History: an earlier wkhtmltoimage/Qt-WebKit renderer could not decode WOFF2 and needed a TTF fallback; the move to Chromium removed that compromise.)

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
- Slide numbers auto-fill (two-digit, by position) for `content`/`chart`. Override with `n` if needed. `final` has no number.
- `font_size` (content) overrides the 108px default for a single slide — use it to prevent clipping on long lines.
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
python scripts/render_carousel.py carousel.json --out-dir out/ [--chromium /path/to/chrome]
```

Outputs `out/<slug>-slide-01.png` … `-slide-09.png` at 1080×1440. Fonts and the mycelium mark are embedded as base64 in each slide's HTML (self-contained); one Chromium instance renders the whole deck.

**Prerequisite — Playwright + Chromium:** `pip install playwright` then `playwright install chromium`. On a server also install the browser's system libraries once: `sudo playwright install-deps chromium` (or `playwright install --with-deps chromium`). If you can't use root (sandboxed), the browser still runs once the shared libs are on `LD_LIBRARY_PATH`. Point `--chromium` at a specific Chrome/Chromium build if you don't want Playwright's bundled one. Chromium is chosen deliberately: it renders the spec's WOFF2 natively and provides the CSS compositing the image layer needs.

### Bundled assets

```
assets/Geist-Regular.woff2       # Geist 400, OFL
assets/Geist-Light.woff2         # Geist 300, OFL
assets/mycelium-mark-olive.png   # transparent PNG, mark mapped to #6B7A3F
scripts/render_carousel.py       # the renderer (single source of truth for the brand spec)
examples/carousel.example.json   # a complete 9-slide reference
examples/demo-image-slide.json   # image-background compositing demo
```

The mark asset was produced from `curAItion_Logo_Image.jpg` by stripping light pixels to transparent and mapping dark pixels to olive #6B7A3F. To regenerate it, see *Regenerating the mark* below.

---

## Layer 4: Packaging and Ingestion

### HTML Preview (review artefact)

Generate a single-file `carousel-[slug]-preview.html` that shows the nine PNGs as a horizontal strip with snap points, at mobile scale, so the carousel can be reviewed before publishing. Reference the PNGs by relative path. This is for editorial review only — the PNGs are the deliverable.

### Asset JSON (local provenance)

Save `carousel-[slug]-asset.json` capturing the full record: title, subtitle, source_content_id, domain, narrative_structure, the caption, and per-slide `{position, slide_function, type, copy | chart_data, png_file, production_note}`, plus a `provenance[]` array of `{data_point, supplementary}`. This is the source of truth for iteration (Layer 5) — never regen from memory.

### CurAItion Ingestion (optional)

If publishing through CurAItion, ingest via `curaition_asset_registry (action: "create", …)` with `asset_type: "instagram_carousel"`. Registry essentials (verified schema): top-level `title`, `source_content_id`, `narrative_angle`, `caption`, `hashtags[]`; per-slide `image_url_original` (the hosted PNG URL — upload happens in the publishing pipeline, not here), `media_type: "image"`, and `cta_url` on the final slide; `provenance[]` as `{data_point, supplementary}` (not `data_lineage`). For a purely local deliverable, skip ingestion. Verify any create with `action: "get"`.

> Note: these carousels have no motif/prompt fields and no video/frame fields — those belonged to the retired AI-imagery pipeline. `image_prompt` is not required for image-free slides; if the registry still mandates a non-null string, pass a bracketed placeholder describing the slide (e.g. `"[typographic content slide — no image]"`).

---

## Layer 5: Editorial Iteration — Single-Slide Re-render

After the first pass the user will want to tweak a slide. This is now **cheap and deterministic** — no Replicate, no spend. A re-render is just running the renderer again for the affected slide(s).

### Triggers

"Regen/tweak/fix slide N", "punchier copy on slide 1", "change the chart to X", "slide 4 is clipping", "make the close line …", "reorder slides", "drop the chart".

### Procedure

1. **Load `carousel-[slug]-asset.json`** — the source of truth.
2. **Edit the target slide** in `carousel.json`: change `copy`, `font_size`, chart `bars`/`title`/`source`, or slide order. Preserve every other slide verbatim.
3. **Re-render.** Either re-run the whole deck (it's fast and guarantees consistency) or render a single slide by passing a one-slide JSON and copying the PNG into place. Prefer whole-deck re-render unless the deck is large.
4. **Update artefacts in lockstep:** the `carousel.json`, the asset JSON (update the slide's `copy`/`chart_data`/`png_file`; append a provenance entry `"Slide N re-rendered: <delta>"`), and the preview HTML (swap the `<img>` for that slide). If ingested, `curaition_asset_registry (action: "update")` with the full slides array, then `get` to verify.
5. **Show the user** the re-rendered slide and confirm before the next change.

### Guardrails

- **No widows and no clipping** — after any copy change, re-check line breaks and longest-line length. Lower `font_size` before letting a line clip.
- **Never fabricate chart data** on a tweak. If the user asks for a number you can't cite, say so.
- **Never introduce imagery** to a content slide. If the user wants a picture, that's the image-gen skill's job (see below), and it produces its own separate slides.
- **Keep the arc coherent** — if a copy change breaks the one-idea-per-slide rule, split or rebalance.
- **Preserve provenance** — append, never delete.

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
| 3 | `scripts/render_carousel.py` | Render carousel.json → 1080×1440 PNGs |
| 3 | Playwright + Chromium | Headless browser the renderer drives (WOFF2 + image compositing) |
| 4 | `curaition_asset_registry` (`create`/`get`) | Optional ingestion + round-trip verify |
| 5 | `scripts/render_carousel.py` | Re-render tweaked slide(s) |
| 5 | `curaition_asset_registry` (`update`/`get`) | Persist iteration if ingested |

---

*CurAItion Intelligence Desk · Carousel Producer · brand-rendered typography · renderer stage of the daily publishing chain · v2.1*
*Changelog v2.1: Renderer moved from wkhtmltoimage to Playwright/Chromium — restores base64 WOFF2 per spec (no TTF fallback) and adds an optional `background` image-composite layer (cover/focal/duotone/scrim/blur/dim + text-colour override) so the future image-gen skill integrates through the same carousel.json. One browser renders the whole deck. Runtime-agnostic: identical output under Cowork or self-hosted (Hermes-Agent).*
*Changelog v2.0: Replaced the AI-imagery pipeline (Flux/Wan, frame extraction, gradient overlays, Bebas Neue) with a deterministic olive-on-cream Geist brand renderer. Added bundled Geist + mycelium mark, a data-chart slide, and a final brand lockup slide.*
