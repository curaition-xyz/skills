# Section Structure Reference — Market Pulse HTML

## Design System

**Fonts:**
- Headings: `'Playfair Display', Georgia, serif`
- Body: `'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif`
- Import: `https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap`

**Colours:**
- Accent: `#FF4D4D` (competitive red — NOT teal, that's Partner Pulse)
- Header background: `#111111`
- Body text: `#333` / `#1a1a1a`
- Muted text: `#666` / `#999`
- Dividers: `#e0e0e0`
- Callout background: `#fff5f5` with `#FF4D4D` left border

**Layout:**
- Root container: `max-width: 660px`, white background
- Content padding: `48px 32px`
- Section margin: `56px` between major sections

## Section Templates

### 1. Header
```html
<header>
  <div class="header-date">Market Pulse</div>
  <h1>[Headline — the single strongest competitive insight, max 6 words]</h1>
  <div class="header-subtitle">[DD Month YYYY] — Issue #[N]</div>
</header>
```

### 2. The Competitive Landscape
Stats bars showing: total competitor content, top 5 brands by volume, format breakdown.
Each stat in a `<div class="stat-bar">` with `<strong>` label and `<p>` detail.

### 3. The Big Move
Deep editorial on one competitor brand. Must include:
- Brand name linked to verified profile (from LINK_REGISTRY)
- At least 1 real content embed (Instagram iframe preferred)
- "What This Means for Gymshark" callout box
- NOT a brand mid-campaign push

### 4. Brand Teardowns
4-5 competitor analyses in `<div class="card">` elements. Each includes:
- Brand name as `<h4>` with link
- `<div class="card-meta">` — item count, lookback period
- Volume strategy, visual language, notable play paragraphs
- Callout with key insight
- ALL DIFFERENT brands from The Big Move

### 5. Format Innovations
Specific creative techniques, NOT which formats are popular. 3-4 innovations with:
- Named technique (e.g., "The Context Stack")
- Which brands are doing it
- How it works (specific enough to replicate)

### 6. Cross-Domain Signals
2-3 signals from Tier 3 (global) data. Each in its own `<h3>` with:
- What's happening (the pattern)
- Why Gymshark should care (the connection)
- At least one embed card linking to the CurAItion source content

### 7. The Watchlist
Brands NOT currently tracked. Each with:
- `<h3>` brand name + positioning description
- Verified handles linked to profiles
- Why track (grounded in competitive data pattern)
- Callout for full scouting brief reference

### 8. What We're Tracking Next
Follow `../_shared/activation-format.md` — three-part format for each signal:
- The Signal (specific, time-bound trigger)
- The Prompt (copy-paste CurAItion query in a callout)
- The Brief Starter (executable creative concept)

### 9. Footer
```html
<footer>
  <p>Market Pulse is a [cadence] competitive intelligence digest for Gymshark's
  Social Media & Content Marketing Team. Data from CurAItion intelligence platform
  ([N] tracked competitor items, [N] domains, [N]-day window). Next issue: [date].</p>
</footer>
```

## Embed Patterns

Follow `../_shared/embed-protocol.md` for all embed HTML. Market Pulse uses the same embed formats as Partner Pulse but with `#FF4D4D` accent colour instead of `#54D4C6`.

## CSS Classes Reference

Key classes (define in `<style>` block):
- `.container` — 660px max-width, white background, centered
- `header` — Dark background, white text, red accent border
- `.stat-bar` — Stats with red left border
- `.callout` — Red-tinted callout box
- `.card` — Brand teardown card
- `.embed-card` — Content embed container
- `.brand-link` — Red link style for brand names
