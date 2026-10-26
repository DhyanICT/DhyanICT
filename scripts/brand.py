"""Shared visual tokens for every generated profile asset.

Colour carries meaning across all assets:
  amber = signal in flight (a query, a step, a pulse)
  teal  = verified (a cited answer, a passing check, a measured result)

Fonts are subset to Basic Latin and embedded as base64 WOFF2 so the SVGs render
identically inside GitHub's <img> sandbox, which blocks external font requests.
Only Python's standard library is needed at build time.
"""
from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
ASSETS = ROOT.parent / "assets"

THEMES = {
    "dark": {
        "bg": "#0F1B2D",       # deep ink blue
        "surface": "#15243B",
        "line": "#2A3D5A",
        "text": "#EAF0F7",
        "muted": "#9AABC2",
        "amber": "#F5A524",
        "teal": "#2EC4B6",
        "teal_soft": "#173E48",
    },
    "light": {
        "bg": "#FBFCFE",
        "surface": "#EFF3F8",
        "line": "#D3DCE8",
        "text": "#0F1B2D",
        "muted": "#53637B",
        "amber": "#B86E00",
        "teal": "#0B8A7F",
        "teal_soft": "#D9F1EE",
    },
}

FONT_FILES = {
    "serif": ("Instrument Serif", "is.woff2", 400),
    "sans": ("Geist", "geist-400.woff2", 400),
    "sans-bold": ("Geist", "geist-600.woff2", 600),
    "mono": ("Geist Mono", "geistmono-500.woff2", 500),
}

FALLBACK = {
    "serif": "Georgia, 'Times New Roman', serif",
    "sans": "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif",
    "mono": "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
}


def font_css(*keys: str) -> str:
    """@font-face rules for the requested font keys, embedded as data URIs."""
    rules = []
    for key in keys:
        family, file, weight = FONT_FILES[key]
        data = base64.b64encode((FONTS / file).read_bytes()).decode()
        rules.append(
            f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
        )
    return "".join(rules)


def family(kind: str) -> str:
    name = {"serif": "Instrument Serif", "sans": "Geist", "mono": "Geist Mono"}[kind]
    return f"'{name}', {FALLBACK[kind]}"


@lru_cache(maxsize=None)
def _metrics(file: str):
    """Advance widths per character, read straight from the WOFF2 file."""
    try:
        from fontTools.ttLib import TTFont  # optional: only for precise layout
    except ImportError:
        return None
    font = TTFont(FONTS / file)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"].metrics
    upem = font["head"].unitsPerEm
    return {chr(c): hmtx[g][0] / upem for c, g in cmap.items()}


def text_width(text: str, key: str, size: float) -> float:
    """Rendered width of text in px. Falls back to an estimate without fontTools."""
    widths = _metrics(FONT_FILES[key][1])
    if widths is None:
        return len(text) * size * (0.6 if key == "mono" else 0.52)
    return sum(widths.get(ch, 0.55) for ch in text) * size


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def write(name: str, theme: str, svg: str) -> Path:
    ASSETS.mkdir(exist_ok=True)
    path = ASSETS / f"{name}-{theme}.svg"
    path.write_text(svg, encoding="utf-8")
    return path
