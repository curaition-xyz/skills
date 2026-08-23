#!/usr/bin/env python3
"""
CurAItion Carousel Producer — brand renderer (Playwright / Chromium), v3.

Renders a carousel JSON into brand slides conforming to the canonical
CurAItion carousel spec (GBrain `curaition/daily-publishing-prompt`,
16 Aug 2026 + `curaition/carousel-slide-density`, 15 Aug 2026).

Two output formats from ONE carousel.json:
  --format ig        1080x1440 PNGs (Instagram)
  --format linkedin  1080x1350 PNGs + a compiled PDF (LinkedIn document upload)
  --format both      both of the above (default)

CANONICAL SPEC (do not restyle per-carousel):
  content : Geist Medium 500, 66px, line-height 1.31, text centred,
            olive #6B7A3F on cream #F1EFE8. Max 3 lines, ideally 2.
            Slide number top-right "N/<total>", Geist Light 300, 28px,
            stone #C8C3B4. Mycelium watermark 32x32px, horizontally
            centred, bottom edge at 96.9% of slide height.
  chart   : vertical bars as SVG <rect> elements, sage #9CAF7A, anchored
            to a 1px stone axis baseline at 86.5% of slide height,
            tallest bar 396px (scaled for 1350). Title left-aligned at
            y=110, Geist Medium olive. Generous empty space above bars.
            Watermark + slide number as content slides.
  final   : mycelium mark 40px tall + "curAItion" wordmark Geist Medium
            42px, all olive (the AI is NOT contrasted), horizontal lockup
            centred. CTA "Read the full story at curaition.substack.com"
            Geist Medium 26px olive, bottom-centre. LinkedIn variant adds
            "Follow curAItion for daily cultural intelligence" in Geist
            Light 300 below the wordmark. No watermark, no slide number.

Widow gate: if the last line of a content slide is 6 characters or fewer
it is merged into the previous line automatically (and reported).

FORWARD-COMPATIBLE IMAGE LAYER (unchanged from v2.1):
  Any slide may carry an optional `background` block; the renderer
  composites a full-bleed image with legibility treatments. Brand slides
  omit it; the image-gen companion skill supplies it.

USAGE
    python render_carousel.py carousel.json --out-dir out/ \
        [--format ig|linkedin|both] [--chromium /path/to/chrome]

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
SAGE = "#9CAF7A"
SCRIM = "20, 22, 14"     # near-black olive, for scrims/dim (rgb tuple string)

W = 1080
H_IG = 1440
H_LI = 1350

# Canonical geometry, expressed as fractions of slide height so both
# formats stay on-spec (absolute values in the spec assume 1440).
WATERMARK_BOTTOM_FRAC = 1412 / 1440       # 96.9%
CHART_BASELINE_FRAC = 1246 / 1440         # 86.5%
CHART_MAX_BAR = 396                       # px at 1440; scaled by H/1440

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT_MEDIUM = ASSETS / "Geist-Medium.woff2"
FONT_REGULAR = ASSETS / "Geist-Regular.woff2"
FONT_LIGHT = ASSETS / "Geist-Light.woff2"
MARK_PNG = ASSETS / "mycelium-mark-olive.png"


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def _font_face_css() -> str:
    return (
        "@font-face{{font-family:'Geist';font-weight:500;font-style:normal;"
        "src:url(data:font/woff2;base64,{med}) format('woff2')}}"
        "@font-face{{font-family:'Geist';font-weight:400;font-style:normal;"
        "src:url(data:font/woff2;base64,{reg}) format('woff2')}}"
        "@font-face{{font-family:'Geist';font-weight:300;font-style:normal;"
        "src:url(data:font/woff2;base64,{light}) format('woff2')}}"
    ).format(med=_b64(FONT_MEDIUM), reg=_b64(FONT_REGULAR),
             light=_b64(FONT_LIGHT))


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


def _mark_style(width: int, color: str, opacity: float | None = None,
                height: int | None = None) -> str:
    """Inline style for the mycelium mark as a recolourable CSS mask.
    The PNG's alpha is the stencil; `color` fills it. Pass `height` to
    size by height instead of width (final-slide lockup)."""
    if height is not None:
        h = height
        w = round(height / MARK_ASPECT)
    else:
        w = width
        h = round(width * MARK_ASPECT)
    uri = _mark_uri()
    op = ("opacity:%s;" % opacity) if opacity is not None else ""
    return (
        "width:%dpx;height:%dpx;background-color:%s;%s"
        "-webkit-mask:url(%s) no-repeat center/contain;"
        "mask:url(%s) no-repeat center/contain;"
        "-webkit-mask-mode:alpha;mask-mode:alpha"
        % (w, h, color, op, uri, uri)
    )


def _mark_color_for(slide: dict) -> str:
    bg = slide.get("background")
    if bg and bg.get("mark_color"):
        return bg["mark_color"]
    if bg and bg.get("image"):
        return CREAM
    return OLIVE


def _base_css(h: int) -> str:
    root = ":root{--olive:%s;--cream:%s;--stone:%s;--sage:%s;--scrim:%s}" % (
        OLIVE, CREAM, STONE, SAGE, SCRIM
    )
    wm_bottom = h - round(h * WATERMARK_BOTTOM_FRAC)  # distance from bottom
    return root + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(w)dpx;height:%(h)dpx}
body{background:var(--cream);font-family:'Geist',sans-serif;
  -webkit-font-smoothing:antialiased}
.slide{position:relative;width:%(w)dpx;height:%(h)dpx;overflow:hidden;
  background:var(--cream)}
.bg{position:absolute;inset:0;background-repeat:no-repeat}
.bg-fx{position:absolute;inset:0}
.num{position:absolute;top:56px;right:64px;font-weight:300;font-size:28px;
  letter-spacing:0.04em;color:var(--stone);z-index:5}
.wm{position:absolute;left:50%%;bottom:%(wmb)dpx;transform:translateX(-50%%);
  z-index:5}
.content-layer{position:absolute;inset:0;z-index:4}
""" % {"w": W, "h": h, "wmb": wm_bottom}


# ---------------------------------------------------------------------------
# Background compositing (forward-compatible image layer) — unchanged v2.1
# ---------------------------------------------------------------------------
def _background_html(bg: dict) -> str:
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
            bg_filters.append("grayscale(1) contrast(1.05)")
            fx_layers.append(
                "<div class='bg-fx' style='background:var(--olive);"
                "mix-blend-mode:multiply'></div>")
            fx_layers.append(
                "<div class='bg-fx' style='background:var(--cream);"
                "mix-blend-mode:screen;opacity:.35'></div>")
        elif name == "dim":
            a = arg or "0.3"
            fx_layers.append(
                "<div class='bg-fx' style='background:rgba(var(--scrim),%s)'></div>" % a)
        elif name == "scrim-bottom":
            fx_layers.append(
                "<div class='bg-fx' style='background:linear-gradient("
                "to bottom,rgba(var(--scrim),0) 42%,rgba(var(--scrim),.86) 100%)'></div>")
        elif name == "scrim-full":
            fx_layers.append(
                "<div class='bg-fx' style='background:rgba(var(--scrim),.5)'></div>")

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
        return CREAM
    return default


def _doc(body: str, h: int, extra_css: str = "") -> str:
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        + _font_face_css() + _base_css(h) + extra_css
        + "</style></head><body>" + body + "</body></html>"
    )


def apply_widow_gate(copy: str) -> tuple[str, bool]:
    """Merge the last line into the previous one if it is <= 6 chars."""
    lines = copy.split("\n")
    if len(lines) >= 2 and 0 < len(lines[-1].strip()) <= 6:
        merged = lines[:-2] + [lines[-2].rstrip() + " " + lines[-1].strip()]
        return "\n".join(merged), True
    return copy, False


# ---- Content slide --------------------------------------------------------
CONTENT_CSS = """
.wrap{display:table;width:100%;height:100%}
.cell{display:table-cell;vertical-align:middle;
  padding:150px 104px 150px;text-align:center}
.copy{font-weight:500;letter-spacing:-0.01em}
"""


def render_content_html(slide: dict, h: int, num_label: str) -> str:
    copy = slide.get("copy", "")
    copy, merged = apply_widow_gate(copy)
    if merged:
        print("  widow gate: merged short last line on a content slide",
              file=sys.stderr)
    size = int(slide.get("font_size", 66))
    lh = slide.get("line_height", 1.31)
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
        "<div class='wm' style='%(mark)s'></div>"
        "</div>"
    ) % {
        "bg": _background_html(slide.get("background")),
        "num": html.escape(num_label),
        "size": size, "lh": lh, "color": color,
        "copy": inner, "mark": _mark_style(32, _mark_color_for(slide)),
    }
    return _doc(body, h, CONTENT_CSS)


# ---- Chart slide (SVG rects — canonical) ----------------------------------
def render_chart_html(slide: dict, h: int, num_label: str) -> str:
    bars = slide.get("bars", [])
    values = [float(b.get("value", 0)) for b in bars] or [1.0]
    vmax = max(values) or 1.0
    unit = slide.get("unit", "")
    scale = h / H_IG

    baseline_y = round(h * CHART_BASELINE_FRAC)
    max_bar = round(CHART_MAX_BAR * scale)
    margin = 104
    plot_w = W - 2 * margin
    n = max(len(bars), 1)
    slot = plot_w / n
    bar_w = round(slot * 0.56)

    rects, vlabels, clabels = [], [], []
    for i, b in enumerate(bars):
        v = float(b.get("value", 0))
        bh = int(round((v / vmax) * max_bar))
        x = round(margin + i * slot + (slot - bar_w) / 2)
        y = baseline_y - bh
        rects.append(
            "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
            % (x, y, bar_w, bh, SAGE))
        val_txt = b.get("display") or ("%g%s" % (v, unit))
        vlabels.append(
            "<text x='%d' y='%d' text-anchor='middle' fill='%s' "
            "font-family='Geist' font-weight='500' font-size='30'>%s</text>"
            % (round(x + bar_w / 2), y - 18, OLIVE,
               html.escape(str(val_txt))))
        clabels.append(
            "<text x='%d' y='%d' text-anchor='middle' fill='%s' "
            "font-family='Geist' font-weight='300' font-size='26'>%s</text>"
            % (round(x + bar_w / 2), baseline_y + 46, OLIVE,
               html.escape(str(b.get("label", "")))))

    axis = ("<rect x='%d' y='%d' width='%d' height='1' fill='%s'/>"
            % (margin, baseline_y, plot_w, STONE))
    title = html.escape(slide.get("title", "")).replace("\n", "<br>")
    source = slide.get("source", "")
    source_html = (
        "<div style='position:absolute;bottom:%dpx;left:104px;width:%dpx;"
        "font-weight:300;font-size:22px;color:%s'>%s</div>"
        % (round(70 * scale) + 40, plot_w, STONE, html.escape(source))
        if source else "")

    body = (
        "<div class='slide'>"
        "<div class='num'>%(num)s</div>"
        "<div style='position:absolute;top:110px;left:104px;width:%(tw)dpx;"
        "text-align:left;font-weight:500;font-size:46px;line-height:1.2;"
        "color:%(olive)s;z-index:4'>%(title)s</div>"
        "<svg width='%(w)d' height='%(h)d' viewBox='0 0 %(w)d %(h)d' "
        "style='position:absolute;inset:0;z-index:3'>"
        "%(axis)s%(rects)s%(vlabels)s%(clabels)s</svg>"
        "%(source)s"
        "<div class='wm' style='%(mark)s'></div>"
        "</div>"
    ) % {
        "num": html.escape(num_label), "tw": plot_w, "olive": OLIVE,
        "title": title, "w": W, "h": h, "axis": axis,
        "rects": "".join(rects), "vlabels": "".join(vlabels),
        "clabels": "".join(clabels), "source": source_html,
        "mark": _mark_style(32, OLIVE),
    }
    return _doc(body, h)


# ---- Final slide ----------------------------------------------------------
FINAL_CSS = """
.wrap{display:table;width:100%;height:100%}
.cell{display:table-cell;vertical-align:middle;text-align:center}
.lockup{display:inline-block;white-space:nowrap}
.fmark{display:inline-block;vertical-align:middle}
.word{font-weight:500;font-size:42px;color:var(--olive);
  vertical-align:middle;margin-left:18px;letter-spacing:-0.01em}
.follow{margin-top:26px;font-weight:300;font-size:28px;color:var(--olive);
  letter-spacing:0.01em}
.cta{position:absolute;left:0;bottom:88px;width:100%;text-align:center;
  font-weight:500;font-size:26px;color:var(--olive);letter-spacing:0.01em}
"""


def render_final_html(slide: dict, h: int, fmt: str) -> str:
    word = slide.get("wordmark", "curAItion")
    cta = slide.get("cta", "Read the full story at curaition.substack.com")
    follow = ""
    if fmt == "linkedin":
        follow_text = slide.get(
            "follow", "Follow curAItion for daily cultural intelligence")
        follow = "<div class='follow'>%s</div>" % html.escape(follow_text)
    body = (
        "<div class='slide'>"
        "<div class='wrap'><div class='cell'><div>"
        "<span class='lockup'><span class='fmark' style='%(mark)s'></span>"
        "<span class='word'>%(word)s</span></span>"
        "%(follow)s"
        "</div></div></div>"
        "<div class='cta'>%(cta)s</div></div>"
    ) % {"mark": _mark_style(0, OLIVE, height=40),
         "word": html.escape(word), "follow": follow,
         "cta": html.escape(cta)}
    return _doc(body, h, FINAL_CSS)


def html_for(slide: dict, h: int, fmt: str, num_label: str) -> str:
    t = slide.get("type", "content")
    if t == "content":
        return render_content_html(slide, h, num_label)
    if t == "chart":
        return render_chart_html(slide, h, num_label)
    if t == "final":
        return render_final_html(slide, h, fmt)
    raise ValueError("unknown slide type: %r" % t)


def _optimize_png(png: Path) -> None:
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(png)
    if im.mode != "RGB":
        im = im.convert("RGB")
    im.save(png, format="PNG", optimize=True)


def _compile_pdf(pngs: list[Path], out_pdf: Path) -> None:
    from PIL import Image
    pages = [Image.open(p).convert("RGB") for p in pngs]
    pages[0].save(out_pdf, save_all=True, append_images=pages[1:],
                  format="PDF", resolution=96.0)
    for p in pages:
        p.close()
    print("compiled", out_pdf)


def render_deck(page, slides, slug, out_dir: Path, fmt: str) -> list[Path]:
    h = H_IG if fmt == "ig" else H_LI
    total = len(slides)
    page.set_viewport_size({"width": W, "height": h})
    written = []
    for i, slide in enumerate(slides, start=1):
        num_label = ""
        if slide.get("type", "content") in ("content", "chart"):
            num_label = slide.get("n") or ("%d/%d" % (i, total))
        out_png = out_dir / ("%s-%s-slide-%02d.png" % (slug, fmt, i))
        page.set_content(html_for(slide, h, fmt, str(num_label)),
                         wait_until="networkidle")
        page.screenshot(path=str(out_png),
                        clip={"x": 0, "y": 0, "width": W, "height": h})
        _optimize_png(out_png)
        written.append(out_png)
        print("rendered", out_png)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render CurAItion brand carousel slides (Chromium).")
    ap.add_argument("carousel_json", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("out"))
    ap.add_argument("--format", choices=("ig", "linkedin", "both"),
                    default="both")
    ap.add_argument("--chromium", default=None,
                    help="explicit Chromium executable (else Playwright's)")
    args = ap.parse_args()

    for asset in (FONT_MEDIUM, FONT_REGULAR, FONT_LIGHT, MARK_PNG):
        if not asset.exists():
            ap.error("missing bundled asset: %s\n(Geist-Medium.woff2 can be "
                     "restored via: npm pack geist && tar -xzf geist-*.tgz && "
                     "cp package/dist/fonts/geist-sans/Geist-Medium.woff2 "
                     "assets/)" % asset)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        ap.error("playwright not installed. Run: pip install playwright "
                 "&& playwright install chromium")

    data = json.loads(args.carousel_json.read_text(encoding="utf-8"))
    slug = data.get("slug", "carousel")
    slides = data["slides"]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    formats = ["ig", "linkedin"] if args.format == "both" else [args.format]

    launch_kwargs = {"args": ["--no-sandbox", "--disable-dev-shm-usage",
                              "--disable-gpu"]}
    if args.chromium:
        launch_kwargs["executable_path"] = args.chromium

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": W, "height": H_IG},
                                device_scale_factor=1)
        for fmt in formats:
            pngs = render_deck(page, slides, slug, args.out_dir, fmt)
            if fmt == "linkedin":
                _compile_pdf(pngs, args.out_dir / ("%s-linkedin.pdf" % slug))
        browser.close()

    print("done -> %s" % args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
