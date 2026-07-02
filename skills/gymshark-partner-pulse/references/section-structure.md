# Section Structure Reference — Partner Pulse HTML

## Design System

**Fonts:**
- Headings: `'Playfair Display', Georgia, serif`
- Body: `'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif`
- Import: `https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&display=swap`

**Colours:**
- Accent: `#54D4C6` (Gymshark teal)
- Header background: `#111111`
- Body text: `#333`
- Headings: `#1a1a1a`
- Muted text: `#888` / `#999`
- Dividers: `#e0e0e0` (light), `#1a1a1a` (heavy)
- Callout background: `#111` with white/teal text

**Layout:**
- Root container: `max-width: 660px`, white background
- Content padding: `0 32px`
- Section dividers: `2px solid #1a1a1a` between major sections, `1px solid #e0e0e0` between sub-sections

## Section Templates

### 1. Special Edition Banner
```html
<div class="special-edition">Partner Ecosystem Intelligence — Internal Briefing</div>
```
Teal background, dark text, uppercase, centered.

### 2. Header
```html
<div class="header">
  <div class="header-top">
    <div class="header-brand">Partner Pulse</div>
    <div class="header-date">[DD Month YYYY] — Issue #[N]</div>
  </div>
  <h1 class="header-title">[Headline — provocative, insight-driven, max 15 words]</h1>
  <p class="header-subtitle">[One-line data summary: total items, athletes, channels, date range]</p>
  <div class="header-cities">
    Birmingham <span>·</span> London <span>·</span> [etc.]
  </div>
</div>
```
The headline should be the single strongest editorial insight from the data. It should make the reader want to scroll.

### 3. Introduction + Table of Contents
```html
<div class="intro">
  <p class="intro-text">[Italic editorial paragraph. Set the tone. Tell them what they're about to read and why it matters. 3-4 sentences.]</p>
  <ul class="toc">
    <li><span class="toc-number">01</span> <a href="#section-id">[Section Title]</a></li>
    ...
  </ul>
</div>
```

### 4. Stats Bar
```html
<div class="stats-bar">
  <div class="stat-item">
    <div class="stat-number accent">[N]</div>
    <div class="stat-label">Content Items</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">~[N]</div>
    <div class="stat-label">Unique Athletes</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">[N]</div>
    <div class="stat-label">Channels Tracked</div>
  </div>
  <div class="stat-item">
    <div class="stat-number accent">[N]</div>
    <div class="stat-label">Gymshark Co-occurrences</div>
  </div>
</div>
```
Always follow with a methodology note explaining the deduplication:
```html
<p class="body-text" style="font-size: 12px; color: #999; margin-top: -16px;">
  <strong>Note on athlete count:</strong> CurAItion tracks [N] individual channels. Many athletes operate 2-3 channels. We estimate ~[N] unique athletes based on entity deduplication across handles. [Additional context if relevant.]
</p>
```

### 5. The Big Story (Section: opinion)
The anchor editorial piece. 800-1000 words. This is where the analyst voice shines.

**Structure:**
- `section-label`: "The Big Story"
- `section-title`: Provocative headline (not a data summary)
- `section-subtitle`: One-line summary
- 3-4 `body-text` paragraphs with inline links to source content
- 1 visual embed card (Instagram or TikTok content)
- 1 callout box with "What This Means" — the actionable takeaway

**Content guidelines:**
- Lead with the most resonant theme from get_cited_themes
- Back every claim with a citation count, co-occurrence number, or source URL
- Connect content patterns to the autonomous athlete model
- End with an implication that makes the team think

### 6. Athlete Spotlight
Deep dive on one standout athlete.

**Structure:**
- `section-label`: "Athlete Spotlight"
- `section-title`: "[Name] did [thing]. [Why it matters in one clause.]"
- 2-3 `body-text` paragraphs
- 1 visual embed card
- Link athlete name to their profile throughout

**Selection criteria:** Choose the athlete with the most compelling story in the data — not necessarily the highest volume. Competition results, personal milestones, viral cultural content, or unusual cross-brand moments all qualify.

### 7. Three Signals
Three patterns worth attention. Each is a mini-essay.

**Structure for each signal:**
```html
<div class="pick">
  <div class="pick-number">0[N]</div>
  <h3 class="pick-title">[Title]</h3>
  <p class="pick-meta">[Athlete handle] · [Data point] · [Theme] · [Citation count]</p>
  <p class="body-text">[2-3 paragraphs]</p>
  <div class="callout">
    <div class="callout-label">[The Opportunity / Ideas for the Team / The Question]</div>
    <p class="callout-text">[Actionable ideas, numbered if multiple]</p>
  </div>
</div>
```

**Signal selection:**
- Signal 1: An opportunity — something the team could act on
- Signal 2: A strategic insight — something about category positioning or competitor landscape
- Signal 3: A structural pattern — something about the ecosystem itself

**Critical framing guidance:**
- If an athlete appears at a supplement/nutrition brand event wearing Gymshark, that is NOT a competitive threat. It's the autonomous model working. Frame it as a co-creation opportunity.
- If an athlete's lifestyle content shows another brand more than Gymshark, that's a category gap — frame it as an opportunity to expand product placement, not a loyalty problem.
- Always include specific, actionable ideas in the callout boxes. Generic advice ("consider leveraging this") is not acceptable.

### 8. Partner Roster
Top 20 athletes table, deduplicated to people.

```html
<table class="athlete-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Athlete</th>
      <th>Items</th>
      <th>Notable Content Signal</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="athlete-rank">[N]</td>
      <td><span class="athlete-name"><a href="[profile URL]">[Name]</a></span></td>
      <td>[N]</td>
      <td><span class="badge badge-[type]">[Signal]</span></td>
    </tr>
  </tbody>
</table>
```

**Badge types:** `badge-culture`, `badge-product`, `badge-lifestyle`, `badge-compete`, `badge-hybrid`, `badge-watch`

Follow the table with:
- A "How to read this table" note
- A content format breakdown callout (percentages by format type)

### 9. Who to Watch
Creators NOT in the system. See "Creator Scouting" in SKILL.md.

Each recommendation must include: name, handles (linked), follower count, current sponsors, and a "Why she/he maps" explanation grounded in a specific data pattern from the ecosystem.

End with a callout about enabling systematic discovery (Creator Discovery MCP).

### 10. Locker Room Talk (Overheard)
6-8 direct quotes from athlete content.

```html
<div class="overheard-item">
  <p class="overheard-quote">"[Direct quote]"</p>
  <p class="overheard-source">— <a href="[source URL]">@[handle]</a> [context]. [Data point if relevant].</p>
</div>
```

**Selection criteria:** Quotes that demonstrate the autonomous model at work — authentic, unscripted, culturally resonant. Mix of: personal vulnerability, cultural commentary, product passion, competition achievement, humour.

### 11. What We're Watching Next
4-6 forward-looking signals.

```html
<p class="body-text">
  <strong>[Signal title]</strong> [1-2 sentences explaining what to track and by when.]
</p>
```

These should be specific and measurable: "If X is still doing Y by Issue #N, then Z." Not generic: "We'll continue to monitor trends."

### 12. Footer
```html
<div class="footer">
  <div class="footer-brand">Partner Pulse by CurAItion</div>
  <p class="footer-text">
    Prepared for the Gymshark Social Media & Content Marketing Team.<br>
    [Data summary].<br>
    [Data window and baseline note].
  </p>
  <div class="footer-sources">
    <strong>Sources & Methodology:</strong><br>
    [List each CurAItion tool used and its parameters]<br>
    [Note any limitations: no historical baseline, manual deduplication, etc.]<br>
    All data scoped to org_id: 297e242a / project_id: 83472bde<br>
    All hyperlinks verified against CurAItion content URLs
  </div>
</div>
```

## CSS Classes Reference

All CSS classes used in the digest should be defined in a `<style>` block in the `<head>`. See the Issue #1 digest for the complete stylesheet. Key classes:

- `.root-container` — 660px max-width, white background, centered
- `.header` — Dark background, white text
- `.section-label` — Small uppercase teal label
- `.section-title` — Large Playfair Display heading
- `.body-text` — Inter 15px, 1.7 line height, #333
- `.body-text a` — Teal links with bottom border
- `.stats-bar` — Flex row of stat items
- `.callout` — Dark background box for key insights
- `.athlete-table` — Styled data table
- `.badge` — Small coloured label
- `.overheard-item` — Quote block with source
- `.visual-card` — Embed card with iframe/image and metadata
- `.pick` — Signal/pick item with number, title, meta
