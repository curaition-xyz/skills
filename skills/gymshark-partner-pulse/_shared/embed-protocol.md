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

### Instagram (PREFERRED — official `blockquote` + `embed.js`, not raw iframe)

**Use Instagram's official embed pattern**, not the `/embed/` iframe URL. The iframe approach requires you to guess width and height — and you'll guess wrong, because real posts come in mixed aspect ratios (9:16 reels, 1:1 photos, 4:5 portrait carousels) and a single hard-coded size will distort at least one of them. Issue 6 (2026-06-02) shipped twice with broken iframe dimensions (first height=540 clipped chrome, then 540×800 gave a 1:1 video the wrong proportions) before switching to this pattern.

`blockquote` + `embed.js` lets Instagram render each post at its real aspect ratio and respects `max-width: 540px` automatically via inline styles Instagram bakes into the blockquote.

**`.embed-card` CSS** (Instagram brings its own border/shadow, so the wrapper just centers and caps width):

```css
.embed-card {
  max-width: 540px;       /* Instagram's native embed render width */
  margin: 22px auto;      /* center inside the 660px article column */
  background: transparent;
}
/* If you also have non-IG "visual citation" cards in the digest, give them a
   different class (e.g. .embed-card.cite) so they keep their framed look. */
.embed-card.cite {
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
  background: #fafafa;
}
.embed-caption {
  padding: 12px 16px;
  margin-top: 8px;        /* sits below the IG blockquote with a small gap */
  font-size: 12px;
  color: #555;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 4px;
}
.embed-card.cite .embed-caption { margin-top: 0; border: 0; border-top: 1px solid #eee; border-radius: 0; }
```

**The embed itself** — extract the shortcode (e.g. `DWGKOYsDGmD` from `https://www.instagram.com/p/DWGKOYsDGmD/`) and use:

```html
<div class="embed-card">
  <blockquote class="instagram-media"
    data-instgrm-permalink="https://www.instagram.com/p/DWGKOYsDGmD/"
    data-instgrm-version="14"
    style="background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin:0; max-width:540px; min-width:326px; padding:0; width:100%;">
    <a href="https://www.instagram.com/p/DWGKOYsDGmD/" target="_blank">View this post on Instagram</a>
  </blockquote>
  <div class="embed-caption">
    <a href="https://www.instagram.com/p/DWGKOYsDGmD/">@handle</a> — Brief context about why this content matters
  </div>
</div>
```

**Include the `embed.js` script ONCE per digest**, just before `</body>`:

```html
<script async src="https://www.instagram.com/embed.js"></script>
```

This script replaces every `blockquote.instagram-media` on the page with a correctly-sized iframe. It only needs to be loaded once.

**For Instagram Reels:** use `/p/SHORTCODE/` in the `data-instgrm-permalink` and the fallback `<a href>`. Do NOT use `/reel/SHORTCODE/embed/` — `embed.js` handles the routing.

**Why this pattern, not the iframe URL:**
- `/embed/` iframe forces a fixed width and height that you have to guess. Mixed aspect ratios in the same digest break this.
- `embed.js` reads the real post dimensions from Instagram's CDN and renders at the true ratio.
- `max-width: 540px` is baked into Instagram's blockquote inline styles, so even if your CSS is overridden by a downstream renderer, the cap holds.
- This is the same code Instagram's own "Embed" share-sheet generates. Use what they ship.

**Fallback when JavaScript is disabled** (e.g. some email clients): the blockquote degrades to a styled "View this post on Instagram" link via the `<a>` tag. The text-only fallback is acceptable — better than a broken iframe.

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
