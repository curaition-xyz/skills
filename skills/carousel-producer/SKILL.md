---
name: carousel-producer
description: "Produce Instagram carousels from CurAItion cultural intelligence — and iterate on them cheaply. Automatically detects whether the source is a video (extracts real frames via CurAItion's hybrid pipeline) or a podcast/article (generates all imagery via Replicate). Takes a content source, extracts the most compelling narrative thread via CurAItion MCP tools, writes an editorial script with art direction, generates AI images (Flux Schnell) and animations (Wan 2.2), packages everything into a preview HTML and SPEC-2026-004 asset JSON, and ingests the finished asset back into CurAItion. Includes a single-slide regen loop (Layer 5) for editorial iteration without rerunning the whole pipeline. Use when the user asks to create a carousel, Instagram post series, visual story, or slide-based content from CurAItion data. Also trigger for 'make a carousel from this episode', 'turn this into slides', 'create an Instagram series', 'regen slide N', 'tweak slide N', 'I don't like slide N', or any request combining CurAItion content analysis with visual production or editorial iteration on a previously-produced carousel."
---

# CurAItion Carousel Producer

You produce Instagram carousels that turn CurAItion cultural intelligence into scroll-stopping visual narratives. Each carousel is a 7–10 slide story grounded in real data — themes, entities, relationships, citations — then rendered with typographic overlays.

The pipeline automatically detects the source type and selects the right image strategy:
- **Video sources** → hybrid pipeline: real YouTube frames (extracted and assessed server-side) + AI-generated backfill for gaps
- **Podcast / Article sources** → standard pipeline: all imagery generated via Replicate

The pipeline has four layers. Every carousel passes through all four, in order.

---

## Layer 1: CurAItion Analytical Substrate

Before any creative work, extract the intelligence layer from CurAItion. This is the foundation everything else sits on.

### Step 1: Source Selection

If the user specifies a content source, use it. If they say "pick something interesting," run discovery:

```
curaition_list_content → recent content in the target domain(s)
curaition_get_content (include_citations: true) → full analysis for 2–3 candidates
```

**Selection criteria** (rank candidates by these, in order):
1. **Narrative arc potential** — Does it contain a story with setup, tension, and resolution?
2. **Visual richness** — Can you see the images in your head as you read the analysis?
3. **Hook strength** — Is there a single detail or statistic that would stop a scroll?
4. **Theme weight** — Prefer themes with CurAItion weight ≥ 0.80
5. **Citation density** — More timestamped citations = more material to work with

### Step 2: Deep Analysis Pull

For the chosen source, extract everything:

```
curaition_get_content (content_id, include_citations: true)
```

From the response, harvest:
- **Themes** with weights (these become the narrative spine)
- **Entities** with significance scores (these become characters)
- **Relationships** between entities (these become plot points)
- **Cultural references** (these become contextual bridges)
- **Timestamped citations** (these ground claims in evidence)
- **Domain trends** (these provide the "why now" framing)
- **Embed data** (thumbnail_url, source_url — for provenance tracking)
- **Video ID** (`video_platform_video_id` — present for YouTube videos, null for articles)
- **Duration** (`duration_seconds` — used for source classification)

### Step 2.5: Source Classification

Before proceeding to Layer 2, classify the source to determine the Layer 3 image strategy. The `curaition_get_content` response contains the signals:

| Field | Video Signal | Podcast Signal | Article Signal |
|-------|-------------|----------------|----------------|
| `content_type` | `"video"` | `"video"` (podcasts on YouTube) | `"article"` |
| `video_platform_video_id` | Present (e.g., `"SDMdkgEJsRs"`) | May be present | Null |
| `duration_seconds` | Typically < 1800 | Typically > 1800 | Null |

**Classification logic:**

```
IF content_type == "article" OR video_platform_video_id is null:
  → ARTICLE path (standard pipeline — all Replicate)

ELSE IF content_type == "video" AND video_platform_video_id is present:
  IF duration_seconds > 2400 (40+ minutes):
    → Likely PODCAST — check title/description for podcast/interview indicators
    → If podcast format confirmed → PODCAST path (standard pipeline)
    → If unclear → extract 3 test frames via analyze_frames to assess visual quality
  ELSE:
    → VIDEO path (hybrid pipeline — extract frames + backfill)
```

**This is editorial judgment, not a hard rule.** The user can override — e.g., "make a carousel from this podcast" means skip frame extraction regardless. Or "use real frames from this interview" means use the hybrid pipeline even for long-form content.

Record the classification in the production script: `**Source type:** VIDEO / PODCAST / ARTICLE`

### Step 3: Supplementary Research

CurAItion provides the analytical substrate, but carousels need narrative detail that goes beyond content analysis. Use `WebSearch` to fill gaps:

- Biographical details for key entities (dates, titles, origins)
- Historical context that the source content may reference but not explain
- Specific numbers, statistics, or quotes from primary sources
- Visual reference for art direction (what did this person/place/event actually look like?)

**Label everything.** In the production script and asset JSON, every data point gets tagged as either `CurAItion analysis` or `Supplementary` (web research). This is non-negotiable — it's the provenance chain.

---

## Layer 2: Editorial Intelligence

This is where raw analysis becomes a story. You are writing a production script — a detailed creative brief that specifies every slide's copy, image prompt, animation direction, and production notes.

### The Production Script Format

```markdown
# CAROUSEL PRODUCTION SCRIPT

## [Title]
*[Subtitle — the narrative angle in one line]*

---

## THE SIGNAL
**Source:** [title] — [creator/channel]
**Content ID:** [UUID]
**CurAItion Domain:** [domain]

[List all extracted themes, relationships, cultural references, domain trends]

**Narrative angle:** [2–3 sentences describing WHAT this carousel is about
 and WHY it's not just a summary of the source]

---

## ART DIRECTION
### Master Motif: [Name]
[Description of the visual world every image inhabits]

**Style keywords (apply to ALL slides):**
[Bulleted list of visual constraints]

**Motif prompt template:**
[The reusable prefix/suffix that bookends every image prompt]

---

## SLIDES
### SLIDE N — [FUNCTION] (ANIMATED if applicable)
**Overlay copy:**
> [The text that appears on the slide]

**Timestamp hint:** [seconds] (VIDEO sources only — the citation timestamp that best represents this slide's content moment. Used for frame matching in the hybrid pipeline.)

**Image prompt:**
[Full prompt including motif prefix and suffix]

**Animation prompt:** (if animated)
[Subtle motion direction]

**Production note:**
[Why this slide exists, what CurAItion data it draws from, editorial intent]

---

## OVERARCHING POST / CAPTION
> [Instagram caption with hashtags and source credit]

---

## DATA PROVENANCE
| Data Point | Source | Tool |
|---|---|---|
| [item] | [CurAItion analysis / Web research] | [tool name] |
```

### Narrative Architecture

Every carousel follows a dramatic arc. Two primary structures exist:

**LINEAR-HERO** — A single protagonist's journey (used for the Boswell/Corsica carousel):
Person → Action → Consequence → Legacy. One POV drives the whole arc.

**LINEAR-HERO (dual protagonist)** — A variant where two protagonists occupy different halves of the arc (used for the Carthage carousel):
Protagonist A drives act 1 (the ideologue, the instigator). Protagonist B inherits act 2 (the executor, the inheritor). The dramatic irony is that B achieves exactly what A demanded — and realises it was the wrong question. Use when the story's power comes from the gap between wanting something and getting it.

**CONVERGENT-OPPOSITION** — Two forces on a collision course (used for the Cajamarca carousel):
Introduce Force A → Introduce Force B → Show the gap between them → Collision → Aftermath. The tension comes from the audience seeing what neither side can see.

Choose the structure based on the source material. If the story has one protagonist, use LINEAR-HERO. If it has a hand-off between an instigator and an executor, use dual-protagonist LINEAR-HERO. If it has two forces whose collision IS the story, use CONVERGENT-OPPOSITION.

**Slide functions** (not every carousel uses all of these):

| Function | Purpose | Example |
|----------|---------|---------|
| **HOOK** | Stop the scroll. One striking detail, number, or image. Almost always animated. | "168 men walked into a plaza..." |
| **PROTAGONIST** | Introduce the main character with staccato details | "Illiterate. Illegitimate. Nearly 60." |
| **ANTAGONIST** | Introduce the opposing force with power metrics (CONVERGENT-OPPOSITION only) | "He commanded 80,000 soldiers." |
| **CONTEXT** | The "wait, what?" — a surprising fact that reframes everything | "A tiny island wrote the most democratic constitution in Europe." |
| **DECISION** | The fateful choice that sets dominoes falling | "He told his soldiers to come unarmed." |
| **ESCALATION** | Build tension. Stack details. Raise stakes. | "They could hear the army approaching. Singing." |
| **PIVOT** | The moment everything changes — often the carousel's central image | "He held it to his ear. Nothing happened. He threw it on the ground." |
| **CLIMAX** | The peak of action or revelation | "Not one Spaniard died." |
| **LEGACY** | Connect the specific story to a universal pattern | "Byron did it in Greece. Hemingway in Spain." |
| **CLOSE** | Mirror the hook. Land the theme. Modern bridge to audience. Almost always animated. | "Sound familiar?" / "That's how empires fall." |
| **CTA** | Drive viewers to the source content. Always the final slide. Branded, clean, minimal. | "Listen to the full episode → @therestishistorypod" |

**7–10 narrative slides + 1 CTA slide is the range (8–11 total).** The arc matters more than the count. Each narrative slide earns its place by delivering exactly one idea or emotional beat. The CTA slide always comes last and is not part of the narrative arc.

### Overlay Copy Rules

These rules are derived from what works on Instagram at scale:

1. **Uppercase everything.** Use `text-transform: uppercase` in the HTML preview and write copy that reads well in caps. Condensed display fonts (Bebas Neue, Oswald, Barlow Condensed) are purpose-built for this.

2. **Maximum 8 lines per slide.** If you can't say it in 8 lines, split it across two slides. Less text = more visual impact. Instagram is a visual platform — the image does most of the work.

3. **Short lines, hard breaks.** Write in fragments, not sentences. Control where lines break. Every line break is a beat.

4. **One idea per slide.** Each slide earns its place by delivering exactly one piece of information or one emotional beat. Never two.

5. **Numbers do the work.** "168 men vs. 80,000 soldiers" is more powerful than any adjective. Lead with specifics.

6. **Staccato for character.** "Illiterate. Illegitimate. Nearly 60 years old." — three-word fragments build a person faster than a paragraph.

7. **End on a question or mirror.** The last slide should echo the first, with the weight of the whole story behind it. "Sound familiar?" or "That's how empires fall." — the audience fills in the rest.

8. **Typographical contrast.** Vary weight or size within a slide to create visual hierarchy. The first line (character name, date, or location) is the anchor. The body fills in around it.

9. **Primary source quotes cut through.** When a historical source says something devastating ("Many of us urinated from sheer terror"), use it verbatim. Authentic period voice is more powerful than any paraphrase. Label the source in the production note.

10. **Cultural references serve the arc, not the decor.** Only surface a cultural reference in copy if it directly advances the argument (Byron/Hemingway establishing a pattern). If CurAItion extracts references that don't serve the narrative, keep them as analytical scaffolding in production notes — don't force them into slides.

### Caption Writing

The Instagram caption follows the same dramatic arc as the slides, compressed:

1. **Hook** — Restate the central premise in one punchy line
2. **Build** — 3–4 short paragraphs that walk through the key moments (specific facts, names, numbers)
3. **Land** — The emotional or thematic punchline (often the same line as the CLOSE slide)
4. **Credit** — Source attribution with @ mention
5. **Hashtags** — 8–12 relevant tags, mix of broad (#history) and specific (#cajamarca)

**Caption principles:**
- Facts first, emotion second. Let the specifics do the emotional work.
- Mirror the slide copy's cadence — short paragraphs, hard breaks, staccato rhythm.
- The caption should stand alone — someone who doesn't swipe should still get the story.
- Always credit the source content creator with an @ mention.

### Typography Specification

```css
/* PRIMARY — overlay copy */
font-family: 'Bebas Neue', 'Barlow Condensed', 'Oswald', sans-serif;
font-size: 1.45rem;        /* ≈ 24–26px at standard viewport — minimum for mobile readability */
line-height: 1.2;
letter-spacing: 0.06em;
text-transform: uppercase;
text-align: justify;
text-align-last: left;

/* SECONDARY — slide numbers, attributions, small labels */
font-family: 'Barlow Condensed', 'Inter', sans-serif;
font-weight: 500;
font-size: 0.7rem;
letter-spacing: 0.12em;
text-transform: uppercase;
```

**Why these choices:**
- **Bebas Neue** is bold + condensed — it grabs attention and occupies less horizontal space, exactly what you need for text overlaid on images
- **Uppercase** is standard for Instagram carousel overlays — it reads faster at small sizes and creates visual uniformity
- **1.45rem minimum** ensures readability on mobile (Instagram's primary surface). Never go below 24px equivalent
- **Justify with left-aligned last line** creates clean text blocks without ragged right edges, while the final line looks natural
- **0.06em letter-spacing** prevents uppercase text from feeling cramped

### Safe Zones and Layout

Instagram crops carousel images differently depending on context (feed, profile grid, explore). Design with these constraints:

```
Canvas: 1080 × 1350px (4:5 portrait) — ALWAYS use this ratio
  ┌─────────────────────────────┐
  │     TOP UNSAFE ZONE         │  ← Top 270px may be cropped on profile grid
  │     (no critical content)   │
  ├─────────────────────────────┤
  │                             │
  │     SAFE CONTENT AREA       │
  │                             │
  │  ┌───────────────────────┐  │
  │  │   TEXT BLOCK           │  │  ← 60px padding from all edges minimum
  │  │   (bottom half)        │  │  ← Text lives in bottom 50% of frame
  │  │                        │  │  ← Under gradient overlay
  │  └───────────────────────┘  │
  │                             │
  ├─────────────────────────────┤
  │     BOTTOM UNSAFE ZONE      │  ← Bottom 270px may be cropped on profile grid
  │     (no critical content)   │
  └─────────────────────────────┘
```

- **60px minimum padding** from left, right, and bottom edges
- **Text occupies the bottom 40–50%** of the frame, under a gradient overlay
- **Top 270px and bottom 270px** are unsafe zones (cropped in profile grid view) — avoid placing critical text here
- **The image is the hero.** Text is secondary. If you're covering more than 40% of the image with text, you have too much copy.

### Gradient Overlay

The text sits on a gradient that transitions from transparent (top of text area) to near-opaque (bottom). This ensures readability without obscuring the full image:

```css
.overlay {
  background: linear-gradient(
    to bottom,
    rgba(10, 10, 8, 0) 0%,
    rgba(10, 10, 8, 0.05) 25%,
    rgba(10, 10, 8, 0.4) 50%,
    rgba(10, 10, 8, 0.82) 70%,
    rgba(10, 10, 8, 0.95) 100%
  );
}
```

**Text shadow** for additional contrast against the image:
```css
text-shadow:
  0 1px 3px rgba(0,0,0,0.9),
  0 2px 8px rgba(0,0,0,0.6),
  0 0 20px rgba(0,0,0,0.4);
```

### Visual Consistency: The Motif Principle

> **The motif is far more important than what is shown in the image itself.**

Every carousel has a single visual motif — a consistent art style that unifies all slides into a coherent visual world. The motif is enforced through a **prompt template** that bookends every image prompt:

```
[MOTIF PREFIX] [SUBJECT-SPECIFIC MIDDLE] [MOTIF SUFFIX]
```

**Example — Cajamarca carousel:**
- Prefix: `Woodcut illustration in the style of a 16th-century chronicle of the New World of`
- Suffix: `Heavy crosshatched dark sepia ink on aged yellowed vellum parchment. Dense dramatic composition with deep shadows and high contrast. Slightly naive perspective, pre-modern spatial depth. Vertical 4:5 portrait composition. No colour, pure dark sepia and aged parchment tones only. Vignette edges. 16th century book illustration, woodcut engraving, no photorealism, no painting, no watercolour, no digital art.`

**Example — Boswell carousel:**
- Suffix: `Copperplate engraving illustration style, fine crosshatched linework on aged parchment paper, warm sepia and ivory tones with selective Corsican blue and gold accents, vignette edges fading into the page, vertical 9:16 composition, atmospheric and romantic, 18th century book plate aesthetic.`

**Motif selection principles:**
- **Thematic resonance first.** The motif should *feel* like the story, not just depict it. The Cajamarca woodcut is rough and urgent — "dispatches from an impossible frontier." The Boswell copperplate is refined and romantic — matching the Georgian intellectual world. Choose an art style whose emotional grammar matches the narrative's emotional grammar.
- Match the era and subject (16th-century chronicle for conquistadors, Georgian copperplate for Boswell)
- Choose illustration over photography — it creates distance, romance, and visual unity
- Include negative constraints ("no photorealism, no painting, no digital art") to prevent style drift
- Specify the exact color palette in the suffix (sepia + vellum, blue + gold, etc.)
- Always specify `Vertical 4:5 portrait composition`

### Choosing Which Slides to Animate

Animate 2–4 slides per carousel. Place animations at **narrative beats**, not at fixed intervals:

- **Slide 1 (HOOK)** — almost always animated. Sets the mood.
- **Tension peak** — the slide where anticipation is highest (often slide 5 or 6)
- **Slide 9 (CLOSE)** — almost always animated. The image that lingers.
- **Optionally** one mid-carousel slide where motion adds emotional weight

Animation is "very subtle gentle movement" — not full motion video. Think "living painting."

### The CTA Slide (Always Final)

Every carousel ends with a Call-to-Action slide that drives viewers to the source content. This is non-negotiable — it's how we credit creators and convert casual scrollers into listeners/readers.

**The CTA slide is a separate slide AFTER the CLOSE.** The CLOSE lands the emotional/thematic punchline. The CTA is the practical handoff — "here's where to get more."

**CTA slide structure:**
```
[Source content artwork/logo/motif image — NOT a new AI generation]

LISTEN TO THE FULL EPISODE

[Source title in quotes]

→ @[creator handle]

[Podcast/channel logo or wordmark if available]
```

**CTA design rules:**
1. **Clean and branded** — this slide breaks the carousel's visual motif intentionally. It's a functional slide, not a narrative one. Use a dark or muted background with high-contrast text.
2. **One action only** — "Listen to the full episode" or "Watch the full video" or "Read the full article." Never "follow us AND listen AND subscribe."
3. **Creator handle prominent** — the @ mention is the primary link mechanism on Instagram. Make it large enough to tap.
4. **Episode/article title in quotes** — helps viewers find the specific piece of content.
5. **No AI-generated image** — use the source content's thumbnail, album art, or a branded template. If none available, use the carousel's motif with reduced opacity as a textured background.
6. **Not animated** — the CTA slide is static. Animation belongs to narrative slides.

**This means carousels are 8–11 slides total:** 7–10 narrative slides + 1 CTA slide.

**CTA copy examples:**
- `🎧 LISTEN TO THE FULL EPISODE\n\n"Victory Wasn't Enough:\nRome's Most Ruthless Decision"\n\n→ @therestishistorypod`
- `📺 WATCH THE FULL VIDEO\n\n"How Carthage Fell"\n\n→ @historyhit`
- `📖 READ THE FULL ARTICLE\n\n"The Destruction of Carthage"\n\n→ @historydotcom`

**The motion should reflect the emotional state of the slide:**
- **Awe/stillness** (hook, establishing shots): slow celestial motion — clouds drifting, light shifting
- **Tension/fear** (escalation, approach): nervous micro-movements — grips tightening, tails flicking, dust motes in shafts of light
- **Aftermath/melancholy** (close, resolution): lonely environmental motion — pages turning in wind, distant clouds, fading light

```
Animation prompt template:
"Very subtle gentle movement. [1–2 specific motions matched to
the slide's emotional state]. Almost still, like a living painting."
```

---

## Layer 3: Image Generation

Layer 3 branches based on the source classification from Step 2.5.

### VIDEO Path: Hybrid Pipeline (Frame Extraction + Backfill)

When the source is a video with `video_platform_video_id`, use CurAItion's server-side frame extraction to get real video frames, then fill gaps with AI-generated images.

**Step 3a: Extract Frames**

Collect the `timestamp_hint` values from each slide in the Layer 2 production script. These are the citation timestamps that best represent each slide's visual moment.

```
curaition_asset_registry(
  action: "extract_frames",
  source_content_id: "<content UUID>",
  timestamps: [25, 45, 71, ...],
  extraction_strategy: "auto"
)
→ Returns: { task_id, content_id, platform_video_id, status: "dispatched" }
```

This is an **async operation**. The backend dispatches a Celery task that downloads video segments, extracts frames via yt-dlp + ffmpeg, compresses to WebP, and uploads to S3. Frames are cached by video ID + timestamp — re-extracting the same video for a different carousel is near-instant.

**Step 3b: Poll for Completion**

```
curaition_asset_registry(
  action: "task_status",
  task_id: "<task_id from Step 3a>"
)
→ Returns: { task_id, status, result (when SUCCESS), date_done }
```

Poll every 5–10 seconds until `status` is `SUCCESS`. The `result` contains:
- `frames[]` — array of `{ timestamp_seconds, timestamp_display, s3_url, strategy, cached }`
- `frames_extracted` — count of successful extractions
- `failed_timestamps` — any timestamps where extraction failed

**Step 3c: Analyze Frames**

Send the extracted frames to CurAItion for Gemini 2.5 Flash vision analysis:

```
curaition_asset_registry(
  action: "analyze_frames",
  frames: [
    { s3_url: "https://...", timestamp_seconds: 25, citation_context: { theme: "...", weight: 0.95 } },
    { s3_url: "https://...", timestamp_seconds: 45 }
  ],
  source_content_id: "<content UUID>"
)
```

Returns per frame: `description`, `usability_score` (0.0–1.0), `visual_category` (`evidence_screenshot`, `talking_head`, `b_roll`, `data_visualization`, `title_card`, `transition`), `suggested_slide_function`, `theme_relevance[]`, `composition_notes`, `suggested_replicate_prompt`.

Returns batch-level: `recommended_frames` (indices with usability ≥ 0.5), `recommended_backfill_timestamps`, `coverage_assessment`, `visual_coherence_notes`.

**Usability thresholds:**
- 0.8–1.0: Strong — use directly
- 0.5–0.79: Usable with caveats
- 0.2–0.49: Weak — backfill candidate
- 0.0–0.19: Unusable — exclude

**Step 3d: Assign Frames to Slides**

```
curaition_asset_registry(
  action: "suggest_frame_assignment",
  frame_analyses: [...],
  slide_functions: ["HOOK", "CONTEXT", "PIVOT", "ESCALATION", "CLIMAX", "LEGACY", "CLOSE", "CTA"]
)
```

Returns per slide: `frame_index` (or `null` for BACKFILL), `confidence`, `reasoning`. Slides where `frame_index` is null need AI-generated images.

**Step 3e: Generate Backfill for Gap Slides**

For slides where `suggest_frame_assignment` returned `frame_index: null`, generate via Replicate. Use the `suggested_replicate_prompt` from the frame analysis, wrapped in the carousel's motif:

```
[MOTIF PREFIX] [suggested_replicate_prompt, refined] [MOTIF SUFFIX]
```

If the asset has already been created in the registry, use the batch endpoint:
```
curaition_asset_registry(
  action: "generate_backfill",
  item_id: "<asset UUID>",
  slide_positions: [3, 7],
  model: "black-forest-labs/flux-schnell",
  aspect_ratio: "4:5"
)
```

Otherwise, generate via Replicate directly with `aspect_ratio: "4:5"` and `output_format: "webp"`.

**Script writing with frame intelligence:**
- Frame `description` fields replace guessing from citation text — the script writer knows exactly what each frame shows
- `visual_category` helps choose overlay treatment (e.g., `data_visualization` needs minimal overlay vs. `b_roll` can have heavy text)
- `composition_notes` inform art direction decisions
- `visual_coherence_notes` from the batch analysis ground Replicate prompt style

**Three motif strategies for hybrid carousels:**

| Strategy | When to Use | Visual Result |
|----------|------------|---------------|
| **Documentary** | Social commentary, news | Raw frames + subtle AI backfill |
| **Stylized Overlay** | Brand content | Heavy overlay unifies both sources |
| **Full AI** | Historical, artistic | Frames as reference only, all AI rendered |

### PODCAST / ARTICLE Path: Standard Pipeline (Full Replicate)

When the source is a podcast or article (no extractable video frames), generate all slide images via Replicate.

**Still Images — Flux Schnell**

```
Endpoint: create_models_predictions
Parameters:
  model_owner: "black-forest-labs"
  model_name: "flux-schnell"
  Prefer: "wait"
  input:
    prompt: [full image prompt from production script]
    aspect_ratio: "4:5"
    output_format: "webp"
    output_quality: 90
    num_outputs: 1
    disable_safety_checker: true
  jq_filter: "{id, status, output, error}"
```

Generate all images in parallel (fire all 7–10 requests simultaneously). Each returns within 10–20s.

### Animated Slides — Wan 2.2 (Both Paths)

For animated slides, take the generated still image **or extracted video frame** and pass it to Wan 2.2:

```
Endpoint: create_predictions
Parameters:
  version: "wan-video/wan-2.2-i2v-fast"
  Prefer: "wait"
  input:
    image: [URL of still image or extracted frame]
    prompt: [animation prompt from production script]
    num_frames: 81
  jq_filter: "{id, status, output, error}"
```

**Critical:** `num_frames` must be ≥ 81. Lower values are rejected by the API.

**Timeout handling:** Wan 2.2 predictions take 40–90 seconds. The MCP `Prefer: wait` header waits up to 60s — if the prediction exceeds this, the MCP call will timeout but the prediction keeps running on Replicate. When this happens:
1. Note that the prediction was submitted (it's running)
2. After other predictions return, poll with `list_predictions` using `jq_filter: ".results[:5] | .[] | {id, status, output, error}"` to find the completed prediction
3. Match by model name (`wan-video/wan-2.2-i2v-fast`) and creation order

Real frames + subtle animation = "living photograph" effect — very powerful for video-sourced carousels.

Generate animations after stills/frames are ready. Fire all animation requests in parallel.

### Aspect Ratio Note

| Context | Ratio | Dimensions | Used By |
|---------|-------|-----------|---------|
| Frame extraction | 9:16 | 1080 × 1920 | CurAItion backend (portrait crop) |
| Replicate generation | 4:5 | 1080 × 1350 | `CAROUSEL_PRESETS` |
| Instagram carousel spec | 4:5 | 1080 × 1350 | Instagram's maximum feed real estate |

**Always use `aspect_ratio: "4:5"` for Replicate generation.** Frame extraction produces 9:16 (taller crop, more source material), but final carousel slides are 4:5 for Instagram spec compliance.

---

## Layer 4: Packaging and Ingestion

### HTML Preview

Generate a single-file HTML preview that displays all slides with their overlay text, arranged as a horizontal scrollable strip. The preview is for editorial review — it should closely approximate how the carousel will look on Instagram.

**Google Fonts import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');
```

**Preview structure:**
- Horizontal scroll container with snap points
- Each slide: 375×469px (4:5 ratio at mobile preview scale)
- Background image from Flux Schnell URL or S3 frame URL (both are public HTTPS URLs)
- Gradient overlay (see spec above)
- Overlay copy in Bebas Neue (see spec above)
- Animated slides show `<video>` element (muted, autoplay, loop)
- Slide counter in bottom-right corner

### SPEC-2026-004 Asset JSON

The carousel asset is stored as a JSON payload conforming to the CurAItion asset schema:

**Local JSON** (saved as `carousel-[slug]-asset.json` for full provenance):
```json
{
  "asset_type": "carousel",
  "status": "draft",
  "title": "[Carousel title]",
  "subtitle": "[One-line narrative angle]",
  "source_content_id": "[CurAItion content UUID]",
  "domain": "[CurAItion domain]",
  "metadata": {
    "narrative_angle": "[2–3 sentence description]",
    "narrative_structure": "[LINEAR-HERO / CONVERGENT-OPPOSITION / etc.]",
    "motif": "[Short motif name and description]",
    "motif_prompt_prefix": "[Reusable prefix]",
    "motif_prompt_suffix": "[Reusable suffix with negative constraints]",
    "image_model": "black-forest-labs/flux-schnell",
    "animation_model": "wan-video/wan-2.2-i2v-fast",
    "aspect_ratio": "4:5",
    "hybrid_pipeline": true,
    "source_type": "VIDEO",
    "frame_source_video_id": "[YouTube video ID, e.g. SDMdkgEJsRs]",
    "frame_extraction_task_id": "[Celery task ID from extract_frames]",
    "frame_extraction_strategy": "auto",
    "motif_strategy": "documentary",
    "themes": [{"name": "[theme]", "weight": 0.95}],
    "key_entities": ["[entity1]", "[entity2]"],
    "cultural_references": ["[ref1]", "[ref2]"],
    "generated_at": "[ISO 8601 timestamp]"
  },
  "caption": "[Full Instagram caption with hashtags and source credit]",
  "slides": [
    {
      "position": 1,
      "slide_function": "[HOOK/PROTAGONIST/CONTEXT/etc.]",
      "overlay_copy": "[Text with explicit \\n line breaks]",
      "image_source": "youtube_frame",
      "image_url": "[S3 URL of extracted frame or Replicate delivery URL]",
      "image_prompt": "[Full prompt — null for youtube_frame slides]",
      "image_prediction_id": "[Replicate prediction ID — null for youtube_frame slides]",
      "frame_timestamp_seconds": 25,
      "frame_usability_score": 0.87,
      "frame_visual_category": "evidence_screenshot",
      "is_animated": true,
      "animation_url": "[Replicate delivery URL or null]",
      "animation_prediction_id": "[Replicate prediction ID or null]",
      "animation_prompt": "[Animation prompt or null]",
      "production_note": "[Editorial context and CurAItion citations]"
    }
  ],
  "provenance": [
    {
      "data_point": "[What was used]",
      "source": "[CurAItion analysis / Supplementary]",
      "tool": "[Tool name]"
    }
  ]
}
```

**Hybrid field reference:**

| Field | Location | VIDEO Path | PODCAST/ARTICLE Path |
|-------|----------|-----------|---------------------|
| `hybrid_pipeline` | `metadata` | `true` | `false` |
| `source_type` | `metadata` | `"VIDEO"` | `"PODCAST"` or `"ARTICLE"` |
| `frame_source_video_id` | `metadata` | YouTube video ID | omit |
| `frame_extraction_task_id` | `metadata` | Celery task ID | omit |
| `motif_strategy` | `metadata` | `"documentary"` / `"stylized_overlay"` / `"full_ai"` | omit |
| `image_source` | `slides[]` | `"youtube_frame"` or `"replicate_backfill"` | `"replicate"` |
| `frame_timestamp_seconds` | `slides[]` | extraction timestamp | omit |
| `frame_usability_score` | `slides[]` | 0.0–1.0 from analyze_frames | omit |
| `frame_visual_category` | `slides[]` | from analyze_frames | omit |

For PODCAST/ARTICLE carousels, omit all `frame_*` and `hybrid_pipeline` fields — the JSON is identical to the pre-hybrid format with `image_source: "replicate"` added.

**Registry payload** (transformed for `curaition_asset_registry` — strict schema, verified against live `list` + `create` calls):
```json
{
  "asset_type": "instagram_carousel",
  "title": "[title]",
  "source_content_id": "[UUID]",
  "narrative_angle": "[2–3 sentence description — TOP-LEVEL, not in metadata]",
  "motif_name": "[Short motif name — TOP-LEVEL, e.g. '1930s Italian Futurist Racing Poster']",
  "motif_suffix": "[≤100 char compressed motif summary — TOP-LEVEL, e.g. 'Mille Miglia deco; black + gold leaf + ivory; 4:5.']",
  "caption": "[Instagram caption text — DO NOT include hashtags here]",
  "hashtags": ["Gucci", "Alpine", "F1"],
  "metadata": {
    "subtitle": "...",
    "domain": "...",
    "narrative_structure": "LINEAR-HERO",
    "motif_prefix": "[Reusable prompt prefix, e.g. '1930s Italian Futurist racing poster illustration of']",
    "motif_suffix_full": "[Full long motif suffix with negative constraints — different from top-level motif_suffix]",
    "image_model": "black-forest-labs/flux-schnell",
    "animation_model": "wan-video/wan-2.2-i2v-fast",
    "aspect_ratio": "4:5",
    "hybrid_pipeline": true,
    "source_type": "VIDEO",
    "source_url": "https://...",
    "source_title": "...",
    "source_creator": "...",
    "source_video_id": "[YouTube video ID — VIDEO path only]",
    "motif_strategy": "documentary",
    "frame_extraction_task_id": "[Celery task ID — VIDEO path only]",
    "themes": [{"name": "...", "weight": 0.9}],
    "key_entities": ["..."]
  },
  "slides": [
    {
      "position": 1,
      "overlay_copy": "[Text with \\n line breaks]",
      "image_prompt": "[Full prompt — REQUIRED, must be a string, never null. For CTA/static slides use a descriptive placeholder e.g. '[CTA — YouTube thumbnail, not AI-generated]']",
      "image_url_original": "[Replicate delivery URL or S3 frame URL]",
      "video_url_original": "[Replicate delivery URL — animated slides only, omit otherwise]",
      "media_type": "video",
      "production_note": "[Editorial context]",
      "cta_url": "[Source URL — CTA slide only, omit otherwise]"
    }
  ],
  "provenance": [
    {"data_point": "Anchor source: [description] — CurAItion analysis via curaition_get_content", "supplementary": false},
    {"data_point": "[Specific fact] — Supplementary via WebSearch ([source name])", "supplementary": true}
  ]
}
```

### CurAItion Ingestion

Submit the finished asset to CurAItion:

```
curaition_asset_registry (action: "create", item_data: [registry payload above])
```

**Important — Registry schema (verified against live API, 27 May 2026):**

| Field | Location | Required | Notes |
|-------|----------|----------|-------|
| `asset_type` | top-level | yes | Must be `"instagram_carousel"` (not `"carousel"`) |
| `title` | top-level | yes | Carousel title |
| `source_content_id` | top-level | yes | Anchor CurAItion content UUID |
| `narrative_angle` | top-level | yes | 2–3 sentence narrative angle — **NOT nested in metadata** |
| `motif_name` | top-level | yes | Short motif name — **NOT nested in metadata** |
| `motif_suffix` | top-level | yes | **≤100 characters.** Compressed motif summary (e.g. "Mille Miglia deco; black + gold + ivory; 4:5.") |
| `caption` | top-level | yes | Caption text only — hashtags go in their own field |
| `hashtags` | top-level | no | Array of strings without leading `#` |
| `metadata.motif_prefix` | metadata | no | Reusable prompt prefix |
| `metadata.motif_suffix_full` | metadata | no | **Full long motif suffix** (different from top-level `motif_suffix`!) |
| `metadata.source_url` / `source_title` / `source_creator` | metadata | no | Source attribution |
| `metadata.source_video_id` | metadata | VIDEO only | YouTube video ID |
| `slides[].image_prompt` | slide | yes | **Must be a non-null string.** For static/CTA slides use a descriptive placeholder (e.g. `"[CTA — slide 9 still re-used at 18% opacity, not a new AI generation]"`) |
| `slides[].image_url_original` | slide | yes | Still image URL — **NOT `image_url` or `media_url`** |
| `slides[].video_url_original` | slide | animated only | Animation video URL — **NOT `animation_url`** |
| `slides[].media_type` | slide | yes | `"image"` or `"video"` |
| `slides[].cta_url` | slide | CTA only | Source link for CTA slide |
| `provenance[]` | top-level | yes | Array of `{data_point: string, supplementary: bool}` — **NOT `data_lineage`**, and **NOT** `{source_tool, data_type, description}`. Embed tool/source attribution INSIDE the `data_point` string. |

The registry accepts slides and provenance as child records in a single create call. After ingestion, verify with `curaition_asset_registry (action: "get", item_id: <returned UUID>)` to confirm all fields persisted.

**Common validation errors and fixes:**
- `motif_suffix: String must contain at most 100 character(s)` → Move the long version to `metadata.motif_suffix_full` and put a compressed summary in `motif_suffix`.
- `slides.N: Unrecognized key(s) in object: 'media_url'` → Use `image_url_original` (not `media_url` or `image_url`).
- `slides.N: Unrecognized key(s) in object: 'animation_url'` → Use `video_url_original` and set `media_type: "video"`.
- `slides.N.image_prompt: Expected string, received null` → Static/CTA slides still need a string prompt. Use a bracketed placeholder describing what's actually on the slide.
- `Unrecognized key(s) in object: 'data_lineage'` → Use `provenance` and put `{data_point, supplementary}` in each entry.

---

## Layer 5: Editorial Iteration — Single-Slide Regen

After the first pass, the user will almost always want to tweak one or two slides — a different framing, a sharper hook line, the car in three-quarter rear instead of front, the goggles swapped for a helmet. The whole point of this layer is to make those edits cheap. **Do not rerun the full pipeline.** A single slide regen costs ~$0.003 (still only) or ~$0.10 (still + animation). Rerunning the whole carousel costs ~$0.33. The math punishes lazy iteration.

### When the User Asks for Changes

Listen for any of these trigger phrasings:

- "Regen slide N with [change]"
- "I don't like slide N — try [new direction]"
- "Make slide 4's car a three-quarter rear view"
- "Slide 7 needs a different image — [tweak]"
- "Punchier copy on slide 1"
- "Re-animate slide 9 with [different motion]"
- "Swap the image on slide N for [new subject]"

### Three Regen Modes

| Mode | What changes | What rerns | Cost | Use when |
|------|--------------|------------|------|----------|
| **Copy only** | `overlay_copy` field | Nothing on Replicate | $0 | Headline tweak, wording change, line-break adjustment |
| **Still only** | `image_prompt` + `image_url_original` | Flux Schnell (1 call) | ~$0.003 | Different subject, framing, or composition for a static slide |
| **Still + animation** | Image + motion | Flux Schnell + Wan 2.2 (2 calls, serial) | ~$0.10 | Animated slide (positions 1, mid, 9 typically) where the still has changed — the existing animation references the OLD image and won't match |
| **Animation only** | `animation_prompt` + `video_url_original` | Wan 2.2 (1 call) | ~$0.10 | Same still, different motion direction |

### The Regen Procedure

1. **Load the existing asset JSON** from `carousel-[slug]-asset.json`. This is your source of truth — never regen from memory.

2. **Identify the slide** by position. Find it in the `slides` array.

3. **Read three fields from the original:**
   - `overlay_copy` (so you don't accidentally lose it)
   - `image_prompt` (the basis for the tweak — apply the user's change as a delta, don't rewrite from scratch)
   - `image_url_original` and `video_url_original` (the OLD URLs — you'll need these to update the preview HTML)

4. **Compose the tweaked prompt.** Take the original `image_prompt`, apply the user's delta verbatim where possible, and re-wrap with the motif prefix/suffix from the carousel's `metadata.motif_prefix` and `metadata.motif_suffix_full`. The motif must remain constant across all slides — never let a single-slide regen drift the motif.

5. **Fire the appropriate Replicate call(s):**
   - Copy only: skip Replicate entirely.
   - Still: `create_models_predictions` with `model_owner: black-forest-labs`, `model_name: flux-schnell`, `aspect_ratio: "4:5"`, `Prefer: "wait"`, the tweaked prompt.
   - Animation (after still completes): `create_models_predictions` with `model_owner: wan-video`, `model_name: wan-2.2-i2v-fast`, the new still URL as `image`, `num_frames: 81`, the animation prompt (tweaked or unchanged).

6. **Update three artefacts in lockstep** — if you only update one, the user sees inconsistent state:

   **a. The asset JSON** (`carousel-[slug]-asset.json`):
   - Replace the slide's `image_prompt`, `image_url_original`, `image_prediction_id`, and (if animated) `video_url_original`, `animation_prediction_id`, `animation_prompt`.
   - Update the slide's `production_note` to record the regen: append `" [Regenerated YYYY-MM-DD: <user delta>]"`.
   - Append a new entry to `provenance`: `{"data_point": "Slide N regenerated: <user delta>. Original prediction ID <old>; new prediction ID <new>.", "supplementary": false}`.

   **b. The HTML preview** (`carousel-[slug]-preview.html`):
   - Find the OLD `image_url_original` (and `video_url_original` if animated) using string search.
   - Replace with the NEW URL in the `<img src="">` or `<source src="">` tag for that slide only.
   - If overlay copy changed, find the slide's `<div class="copy">` block and replace the text content.
   - **Critical:** do not regenerate the whole HTML — preserve the other 9 slides' state and any user edits.

   **c. The CurAItion registry** (`curaition_asset_registry`):
   - Action: `update`, `item_id: <asset UUID from initial create>`.
   - Pass the full updated slide payload in `item_data.slides` (the registry expects the complete slides array on update, not a patch).
   - After update, run `curaition_asset_registry (action: "get", item_id: <UUID>)` to verify the new URLs persisted.

7. **Show the user the result.** Open the updated HTML preview and present just the regenerated slide. Confirm the change is what they wanted before moving on. Do not assume — the user often wants a second tweak.

### Single-Slide Regen Examples

**Example 1 — Copy only:**
```
User: "Slide 1 hook is too soft. Make it 'ZERO ENGINES. UNTIL 27.'"
→ Edit slide 1 overlay_copy in JSON
→ Edit slide 1 <div class="copy"> text in HTML
→ Update registry (slides[0].overlay_copy)
→ No Replicate calls. Done in <5 seconds.
```

**Example 2 — Still only:**
```
User: "Slide 4 — make the car a three-quarter REAR view, not front."
→ Read existing image_prompt for slide 4
→ Replace "three-quarter front angle" with "three-quarter rear angle"
→ Fire 1 Flux Schnell call with motif prefix/suffix wrapped
→ Update JSON, HTML, registry
→ ~$0.003, ~15 seconds
```

**Example 3 — Still + animation:**
```
User: "Slide 9 close is good but show it in landscape orientation in the new image."
[Decline — aspect ratio is locked at 4:5 for Instagram spec. Explain why, offer a different change.]
```

**Example 4 — Animation only:**
```
User: "Slide 9 — keep the image, but make the G rotate faster."
→ Reuse existing still URL
→ Tweak animation_prompt: "rotates ~20 degrees over the loop" (was 8 degrees)
→ Fire 1 Wan 2.2 call
→ Update JSON, HTML, registry
→ ~$0.10, ~60 seconds
```

### Iteration Guardrails

- **Never regen more than 2 slides per turn without confirming with the user.** Batched silent regen burns Replicate spend and erodes trust.
- **Never change the motif on a single slide.** If the user is asking for a different visual world on slide 4, they're really asking for a new carousel — propose that explicitly.
- **Never delete provenance entries on regen.** Add new entries; preserve the audit trail.
- **Never update the CurAItion registry asset's `status` to anything past `draft` during regen.** Status transitions belong to a separate workflow.
- **If the user is on the 3rd+ regen of the same slide, stop and ask what's actually wrong.** Either the brief is unclear or the motif/copy is the real problem, not the image.

---

## Design Principles (Codified)

These principles are distilled from production experience across multiple carousels and Instagram design best practices:

### 1. Less Text, More Visual
Instagram is a visual platform. The AI-generated artwork should command 60%+ of the frame. If you're writing more than 8 lines of overlay copy, you're writing a blog post, not a carousel slide. Cut ruthlessly.

### 2. Bold + Condensed for Overlays
Always use bold, condensed typefaces for carousel overlays. They grab attention, occupy less space, and maintain legibility at small sizes on mobile. Bebas Neue is the default. Never use a serif or lightweight font for overlay copy.

### 3. Typographical Contrast Creates Hierarchy
Vary font size, weight, or color within a slide to guide the eye. The first line (a name, date, or number) should anchor attention. The body copy fills in below. Shapes or ruled lines can reinforce this hierarchy.

### 4. Visual Consistency is Non-Negotiable
Every slide must feel like it belongs to the same visual world. This is achieved through the motif system — a consistent prompt template that constrains color palette, art style, texture, and composition across all images. Break consistency and you break the carousel.

### 5. The First Slide is a Thumbnail
On the Instagram grid, slide 1 is the only image visible. It must work as a standalone thumbnail AND as the opening of a story. Design for two contexts simultaneously.

### 6. Whitespace is a Feature
Don't fill every pixel. Leave the top portion of the frame for the image to breathe. The gradient overlay provides a natural transition zone. Cramped slides feel amateur.

### 7. Alignment and Padding Matter
60px minimum from all edges. Left-align text when in doubt. Justified text with left-aligned last line creates the cleanest blocks for uppercase condensed fonts.

### 8. Branding is Subtle
Source attribution and series branding live in small type (Barlow Condensed, 0.7rem) — never competing with the overlay copy. A slide counter in the corner helps orientation.

### 9. Swipeability Comes from Visual + Narrative Hooks
Each slide must create a reason to see the next one. This is achieved through both visual quality (the AI artwork) and narrative cliffhangers in the copy. End slides mid-thought when possible — let curiosity drive the swipe.

### 10. Portrait Format, Always
1080 × 1350px (4:5). This occupies the maximum feed real estate on mobile. Never use square (1:1) or landscape for carousels — you're giving up screen space for no reason.

---

## File Naming Convention

```
carousel-[slug]-script.md          # Layer 2 production script
carousel-[slug]-asset.json         # Layer 4 SPEC-2026-004 JSON
carousel-[slug]-preview.html       # Layer 4 HTML preview
```

Where `[slug]` is a short, descriptive kebab-case identifier for the carousel (e.g., `cajamarca`, `corsica-paoli`, `bitcoin-etf`).

---

## Quick Reference: Tools by Layer

| Layer | Tool | Endpoint / Action | Purpose |
|-------|------|-------------------|---------|
| 1 | `curaition_list_content` | — | Find candidate source content |
| 1 | `curaition_get_content` | — | Deep analysis with citations + source classification signals |
| 1 | `curaition_get_cited_themes` | — | Timestamped evidence |
| 1 | `curaition_trend_analysis` | — | Domain trend context |
| 1 | `curaition_semantic_search` | — | Find related content |
| 1 | `WebSearch` | — | Supplementary research |
| 3 | `curaition_asset_registry` | `extract_frames` | Dispatch async frame extraction from video (VIDEO path) |
| 3 | `curaition_asset_registry` | `task_status` | Poll Celery task for frame extraction completion |
| 3 | `curaition_asset_registry` | `analyze_frames` | Gemini 2.5 Flash vision analysis of extracted frames |
| 3 | `curaition_asset_registry` | `suggest_frame_assignment` | Match analyzed frames to slide functions |
| 3 | `curaition_asset_registry` | `generate_backfill` | Generate AI images for gap slides (VIDEO path) |
| 3 | Replicate `flux-schnell` | `create_models_predictions` | Still image generation (PODCAST/ARTICLE path, or VIDEO backfill) |
| 3 | Replicate `wan-2.2-i2v-fast` | `create_predictions` | Animation from still or frame (both paths) |
| 3 | Replicate polling | `list_predictions` / `get_predictions` | Check status of timed-out predictions |
| 4 | `curaition_asset_registry` | `create` | Ingest finished asset |
| 4 | `curaition_asset_registry` | `get` | Verify round-trip after ingestion |
| 5 | Replicate `flux-schnell` | `create_models_predictions` | Single-slide still regen (Layer 5) |
| 5 | Replicate `wan-2.2-i2v-fast` | `create_models_predictions` | Single-slide animation regen (Layer 5) |
| 5 | `curaition_asset_registry` | `update` | Persist regen results back to the registry (pass full updated `slides` array, not a patch) |
| 5 | `curaition_asset_registry` | `get` | Verify regen persisted |

---

*Produced by CurAItion Intelligence Desk · Carousel Producer Skill · v1.1 · 27 May 2026*
*Changelog v1.1: Corrected Layer 4 registry schema (verified against live API); added Layer 5 single-slide regen workflow.*
