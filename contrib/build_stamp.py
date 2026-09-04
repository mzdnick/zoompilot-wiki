#!/usr/bin/env python3
"""Bake the latest zoompilot/main commit into the build-stamp lines.

Runs before zensical build in CI (harmless by hand). The stamp is
static text in the pages, so visitors need no API call of their own
and the stamp never goes missing. Reads the commits atom feed for the
main branch — the branch the install URL serves — which has no rate
limit, unlike the REST API. On any failure the existing stamp is kept,
so a build never breaks and offline builds stay coherent.

In CI the edit is ephemeral: the checkout is thrown away after the
deploy. The committed .md files carry the last stamp anyone wrote on
purpose; refresh them by running this script before committing.
"""

import pathlib
import re
import sys
import urllib.request

FEED = "https://github.com/zoompilot/zoompilot/commits/main.atom"
PAGES = [
    pathlib.Path("docs/index.md"),
    pathlib.Path("docs/getting-started/install.md"),
]
STAMP_RE = re.compile(r'<span class="zp-stamp">[^<]*</span>')

try:
    xml = urllib.request.urlopen(FEED, timeout=15).read().decode()
    entry = xml.split("<entry>", 1)[1]
    sha = re.search(r"/commit/([0-9a-f]{40})", entry).group(1)[:10]
    date = re.search(r"<updated>(\d{4}-\d{2}-\d{2})T", entry).group(1)
except Exception as err:  # noqa: BLE001 - any failure keeps the old stamp
    print(f"build stamp: kept existing ({err})")
    sys.exit(0)

stamp = f'<span class="zp-stamp">· build {sha} · {date}</span>'
changed = 0
for page in PAGES:
    text = page.read_text()
    if not STAMP_RE.search(text):
        sys.exit(f"build stamp: no stamp span in {page}")
    new = STAMP_RE.sub(stamp, text)
    if new != text:
        page.write_text(new)
        changed += 1
print(f"build stamp: {'wrote' if changed else 'unchanged'} ({sha} · {date})")
