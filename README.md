# Free Shift Planner Kit

Printable shift planners for nurses and shift workers: brain sheets, sleep logs,
handoff templates, and weekly schedules. Large-print friendly, no account
needed, no sign-up, no tracking.

**Published by Asdale Dynamics, LLC** — beginner-friendly AI education, books,
and practical tools. Find more at dylanasdale.github.io.

---

## Who this is for

Nurses, CNAs, and other shift workers who want a simple paper tool to keep track
of a shift, a week of sleep, or a patient handoff. Designed to be easy to read
and easy to write on — large print, big checkboxes, and plenty of writing space.

These are **education-only, practical aids**, not medical advice. They are not a
substitute for clinical judgment, facility policy, or professional training.

---

## What's inside

| Planner | File | Best for |
|---|---|---|
| Brain Sheet (shift report) | `planners/brain-sheet.html` | End-of-shift patient summary and handoff notes |
| Sleep Log | `planners/sleep-log.html` | One week of sleep, shifts, caffeine, and rest |
| SBAR Handoff Template | `planners/handoff-template.html` | Structured Situation-Background-Assessment-Recommendation handoffs |
| Weekly Schedule | `planners/weekly-schedule.html` | Week-at-a-glance shifts, sleep, and appointments |

Each planner exists in two forms:
- **Markdown source** (`planners/*.md`) — readable, editable plain text
- **Print-ready HTML** (`planners/*.html`) — open in a browser and print

---

## How to use

1. Open any `planners/*.html` file in your web browser.
2. Print it (`Ctrl+P` / `Cmd+P`). US Letter margins are set for printing.
   Choose "Background graphics" if you want the shaded header rows; otherwise it
   prints clean black on white.
3. Fill it in by hand on the unit or at home.

No account, no email, no data collection. Nothing you type or write in these
pages is saved or sent anywhere — they run entirely in your browser.

---

## Rebuild from source (optional)

The HTML files are generated from Markdown. To rebuild them:

```bash
python3 tools/build.py
```

Run the verification suite:

```bash
python3 tools/verify.py
```

This checks HTML structure, print styles, credits, the license, and scans for
secrets.

---

## Credit

Created and published by **Asdale Dynamics, LLC** (Dylan Asdale, registered
nurse turned AI author). More plain-English, step-by-step AI guides at
dylanasdale.github.io.

---

## License

[MIT License](LICENSE) — Copyright (c) 2026 Asdale Dynamics, LLC.
