# Embed Protocol — Real Content, Not Placeholders

Every Gymshark digest MUST contain real embedded content. No emoji placeholders. No empty divs with captions. The reader must be able to see or click through to the actual content being discussed.

## Minimum Embed Counts

| Digest | Section | Minimum Embeds |
|---|---|---|
| Partner Pulse | The Big Story | 1 |
| Partner Pulse | Athlete Spotlight | 1 |
| Partner Pulse | Three Signals (total) | 1 |
| Market Pulse | The Big Move | 1 |
| Market Pulse | Brand Teardowns (total) | 2 |
| Market Pulse | Cross-Domain Signals (total) | 1 |

**Total minimum per digest: 3 real embeds.**

## Sourcing Embed URLs

All embed URLs must come from CurAItion data:

1. During Batch 3 (source URL collection), identify 5-8 high-quality content items suitable for embedding
2. Prioritise: Instagram carousels and posts (most reliable embeds), TikTok videos, YouTube thumbnails
3. Extract the `url` / `source_url` from `curaition_semantic_search` or `curaition_list_content` results
4. Parse platform and content ID from the URL

## Embed Formats by Platform

### Instagram (PREFERRED — most reliable)

Extract the shortcode from the URL. For `https://www.instagram.com/p/DWGKOYsDGmD/`, the shortcode is `DWGKOYsDGmD`.

```html
<div class="embed-card">
  <iframe
    src="https://www.instagram.com/p/DWGKOYsDGmD/embed/"
    width="100%"
    height="480"
    frameborder="0"
    scrolling="no"
    allowtransparency="true"
    style="border: none; overflow: hidden;">
  </iframe>
  <div class="embed-caption">
    <a href="https://www.instagram.com/p/DWGKOYsDGmD/">@handle</a> — Brief context about why this content matters
  </div>
</div>
```

For Instagram Reels: `https://www.instagram.com/reel/SHORTCODE/embed/`

### TikTok

Use the blockquote embed format. For `https://www.tiktok.com/@fitnessnojo/video/7618630671807941910`:

```html
<div class="embed-card">
  <blockquote class="tiktok-embed"
    cite="https://www.tiktok.com/@fitnessnojo/video/7618630671807941910"
    data-video-id="7618630671807941910"
    style="max-width: 605px; min-width: 325px;">
    <section>
      <a target="_blank" href="https://www.tiktok.com/@fitnessnojo/video/7618630671807941910">
        View on TikTok — @fitnessnojo
      </a>
    </section>
  </blockquote>
  <script async src="https://www.tiktok.com/embed.js"></script>
  <div class="embed-caption">
    <a href="https://www.tiktok.com/@fitnessnojo">@fitnessnojo</a> — Brief context
  </div>
</div>
```

**Note:** TikTok embeds require JavaScript and may not render in all email clients or static HTML viewers. Always include a fallback link inside the blockquote.

### YouTube (VISUAL CARD ONLY — no iframe)

YouTube iframes frequently fail with player configuration errors in static HTML contexts. Use a styled visual card instead:

```html
<div class="embed-card">
  <a href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank"
     style="display: block; text-decoration: none;">
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #333 100%);
                padding: 40px 20px; text-align: center; color: white;">
      <div style="font-size: 48px; margin-bottom: 12px;">▶</div>
      <div style="font-size: 14px; font-weight: 600;">Video Title</div>
      <div style="font-size: 12px; color: #999; margin-top: 4px;">@handle · YouTube</div>
    </div>
  </a>
  <div class="embed-caption">
    <a href="https://www.youtube.com/watch?v=VIDEO_ID">Watch on YouTube</a> — Brief context
  </div>
</div>
```

## Fallback: Styled Citation Card

If an embed cannot be created (content deleted, private, or platform not supported), use a styled citation card:

```html
<div class="embed-card" style="border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden;">
  <div style="padding: 20px; background: #f5f5f5;">
    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #999; margin-bottom: 8px;">
      [Platform] · [Content Type]
    </div>
    <div style="font-size: 15px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px; line-height: 1.4;">
      [Content Title — actual title from CurAItion data]
    </div>
    <div style="font-size: 13px; color: #666;">
      <a href="[source_url]">@handle</a> · [date] · [engagement metric if available]
    </div>
  </div>
</div>
```

This is always better than an emoji placeholder in a coloured div.

## What NOT To Do

```html
<!-- WRONG: Emoji placeholder -->
<div class="embed-thumbnail">⚽</div>

<!-- WRONG: Empty embed card with only text -->
<div class="embed-card">
  <div class="embed-caption">Featured Content: @handle — topic</div>
</div>

<!-- WRONG: YouTube iframe (frequently fails) -->
<iframe src="https://www.youtube.com/embed/VIDEO_ID" ...></iframe>
```
