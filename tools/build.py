"""Build printable HTML planners from Markdown sources.

Reads planners/*.md, converts each to HTML with the shared large-print
stylesheet (styles/print.css), and writes planners/*.html.

Run:  python3 tools/build.py
"""

from pathlib import Path

import markdown
import re

ROOT = Path(__file__).resolve().parent.parent
PLANNERS = ROOT / "planners"
STYLE = ROOT / "styles" / "print.css"
STYLE_NAME = "styles/print.css"

MD_EXTENSIONS = ["tables", "fenced_code", "footnotes", "sane_lists"]

TASK_LIST_RE = re.compile(r"^(\s*)- \[\s*([xX]?)\s*\](?: (.*))?$", re.MULTILINE)


def task_list_to_html(match: re.Match) -> str:
    indent, checked, text = match.groups()
    checked_attr = " checked" if checked.lower() == "x" else ""
    text = text or ""
    return (
        f'{indent}<div class="task">'
        f'<label class="check">'
        f'<input class="check-box" type="checkbox"{checked_attr}> {text}'
        f"</label></div>"
    )


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{style}">
</head>
<body>
<div class="planner">
{body}
</div>
</body>
</html>
"""


def title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build_one(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    text = TASK_LIST_RE.sub(task_list_to_html, text)
    title = title_from_markdown(text, md_path.stem.replace("-", " ").title())
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)
    # Every table in these planners is a writable grid; give them the grid
    # stylesheet class so borders, headers, and writing-space rows render.
    body = body.replace("<table>", '<table class="grid">')
    return HTML_TEMPLATE.format(title=title, style=STYLE_NAME, body=body)


def main() -> int:
    md_files = sorted(PLANNERS.glob("*.md"))
    if not md_files:
        print("No Markdown planners found in", PLANNERS)
        return 1
    written = 0
    for md_path in md_files:
        html_path = md_path.with_suffix(".html")
        html_path.write_text(build_one(md_path), encoding="utf-8")
        print(f"built {html_path.relative_to(ROOT)}")
        written += 1
    print(f"built {written} planner(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
