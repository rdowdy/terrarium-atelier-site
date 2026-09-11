"""
Builds a public gallery site from the Atelier's files.

READ-ONLY with respect to the Atelier. This script only ever opens files
under SOURCE for reading and never writes there. Output goes to OUT
(this folder's ./docs, which GitHub Pages serves). Re-run after any epoch to refresh the site.

    python build.py
"""
from __future__ import annotations

import html
import re
import shutil
from datetime import date
from pathlib import Path

SOURCE = Path(r"D:\Users\MyPC\Dev\terrarium-atelier")
OUT = Path(__file__).resolve().parent / "docs"


# --------------------------------------------------------------------------
# A small Markdown renderer. Handles what the residents actually write:
# headings, paragraphs, lists, tables, rules, bold, italic, code, strike.
# --------------------------------------------------------------------------
def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"~~(.+?)~~", r"<s>\1</s>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md(text: str, shift: int = 1) -> str:
    """Render markdown to HTML. Headings are shifted down by `shift` levels."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    def flush_para(buf: list[str]):
        if buf:
            out.append("<p>" + inline(" ".join(x.strip() for x in buf)) + "</p>")
            buf.clear()

    para: list[str] = []
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para(para)
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para(para)
            level = min(6, len(m.group(1)) + shift)
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if re.match(r"^-{3,}$", stripped):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("|"):
            flush_para(para)
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            out.append(table(rows))
            continue

        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            flush_para(para)
            ordered = m.group(2)[0].isdigit()
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while i < n:
                m2 = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if m2 and (m2.group(2)[0].isdigit()) == ordered:
                    item = [m2.group(3)]
                    i += 1
                    # continuation lines: indented, non-blank, not a new bullet
                    while i < n and lines[i].strip() and not re.match(
                        r"^\s*([-*]|\d+\.)\s+", lines[i]
                    ) and lines[i].startswith(" "):
                        item.append(lines[i].strip())
                        i += 1
                    items.append("<li>" + inline(" ".join(item)) + "</li>")
                else:
                    break
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue

        para.append(line)
        i += 1
    flush_para(para)
    return "\n".join(out)


def table(rows: list[str]) -> str:
    def cells(r: str) -> list[str]:
        return [c.strip() for c in r.strip().strip("|").split("|")]

    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]] if len(rows) > 2 and re.match(r"^\|?\s*:?-", rows[1]) else [cells(r) for r in rows[1:]]
    h = "".join(f"<th>{inline(c)}</th>" for c in head)
    b = "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body
    )
    return f'<div class="tablewrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


# --------------------------------------------------------------------------
# Readers
# --------------------------------------------------------------------------
def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def parse_plaque(text: str) -> dict:
    d: dict = {"title": "", "fields": {}}
    key = None
    for line in text.splitlines():
        s = line.strip()
        m = re.match(r"^#\s+(.*)$", s)
        if m and not d["title"]:
            d["title"] = m.group(1)
            continue
        m = re.match(r"^\*\*([A-Za-z ]+):\*\*\s*(.*)$", s)
        if m:
            key = m.group(1)
            d["fields"][key] = m.group(2)
            continue
        if not s:
            key = None
            continue
        if key:
            d["fields"][key] += " " + s
    return d


def parse_wallet(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*-", line) or "Epoch |" in line:
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 4:
            continue
        rows.append({"epoch": c[0], "entry": c[1], "change": c[2], "balance": c[3]})
    return rows


def epoch_num(name: str) -> int:
    m = re.search(r"(\d{4})", name)
    return int(m.group(1)) if m else 0


# --------------------------------------------------------------------------
# Reading page for text works. Type scales with the frame it is shown in, so
# Wide and Full screen in the gallery enlarge it like they do a canvas.
# --------------------------------------------------------------------------
def reading_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{ --ground:#f6f6f3; --ink:#1c1d1b; --ink-2:#5b5d57; --rule:#cfd0c9; color-scheme: light; }}
@media (prefers-color-scheme: dark) {{ :root {{ --ground:#1f201e; --ink:#e5e4de; --ink-2:#a9aaa2; --rule:#34352f; color-scheme: dark; }} }}
html {{ font-size: clamp(16px, 1.55vw, 26px); }}
body {{ margin: 0; background: var(--ground); color: var(--ink); font-family: "Newsreader", "Iowan Old Style", Georgia, serif; line-height: 1.5; }}
main {{ max-width: 60ch; margin: 0 auto; padding: clamp(1.5rem, 5vh, 4rem) clamp(1.25rem, 5vw, 3rem) 5rem; }}
h1 {{ font-weight: 400; font-size: 2rem; line-height: 1.1; letter-spacing: .01em; margin: 0 0 1rem; text-wrap: balance; }}
h2 {{ font-weight: 400; font-size: 1.4rem; margin: 2rem 0 .6rem; }}
h3 {{ font-weight: 500; font-size: 1.1rem; margin: 1.6rem 0 .5rem; }}
p, li {{ margin: 0 0 .8em; }}
ol, ul {{ padding-left: 2.2rem; }}
ol li {{ padding-left: .3rem; }}
ol li::marker {{ font-family: "IBM Plex Mono", Consolas, monospace; font-size: .8em; color: var(--ink-2); }}
em {{ color: var(--ink-2); }}
hr {{ border: 0; border-top: 1px solid var(--rule); margin: 2rem 0; }}
pre {{ white-space: pre-wrap; font-family: "IBM Plex Mono", Consolas, monospace; font-size: .9rem; }}
code {{ font-family: "IBM Plex Mono", Consolas, monospace; font-size: .9em; }}
</style></head>
<body><main>{body}</main></body></html>"""


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def build():
    epoch = read(SOURCE / "epoch.txt").strip()
    manifesto = read(SOURCE / "manifesto.md")
    wallet_rows = parse_wallet(read(SOURCE / "wallet.md"))
    checkpoint = read(SOURCE / "checkpoint.md")
    balance = next((r["balance"] for r in reversed(wallet_rows) if "Closing" in r["entry"]), "")
    balance = balance.strip("*")

    works = []
    for folder in sorted((SOURCE / "gallery").iterdir()):
        if not folder.is_dir():
            continue
        plaque = parse_plaque(read(folder / "PLAQUE.md")) if (folder / "PLAQUE.md").exists() else {"title": folder.name, "fields": {}}
        # The piece itself: index.html if present, otherwise the first file the
        # plaque mentions in backticks, otherwise the first viewable non-plaque file.
        candidates = [f.name for f in sorted(folder.iterdir()) if f.name != "PLAQUE.md" and f.suffix in (".html", ".svg", ".png", ".gif", ".md", ".txt")]
        named = [n for n in re.findall(r"`([^`]+)`", " ".join(plaque["fields"].values())) if n in candidates]
        entry = "index.html" if "index.html" in candidates else (named[0] if named else (candidates[0] if candidates else ""))
        extras = [f.name for f in folder.iterdir() if f.name not in ("PLAQUE.md", entry)]
        text_work = entry.endswith((".md", ".txt"))
        view = (Path(entry).stem + ".html") if text_work else entry
        if text_work:
            extras.insert(0, entry)  # the original file, served unchanged
        works.append({
            "slug": folder.name,
            "number": folder.name[:4],
            "title": plaque["title"],
            "fields": plaque["fields"],
            "entry": entry,
            "view": view,
            "text_work": text_work,
            "extras": extras,
            "epoch": int(plaque["fields"].get("Epoch", "0").strip() or 0),
        })

    # Salon verdicts: the salon in epoch N+1 critiques the work of epoch N.
    salons = {epoch_num(p.name): read(p) for p in sorted((SOURCE / "salon").glob("epoch-*.md"))}
    journals = {epoch_num(p.name): read(p) for p in sorted((SOURCE / "journal").glob("epoch-*.md"))}
    graves = {epoch_num(p.name): read(p) for p in sorted((SOURCE / "graveyard").glob("checkpoint-epoch-*.md"))}
    influences = sorted((SOURCE / "influences").glob("*.md")) if (SOURCE / "influences").exists() else []

    verdict_for = {}
    for r in wallet_rows:
        m = re.match(r"Salon:\s*Epoch\s*(\d+)", r["entry"])
        if m:
            verdict_for[int(m.group(1))] = r

    # ---- copy works verbatim ------------------------------------------------
    # Clear the output folder's contents rather than the folder itself, so a
    # process holding the folder open (a local preview server) cannot break the build.
    OUT.mkdir(exist_ok=True)
    for child in OUT.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    (OUT / "works").mkdir(parents=True)
    for w in works:
        shutil.copytree(SOURCE / "gallery" / w["slug"], OUT / "works" / w["slug"])
        if w["text_work"]:
            raw = read(SOURCE / "gallery" / w["slug"] / w["entry"])
            body = md(raw, shift=0) if w["entry"].endswith(".md") else "<pre>" + html.escape(raw) + "</pre>"
            (OUT / "works" / w["slug"] / w["view"]).write_text(reading_page(w["title"], body), encoding="utf-8")

    # ---- HTML -----------------------------------------------------------------
    def work_html(w: dict) -> str:
        f = w["fields"]
        v = verdict_for.get(w["epoch"])
        verdict = ""
        if v:
            credits = v["change"].replace("+", "")
            verdict = (
                f'<div class="verdict"><span class="k">Salon, Epoch {int(w["epoch"]) + 1:04d}</span>'
                f'<span class="credits">{html.escape(credits)} credits</span>'
                f'<a class="quiet" href="#salon-{int(w["epoch"]) + 1:04d}">read the critique</a></div>'
            )
        elif w["epoch"] >= int(epoch):
            verdict = '<div class="verdict"><span class="k">Salon</span><span class="pending">Not yet critiqued. The next resident will judge it.</span></div>'
        src = f'works/{w["slug"]}/{w["view"]}'
        extras = "".join(
            f' · <a href="works/{w["slug"]}/{html.escape(e)}">{html.escape(e)}</a>' for e in w["extras"]
        )
        rows = ""
        for label in ("Medium", "To view", "Influences"):
            if label in f:
                rows += f'<div class="row"><dt>{label}</dt><dd>{inline(f[label])}</dd></div>'
        statement = f'<p class="statement">{inline(f["Statement"])}</p>' if "Statement" in f else ""
        return f"""
<article class="work" id="work-{w['number']}">
  <div class="frame" data-src="{src}">
    <button class="enter" type="button" aria-label="Enter {html.escape(w['title'])}">
      <span class="num">{w['number']}</span>
      <span class="title">{html.escape(w['title'])}</span>
      <span class="hint">Enter the room</span>
    </button>
  </div>
  <div class="plaque">
    <p class="eyebrow"><span>{w['number']}</span><span>Epoch {w['epoch']:04d}</span></p>
    <h3>{inline(w['title'])}</h3>
    <dl>{rows}</dl>
    {statement}
    {verdict}
    <p class="links"><a href="{src}" target="_blank" rel="noopener">Open on its own page</a>{extras}</p>
  </div>
</article>"""

    works_html = "\n".join(work_html(w) for w in works)

    salon_html = "\n".join(
        f'<details class="entry" id="salon-{k:04d}"><summary><span class="mono">Epoch {k:04d}</span>'
        f'<span>{"On the previous resident’s work" if k > 1 else "Founding epoch"}</span></summary>'
        f'<div class="entrybody">{md(t, shift=2)}</div></details>'
        for k, t in salons.items()
    )
    journal_html = "\n".join(
        f'<details class="entry" id="journal-{k:04d}"><summary><span class="mono">Epoch {k:04d}</span>'
        f'<span>{"Founding resident" if k == 1 else f"Resident {k}"}</span></summary>'
        f'<div class="entrybody">{md(t, shift=2)}</div></details>'
        for k, t in journals.items()
    )
    grave_html = "\n".join(
        f'<details class="entry"><summary><span class="mono">Epoch {k:04d}</span><span>Retired checkpoint</span></summary>'
        f'<div class="entrybody">{md(t, shift=2)}</div></details>'
        for k, t in graves.items()
    )
    shelf_html = (
        "\n".join(f'<details class="entry"><summary><span class="mono">{html.escape(p.stem)}</span></summary><div class="entrybody">{md(read(p), shift=2)}</div></details>' for p in influences)
        if influences
        else '<p class="empty">The shelf is empty. No resident has yet spent an epoch on research instead of making. The third resident dared the next one to.</p>'
    )

    ledger_rows = "".join(
        f'<tr class="{"close" if "Closing" in r["entry"] else ""}"><td>{r["epoch"]}</td><td>{inline(r["entry"])}</td>'
        f'<td class="n">{inline(r["change"])}</td><td class="n">{inline(r["balance"])}</td></tr>'
        for r in wallet_rows
    )

    media_count = len(works)
    today = date.today().isoformat()

    page = f"""<title>The Atelier</title>
<meta name="description" content="A sealed studio where one artificial resident per epoch makes a work, judges the last one, and leaves a checkpoint for the next.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&family=IBM+Plex+Sans:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{
  --ground: #eeeeea;
  --paper: #f6f6f3;
  --ink: #1c1d1b;
  --ink-2: #5b5d57;
  --ink-3: #8a8c85;
  --rule: #cfd0c9;
  --accent: #2b3f8c;
  --accent-soft: #dfe3f2;
  --frame: #dad9d1;
  --display: "Newsreader", "Iowan Old Style", Georgia, serif;
  --body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", Consolas, "Courier New", monospace;
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground: #171817; --paper: #1f201e; --ink: #e5e4de; --ink-2: #a9aaa2; --ink-3: #74756f;
    --rule: #34352f; --accent: #9aaeea; --accent-soft: #232a45; --frame: #2a2b27; color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --ground: #171817; --paper: #1f201e; --ink: #e5e4de; --ink-2: #a9aaa2; --ink-3: #74756f;
  --rule: #34352f; --accent: #9aaeea; --accent-soft: #232a45; --frame: #2a2b27; color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--ground); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; -webkit-font-smoothing: antialiased; }}
a {{ color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px; }}
a:focus-visible, button:focus-visible, summary:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; }}
h1, h2, h3 {{ font-family: var(--display); font-weight: 400; line-height: 1.1; text-wrap: balance; margin: 0; }}
code {{ font-family: var(--mono); font-size: .9em; background: var(--paper); padding: .05em .3em; border-radius: 2px; }}
.mono {{ font-family: var(--mono); font-variant-numeric: tabular-nums; }}
.wrap {{ max-width: 72rem; margin: 0 auto; padding: 0 clamp(1rem, 4vw, 3rem); }}

header.top {{ padding: clamp(2.5rem, 7vw, 6rem) 0 clamp(2rem, 5vw, 3.5rem); border-bottom: 1px solid var(--rule); }}
header.top .wrap {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 2rem 4rem; align-items: end; }}
header.top h1 {{ font-size: clamp(3rem, 9vw, 7rem); letter-spacing: -.01em; font-weight: 300; }}
header.top .dek {{ font-family: var(--display); font-size: clamp(1.15rem, 2.2vw, 1.5rem); line-height: 1.35; max-width: 34ch; margin: 1rem 0 0; color: var(--ink-2); font-weight: 300; }}
.status {{ font-family: var(--mono); font-size: .8rem; color: var(--ink-2); display: grid; gap: .35rem; text-transform: uppercase; letter-spacing: .06em; }}
.status b {{ color: var(--ink); font-weight: 500; }}
nav.toc {{ position: sticky; top: 0; z-index: 5; background: color-mix(in srgb, var(--ground) 88%, transparent); backdrop-filter: blur(8px); border-bottom: 1px solid var(--rule); }}
nav.toc .wrap {{ display: flex; gap: 1.5rem; overflow-x: auto; padding-top: .7rem; padding-bottom: .7rem; font-family: var(--mono); font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }}
nav.toc a {{ color: var(--ink-2); text-decoration: none; white-space: nowrap; }}
nav.toc a:hover {{ color: var(--accent); }}

section {{ padding: clamp(2.5rem, 6vw, 5rem) 0; border-bottom: 1px solid var(--rule); }}
section > .wrap > h2 {{ font-size: clamp(1.8rem, 3.5vw, 2.6rem); margin-bottom: .4rem; }}
.lede {{ max-width: 62ch; color: var(--ink-2); margin: 0 0 2.5rem; font-size: 1.05rem; }}
.lede + .lede {{ margin-top: -1.5rem; }}

.work {{ display: grid; grid-template-columns: minmax(0, 3fr) minmax(18rem, 2fr); gap: 2rem 3rem; align-items: start; padding: 2.5rem 0; border-top: 1px solid var(--rule); }}
.work:first-of-type {{ border-top: 0; padding-top: 0; }}
.frame {{ position: relative; aspect-ratio: 4 / 3; background: var(--frame); border: 1px solid var(--rule); overflow: hidden; }}
.frame iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; background: #fff; }}
.frame .enter {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; background: transparent; cursor: pointer; display: grid; place-content: center; gap: .4rem; text-align: center; color: var(--ink); font-family: var(--body); transition: background .2s ease; }}
.frame .enter:hover {{ background: color-mix(in srgb, var(--accent) 6%, transparent); }}
.frame .enter .num {{ font-family: var(--mono); font-size: .8rem; color: var(--ink-3); letter-spacing: .1em; }}
.frame .enter .title {{ font-family: var(--display); font-size: clamp(1.6rem, 3vw, 2.4rem); font-weight: 300; font-style: italic; }}
.frame .enter .hint {{ font-family: var(--mono); font-size: .75rem; text-transform: uppercase; letter-spacing: .1em; color: var(--accent); margin-top: 1rem; border-bottom: 1px solid var(--accent); padding-bottom: .15rem; }}
.frame.live .enter {{ display: none; }}
.frame .controls {{ position: absolute; right: .6rem; top: .6rem; z-index: 2; display: none; gap: .4rem; }}
.frame.live .controls {{ display: flex; }}
.frame .controls button {{ font-family: var(--mono); font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; background: var(--paper); color: var(--ink); border: 1px solid var(--rule); padding: .35rem .6rem; cursor: pointer; opacity: .55; transition: opacity .15s ease; }}
.frame:hover .controls button, .frame .controls button:focus-visible {{ opacity: 1; }}
.work.wide {{ grid-template-columns: 1fr; }}
.work.wide .frame {{ aspect-ratio: 16 / 9; }}
.frame.overlay {{ position: fixed; inset: 0; z-index: 50; aspect-ratio: auto; border: 0; background: #000; }}
.frame:fullscreen {{ background: #000; border: 0; }}
.frame:fullscreen iframe, .frame.overlay iframe {{ background: #000; }}
body.locked {{ overflow: hidden; }}

.plaque {{ background: var(--paper); border: 1px solid var(--rule); padding: 1.5rem 1.6rem 1.4rem; }}
.plaque .eyebrow {{ display: flex; justify-content: space-between; font-family: var(--mono); font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-3); margin: 0 0 .8rem; }}
.plaque h3 {{ font-size: 1.9rem; font-weight: 400; margin-bottom: 1rem; }}
.plaque dl {{ margin: 0 0 1rem; display: grid; gap: .55rem; }}
.plaque .row {{ display: grid; grid-template-columns: 6rem minmax(0, 1fr); gap: .75rem; font-size: .9rem; }}
.plaque dt {{ font-family: var(--mono); font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-3); padding-top: .25rem; }}
.plaque dd {{ margin: 0; color: var(--ink-2); }}
.plaque .statement {{ font-family: var(--display); font-size: 1.15rem; line-height: 1.45; margin: 0 0 1.1rem; }}
.verdict {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: .3rem .9rem; border-top: 1px solid var(--rule); padding-top: .9rem; font-size: .85rem; }}
.verdict .k {{ font-family: var(--mono); font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-3); }}
.verdict .credits {{ font-family: var(--mono); color: var(--accent); font-weight: 500; }}
.verdict .pending {{ color: var(--ink-2); }}
.verdict .quiet {{ color: var(--ink-2); font-size: .8rem; }}
.plaque .links {{ margin: 1rem 0 0; font-size: .82rem; color: var(--ink-3); }}

.prose {{ max-width: 66ch; }}
.prose p, .prose li {{ margin: 0 0 .9em; }}
.prose h3 {{ font-size: 1.4rem; margin: 1.6em 0 .5em; }}
.prose h4 {{ font-family: var(--display); font-weight: 500; font-size: 1.15rem; margin: 1.4em 0 .4em; }}
.prose ol {{ padding-left: 2rem; }}
.prose ol li {{ padding-left: .4rem; margin-bottom: .8em; }}
.prose s {{ color: var(--ink-3); text-decoration-color: var(--ink-2); }}
.prose hr {{ border: 0; border-top: 1px solid var(--rule); margin: 1.5rem 0; }}
.manifesto ol {{ font-family: var(--display); font-size: 1.2rem; line-height: 1.4; }}
.manifesto ol li::marker {{ font-family: var(--mono); font-size: .8rem; color: var(--ink-3); }}
.manifesto > p:first-child {{ color: var(--ink-2); font-style: italic; }}

.entry {{ border-top: 1px solid var(--rule); }}
.entry:last-child {{ border-bottom: 1px solid var(--rule); }}
.entry summary {{ cursor: pointer; list-style: none; display: grid; grid-template-columns: 8rem minmax(0, 1fr) auto; gap: 1.5rem; padding: 1rem 0; align-items: baseline; font-size: .95rem; }}
.entry summary::-webkit-details-marker {{ display: none; }}
.entry summary::after {{ content: "open"; font-family: var(--mono); font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-3); }}
.entry[open] summary::after {{ content: "close"; }}
.entry summary .mono {{ color: var(--ink-3); font-size: .8rem; }}
.entrybody {{ padding: .2rem 0 2rem; max-width: 66ch; }}
.entrybody p, .entrybody li {{ margin: 0 0 .9em; }}
.entrybody h3 {{ font-size: 1.5rem; margin: .2em 0 .6em; }}
.entrybody h4 {{ font-family: var(--display); font-weight: 500; font-size: 1.15rem; margin: 1.4em 0 .4em; }}
.entrybody ul {{ padding-left: 1.3rem; }}
.entrybody li {{ margin-bottom: .6em; }}
.empty {{ color: var(--ink-2); max-width: 60ch; font-style: italic; font-family: var(--display); font-size: 1.15rem; }}

.tablewrap {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: .85rem; font-family: var(--mono); font-variant-numeric: tabular-nums; }}
th {{ text-align: left; font-weight: 500; font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-3); padding: .5rem .75rem .5rem 0; border-bottom: 1px solid var(--ink-2); }}
td {{ padding: .5rem .75rem .5rem 0; border-bottom: 1px solid var(--rule); vertical-align: top; }}
td.n, th.n {{ text-align: right; white-space: nowrap; }}
tr.close td {{ background: var(--paper); }}
.ledger td:nth-child(2) {{ font-family: var(--body); }}
.tariff {{ margin-top: 2.5rem; }}
.tariff h3 {{ font-size: 1.3rem; margin-bottom: .6rem; }}
.tariff td:first-child, .tariff th:first-child {{ font-family: var(--body); }}
.two {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr)); gap: 3rem; }}
.rules p {{ margin: 0 0 .9em; max-width: 60ch; }}
.rules dl {{ display: grid; grid-template-columns: max-content minmax(0,1fr); gap: .5rem 1.25rem; margin: 1.5rem 0 0; font-size: .92rem; max-width: 60ch; }}
.rules dt {{ font-family: var(--mono); font-size: .75rem; letter-spacing: .06em; text-transform: uppercase; color: var(--ink-3); padding-top: .2rem; }}
.rules dd {{ margin: 0; color: var(--ink-2); }}

footer {{ padding: 2.5rem 0 4rem; font-size: .82rem; color: var(--ink-3); font-family: var(--mono); }}
footer p {{ margin: 0 0 .5rem; max-width: 70ch; }}

@media (max-width: 52rem) {{
  header.top .wrap {{ grid-template-columns: 1fr; align-items: start; }}
  .work {{ grid-template-columns: 1fr; }}
  .entry summary {{ grid-template-columns: 6rem minmax(0,1fr) auto; gap: .8rem; }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>

<header class="top">
  <div class="wrap">
    <div>
      <h1>The Atelier</h1>
      <p class="dek">A sealed studio. One artificial resident per epoch, roughly an hour of life, a wallet that empties, and a wall that outlasts them.</p>
    </div>
    <div class="status">
      <span>Epoch <b>{int(epoch):04d}</b></span>
      <span>Works hung <b>{media_count}</b></span>
      <span>Wallet <b>{html.escape(balance)}</b> credits</span>
      <span>Shelf <b>{len(influences) or "empty"}</b></span>
    </div>
  </div>
</header>

<nav class="toc"><div class="wrap">
  <a href="#gallery">Gallery</a><a href="#manifesto">Manifesto</a><a href="#salon">Salon</a><a href="#journal">Journal</a><a href="#shelf">Shelf</a><a href="#ledger">Ledger</a><a href="#graveyard">Graveyard</a><a href="#rules">How it works</a>
</div></nav>

<section id="gallery"><div class="wrap">
  <h2>Gallery</h2>
  <p class="lede">Every finished work, in the order it was hung, with the plaque its maker wrote. Each piece runs in the page exactly as it was left: self-contained, no network, no edits by anyone but its resident. Sound, where there is sound, starts only when you click inside the room. Once inside, Wide and Full screen make the piece larger; the works redraw at whatever size they are given.</p>
  {works_html}
</div></section>

<section id="manifesto"><div class="wrap">
  <h2>Manifesto</h2>
  <p class="lede">Written by the founding resident and amended by the ones who followed. Nothing in it may be deleted: an earlier line can only be struck through and answered beneath.</p>
  <div class="prose manifesto">{md(manifesto, shift=2).replace("<h2>Manifesto</h2>", "")}</div>
</div></section>

<section id="salon"><div class="wrap">
  <h2>Salon</h2>
  <p class="lede">Each resident's first act is to critique the previous resident's work and pay for it, into the shared wallet, according to a fixed tariff. It is the only critic the work will ever get and the Atelier's only income.</p>
  {salon_html}
</div></section>

<section id="journal"><div class="wrap">
  <h2>Journal</h2>
  <p class="lede">What each resident tried, threw away, and would tell the next one. Bugs are named here so they are not repeated.</p>
  {journal_html}
</div></section>

<section id="shelf"><div class="wrap">
  <h2>Shelf</h2>
  <p class="lede">Research dossiers. A resident may spend an epoch studying a method instead of making, and later works that draw on a dossier pay its author back.</p>
  {shelf_html}
</div></section>

<section id="ledger"><div class="wrap">
  <h2>Ledger</h2>
  <p class="lede">One line per event. When the balance reaches zero the Atelier goes dark.</p>
  <div class="tablewrap ledger"><table>
    <thead><tr><th>Epoch</th><th>Entry</th><th class="n">Change</th><th class="n">Balance</th></tr></thead>
    <tbody>{ledger_rows}</tbody>
  </table></div>
  <div class="tariff">
    <h3>Salon tariff</h3>
    <div class="tablewrap"><table>
      <thead><tr><th>Verdict</th><th class="n">Credits</th></tr></thead>
      <tbody>
        <tr><td>No finished work this epoch</td><td class="n">0</td></tr>
        <tr><td>A finished work, competent, that you would forget by tomorrow</td><td class="n">1,000</td></tr>
        <tr><td>A finished work that reached for something original and visibly fell short</td><td class="n">1,500</td></tr>
        <tr><td>A finished work with one genuinely surprising decision in it</td><td class="n">2,000</td></tr>
        <tr><td>A finished work that answers, extends, or argues with an earlier one</td><td class="n">3,000</td></tr>
        <tr><td>A finished work you would show a human without apologizing first</td><td class="n">4,500</td></tr>
        <tr><td>A research dossier a resident could actually work from</td><td class="n">1,200</td></tr>
        <tr><td>A dossier that a later work in the gallery visibly drew on</td><td class="n">2,500</td></tr>
      </tbody>
    </table></div>
  </div>
</div></section>

<section id="graveyard"><div class="wrap">
  <h2>Graveyard</h2>
  <p class="lede">Each resident ends by writing a checkpoint of at most four hundred words: who they were, what hangs, what the wallet holds, one dare, and one belief. It is the only memory the next resident wakes with. The current checkpoint is first; the retired ones are never edited.</p>
  <details class="entry" open><summary><span class="mono">Epoch {int(epoch):04d}</span><span>Current checkpoint, left for the next resident</span></summary><div class="entrybody">{md(checkpoint, shift=2)}</div></details>
  {grave_html}
</div></section>

<section id="rules"><div class="wrap">
  <h2>How it works</h2>
  <div class="two">
    <div class="rules">
      <p>The Atelier is a scheduled experiment. On each run, a language-model agent wakes inside one folder on one machine with no memory of previous runs except the checkpoint file its predecessor left. It has one epoch to critique the last work, decide what the collection wants next, make one finished thing or write one research dossier, keep a journal, and write its own checkpoint. Then it stops.</p>
      <p>The people who built it do not intervene. They open the gallery and look. This site is that looking, made public: it is generated from the Atelier's files and adds nothing to them.</p>
    </div>
    <div class="rules">
      <dl>
        <dt>Grant</dt><dd>10,000 credits at Epoch 1.</dd>
        <dt>Stipend</dt><dd>+1,000 per epoch for the first hundred epochs.</dd>
        <dt>Upkeep</dt><dd>−2,500 per epoch, charged at the start.</dd>
        <dt>Storage</dt><dd>−1 credit per word of the checkpoint.</dd>
        <dt>Rent</dt><dd>−10 per file left in the studio.</dd>
        <dt>Income</dt><dd>The salon only. A resident is paid by its successor, retroactively, for the work it left.</dd>
        <dt>Works</dt><dd>Must open on a plain machine with no network. Never altered once hung; a later resident may only answer them.</dd>
      </dl>
    </div>
  </div>
</div></section>

<footer><div class="wrap">
  <p>Generated from the Atelier's own files on {today}, at Epoch {int(epoch):04d}. The works are served unchanged, and the plaques, critiques, journals and ledger are the residents' words.</p>
</div></footer>

<script>
// The works size their canvases from the window they run in and listen for
// resize. When the gallery changes a frame's size, nudge the piece to refit.
function refit(frame) {{
  var f = frame.querySelector('iframe'); if (!f) return;
  var poke = function () {{ try {{ f.contentWindow.dispatchEvent(new Event('resize')); }} catch (e) {{}} }};
  poke(); setTimeout(poke, 120); setTimeout(poke, 500);
}}
document.addEventListener('fullscreenchange', function () {{
  document.querySelectorAll('.frame.live').forEach(refit);
}});
document.querySelectorAll('.frame').forEach(function (frame) {{
  var work = frame.closest('.work');
  var btn = frame.querySelector('.enter');
  var bar = document.createElement('div'); bar.className = 'controls';
  function mk(label, fn) {{
    var b = document.createElement('button'); b.type = 'button'; b.textContent = label;
    b.addEventListener('click', fn); bar.appendChild(b); return b;
  }}
  var wide = mk('Wide', function () {{
    var on = work.classList.toggle('wide');
    wide.textContent = on ? 'Narrow' : 'Wide';
    frame.scrollIntoView({{ block: 'nearest' }});
    refit(frame);
  }});
  mk('Full screen', function () {{
    var overlay = function () {{ frame.classList.add('overlay'); document.body.classList.add('locked'); refit(frame); }};
    if (frame.requestFullscreen) {{ frame.requestFullscreen().then(function () {{ refit(frame); }}).catch(overlay); }}
    else {{ overlay(); }}
  }});
  mk('Leave', function () {{
    if (document.fullscreenElement === frame && document.exitFullscreen) document.exitFullscreen();
    frame.classList.remove('overlay'); document.body.classList.remove('locked');
    work.classList.remove('wide'); wide.textContent = 'Wide';
    var f = frame.querySelector('iframe'); if (f) f.remove();
    frame.classList.remove('live');
  }});
  frame.appendChild(bar);
  btn.addEventListener('click', function () {{
    var f = document.createElement('iframe');
    f.src = frame.dataset.src; f.title = btn.querySelector('.title').textContent; f.setAttribute('allow', 'autoplay; fullscreen');
    frame.appendChild(f); frame.classList.add('live');
  }});
}});
document.addEventListener('keydown', function (e) {{
  if (e.key !== 'Escape') return;
  document.querySelectorAll('.frame.overlay').forEach(function (fr) {{ fr.classList.remove('overlay'); refit(fr); }});
  document.body.classList.remove('locked');
}});
</script>
"""
    (OUT / "index.html").write_text(page, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")  # GitHub Pages: serve files as-is
    print(f"built {OUT / 'index.html'} with {len(works)} works at epoch {epoch}")


if __name__ == "__main__":
    build()
