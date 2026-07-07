# Installing `carousel-producer` (v2.1)

Brand-locked Instagram carousel producer for CurAItion. Turns CurAItion cultural
intelligence into 1080×1440 typographic PNG slides (olive-on-cream Geist, mycelium
watermark, one data chart, brand outro), rendered deterministically by headless
Chromium via Playwright. Image generation is intentionally a **separate** skill;
this one owns the brand renderer and the `carousel.json` schema (including the
optional image-composite layer that the future image-gen skill plugs into).

---

## 1. Package contents

```
carousel-producer/
├── SKILL.md                       # the skill (intelligence layers + brand spec)
├── INSTALL.md                     # this file
├── assets/
│   ├── Geist-Regular.woff2        # Geist 400 (OFL)
│   ├── Geist-Light.woff2          # Geist 300 (OFL)
│   └── mycelium-mark-olive.png    # mark; alpha used as a recolourable CSS mask
├── scripts/
│   └── render_carousel.py         # carousel.json → PNG renderer (the brand spec in code)
└── examples/
    ├── carousel.example.json      # a complete 9-slide reference
    └── demo-image-slide.json      # image-background compositing demo
```

The renderer is runtime-agnostic — a plain `carousel.json → PNG` module with no host
coupling. It runs identically under Cowork, Claude Code, or a self-hosted Hermes-Agent.

---

## 2. Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.10+** | The renderer is pure Python. |
| **Playwright (Python)** | `pip install playwright` |
| **Chromium** | `playwright install chromium` (downloads ~110 MB) |
| **Chromium system libraries** | `sudo playwright install-deps chromium` (Debian/Ubuntu). One-time. |
| **Pillow** *(optional)* | `pip install pillow` — recompresses PNGs (6 MB → ~100 KB). Renderer skips this step gracefully if absent. |

Install the renderer stack:

```bash
pip install playwright pillow
playwright install chromium
sudo playwright install-deps chromium   # skip only if libs already present
```

Verify Chromium is usable:

```bash
python -c "from playwright.sync_api import sync_playwright as s; \
  b=s().start().chromium.launch(); print('chromium ok'); b.close()"
```

> **No root?** If you can't run `install-deps` (locked-down host / sandbox), the
> bundled Chromium still runs once its shared libraries are reachable. Download the
> dep `.deb`s, extract them into a prefix, and launch with
> `LD_LIBRARY_PATH=/your/prefix/usr/lib/<arch>` and
> `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`. On a normal server you won't need
> this — `install-deps` is the supported path.

---

## 3. Install the skill

### Cowork (Claude desktop)

Use the **Save skill** button on the `carousel-producer.skill` card, then confirm it
under **Settings → Capabilities**. (A running session uses a read-only cache; installing
the `.skill` is what registers it.)

### Claude Code

Unzip the package into your skills directory:

```bash
unzip carousel-producer.skill -d ~/.claude/skills/
# result: ~/.claude/skills/carousel-producer/SKILL.md (+ assets, scripts, examples)
```

### Self-hosted Hermes-Agent

Hermes uses the same `SKILL.md` model (name + description + procedure, loaded on demand).
Drop the folder into a Hermes skills directory and sync:

```bash
# place carousel-producer/ under your Hermes skills path, then:
hermes skills opt-in --sync
```

See the Hermes “Skills System” docs for the exact external-skill-directory location on
your install.

---

## 4. Connect CurAItion (MCP)

Layers 1–2 of the skill call CurAItion MCP tools (`curaition_list_content`,
`curaition_get_content`, `curaition_get_cited_themes`, `curaition_trend_analysis`) plus
`WebSearch`. Wire the CurAItion MCP server for your host:

**Cowork / Claude Code** — add the CurAItion connector (HTTP MCP endpoint with your
CurAItion auth) in the app's connector settings.

**Hermes-Agent** — declare it in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  curaition:
    url: "https://<your-curaition-mcp-endpoint>/mcp"   # fill in
    auth: oauth            # or: headers: { Authorization: "Bearer <token>" }
    timeout: 180
```

or `hermes mcp add curaition --url https://<endpoint>/mcp --auth oauth`.

> CurAItion ingestion (`curaition_asset_registry`) is **optional** and used only when
> publishing through CurAItion. For a local deliverable you can skip it. Note: registry
> ingestion of image-free slides hasn't yet been validated against the live API — test
> a `create` before relying on it in a pipeline.

---

## 5. Verify the install

Render the bundled example and check the output:

```bash
cd carousel-producer
python scripts/render_carousel.py examples/carousel.example.json --out-dir out/
```

Expect nine `out/example-slide-01.png … -09.png` files at **1080×1440**. Open
`examples/preview.html` (if present in your bundle) to review them as a strip.

Test the image-composite layer too:

```bash
python scripts/render_carousel.py examples/demo-image-slide.json --out-dir out-demo/
```

Slide 1 is image-free (olive mark); slides 2–3 composite text over an image with cream
text and a cream mark.

---

## 6. Usage

Author a `carousel.json` and render it:

```bash
python scripts/render_carousel.py carousel-<slug>.json --out-dir out/ \
  [--chromium /path/to/chrome]     # optional explicit Chromium build
```

Minimal schema (full reference in `examples/carousel.example.json` and `SKILL.md`):

```json
{
  "slug": "my-carousel",
  "slides": [
    {"type": "content", "copy": "Line one\nLine two"},
    {"type": "content", "copy": "A shorter beat.", "font_size": 100},
    {"type": "chart", "title": "A cited figure", "unit": "%",
     "source": "Source: … (CurAItion cited)",
     "bars": [{"label": "A", "value": 58}, {"label": "B", "value": 41}]},
    {"type": "content", "copy": "…"},
    {"type": "final"}
  ]
}
```

- **Default shape:** 8 content slides + 1 `final`, with one `chart` at position 3–5.
  Overridable — flex the count, drop the chart if there's no honest figure.
- **`content`**: `copy` (use `\n` for hard line breaks — you own every break; no widows),
  optional `font_size` to prevent long-line clipping.
- **`chart`**: `title`, `bars[{label,value}]`, `unit`, `source`. One chart, real cited numbers.
- **`final`**: optional `wordmark` (default `curAItion`) and `url` (default `curaition.xyz`).
- **Image layer** (image-gen skill only): add a `background` block to any slide —
  `{image, fit, focal, treatments:[duotone|scrim-bottom|scrim-full|blur:N|dim:N|grayscale], text_color, mark_color}`.
  Brand content cards stay image-free by design.

Brand tokens (owned by the renderer — don't hand-tune per carousel): olive `#6B7A3F`,
cream `#F1EFE8`, stone `#C8C3B4`, Geist 400/300, 1080×1440.

---

## 7. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `Host system is missing dependencies` / browser won't launch | Run `sudo playwright install-deps chromium`. Rootless: see the `LD_LIBRARY_PATH` note in §2. |
| `playwright not installed` | `pip install playwright && playwright install chromium`. |
| Text renders in a system font, not Geist | The bundled fonts are **WOFF2** and require a real browser engine (Chromium decodes them). Don't substitute a legacy rasteriser like wkhtmltoimage — its Qt WebKit can't decode WOFF2. |
| Mark invisible on an image slide | Set `background.mark_color`, or ensure the slide has a `background` (the mark auto-switches to cream over images). |
| `missing bundled asset` | Run the renderer from inside the `carousel-producer/` folder so it finds `../assets`. Don't move `scripts/` away from `assets/`. |
| PNGs are ~6 MB each | Install Pillow (`pip install pillow`) so the optimization pass runs. |
| Registry `create` rejects a slide | Image-free slides have no `image_prompt`/`image_url_original`; pass a bracketed placeholder and host the PNG in your publishing step. Verify with `curaition_asset_registry action:get`. |

---

*carousel-producer v2.1 · brand-render pipeline (Chromium) · CurAItion Intelligence Desk*
