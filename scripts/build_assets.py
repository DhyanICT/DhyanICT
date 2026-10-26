"""Generate the static SVG assets for the profile README.

    python scripts/build_assets.py

Edit the content blocks below and re-run; every asset is written in a dark and a
light variant (assets/<name>-dark.svg, assets/<name>-light.svg).
Requires: Python 3.9+, and fontTools (pip install fonttools brotli) for exact text
measurement. Without fontTools, widths are estimated.
"""
from __future__ import annotations

from brand import THEMES, esc, family, font_css, text_width, write

# ---------------------------------------------------------------- content ---

HERO = {
    "name": "Dhyan Patel",
    "role": "Applied AI & full-stack engineer",
    "thesis": "I build AI systems that show their work.",
    "trace": ["question", "graph + vector retrieval", "LLM", "answer with citations"],
}

# Every number here is taken from the repository it describes.
PLATES = [
    {
        "slug": "plate-trustmed",
        "name": "TrustMed AI",
        "line": "Medical Q&A grounded in a knowledge graph, with citations",
        "pipeline": ["question", "Neo4j graph", "FAISS search", "Llama 3.1", "cited answer"],
        "proof": "Recall@15  87.5%",
    },
    {
        "slug": "plate-cua",
        "name": "Computer-Use Automation",
        "line": "An agent learns a UI task once; replays run without an LLM",
        "pipeline": ["goal", "LLM discovery", "typed artifact", "deterministic replay"],
        "proof": "0 LLM calls on replay",
    },
    {
        "slug": "plate-proofboard",
        "name": "Proofboard",
        "line": "Real-time group decisions with a visible rationale",
        "pipeline": ["board", "live sync", "one vote per person", "recorded outcome"],
        "proof": "14 tests, deployed",
    },
]

# evaluations/comprehensive_evaluation_results_20251117_011410.json
RETRIEVAL = {
    "k": [5, 10, 15],
    "Precision": [74.3, 68.6, 69.5],
    "Recall": [77.7, 81.3, 87.5],
    "F1": [74.4, 68.9, 70.6],
}

# ------------------------------------------------------------------ hero ---


def hero(t: dict) -> str:
    W, H = 1200, 400
    x0, x1, ty = 66, 1134, 312
    nodes = [x0 + (x1 - x0) * i / (len(HERO["trace"]) - 1) for i in range(len(HERO["trace"]))]
    length = x1 - x0
    dur, delay = 2.2, 0.5

    def arrival(x: float) -> float:  # when the pulse reaches x (linear timing)
        return delay + dur * (x - x0) / length

    labels = []
    for i, (x, label) in enumerate(zip(nodes, HERO["trace"])):
        anchor = "start" if i == 0 else "end" if i == len(nodes) - 1 else "middle"
        dx = -10 if i == 0 else 10 if i == len(nodes) - 1 else 0
        cls = "lbl lbl-end" if i == len(nodes) - 1 else "lbl"
        labels.append(
            f'<text x="{x + dx:.0f}" y="{ty + 50}" text-anchor="{anchor}" class="{cls}">{esc(label)}</text>'
        )

    mids = "".join(
        f'<circle cx="{x:.1f}" cy="{ty}" r="8" class="node" style="animation-delay:{arrival(x):.2f}s"/>'
        for x in nodes[:-1]
    )
    end = nodes[-1]
    t_end = arrival(end)

    # faint knowledge-graph constellation; two nodes are 'retrieved' (teal)
    pts = [(860, 92), (944, 60), (1030, 104), (1104, 70), (918, 156), (1008, 186), (1110, 160), (820, 176)]
    edges = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 2), (5, 6), (3, 6), (4, 7), (1, 4)]
    hot = {2, 5}
    graph = "".join(
        f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" class="edge'
        f'{" edge-hot" if a in hot and b in hot else ""}"/>'
        for a, b in edges
    ) + "".join(
        f'<circle cx="{x}" cy="{y}" r="{6 if i in hot else 4.5}" class="{"g-hot" if i in hot else "g"}"/>'
        for i, (x, y) in enumerate(pts)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">
<title id="title">{esc(HERO['name'])}: {esc(HERO['role'])}</title>
<desc id="desc">{esc(HERO['thesis'])} A signal travels from a question through retrieval and an LLM to an answer with citations.</desc>
<style>
{font_css('serif', 'sans', 'sans-bold', 'mono')}
.name{{font-family:{family('serif')};font-size:108px;fill:{t['text']};letter-spacing:-1px}}
.role{{font-family:{family('sans')};font-weight:600;font-size:31px;fill:{t['text']}}}
.thesis{{font-family:{family('sans')};font-size:31px;fill:{t['muted']}}}
.lbl{{font-family:{family('mono')};font-weight:500;font-size:22px;fill:{t['muted']}}}
.lbl-end{{fill:{t['teal']}}}
.rail{{stroke:{t['line']};stroke-width:3;stroke-linecap:round}}
.signal{{stroke:{t['amber']};stroke-width:3;stroke-linecap:round;stroke-dasharray:{length};stroke-dashoffset:0;
  animation:draw {dur}s linear {delay}s backwards}}
.node{{fill:{t['amber']};stroke:{t['amber']};stroke-width:3;animation:lit .25s ease-out backwards}}
.pulse{{fill:{t['amber']};opacity:0;animation:travel {dur}s linear {delay}s both}}
.done{{fill:{t['teal']};animation:land .45s cubic-bezier(.3,1.6,.5,1) {t_end:.2f}s backwards;transform-box:fill-box;transform-origin:center}}
.ring{{fill:none;stroke:{t['teal']};stroke-width:2;opacity:0;animation:ring 1.4s ease-out {t_end + .1:.2f}s both;transform-box:fill-box;transform-origin:center}}
.tick{{fill:none;stroke:{t['bg']};stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}}
.edge{{stroke:{t['line']};stroke-width:1.5}}
.edge-hot{{stroke:{t['teal']};stroke-opacity:.7}}
.g{{fill:{t['bg']};stroke:{t['line']};stroke-width:1.5}}
.g-hot{{fill:{t['teal']}}}
@keyframes draw{{from{{stroke-dashoffset:{length}}}to{{stroke-dashoffset:0}}}}
@keyframes lit{{from{{fill:{t['bg']};stroke:{t['muted']}}}}}
@keyframes travel{{0%{{opacity:1;transform:translateX(0)}}96%{{opacity:1}}100%{{opacity:0;transform:translateX({length}px)}}}}
@keyframes land{{from{{fill:{t['bg']};transform:scale(.55)}}}}
@keyframes ring{{0%{{opacity:.9;transform:scale(1)}}100%{{opacity:0;transform:scale(2.6)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1.5"/>
<g>{graph}</g>
<text x="60" y="144" class="name">{esc(HERO['name'])}</text>
<text x="66" y="210" class="role">{esc(HERO['role'])}</text>
<text x="66" y="253" class="thesis">{esc(HERO['thesis'])}</text>
<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" class="rail"/>
<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" class="signal"/>
{mids}
<circle cx="{x0}" cy="{ty}" r="7" class="pulse"/>
<circle cx="{end}" cy="{ty}" r="15" class="ring"/>
<g class="done"><circle cx="{end}" cy="{ty}" r="15"/></g>
<path d="M{end - 6.5} {ty + .5} l4.5 4.5 l8.5 -9" class="tick"/>
{''.join(labels)}
</svg>"""


# ---------------------------------------------------------------- plates ---


def plate(t: dict, p: dict) -> str:
    W, H = 1200, 250
    mono = 22
    gap_line = 24  # connector length between pipeline steps
    # lay the pipeline out left to right using real glyph widths
    x, y = 72, 198
    parts = []
    for i, step in enumerate(p["pipeline"]):
        last = i == len(p["pipeline"]) - 1
        r = 7 if last else 5.5
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" class="{"pv" if last else "pn"}"/>')
        x += 14
        parts.append(f'<text x="{x:.1f}" y="{y + 6.5}" class="{"pl pl-end" if last else "pl"}">{esc(step)}</text>')
        x += text_width(step, "mono", mono) + 14
        if not last:
            parts.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x + gap_line:.1f}" y2="{y}" class="pc"/>')
            x += gap_line + 14
    if x > W - 60:
        raise SystemExit(f"{p['slug']}: pipeline too wide ({x:.0f}px); shorten step labels")

    chip_w = text_width(p["proof"], "sans-bold", 24) + 44
    cx = W - 64 - chip_w
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{esc(p['name'])}</title>
<desc id="d">{esc(p['line'])}. Pipeline: {esc(' to '.join(p['pipeline']))}. Result: {esc(p['proof'])}.</desc>
<style>
{font_css('serif', 'sans', 'sans-bold', 'mono')}
.n{{font-family:{family('serif')};font-size:66px;fill:{t['text']}}}
.l{{font-family:{family('sans')};font-size:29px;fill:{t['muted']}}}
.pl{{font-family:{family('mono')};font-weight:500;font-size:{mono}px;fill:{t['muted']}}}
.pl-end{{fill:{t['teal']}}}
.pn{{fill:{t['amber']}}}
.pv{{fill:{t['teal']}}}
.pc{{stroke:{t['line']};stroke-width:2.5;stroke-linecap:round}}
.chip{{fill:{t['teal_soft']};stroke:{t['teal']};stroke-opacity:.55}}
.ct{{font-family:{family('sans')};font-weight:600;font-size:24px;fill:{t['teal']};white-space:pre}}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1.5"/>
<rect x="{cx:.1f}" y="38" width="{chip_w:.1f}" height="48" rx="24" class="chip"/>
<text x="{cx + chip_w / 2:.1f}" y="70" text-anchor="middle" class="ct" xml:space="preserve">{esc(p['proof'])}</text>
<text x="62" y="108" class="n">{esc(p['name'])}</text>
<text x="66" y="152" class="l">{esc(p['line'])}</text>
{''.join(parts)}
</svg>"""


# --------------------------------------------------------- retrieval chart ---


def retrieval_chart(t: dict) -> str:
    W, H = 1200, 400
    top, base = 150, 330
    span = base - top
    series = [("Precision", t["amber"]), ("Recall", t["teal"]), ("F1", t["muted"])]
    bw, bg, group_w = 78, 14, 3 * 78 + 2 * 14
    gx = [130 + i * 360 for i in range(3)]

    bars = []
    for gi, k in enumerate(RETRIEVAL["k"]):
        for si, (name, color) in enumerate(series):
            v = RETRIEVAL[name][gi]
            h = span * v / 100
            x = gx[gi] + si * (bw + bg)
            op = ' fill-opacity=".55"' if name == "F1" else ""
            bars.append(
                f'<rect x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="6" fill="{color}"{op}/>'
                f'<text x="{x + bw / 2}" y="{base - h - 12:.1f}" text-anchor="middle" class="v">{v:.1f}</text>'
            )
        bars.append(
            f'<text x="{gx[gi] + group_w / 2}" y="{base + 40}" text-anchor="middle" class="k">top {k}</text>'
        )

    legend, lx = [], W - 64
    for name, color in reversed(series):
        w = text_width(name, "sans", 22)
        lx -= w
        legend.append(f'<text x="{lx:.1f}" y="66" class="lg">{name}</text>')
        lx -= 28
        op = ' fill-opacity=".55"' if name == "F1" else ""
        legend.append(f'<rect x="{lx:.1f}" y="49" width="18" height="18" rx="4" fill="{color}"{op}/>')
        lx -= 26

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">TrustMed AI retrieval quality</title>
<desc id="d">Precision, recall and F1 at top 5, 10 and 15 results on a 7-query ground-truth set. Recall at 15 is 87.5 percent; precision at 5 is 74.3 percent.</desc>
<style>
{font_css('sans', 'sans-bold', 'mono')}
.h{{font-family:{family('sans')};font-weight:600;font-size:30px;fill:{t['text']}}}
.s{{font-family:{family('sans')};font-size:22px;fill:{t['muted']}}}
.lg{{font-family:{family('sans')};font-size:22px;fill:{t['muted']}}}
.v{{font-family:{family('sans')};font-weight:600;font-size:22px;fill:{t['text']}}}
.k{{font-family:{family('mono')};font-weight:500;font-size:20px;fill:{t['muted']}}}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1.5"/>
<text x="64" y="70" class="h">TrustMed AI retrieval quality, %</text>
<text x="64" y="106" class="s">7-query ground-truth set, November 2025. Warm retrieval averages about 30 ms.</text>
{''.join(legend)}
<line x1="64" y1="{base}" x2="{W - 64}" y2="{base}" stroke="{t['line']}" stroke-width="2"/>
{''.join(bars)}
</svg>"""


# ------------------------------------------------------------------ main ---

if __name__ == "__main__":
    for theme, tokens in THEMES.items():
        write("hero", theme, hero(tokens))
        for p in PLATES:
            write(p["slug"], theme, plate(tokens, p))
        write("trustmed-retrieval", theme, retrieval_chart(tokens))
    print("assets written")
