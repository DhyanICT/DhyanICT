"""Keep the "N merged PRs" figure on the profile in sync with GitHub search.

Counts the same thing as the search  is:pr is:merged author:<login>  and then
  1. updates the "proof" chip of the Next Play plate in scripts/build_assets.py,
  2. updates the plate's alt text in README.md ("N merged pull requests"),
  3. re-renders only assets/plate-nextplay-{dark,light}.svg.

Needs a token that can see the private Next-Play-Games repositories
(the ACTIVITY_TOKEN secret). Without one, GitHub reports public PRs only, so the
script refuses to lower the number: a merged PR can't be "un-merged", so a drop
almost always means the token lost access, not that the count really fell.

    ACTIVITY_TOKEN=... python scripts/update_pr_count.py
    python scripts/update_pr_count.py --count 175+    # set it by hand ("+" is kept)
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "scripts" / "build_assets.py"
README = ROOT / "README.md"
LOGIN = os.environ.get("PROFILE_LOGIN", "DhyanICT")
PLATE_SLUG = "plate-nextplay"

CHIP = re.compile(r'("proof":\s*")(\d+)(\+?)( merged PRs")')
ALT = re.compile(r"(\d+\+?)( merged pull requests)")


def fetch_count(token: str, attempts: int = 4) -> int:
    query = f"is:pr is:merged author:{LOGIN}"
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode({"q": query, "per_page": 1})
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{LOGIN}-profile-pr-count",
    }
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
                body = json.load(resp)
            if body.get("incomplete_results"):
                raise ValueError("GitHub returned incomplete search results")
            return int(body["total_count"])
        except urllib.error.HTTPError as err:
            if err.code in (401, 404, 422):
                raise SystemExit(f"Search failed with HTTP {err.code}; check the ACTIVITY_TOKEN secret")
            reason = f"HTTP {err.code}"
        except (urllib.error.URLError, TimeoutError, ValueError) as err:
            reason = str(err)
        if attempt == attempts:
            raise SystemExit(f"Giving up after {attempts} attempts ({reason}); profile left unchanged")
        wait = 10 * 2 ** (attempt - 1)
        print(f"Attempt {attempt} failed ({reason}); retrying in {wait}s")
        time.sleep(wait)
    raise AssertionError("unreachable")


def current_label(build_src: str) -> str:
    match = CHIP.search(build_src)
    if not match:
        raise SystemExit('Could not find the "N merged PRs" chip in scripts/build_assets.py')
    return match.group(2) + match.group(3)


def rerender_plate() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_assets  # imported after the edit so it sees the new number
    from brand import THEMES, write

    plate = next(p for p in build_assets.PLATES if p["slug"] == PLATE_SLUG)
    for theme, tokens in THEMES.items():
        write(plate["slug"], theme, build_assets.plate(tokens, plate))


def main() -> None:
    build_src = BUILD.read_text(encoding="utf-8")
    old_label = current_label(build_src)
    old = int(old_label.rstrip("+"))

    manual = "--count" in sys.argv
    if manual:
        label = sys.argv[sys.argv.index("--count") + 1].strip()
        if not re.fullmatch(r"\d+\+?", label):
            raise SystemExit('Use a number like 175 or 175+')
        new = int(label.rstrip("+"))
    else:
        token = os.environ.get("ACTIVITY_TOKEN")
        if not token:
            print("ACTIVITY_TOKEN is not set, so private PRs can't be counted; leaving the number unchanged.")
            return
        new = fetch_count(token)
        label = str(new)

    print(f"Merged PRs: profile shows {old_label}, new value {label}")
    if new < old and not manual:
        print("New count is lower than the current one; the token probably can't see every repo. Leaving it unchanged.")
        return
    readme_src = README.read_text(encoding="utf-8")
    readme_new = ALT.sub(lambda m: f"{label}{m.group(2)}", readme_src, count=1)
    if label == old_label and readme_new == readme_src:
        print("Already up to date.")
        return

    BUILD.write_text(CHIP.sub(lambda m: f"{m.group(1)}{label}{m.group(4)}", build_src, count=1), encoding="utf-8")
    README.write_text(readme_new, encoding="utf-8")
    rerender_plate()
    print(f"Updated to {label} merged PRs")


if __name__ == "__main__":
    main()
