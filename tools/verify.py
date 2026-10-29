"""Verify the shift planner kit builds correctly.

Checks:
  - every planners/*.html parses as well-formed HTML
  - each page has a <title>, stylesheet link, checkboxes, and credit line
  - shared CSS has @media print and large-print base font size
  - LICENSE carries the exact Asdale Dynamics copyright line
  - README credits Asdale Dynamics, LLC
  - no secret-like strings in any text file

Run:  python3 tools/verify.py
"""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PLANNERS = ROOT / "planners"
STYLE = ROOT / "styles" / "print.css"

failures = []


def fail(msg: str) -> None:
    failures.append(msg)
    print("FAIL:", msg)


class StrictParser(HTMLParser):
    """Rudimentary well-formedness check: tags must balance."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.void = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }

    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if not self.stack or self.stack[-1] != tag:
            raise ValueError(f"unexpected closing tag </{tag}>")
        self.stack.pop()

    def check(self) -> None:
        if self.stack:
            raise ValueError(f"unclosed tags: {self.stack}")


SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",
    r"api[_-]?key",
    r"secret[_-]?key",
    r"password\s*[:=]",
    r"token\s*[:=]\s*['\"]?[A-Za-z0-9]{16,}",
    r"-----BEGIN [A-Z ]+PRIVATE KEY-----",
]


def scan_for_secrets(text: str, path: Path) -> None:
    low = text.lower()
    for pat in SECRET_PATTERNS:
        for m in re.finditer(pat, low):
            fail(f"possible secret in {path}: {m.group(0)[:40]}")


def check_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    scan_for_secrets(text, path)
    parser = StrictParser()
    try:
        parser.feed(text)
        parser.check()
    except ValueError as exc:
        fail(f"{path.name}: not well-formed HTML ({exc})")
        return
    if "<title>" not in text.lower():
        fail(f"{path.name}: missing <title>")
    if 'styles/print.css' not in text:
        fail(f"{path.name}: missing stylesheet link")
    if 'Asdale Dynamics, LLC' not in text:
        fail(f"{path.name}: missing Asdale Dynamics, LLC credit")
    if '<input' not in text and '\u2610' not in text:
        fail(f"{path.name}: no printable form inputs")
    if '<table>' in text:
        fail(f"{path.name}: table missing class=\"grid\"")


def check_css() -> None:
    text = STYLE.read_text(encoding="utf-8")
    scan_for_secrets(text, STYLE)
    if "@media print" not in text:
        fail("styles/print.css: missing @media print")
    if "font-size: 16px" not in text and "font-size:16px" not in text:
        fail("styles/print.css: missing 16 px large-print base font size")


def check_license() -> None:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    scan_for_secrets(text, ROOT / "LICENSE")
    if "Copyright (c) 2026 Asdale Dynamics, LLC" not in text:
        fail("LICENSE: missing exact copyright line")


def check_readme() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    scan_for_secrets(text, ROOT / "README.md")
    if "Asdale Dynamics, LLC" not in text:
        fail("README.md: missing Asdale Dynamics, LLC credit")


def main() -> int:
    html_files = sorted(PLANNERS.glob("*.html"))
    if not html_files:
        fail("no planners/*.html found — run tools/build.py first")
    for path in html_files:
        check_html(path)
    check_css()
    check_license()
    check_readme()

    # scan all text files for secrets
    for path in ROOT.rglob("*"):
        if "tools" in path.parts:
            continue
        if path.is_file() and path.suffix in {
            ".md", ".html", ".css", ".py", ".txt", ".json", ".toml",
        }:
            try:
                scan_for_secrets(path.read_text(encoding="utf-8"), path)
            except UnicodeDecodeError:
                pass

    if failures:
        print(f"\n{len(failures)} check(s) failed.")
        return 1
    print(f"all checks passed ({len(html_files)} HTML planners, CSS, LICENSE, README).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
