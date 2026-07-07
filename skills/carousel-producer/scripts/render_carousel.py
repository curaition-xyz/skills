#!/usr/bin/env python3
"""
CurAItion Carousel Producer — brand renderer (Playwright / Chromium).

Renders a carousel JSON into 1080x1440 PNG slides conforming to the CurAItion
brand carousel spec, using headless Chromium via Playwright. Chromium is the
deliberate choice over lighter rasterisers: it renders the spec's WOFF2 fonts
natively, and — crucially — it gives the future image-generation companion
skill a real CSS compositing layer (scrims, blend modes, blur, duotone) to
place brand typography over generated imagery. See the `background` block.

BRAND SLIDES (image-free):
  - content : olive #6B7A3F on cream #F1EFE8, large centred Geist, block just
              below centre, two-digit number top-right, mycelium mark ~62px
              centred at the bottom.
  - chart   : olive bars on cream, sparse grid, Geist labels, ghosted mark at
              5% behind the plot.
  - final   : mark + "curAItion" wordmark inline lockup, truly centred;
              curaition.xyz in Geist Light at the bottom.

FORWARD-COMPATIBLE IMAGE LAYER:
  Any slide may carry an optional `background` block. When present, the renderer
  composites a full-bleed image behind the slide content with legibility
  treatments. Brand content slides omit it; the image-gen skill supplies it.
  This keeps ONE renderer and ONE carousel.json schema across both skills.

    "background": {
      "image": "file:///abs/path.png" | "https://...",
      "fit": "cover",                     # cover|contain, default cover
      "focal": "50% 40%",                 # background-position, default 50% 50%
      "treatments": ["duotone", "scrim-bottom", "dim:0.25", "blur:4"],
      "text_color": "#F1EFE8"             # override copy colour for legibility
    }

  Treatment tokens: scrim-bottom | scrim-full | dim:<0..1> | blur:<px> |
  duotone | grayscale.  Order in the list is the paint order (bottom to top).

USAGE
    python render_carousel.py carousel.json --out-dir out/ \
        [--chromium /path/to/chrome]     # optional explicit executable

The carousel JSON schema is documented in examples/carousel.example.json.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import sys
from pathlib import Path

# ---- Brand constants (single source of truth) -----------------------------
OLIVE = "#6B7A3F"
CREAM = "#F1EFE8"
STONE = "#C8C3B4"
SCRIM = "20, 22, 14"     # near-black olive, for scrims/dim (rgb tuple string)
W, H = 1080, 1440

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT_REGULAR = ASSETS / "Geist-Regular.woff2"
FONT_LIGHT = ASSETS / "Geist-Light.woff2"
MARK_PNG = ASSETS / "mycelium-mark-olive.png"


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def _font_face_css() -> str:
    return (
        "@font-face{{font-family:'Geist';font-weight:400;font-style:normal;"
        "src:url(data:font/woff2;base64,{reg}) format('woff2')}}"
        "@font-face{{font-family:'Geist';font-weight:300;font-style:normal;"
        "src:url(data:font/woff2;base64,{light}) format('woff2')}}"
    ).format(reg=_b64(FONT_REGULAR), light=_b64(FONT_LIGHT))


def _mark_uri() -> str:
    return "data:image/png;base64," + _b64(MARK_PNG)


def _png_size(path: Path) -> tuple[int, int]:
    """Read width/height from a PNG IHDR without importing PIL."""
    import struct
    data = path.read_bytes()[16:24]
    w, h = struct.unpack(">II", data)
    return w, h


_MARK_W, _MARK_H = _png_size(MARK_PNG)
MARK_ASPECT = _MARK_H / _MARK_W  # height / width


def _mark_style(width: int, color: str, opacity: float | None = None) -> str:
    """Inline style for the mycelium mark as a recolourable CSS mask.
    The PNG's alpha is the stencil; `color` fills it — so the same asset
    renders olive on brand slides and cream over dark imagery."""
    h = round(width * MARK_ASPECT)
    uri = _mark_uri()
    op = ("opacity:%s;" % opacity) if opacity is not None else ""
    return (
        "width:%dpx;height:%dpx;background-color:%s;%s"
        "-webkit-mask:url(%s) no-repeat center/contain;"
        "mask:url(%s) no-repeat center/contain;"
        "-webkit-mask-mode:alpha;mask-mode:alpha"
        % (width, h, color, op, uri, uri)
    )


def _mark_color_for(slide: dict) -> str:
    """Mark follows the light/dark context like the copy: cream over an
    image, olive on a brand card. Overridable via background.mark_color."""
    bg = slide.get("background")
    if bg and bg.get("mark_color"):
        return bg["mark_color"]
    if bg and bg.get("image"):
        return CREAM
    return OLIVE


# :root tokens injected via concatenation so the rest of the sheet may safely
# contain literal '%' (e.g. translateX(-50%)) without breaking % formatting.
_ROOT_CSS = ":root{--olive:%s;--cream:%s;--stone:%s;--scrim:%s}" % (
    OLIVE, CREAM, STONE, SCRIM
)
BASE_CSS = _ROOT_CSS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1440px}
body{background:var(--cream);font-family:'Geist',sans-serif;
  -webkit-font-smoothing:antialiased}
.slide{position:relative;width:1080px;height:1440px;overflow:hidden;
  background:var(--cream)}
/* --- optional background image layer --- */
.bg{position:absolute;inset:0;background-repeat:no-repeat}
.bg-fx{position:absolute;inset:0}
.num{position:absolute;top:58px;right:66px;font-weight:300;font-size:30px;
  letter-spacing:0.05em;color:var(--stone);z-index:5}
.mark-bottom{position:absolute;left:50%;bottom:66px;
  transform:translateX(-50%);z-index:5}
.content-layer{position:absolute;inset:0;z-index:4}
"""


# ---------------------------------------------------------------------------
# Background compositing (forward-compatible image layer)
# ---------------------------------------------------------------------------
def _background_html(bg: dict) -> str:
    """Return the HTML for the background image + treatment layers."""
    if not bg or not bg.get("image"):
        return ""
    image = html.escape(bg["image"], quote=True)
    fit = bg.get("fit", "cover")
    focal = bg.get("focal", "50% 50%")
    treatments = bg.get("treatments", []) or []

    bg_filters = []
    fx_layers = []
    for t in treatments:
        name, _, arg = str(t).partition(":")
        name = name.strip()
        if name == "blur":
            bg_filters.append("blur(%spx)" % (arg or "4"))
        elif name == "grayscale":
            bg_filters.append("grayscale(1)")
        elif name == "duotone":
            # desaturate the image, then blend olive (multiply) + cream (screen)
            bg_filters.append("grayscale(1) contrast(1.05)")
            fx_layers.append(
                "<div class='bg-fx' style='background:var(--olive);"
                "mix-blend-mode:multiply'></div>"
            )
            fx_layers.append(
                "<div class='bg-fx' style='background:var(--cream);"
                "mix-blend-mode:screen;opacity:.35'></div>"
            )
        elif name == "dim":
            a = arg or "0.3"
            fx_layers.append(
                "<div class='bg-fx' style='background:rgba(var(--scrim),%s)'></div>" % a
            )
        elif name == "scrim-bottom":
            fx_layers.append(
                "<div class='bg-fx' style='background:linear-gradient("
                "to bottom,rgba(var(--scrim),0) 42%,rgba(var(--scrim),.86) 100%)'></div>"
            )
        elif name == "scrim-full":
            fx_layers.append(
                "<div class='bg-fx' style='background:rgba(var(--scrim),.5)'></div>"
            )

    filt = ("filter:%s;" % " ".join(bg_filters)) if bg_filters else ""
    bg_div = (
        "<div class='bg' style=\"background-image:url('%s');"
        "background-size:%s;background-position:%s;%s\"></div>"
        % (image, fit, focal, filt)
    )
    return bg_div + "".join(fx_layers)


def _text_color(slide: dict, default: str = OLIVE) -> str:
    bg = slide.get("background")
    if bg and bg.get("text_color"):
        return bg["text_color"]
    if bg and bg.get("image"):
        return CREAM  # sensible default over imagery
    return default


def _doc(body: str, extra_css: str = "") -> str:
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        + _font_face_css() + BASE_CSS + extra_css
        + "</style></head><body>" + body + "</body></html>"
    )


def _num(n) -> str:
    if n is None:
        return ""
    try:
        return "%02d" % int(n)
    except (TypeError, ValueError):
        return html.escape(str(n))


# ---- Content slide --------------------------------------------------------
CONTENT_CSS = """
.wrap{display:table;width:1080px;height:1440px}
.cell{display:table-cell;vertical-align:middle;
  padding:180px 104px 130px;text-align:center}
.copy{font-weight:400;letter-spacing:-0.012em}
"""


def render_content_html(slide: dict) -> str:
    copy = slide.get("copy", "")
    size = int(slide.get("font_size", 108))
    lh = slide.get("line_height", 1.08)
    color = _text_color(slide)
    inner = "<br>".join(html.escape(ln) for ln in copy.split("\n"))
    body = (
        "<div class='slide'>"
        "%(bg)s"
        "<div class='num'>%(num)s</div>"
        "<div class='content-layer'><div class='wrap'><div class='cell'>"
        "<div class='copy' style='font-size:%(size)dpx;line-height:%(lh)s;"
        "color:%(color)s'>%(copy)s</div>"
        "</div></div></div>"
        "<div class='mark-bottom' style='%(mark)s'></div>"
        "</div>"
    ) % {
        "bg": _background_html(slide.get("background")),
        "num": _num(slide.get("n")),
        "size": size, "lh": lh, "color": color,
        "copy": inner, "mark": _mark_style(62, _mark_color_for(slide)),
    }
    return _doc(body, CONTENT_CSS)


# ---- Chart slide ----------------------------------------------------------
CHART_CSS = """
.ctitle{position:absolute;top:150px;left:104px;width:872px;text-align:center;
  font-weight:400;font-size:46px;line-height:1.15;color:var(--olive);
  letter-spacing:-0.01em;z-index:4}
.ghost{position:absolute;left:50%;top:760px;transform:translate(-50%,-50%);z-index:1}
.plot{position:absolute;left:132px;top:470px;width:816px;height:560px;z-index:3}
.grid{position:absolute;left:0;width:816px;height:1px;background:var(--olive);
  opacity:0.12}
.bars{position:absolute;left:0;bottom:0;width:816px;height:560px;
  display:table;table-layout:fixed}
.bcol{display:table-cell;vertical-align:bottom;text-align:center;padding:0 10px}
.bval{font-weight:400;font-size:30px;color:var(--olive);margin-bottom:14px}
.bar{background:var(--olive);margin:0 auto;width:78%}
.blabel{position:absolute;left:0;top:566px;width:816px;height:70px;
  display:table;table-layout:fixed}
.blcell{display:table-cell;text-align:center;padding:0 8px;
  font-weight:300;font-size:26px;color:var(--olive);letter-spacing:0.01em}
.csource{position:absolute;bottom:120px;left:104px;width:872px;text-align:center;
  font-weight:300;font-size:24px;color:var(--stone);letter-spacing:0.02em;z-index:4}
"""


def render_chart_html(slide: dict) -> str:
    bars = slide.get("bars", [])
    values = [float(b.get("value", 0)) for b in bars] or [1.0]
    vmax = max(values) or 1.0
    unit = slide.get("unit", "")
    plot_h = 560

    grid = "".join(
        "<div class='grid' style='top:%dpx'></div>" % round(plot_h * f)
        for f in (0.0, 0.25, 0.5, 0.75, 1.0)
    )
    cols, labels = [], []
    for b in bars:
        v = float(b.get("value", 0))
        h_px = int(round((v / vmax) * (plot_h - 60)))
        val_txt = b.get("display") or ("%g%s" % (v, unit))
        cols.append(
            "<div class='bcol'><div class='bval'>%s</div>"
            "<div class='bar' style='height:%dpx'></div></div>"
            % (html.escape(str(val_txt)), h_px)
        )
        labels.append("<div class='blcell'>%s</div>"
                      % html.escape(str(b.get("label", ""))))

    title = html.escape(slide.get("title", "")).replace("\n", "<br>")
    source = slide.get("source", "")
    source_html = "<div class='csource'>%s</div>" % html.escape(source) if source else ""

    body = (
        "<div class='slide'>"
        "<div class='num'>%(num)s</div>"
        "<div class='ctitle'>%(title)s</div>"
        "<div class='ghost' style='%(mark)s'></div>"
        "<div class='plot'>%(grid)s<div class='bars'>%(cols)s</div>"
        "<div class='blabel'>%(labels)s</div></div>"
        "%(source)s</div>"
    ) % {
        "num": _num(slide.get("n")), "title": title,
        "mark": _mark_style(560, OLIVE, opacity=0.05),
        "grid": grid, "cols": "".join(cols), "labels": "".join(labels),
        "source": source_html,
    }
    return _doc(body, CHART_CSS)


# ---- Final slide ----------------------------------------------------------
FINAL_CSS = """
.wrap{display:table;width:1080px;height:1440px}
.cell{display:table-cell;vertical-align:middle;text-align:center}
.lockup{display:inline-block;white-space:nowrap}
.fmark{display:inline-block;vertical-align:middle}
.word{font-weight:400;font-size:90px;color:var(--olive);vertical-align:middle;
  margin-left:28px;letter-spacing:-0.02em}
.url{position:absolute;left:0;bottom:96px;width:1080px;text-align:center;
  font-weight:300;font-size:31px;color:var(--olive);letter-spacing:0.02em}
"""


def render_final_html(slide: dict) -> str:
    word = slide.get("wordmark", "curAItion")
    url = slide.get("url", "curaition.xyz")
    body = (
        "<div class='slide'>"
        "<div class='wrap'><div class='cell'>"
        "<span class='lockup'><span class='fmark' style='%(mark)s'></span>"
        "<span class='word'>%(word)s</span></span>"
        "</div></div>"
        "<div class='url'>%(url)s</div></div>"
    ) % {"mark": _mark_style(90, OLIVE), "word": html.escape(word), "url": html.escape(url)}
    return _doc(body, FINAL_CSS)


RENDERERS = {
    "content": render_content_html,
    "chart": render_chart_html,
    "final": render_final_html,
}


def html_for(slide: dict) -> str:
    t = slide.get("type", "content")
    if t not in RENDERERS:
        raise ValueError("unknown slide type: %r" % t)
    return RENDERERS[t](slide)


def _optimize_png(png: Path) -> None:
    """Flatten to RGB and recompress. Chromium PNGs are already reasonable,
    but this guarantees small, consistent output."""
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(png)
    if im.mode != "RGB":
        im = im.convert("RGB")
    im.save(png, format="PNG", optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render CurAItion brand carousel slides (Chromium).")
    ap.add_argument("carousel_json", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("out"))
    ap.add_argument("--chromium", default=None,
                    help="explicit Chromium executable (else Playwright's bundled build)")
    args = ap.parse_args()

    for asset in (FONT_REGULAR, FONT_LIGHT, MARK_PNG):
        if not asset.exists():
            ap.error("missing bundled asset: %s" % asset)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        ap.error("playwright not installed. Run: pip install playwright && playwright install chromium")

    data = json.loads(args.carousel_json.read_text(encoding="utf-8"))
    slug = data.get("slug", "carousel")
    slides = data["slides"]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    launch_kwargs = {"args": ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]}
    if args.chromium:
        launch_kwargs["executable_path"] = args.chromium

    written = []
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, slide in enumerate(slides, start=1):
            if slide.get("type", "content") in ("content", "chart") and "n" not in slide:
                slide["n"] = i
            out_png = args.out_dir / ("%s-slide-%02d.png" % (slug, i))
            page.set_content(html_for(slide), wait_until="networkidle")
            page.screenshot(path=str(out_png),
                            clip={"x": 0, "y": 0, "width": W, "height": H})
            _optimize_png(out_png)
            written.append(out_png)
            print("rendered", out_png)
        browser.close()

    print("done: %d slides -> %s" % (len(written), args.out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
