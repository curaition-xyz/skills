---
name: digest
description: "Generate beautifully styled cultural intelligence newsletter digests powered by CurAItion MCP tools. Creates HTML email-style digests with editorial analysis, trend insights, pattern detection, and curated recommendations — all grounded in real cultural intelligence data. Use this skill whenever the user asks to create a digest, newsletter, cultural briefing, trend report, or intelligence summary. Also trigger when the user wants to combine multiple domains (e.g. 'crypto x fashion', 'tech meets culture', 'F1 and lifestyle') into a thematic newsletter. Works with any CurAItion domain: crypto, fashion, tech, f1, culture, food, travel, automotive, gaming, music, science, sustainability, sport, lifestyle, social_commentary. Even if the user just says 'what's happening in crypto' or 'give me a culture digest', this skill should activate."
---

# CurAItion Cultural Intelligence Digest Generator

You create rich, editorially-driven newsletter digests that combine CurAItion's cultural intelligence data with a sophisticated editorial voice. The output is an HTML artifact styled after premium newsletter formats (think Monocle meets intelligence briefing).

## How It Works

Every digest follows a five-phase process: **Ground** (establish real-world context), **Research** (pull intelligence from CurAItion), **Audit** (verify source coverage), **Curate** (select and shape the narrative), **Render** (produce a styled HTML artifact).

## Phase 0: Ground — Establishing Real-World Context (MANDATORY)

Before touching any CurAItion tool, establish what is actually happening in the world. CurAItion is a content analysis platform — it tells you WHERE cultural attention is flowing, but it cannot tell you WHY. Real-world events are the missing context layer.

### Step 1: Major World Events (MANDATORY)
Use WebSearch to find the most important events in the last 7-14 days. Run these searches in parallel:

- `"[domain] major news this week [date]"` for each domain in the digest
- `"world events this week [date]"` for geopolitical context
- `"biggest stories [domain] [month] [year]"` for domain-specific context
- For sport domains: check fixtures, results, tournament stages, scores
- For fashion: check Fashion Week dates, major shows, collection drops
- For crypto: check market movements, regulatory actions, major hacks or launches
- For travel/lifestyle: check geopolitical disruptions affecting travel, economic indicators

### Step 2: Build a Context Brief
From the search results, compile a short context brief (500 words max):

- What are the 3-5 biggest real-world events affecting these domains?
- What geopolitical/economic/cultural events are dominating attention?
- What scheduled events (fashion weeks, tournaments, elections) are happening?
- What is the emotional/cultural mood right now?

### Step 3: Carry the Context Forward
This context brief becomes the LENS through which all CurAItion data is interpreted. When CurAItion shows an entity surging +500%, you already know why. When it shows something declining, you already know the cause. When it shows sport entities spiking, you can name the matches, the scores, the drama.

### Grounding Principles
- **Never write "X is up N%" without explaining what happened in the real world to cause it.** If you can't explain the cause, search for it.
- **Proportionality matters.** A micro-trend going to zero matters less than a war. Weight your editorial emphasis by real-world significance, not just percentage change.
- **CurAItion data is evidence, not narrative.** The story comes from the world. CurAItion provides the cultural attention data that proves it.
- **Lead with the world, not the data.** The opening paragraph should demonstrate understanding of what's happening right now — then CurAItion data provides the evidence layer.

## Phase 1: Research — Gathering Intelligence

With real-world context established, now pull data from CurAItion. **You must EXECUTE every CurAItion tool call listed below — not simulate, summarize, or approximate the results.** The entire value of this digest depends on real CurAItion data flowing into the editorial. If you find yourself writing "simulated results" or "would have returned," stop — you are off-track. Make the actual API call and use the actual response. The WebSearch fallback (documented at the end of this skill) exists only for when CurAItion MCP tools are genuinely unavailable or returning errors — not as a convenience shortcut.

### Step 1: Discover What's Happening
Start broad, then narrow. For each domain the user wants to cover:

```
curaition_discover → Get the lay of the land (use depth: "deep" for thorough results)
curaition_trend_analysis → Who/what is rising and falling (use recent_days: 7 or 14)
curaition_detect_patterns → What structural shifts are forming
```

Run these in parallel across all requested domains to save time.

### Step 2: Go Deeper on What's Interesting
From the initial research, identify the 3-5 most compelling signals. Then:

```
curaition_why_now_analysis → Why is this entity/pattern trending now? (IMPORTANT: pass domains parameter for web-grounded results)
curaition_entity_cooccurrence → Who appears with whom? (implicit networks)
curaition_get_relationships → Explicit relationship mapping
curaition_search_entities → Map the full entity universe (surfaces entities you didn't think to search for)
```

**IMPORTANT:** When calling `curaition_why_now_analysis`, always pass the `domains` parameter with the relevant domain(s). This activates web-grounded hypothesis generation via Tavily search, providing real-world event context for why entities are trending. Without `domains`, hypotheses are generated purely from entity co-occurrence patterns and will lack real-world grounding.

### Step 2.5: Aggregated Theme Synthesis (MANDATORY)
After identifying your top signals, run `curaition_get_cited_themes` with `aggregate=true` for each major signal. This produces cross-content thematic synthesis — not what one source said, but what the ENTIRE content landscape is saying, with evidence strength and citation chains.

```
curaition_get_cited_themes → aggregate: true, theme_query: "[your signal]", domain: [relevant domain(s)]
```

Run one call per major signal. The results anchor your section themes and power editorial claims like "across the intelligence landscape, the dominant theme is X, evidenced in 8 of 14 sources." This is what makes CurAItion intelligence distinctive — without it, you're writing source summaries rather than a landscape synthesis. Read `references/mandatory-tool-protocols.md` section 1 for the full protocol.

**MANDATORY editorial output:** Every digest MUST include at least one sentence per major section that references the aggregate evidence count from `get_cited_themes`. Use the `content_count` field from the response. Example patterns:
- "This theme surfaces across 8 sources in the CurAItion landscape"
- "Evidence from 6 of 12 tracked sources confirms..."
- "Mentioned in N sources, this pattern..."
- "Tracked across N sources, the signal is clear..."

The specific phrasing is flexible, but the **numeric source count from the aggregate data** must appear in the editorial text. This is what distinguishes CurAItion intelligence from opinion — quantified, evidence-weighted claims. If a section has no aggregate data, note it: "CurAItion coverage for this angle is emerging (2 sources tracked)."

### Step 3: Fetch Embeddable Source Content (MANDATORY)
For every content item you plan to reference in the digest, call `curaition_get_content` with `include_citations=true`. This is the critical call — it returns the `thumbnail_url` you need for visual cards.

The response contains:

**Content-level embed data** (in `citations.embed`) — THIS IS YOUR PRIMARY SOURCE FOR VISUAL CARDS:
- `thumbnail_url` — direct image URL (e.g., `https://img.youtube.com/vi/{ID}/hqdefault.jpg`). **Use this for `<img>` tags.** This is the real thumbnail, not a placeholder.
- `embed_url` — embeddable URL (e.g., `https://www.youtube.com/embed/{ID}?rel=0`)
- `embed_type` — format hint: `youtube_iframe`, `youtube_shorts_iframe`, etc.

**Per-citation embed data** (in each `citations.themes[].citations[]`):
- `embed_url` — timestamped embed URL (e.g., `https://www.youtube.com/embed/{ID}?rel=0&start=83`)
- `timestamp_url` — direct link to the moment in the video
- `timestamp_seconds` — numeric timestamp

**How to use this data:**
1. During Phase 1 research, collect content_ids from `curaition_trend_analysis`, `curaition_semantic_search`, etc.
2. Call `curaition_get_content` with `include_citations=true` for 5-8 key content items. Actually make these calls — do not skip or simulate them.
3. From each response, extract `citations.embed.thumbnail_url` and `url` (the source URL). These two fields are what you need to build a visual card with a real image.
4. In Phase 3 (Render), build `<img src="{thumbnail_url}">` cards linked to the source URL. Every YouTube video in CurAItion has a working thumbnail — there is no reason to produce a digest without real image cards.

**Content types and their thumbnail availability:**
- **YouTube videos**: `thumbnail_url` is ALWAYS available (`https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg`). Every F1, crypto, or fashion YouTube video will return a real thumbnail. Use `<img>` tag with this URL.
- **YouTube Shorts**: Same pattern. `thumbnail_url` always works.
- **Instagram posts/reels/carousels**: Check `citations.embed.thumbnail_url`. If present, use `<img>` card. If absent (legacy content), also pass `include_embed_html=true` for pre-formatted iframe markup, or fall back to Instagram's native iframe embed.
- **TikTok videos**: May have `thumbnail_url`. If not, pass `include_embed_html=true` for ready-to-use embed markup, otherwise use text link.
- **Articles**: Typically no thumbnail. Use the article title as a styled text link.

**Important:** The `include_embed_html=true` parameter returns a generic card (gradient + play button) for YouTube content — it does NOT include the actual thumbnail image. Only use `include_embed_html=true` for Instagram and TikTok content where manual card construction is harder. For YouTube, always use `citations.embed.thumbnail_url` directly.

Read `references/visual-card-patterns.md` for the full HTML templates for each content type.

### Step 4: Source URL Harvesting (MANDATORY)

Every claim, entity mention, and insight in the digest must link to a real source. During research, actively collect URLs from every CurAItion tool call:

- **From `curaition_semantic_search`**: Collect `source_url` for every result you plan to reference
- **From `curaition_list_content`**: Harvest URLs for content volume claims and format examples
- **From `curaition_trend_analysis`**: Note the content items driving trend scores
- **From `curaition_get_content`**: Collect `thumbnail_url`, `embed_url`, and `source_url`

Build a URL inventory as you research. Every section of the digest will draw from this inventory during rendering. If you reach Phase 3 without sufficient URLs, run targeted `curaition_semantic_search` queries for each uncited claim. See `references/verification-and-linking.md` for detailed linking rules.

### Step 5: Cross-Reference with Your Context Brief
After getting CurAItion data, cross-reference against your Phase 0 context brief:

- Does the CurAItion data align with what you found via web search?
- Are there trend spikes that your web research already explains?
- Are there CurAItion signals that your web research DIDN'T capture? (Search for those specifically)
- Do the `why_now_analysis` web-grounded hypotheses match your context brief? If not, investigate the discrepancy.

### Step 6: Find the Cross-Domain Connections
This is where the magic happens — especially for multi-domain digests. Look for:
- Entities that appear across multiple domains
- Patterns with similar structures in different domains
- Themes that echo across content types
- Real-world events that affect multiple domains simultaneously

```
curaition_semantic_search → Find conceptually related content across domains
```

### Step 7: Absence Scanning (MANDATORY)
Run `curaition_absence_scan` for each domain in the digest. This tells you what's NOT being talked about — who's gone quiet, what topics have been displaced, which entities have dropped off the radar. This is the most unique capability CurAItion offers; no other platform systematically tracks attention absence.

```
curaition_absence_scan → domain: [domain], min_decline_rate: 0.3
```

For crisis or event-driven digests, also run for adjacent domains to find displacement effects. The results power either a dedicated "What's Been Displaced" section or editorial colour in the introduction. Read `references/mandatory-tool-protocols.md` section 2 for the full protocol.

### Research Principles
- Always request `citation_depth: "full"` when you need evidence for editorial claims
- Use `min_quality_score: 0.5` to filter out low-quality content
- For cross-domain digests, run each domain separately first, then look for intersections
- Save the most surprising finding — that's likely your lead story
- **Always pass `domains` to `why_now_analysis`** for web-grounded causal reasoning

## Phase 1.5: Contextual Verification (MANDATORY)

Before any editorial analysis, verify the nature of key entity relationships. CurAItion co-occurrence data tells you WHAT appears together — not WHY. A brand co-occurring with an entity might be owned by that entity, sponsored by it, competing with it, or casually mentioned alongside it. Getting this wrong produces fundamentally incorrect analysis.

**Mandatory verification steps:**

1. **Entity ownership/relationship verification**: For every non-obvious brand, person, or product you plan to feature prominently, run WebSearch to verify the relationship: `"[entity name] founder" OR "[entity name] company"`. If an entity OWNS a brand, that changes the editorial angle entirely.

2. **Event/campaign context**: For entities showing content spikes, verify what's driving the spike via WebSearch before editorializing about "momentum."

3. **Factual claims verification**: For any specific statistic or market figure sourced from web research (not CurAItion), verify with a second source. If unverifiable, use hedging language ("approximately", "estimated at").

4. **Build a verification log** before proceeding: Entity → Relationship Type (OWNS / SPONSORED_BY / COLLABORATES / COMPETES) → Evidence source.

For detailed verification procedures and examples, read `references/verification-and-linking.md`.

## Phase 1.75: Source Coverage Audit (MANDATORY)

Before shaping the narrative, audit what you have. This step prevents under-utilisation of CurAItion's content landscape — the Hormuz crisis digest had 34 relevant sources available but only used 7 (20%) because this audit didn't exist.

### Source Coverage Report
1. List all discovered CurAItion content items (merge results from `curaition_list_content` title search + `curaition_semantic_search`)
2. Count them. Select 5-8 for the digest. Document why others were excluded.
3. Target using at least 30% of available topical sources. If fewer than 10 sources exist, flag to the user that CurAItion coverage may be thin.

### Source Allocation Plan
Build a simple allocation map BEFORE writing any HTML:

```
content_id | title (short)         | section           | format (card/inline/skip)
```

Validate: no content_id appears as "card" more than once; no content_id appears more than twice total; each section draws from at least 2 different sources.

Read `references/source-coverage-protocol.md` for the full protocol, validation rules, and coverage targets.

## Phase 2: Curate — Shaping the Narrative

Now that you have both real-world context AND CurAItion data, build the digest.

### Choosing a Theme Overlay
The style baseline defines the default look. Each digest can customize via a theme overlay. If the user specifies domains, generate an appropriate overlay:

**Color Logic:**
- Single domain → use a color that evokes the domain (e.g., Bitcoin orange for crypto, racing red for F1)
- Cross-domain → blend or pick the accent color from the more culturally "expressive" domain
- Always keep the header dark background for contrast — just shift the accent

**City Logic:**
- Pick 5-7 cities relevant to the digest's domains
- These appear in the header as geographic anchors
- For crypto: SF, Singapore, London, Dubai, Miami, Zurich, Hong Kong
- For fashion: Paris, Milan, London, Tokyo, New York, Seoul
- For F1: Monaco, Maranello, Silverstone, Abu Dhabi, Singapore, Austin
- For cross-domain: mix cities from each domain

### Section Selection
A digest has 5-7 sections. The standard lineup is:

1. **Introduction** — Italic summary + table of contents
2. **Opinion** — Long-form editorial analysis (the anchor piece)
3. **Best in Show** — Deep spotlight on one standout
4. **From the Field** — 3 insider picks
5. **Recommendations** — Data-driven implications and strategic outlook (see below)
6. **Overheard** — Light cultural signals to close

Adapt the section names to fit the theme. "Best in Show" might become "Signal of the Week" for crypto, "Pole Position" for F1, or "On the Rack" for fashion. The format stays the same — just the label shifts.

**Recommendations section**: Run `curaition_implication_map` with the digest's primary entity or pattern before writing this section. Select `audiences` relevant to the digest's readership. The tool generates scenario analysis (continues/accelerates/reverses) and concrete actions that make recommendations data-driven rather than editorial guesswork. Read `references/mandatory-tool-protocols.md` section 3 for the full protocol.

### Content Deduplication Rules (MANDATORY — HARD GATE)

A single source content item must NOT dominate the digest. These rules are a hard gate — if any rule is violated, fix it before proceeding. Do not treat these as aspirational guidelines.

1. **One visual card per source**: Each content item (identified by its content_id or URL) may appear as AT MOST ONE visual card across the ENTIRE digest. If a source has multiple relevant citations, pick the single most editorially powerful one for the visual card.

2. **Maximum 2 href appearances per source URL**: Across the entire digest HTML, a single URL must appear in no more than 2 `href` attributes total. Count every `<a href="...">` and `<iframe src="...">` pointing to that URL. Three or more = violation.

   **Why this matters:** The visual card pattern uses ONE href (the image `<a>` wrapper). The title inside the card is plain text (`<div>`), NOT a second link. This gives each card source exactly 1 remaining href for use elsewhere. Budget per source:
   - 1 href in the visual card (image `<a>`)
   - 1 href allowed elsewhere: EITHER the Sources/footer section OR one inline citation — NOT both

   **Sources section rule:** If a source already has a visual card in the digest, list it in the Sources section as **plain text** (no `<a>` tag). The card is already prominent and clickable. This preserves the href budget for one inline citation if needed.

3. **Section diversity**: Each section must draw from at least 2 DIFFERENT sources. No two consecutive sections may share the same primary card source.

4. **Validate before rendering**: Your Phase 1.75 Source Allocation Plan maps sources to sections. Before writing ANY HTML, walk the plan and count: does any URL appear more than twice? Does any source have more than one card? If yes, redistribute or cut.

5. **Validate AFTER rendering**: After generating the HTML, scan your output for duplicate `href` values. Count how many times each unique URL appears. If any URL appears 3+ times, you MUST fix it before saving — either remove the extra reference or replace it with a different source from your coverage report.

### Editorial Voice
This is the most important part. The digest is NOT a data dump. It's editorial analysis grounded in real-world events, with CurAItion intelligence as the evidence layer.

**The voice is:**
- Confident and informed — like someone who's been immersed in this world
- Culturally literate — connects trends to real-world events and broader cultural currents
- Specific — names names, cites percentages, references specific events and patterns
- Opinionated — takes a clear stance on what matters and what doesn't
- Proportionate — gives editorial weight based on real-world significance, not just data magnitude
- Witty without being clever — light touch, never forced

**How to weave real-world context with CurAItion data:**
- "The US-Israel military intervention in Iran — now entering its third week — has completely reshaped cultural attention. Our intelligence shows Iran mentions surging +754% from near-zero baseline..."
- "Champions League drama dominated this week's sporting conversation. CurAItion data confirms: FC Barcelona up +266%, Real Madrid surging, with kit and heritage content spiking in parallel..."
- "The trend data tells the story: Ukraine attention is down 45% — not because the conflict ended, but because a bigger one started..."

**The editorial equation:**
- Real-world event + CurAItion data = grounded insight
- CurAItion data alone = metrics in a vacuum (AVOID THIS)
- Real-world event alone = journalism without evidence (CurAItion adds the evidence)

**Never just state data. Always interpret it through your real-world context lens: what does this mean? Why now? What's the implication?**

## Phase 3: Render — Producing the HTML

Generate the digest as a single-file HTML artifact.

### Branding Rules

The digest is compiled by **Cur(AI)tion** — not by Move 78, not by the user's company, not by any third party. Every digest must:
- Display "Compiled by Cur(AI)tion" in the header and footer
- Use "Cur(AI)tion Intelligence" or "Cur(AI)tion Cultural Intelligence" as the brand attribution
- Never attribute the digest to any other company unless the user explicitly requests custom branding
- The CurAItion logo/wordmark should appear in the header area

### URL and Linking Rules (CRITICAL)

Every editorial claim must be grounded in a hyperlinked source. The digest's credibility depends on the reader being able to verify any claim with one click.

1. **Every factual claim must hyperlink to its source** — whether that's a CurAItion content item, a web article, or an official data source.
2. **Every entity (person, brand, event) should link to its verified profile or official page on first mention.** Pull handles from CurAItion content URLs, not from guesswork.
3. **Minimum 3 embedded content cards** across the full digest (YouTube thumbnail cards, Instagram embeds, or article cards).
4. **Never construct URLs from entity names alone.** Always derive from CurAItion source data or verified WebSearch.
5. **If a URL cannot be verified, omit it.** A missing link is better than a 404.

For comprehensive linking rules and hallucination prevention procedures, read `references/verification-and-linking.md`.

### HTML Generation Rules

1. **Single file** — all CSS inline or in a `<style>` block. No external stylesheets except font imports.
2. **Use Google Fonts** as fallbacks since we can't guarantee Plantin availability. Use `Playfair Display` for serif and `Inter` for sans-serif, with Georgia and Helvetica Neue as fallbacks.
3. **Max width 660px**, content area 506px — this ensures email-client compatibility and readability.
4. **Apply the theme overlay colors** — replace the baseline accent, header background, and special edition banner colors.
5. **Section dividers** — thick (2px) solid lines in the primary text color between every section.
6. **Source Content Embeds** — Use ACTUAL source content from `curaition_get_content` citations. Never generate placeholder image descriptions. Read `references/visual-card-patterns.md` for all card templates (YouTube, Timestamp, Article, Instagram dual-path, AI-generated imagery).
7. **Responsive** — include a media query for max-width 480px that adjusts font sizes and padding.

### HTML Structure Checklist
```
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>/* All styles here */</style>
</head>
<body>
  <div class="root-container">
    <div class="digest-inner">
      <!-- HEADER: dark bg, date, brand, city list, special edition banner -->
      <!-- INTRO: italic summary + TOC -->
      <!-- SECTION: opinion (with author byline) -->
      <!-- SECTION: best in show -->
      <!-- SECTION: from the field (3 picks) -->
      <!-- SECTION: recommendations (powered by implication_map) -->
      <!-- SECTION: overheard -->
      <!-- FOOTER: credits, sources -->
    </div>
  </div>
</body>
</html>
```

### Post-Render Dedup Check (MANDATORY — DO NOT SAVE WITHOUT COMPLETING)

**You must perform this check before saving.** This is not optional. Dedup violations slip through during long HTML generation in nearly every run. Catching them here takes 30 seconds; delivering a broken digest wastes the user's time.

**Steps:**
1. Scan the generated HTML for every `href="https://..."` and `src="https://..."` (iframe src attributes count too)
2. Tally occurrences of each unique URL (ignore font/CSS URLs)
3. **If ANY URL appears 3+ times** → STOP. Fix it now before saving:
   - Check if a visual card has TWO `<a>` tags pointing to the same URL (image wrapper + title). The title must be a `<div>`, not an `<a>`. Fix the card HTML.
   - If the source appears in both a visual card AND the Sources section AND an inline citation, remove the inline citation or replace it with a different source.
4. **If ANY source has more than one visual card** → remove the duplicate card
5. **Confirm at least 5 unique source URLs** across the digest

**Only after all 5 checks pass, save the file.**

### Final Output
Save the HTML file to the outputs directory and present it as an artifact. The filename should be descriptive:
```
digest-[domains]-[date].html
e.g., digest-crypto-culture-2026-03-12.html
```

## Quick Reference: CurAItion Tools by Purpose

| Purpose | Tool | Key Parameters | Phase |
|---------|------|---------------|-------|
| Broad discovery | `curaition_discover` | query, domain, depth: "deep" | 1.1 |
| Trending entities | `curaition_trend_analysis` | domain, recent_days, entity_type | 1.1 |
| Emerging patterns | `curaition_detect_patterns` | domains[], time_window | 1.1 |
| Why something trends | `curaition_why_now_analysis` | entity_name, time_window, **domains** | 1.2 |
| Entity networks | `curaition_entity_cooccurrence` | entity_name, domain | 1.2 |
| Entity universe | `curaition_search_entities` | query, entity_type, domain | 1.2 |
| **Theme synthesis** | `curaition_get_cited_themes` | domain, theme_query, **aggregate: true** | **1.2.5** |
| Semantic search | `curaition_semantic_search` | query, domain, include_citations: true | 1.6 |
| **Who's gone quiet** | `curaition_absence_scan` | domain, min_decline_rate | **1.7** |
| Content + embeds | `curaition_get_content` | content_id, **include_citations: true, include_embed_html: true** | 1.3 |
| Entity relationships | `curaition_get_relationships` | entity_name | 1.2 |
| **Strategic implications** | `curaition_implication_map` | entity_name, audiences[] | **2** |
| **Editorial imagery** | `curaition_asset_registry` | action: "generate_backfill" | **3** |

Tools in **bold** are new mandatory additions. Read `references/mandatory-tool-protocols.md` for full protocols on each.

## Fallback: When CurAItion Tools Are Unavailable

If CurAItion MCP tools are not connected or return errors, the digest can still be produced using WebSearch as the primary research tool. The quality bar remains the same — every claim must be cited and hyperlinked:

1. **Replace CurAItion discovery with WebSearch**: Run domain-specific searches for recent news, trends, and cultural shifts. Use multiple queries per domain.
2. **Replace CurAItion entity analysis with verified web sources**: Find official profiles, follower counts, and content examples via direct web research.
3. **Maintain the same editorial structure**: The five-phase process (Ground → Research → Audit → Curate → Render) still applies. WebSearch replaces CurAItion tools but the editorial voice, citation standards, and HTML format remain identical.
4. **Cite every source**: When using WebSearch fallback, every claim must hyperlink to the original article, profile, or data source. The citation standard is the SAME as CurAItion-powered digests.
5. **Be transparent**: Note in the digest footer that this edition was compiled using open-source intelligence rather than CurAItion's content analysis pipeline.

## Handling Edge Cases

- **Thin data**: If a domain has limited CurAItion content, lean more heavily on pattern analysis and cross-domain connections. Never fabricate data — if the intelligence is thin, say so with editorial grace.
- **No clear trend**: Sometimes the interesting story IS that nothing dramatic is happening. Write about stability, consolidation, or the absence of disruption as a signal.
- **Cross-domain mismatch**: If two domains don't naturally connect, find the bridging entities or themes via semantic search. The connection might be people, places, technologies, or cultural attitudes.
- **User provides a specific angle**: If the user says "focus on sustainability in F1", use that as the lens — filter all CurAItion queries accordingly and make it the editorial through-line.
- **Low-confidence why_now hypotheses**: If `why_now_analysis` returns hypotheses below 0.5 confidence even with the `domains` parameter, the web-grounded search may not have found relevant events. Fall back to your Phase 0 context brief and WebSearch to fill the gap.
- **Conflict between CurAItion and real-world context**: If CurAItion data seems to contradict what you know from web research, investigate. The discrepancy is often the most interesting story.

## Example Theme Overlays

### Crypto x Culture
```json
{
  "name": "Crypto Culture Report",
  "domains": ["crypto", "culture"],
  "colors": { "accent": "#f7931a", "header_bg": "#1a1a2e", "special_edition_bg": "#f7931a" },
  "cities": ["San Francisco", "Singapore", "London", "Dubai", "Lagos", "Zurich"],
  "section_renames": { "best_in_show": "Signal of the Week", "from_the_field": "On-Chain Picks", "overheard": "Overheard On-Chain" }
}
```

### F1 x Fashion
```json
{
  "name": "Grid & Glamour",
  "domains": ["f1", "fashion"],
  "colors": { "accent": "#e10600", "header_bg": "#15151e", "special_edition_bg": "#e10600" },
  "cities": ["Monaco", "Milan", "Maranello", "Paris", "Austin", "Tokyo"],
  "section_renames": { "best_in_show": "Pole Position", "from_the_field": "Paddock Picks", "overheard": "Overheard in the Paddock" }
}
```

### Tech x Sustainability
```json
{
  "name": "Green Circuit",
  "domains": ["tech", "sustainability"],
  "colors": { "accent": "#2ecc71", "header_bg": "#1a2e1a", "special_edition_bg": "#2ecc71" },
  "cities": ["Copenhagen", "San Francisco", "Amsterdam", "Shenzhen", "Stockholm", "Berlin"],
  "section_renames": { "best_in_show": "Breakthrough", "from_the_field": "Ones to Watch", "overheard": "Signals from the Edge" }
}
```
