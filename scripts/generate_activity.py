"""Render assets/activity-{dark,light}.svg from the GitHub GraphQL API.

Runs weekly in .github/workflows/activity.yml with the built-in GITHUB_TOKEN,
so the profile depends on no third-party stats service.

    GITHUB_TOKEN=... python scripts/generate_activity.py
    python scripts/generate_activity.py --mock      # offline preview

Standard library only. Counts reflect public activity unless the token can see
private contributions.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date

from brand import THEMES, esc, family, font_css, write

LOGIN = os.environ.get("PROFILE_LOGIN", "DhyanICT")
WEEKS = 26  # half a year keeps the grid legible on phones

# Coursework, tutorials and scratch repos would distort the language mix.
EXCLUDE_REPOS = {
    "Openend-8", "token-10", "GitTest", "HTML-Portfolio", "SRI",
    "Lab-1_202001225", "Lab5_202001225", "Lab-8_202001225",
}
EXCLUDE_LANGS = {"Dockerfile", "Shell", "Batchfile", "PowerShell"}

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    pullRequests(states: MERGED) { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      nodes { name languages(first: 6, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""


def fetch(attempts: int = 4) -> dict:
    """Query GraphQL, retrying transient failures (5xx, timeouts) with backoff.

    GitHub's GraphQL API occasionally returns 502/504 on contribution queries;
    a later attempt almost always succeeds.
    """
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set (use --mock for an offline preview)")
    payload = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": f"{LOGIN}-profile-activity",
    }
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request("https://api.github.com/graphql", data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as resp:
                body = json.load(resp)
            if body.get("data", {}).get("user"):
                if "errors" in body:  # partial data is still usable
                    print(f"GraphQL warnings: {body['errors']}")
                return body["data"]["user"]
            reason = f"GraphQL error: {body.get('errors')}"
        except urllib.error.HTTPError as err:
            if err.code < 500:  # auth or query problem: retrying won't help
                raise SystemExit(f"GitHub API returned {err.code}: {err.read()[:300]!r}")
            reason = f"HTTP {err.code}"
        except (urllib.error.URLError, TimeoutError) as err:
            reason = f"network error: {err}"
        if attempt == attempts:
            raise SystemExit(f"Giving up after {attempts} attempts ({reason}); existing panel left unchanged")
        wait = 10 * 2 ** (attempt - 1)  # 10s, 20s, 40s
        print(f"Attempt {attempt} failed ({reason}); retrying in {wait}s")
        time.sleep(wait)


def mock() -> dict:
    import random
    random.seed(7)
    days = []
    start = date.fromordinal(date.today().toordinal() - 7 * 52)
    for i in range(7 * 52):
        d = date.fromordinal(start.toordinal() + i)
        burst = 1 if (i // 21) % 3 == 0 else 0
        days.append({"date": d.isoformat(), "contributionCount": random.choice([0, 0, 1, 2, 4, 7]) * burst})
    weeks = [{"contributionDays": days[i:i + 7]} for i in range(0, len(days), 7)]
    langs = [("Python", 61_000), ("TypeScript", 54_000), ("HTML", 22_000), ("Java", 18_000), ("JavaScript", 9_000)]
    return {
        "contributionsCollection": {"contributionCalendar": {
            "totalContributions": sum(d["contributionCount"] for d in days), "weeks": weeks}},
        "pullRequests": {"totalCount": 4},
        "repositories": {"nodes": [{"name": "mock", "languages": {"edges": [
            {"size": s, "node": {"name": n}} for n, s in langs]}}]},
    }


def summarise(user: dict) -> dict:
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]][-WEEKS:]
    totals: dict[str, int] = {}
    for repo in user["repositories"]["nodes"]:
        if repo["name"] in EXCLUDE_REPOS:
            continue
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name not in EXCLUDE_LANGS:
                totals[name] = totals.get(name, 0) + edge["size"]
    grand = sum(totals.values()) or 1
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:5]
    return {
        "total": cal["totalContributions"],
        "prs": user["pullRequests"]["totalCount"],
        "weeks": weeks,
        "langs": [(n, 100 * s / grand) for n, s in top],
    }


def render(s: dict, t: dict) -> str:
    W, H = 1200, 360
    cell, gap = 24, 6
    gx, gy = 64, 118
    counts = sorted(c for w in s["weeks"] for c in w if c > 0)

    def level(c: int) -> int:
        if c == 0 or not counts:
            return 0
        q = [counts[int(len(counts) * f)] for f in (0.25, 0.5, 0.75)]
        return 1 + sum(c > x for x in q)

    opacity = {1: 0.35, 2: 0.55, 3: 0.78, 4: 1.0}
    cells = []
    for wi, week in enumerate(s["weeks"]):
        for di, c in enumerate(week):
            x, y = gx + wi * (cell + gap), gy + di * (cell + gap)
            lv = level(c)
            fill = f'fill="{t["teal"]}" fill-opacity="{opacity[lv]}"' if lv else f'fill="{t["surface"]}"'
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="5" {fill}/>')

    lx, lw = 910, 226
    rows = []
    for i, (name, pct) in enumerate(s["langs"]):
        y = gy + 52 + i * 38
        rows.append(
            f'<text x="{lx}" y="{y}" class="ln">{esc(name)}</text>'
            f'<text x="{lx + lw}" y="{y}" text-anchor="end" class="lp">{pct:.0f}%</text>'
            f'<rect x="{lx}" y="{y + 10}" width="{lw}" height="6" rx="3" fill="{t["surface"]}"/>'
            f'<rect x="{lx}" y="{y + 10}" width="{max(6, lw * pct / 100):.1f}" height="6" rx="3" fill="{t["amber"]}"/>'
        )

    # PRs merged in private repos are invisible to the workflow token, so a
    # zero here usually means "not visible", not "none". Leave it out then.
    headline = f'{s["total"]:,} contributions in the past year'
    if s["prs"] > 0:
        headline += f', {s["prs"]} merged pull request{"s" if s["prs"] != 1 else ""}'
    stamp = f"Updated {date.today():%-d %b %Y}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">GitHub activity for {esc(LOGIN)}</title>
<desc id="d">{esc(headline)}. Top languages: {esc(', '.join(f'{n} {p:.0f}%' for n, p in s['langs']))}.</desc>
<style>
{font_css('sans', 'sans-bold', 'mono')}
.h{{font-family:{family('sans')};font-weight:600;font-size:27px;fill:{t['text']}}}
.m{{font-family:{family('sans')};font-size:19px;fill:{t['muted']}}}
.ln{{font-family:{family('sans')};font-size:22px;fill:{t['text']}}}
.lp{{font-family:{family('mono')};font-weight:500;font-size:19px;fill:{t['muted']}}}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1.5"/>
<text x="64" y="76" class="h">{esc(headline)}</text>
<text x="{W - 64}" y="76" text-anchor="end" class="m">{stamp}</text>
{''.join(cells)}
<text x="{lx}" y="{gy + 12}" class="m">Top languages, by bytes</text>
{''.join(rows)}
</svg>"""


if __name__ == "__main__":
    data = mock() if "--mock" in sys.argv else fetch()
    summary = summarise(data)
    for theme, tokens in THEMES.items():
        write("activity", theme, render(summary, tokens))
    print(f"activity written: {summary['total']} contributions, langs={summary['langs']}")
