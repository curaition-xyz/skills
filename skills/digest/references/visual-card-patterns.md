# Visual Citation Card Patterns — Detailed Reference

Every digest section should include 1-2 visual citation cards that embed REAL source content. These cards ground the editorial analysis in actual evidence the reader can click through to.

## Table of Contents

1. YouTube Video Card
2. YouTube Timestamp Card
3. Article/Text-Only Card
4. Instagram Card (dual-path)
5. AI-Generated Editorial Imagery
6. General Principles

---

## 1. YouTube Video Card (thumbnail + link)

**IMPORTANT — single href per card:** The entire card links via the image. The title is plain text (not a second `<a>` tag). This prevents the card from consuming 2 of the source's max-2 href budget before it even appears in the Sources section.

```html
<div style="margin: 24px 0; border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden;">
  <a href="{VIDEO_URL}" target="_blank" style="display: block; text-decoration: none;">
    <img src="{THUMBNAIL_URL}" alt="{TITLE}" style="width: 100%; height: auto; display: block;" />
  </a>
  <div style="padding: 12px 16px; background: #fafafa;">
    <div style="font-family: 'Inter', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #999; margin-bottom: 4px;">{CONTENT_TYPE} · {SOURCE}</div>
    <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 16px; color: #1a1a1a; font-weight: 600;">{TITLE}</div>
    <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: #666; margin: 8px 0 0 0; line-height: 1.4;">{EDITORIAL_CONTEXT}</p>
  </div>
</div>
```

Where:
- `{THUMBNAIL_URL}` = `citations.embed.thumbnail_url` from `curaition_get_content`
- `{VIDEO_URL}` = the content's `source_url` (prefer the direct watch URL, not the embed URL)
- `{TITLE}` = content title from CurAItion
- `{CONTENT_TYPE}` = "VIDEO", "SHORT", "REEL", etc.
- `{SOURCE}` = channel/creator name
- `{EDITORIAL_CONTEXT}` = one sentence of editorial analysis connecting this source to the section's narrative

## 2. YouTube Timestamp Card (for specific cited moments)

```html
<div style="margin: 16px 0; padding: 12px 16px; background: #f8f8f8; border-left: 3px solid {ACCENT_COLOR}; border-radius: 0 4px 4px 0;">
  <div style="font-family: 'Inter', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #999; margin-bottom: 4px;">SOURCE · {TIMESTAMP}</div>
  <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #333; margin: 0; line-height: 1.5;">"{QUOTE}"</p>
  <a href="{TIMESTAMP_URL}" target="_blank" style="font-family: 'Inter', sans-serif; font-size: 12px; color: {ACCENT_COLOR}; text-decoration: none; margin-top: 8px; display: inline-block;">Watch from {TIMESTAMP} →</a>
</div>
```

Where:
- `{TIMESTAMP_URL}` = `citations.themes[].citations[].timestamp_url`
- `{TIMESTAMP}` = `citations.themes[].citations[].timestamp` (e.g., "01:23")
- `{QUOTE}` = the citation quote text

## 3. Article/Text-Only Card (when no thumbnail available)

```html
<div style="margin: 16px 0; padding: 16px; border: 1px solid #e0e0e0; border-radius: 4px; background: #fafafa;">
  <div style="font-family: 'Inter', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #999; margin-bottom: 4px;">ARTICLE · {SOURCE}</div>
  <a href="{URL}" target="_blank" style="font-family: 'Playfair Display', Georgia, serif; font-size: 16px; color: #1a1a1a; text-decoration: none; font-weight: 600;">{TITLE}</a>
  <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: #666; margin: 8px 0 0 0; line-height: 1.4;">{EDITORIAL_CONTEXT}</p>
</div>
```

## 4. Instagram Card (dual-path: thumbnail preferred, iframe fallback)

### Path A (preferred) — When `citations.embed.thumbnail_url` IS present

Use the same single-href `<img>` card pattern as YouTube. Title is plain text — the image is the clickable element.

```html
<div style="margin: 24px 0; border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden;">
  <a href="{POST_URL}" target="_blank" style="display: block; text-decoration: none;">
    <img src="{THUMBNAIL_URL}" alt="{TITLE}" style="width: 100%; height: auto; display: block;" />
  </a>
  <div style="padding: 12px 16px; background: #fafafa;">
    <div style="font-family: 'Inter', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #999; margin-bottom: 4px;">INSTAGRAM · @{HANDLE}</div>
    <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 15px; color: #1a1a1a; font-weight: 600;">{TITLE}</div>
    <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: #666; margin: 8px 0 0 0; line-height: 1.4;">{EDITORIAL_CONTEXT}</p>
  </div>
</div>
```

### Path B (fallback) — When `citations.embed.thumbnail_url` is absent (legacy content)

Use the native Instagram embed iframe. The iframe src counts as one href — keep the title as plain text to stay within budget.

```html
<div style="margin: 24px 0; border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden;">
  <iframe src="https://www.instagram.com/p/{SHORTCODE}/embed/"
          width="100%" height="480"
          frameborder="0" scrolling="no"
          allowtransparency="true"
          style="border: none; display: block;">
  </iframe>
  <div style="padding: 12px 16px; background: #fafafa;">
    <div style="font-family: 'Inter', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #999; margin-bottom: 4px;">INSTAGRAM · @{HANDLE}</div>
    <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 15px; color: #1a1a1a; font-weight: 600;">{TITLE}</div>
    <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: #666; margin: 8px 0 0 0; line-height: 1.4;">{EDITORIAL_CONTEXT}</p>
  </div>
</div>
```

Where:
- `{SHORTCODE}` = extracted from the Instagram URL (e.g., `DVWMwWzAQAQ` from `https://www.instagram.com/p/DVWMwWzAQAQ/`)
- `{POST_URL}` = the full Instagram post URL from CurAItion
- `{HANDLE}` = the Instagram account handle (extract from URL or content metadata)

Always check `citations.embed.thumbnail_url` first. If present, use Path A. If absent, use Path B. Never fall back to text-only cards for Instagram content — one of these two paths will always work.

## 5. AI-Generated Editorial Imagery (via CurAItion Asset Registry)

For sections without strong visual source content, use `curaition_asset_registry` with action `generate_backfill` to create custom editorial illustrations via Replicate (Flux Schnell).

**When to use:**
- A section has no CurAItion content items with usable thumbnails
- The digest covers a topic where source content is text-heavy (articles, reports)
- You want a custom section header image that captures the editorial theme

**How to use:**
```
curaition_asset_registry → action: "generate_backfill"
```
Provide a prompt grounded in the digest's content analysis. The tool generates unique imagery. Use the returned image URL in a standard card layout.

**When NOT to use:**
- When real source thumbnails exist — always prefer authentic content imagery
- For every section — use sparingly (1-2 per digest max) to maintain editorial authenticity

## 6. General Principles

- Use REAL `thumbnail_url` values from `curaition_get_content` — never generate placeholder image text descriptions
- For Instagram, check `citations.embed.thumbnail_url` first (preferred), then iframe fallback
- Every major section (Opinion, Best in Show, From the Field) should have at least one visual citation card
- If no thumbnail AND no iframe is possible, fall back to the Article/Text-Only card
- Always link to the original source via `source_url`
- Keep editorial context to one sentence — the card is evidence, not analysis
- YouTube thumbnails are hotlinked from YouTube CDN — they render in any email client or browser
- Instagram thumbnails (when available) render everywhere; iframe fallback renders in browsers only
- **DEDUP**: Each source content item gets AT MOST one visual card across the entire digest (see Content Deduplication Rules in SKILL.md)
