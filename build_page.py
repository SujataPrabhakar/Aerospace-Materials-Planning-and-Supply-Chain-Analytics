"""Assemble the standalone dashboard page.

The template is written as a body fragment (that is the form the Claude artifact
host expects, since it supplies its own document wrapper). Served directly from
GitHub Pages the same fragment would render in quirks mode, so this script wraps
it in a complete HTML document: doctype, language, charset, viewport, social
metadata and an inline favicon.
"""
import re

TEMPLATE = "dashboard_template.html"
DATA = "dashboard_data.json"
OUT = "index.html"

DESCRIPTION = (
    "Interactive aerospace materials planning dashboard: demand forecast, inventory "
    "availability, replenishment requirements and supplier reliability across 1,800 "
    "part-site plans."
)

# Aircraft mark in the brand blue, matching the rail glyph.
FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E"
    "%3Crect width='24' height='24' rx='5' fill='%230d1520'/%3E"
    "%3Cpath d='M12 4.2 3.6 15h5.1L12 19.8 15.3 15h5.1z' fill='none' stroke='%233987e5' "
    "stroke-width='1.9' stroke-linejoin='round'/%3E%3C/svg%3E"
)

body = open(TEMPLATE, encoding="utf-8").read()
data = open(DATA, encoding="utf-8").read()
body = body.replace("/*__DATA__*/", data)

# The title belongs in <head>, not floating at the top of <body>.
m = re.search(r"<title>(.*?)</title>\s*", body, re.S)
title = m.group(1).strip()
body = body[: m.start()] + body[m.end():]

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{DESCRIPTION}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{FAVICON}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:type" content="website">
</head>
<body>
{body}</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(page)

import os
print(f"{OUT}: {os.path.getsize(OUT)/1e6:.2f} MB")
print("doctype:", page.lstrip().startswith("<!doctype html>"))
print("title:", title)
print("single <title>:", page.count("<title>") == 1)
print("data injected:", "__DATA__" not in page)
