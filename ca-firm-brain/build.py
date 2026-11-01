"""Write the CA firm brain poster as one HTML page holding one SVG.

Dark terminal-box style: mono type, thin boxes, numbered sections, one folder tree,
one page example, one flow with a human gate, one table, one example walk, a legend.
Box border carries the category (see LEGEND at the bottom of the poster).

Usage:
  python3 -I ca-firm-brain/build.py
  node ca-firm-brain/render.cjs        # writes 01-ca-firm-brain.png (dark) + -light.png
"""
from pathlib import Path
from html import escape

HERE = Path(__file__).resolve().parent
W = 1600
L, R = 70, 1530
CW = R - L  # 1460

HEAD = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap">
<style>
  :root {{
    --bg: #0e1014; --panel: #14171c; --fg: #e8e8ea; --dim: #8a8f99; --line: #2b3038;
    --in: #4fc1c9;     /* what comes in */
    --brain: #e0a84a;  /* the brain: pages, graph, timeline */
    --agent: #a98bf0;  /* the agent and its skills */
    --gate: #e07aa8;   /* a person must say yes */
    --ok: #6ccf7a;     /* a result */
    --never: #e06a6a;  /* never */
    --mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
  }}
  :root[data-theme="light"] {{
    --bg: #f3f3f1; --panel: #ffffff; --fg: #16181d; --dim: #5d626c; --line: #d3d5da;
    --in: #0f8b94; --brain: #a86f0f; --agent: #6b4fd1; --gate: #b8336f; --ok: #2b8a3e; --never: #c0392b;
  }}
  html, body {{ margin: 0; background: var(--bg); }}
  .fig {{ max-width: {w}px; margin: 0 auto; }}
  svg {{ display: block; width: 100%; height: auto; background: var(--bg); }}
  svg text {{ font-family: var(--mono); fill: var(--fg); font-size: 18px; white-space: pre; }}
  svg .t {{ font-size: 44px; font-weight: 700; letter-spacing: .02em; }}
  svg .sub {{ font-size: 21px; fill: var(--dim); }}
  svg .sec {{ font-size: 24px; font-weight: 600; letter-spacing: .05em; }}
  svg .h {{ font-size: 21px; font-weight: 600; letter-spacing: .02em; }}
  svg .s {{ font-size: 16px; }}
  svg .xs {{ font-size: 14px; }}
  svg .lab {{ font-size: 13.5px; font-weight: 600; letter-spacing: .1em; fill: var(--dim); }}
  svg .d {{ fill: var(--dim); }}
  svg .b {{ font-weight: 600; }}
  svg .in {{ fill: var(--in); }} svg .brain {{ fill: var(--brain); }} svg .agent {{ fill: var(--agent); }}
  svg .gate {{ fill: var(--gate); }} svg .ok {{ fill: var(--ok); }} svg .never {{ fill: var(--never); }}
  svg .bx {{ fill: var(--panel); stroke: var(--line); stroke-width: 1.4; }}
  svg .bx-in {{ fill: var(--panel); stroke: var(--in); stroke-width: 1.6; }}
  svg .bx-brain {{ fill: var(--panel); stroke: var(--brain); stroke-width: 1.6; }}
  svg .bx-agent {{ fill: var(--panel); stroke: var(--agent); stroke-width: 1.6; }}
  svg .bx-gate {{ fill: var(--panel); stroke: var(--gate); stroke-width: 3.2; }}
  svg .bx-ok {{ fill: var(--panel); stroke: var(--ok); stroke-width: 1.6; }}
  svg .bx-never {{ fill: var(--panel); stroke: var(--never); stroke-width: 1.6; }}
  svg .ex {{ fill: none; stroke: var(--dim); stroke-width: 1.2; stroke-dasharray: 5 5; }}
  svg .ln {{ fill: none; stroke: var(--dim); stroke-width: 1.5; }}
  svg .rule {{ stroke: var(--line); stroke-width: 1; }}
  svg .rule-fg {{ stroke: var(--fg); stroke-width: 1.2; }}
  svg .tip {{ fill: var(--dim); }}
  svg .thead {{ fill: var(--line); opacity: .55; }}
</style>
</head>
<body>
<div class="fig">
<svg id="diagram" viewBox="0 0 {w} {h}" role="img" aria-labelledby="dt" xmlns="http://www.w3.org/2000/svg">
<title id="dt">{title}</title>
<defs><marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" class="tip"/></marker></defs>
"""
TAIL = """</svg>
</div>
</body>
</html>
"""

SIZE = {"t": 44, "sub": 21, "sec": 24, "h": 21, "s": 16, "xs": 14, "lab": 13.5, "": 18}


class Svg:
    def __init__(self):
        self.out = []
        self.warn = []

    def text(self, x, y, s, cls="", anchor=None, maxw=None):
        a = f' text-anchor="{anchor}"' if anchor else ""
        c = f' class="{cls}"' if cls else ""
        if maxw:
            size = 18
            for k in cls.split():
                if k in SIZE:
                    size = SIZE[k]
            est = len(s) * size * 0.6
            if est > maxw:
                self.warn.append(f"overflow {int(est)}>{maxw}: {s!r}")
        self.out.append(f'<text x="{x}" y="{y}"{c}{a}>{escape(s)}</text>')

    def lines(self, x, y, items, cls="", lh=26, maxw=None):
        for i, s in enumerate(items):
            self.text(x, y + i * lh, s, cls, maxw=maxw)
        return y + len(items) * lh

    def rect(self, x, y, w, h, cls="bx"):
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}"/>')

    def path(self, d, arrow=True, cls="ln"):
        m = ' marker-end="url(#ah)"' if arrow else ""
        self.out.append(f'<path d="{d}" class="{cls}"{m}/>')

    def hr(self, y, cls="rule", x1=L, x2=R):
        self.out.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="{cls}"/>')

    def section(self, y, label, note=""):
        self.text(L, y, label, "sec")
        if note:
            self.text(R, y, note, "s d", "end")


def poster():
    g = Svg()

    # ---------- header
    g.text(L, 96, "A CA FIRM ON ONE BRAIN", "t")
    g.text(R, 96, "chartered accountancy · brain map", "s d", "end")
    g.text(L, 140, "how a practice runs client memory, notices and deadlines through an agent brain,", "sub")
    g.text(L, 170, "so no position, due date or past reply is ever lost when a person is busy or gone", "sub")
    g.hr(204, "rule-fg")

    # ---------- 01 the system
    y = 262
    g.section(y, "01 / THE SYSTEM", "you speak plainly · the agent reads its skills · the brain keeps the facts")
    bw, gap, bh = 340, 33, 160
    top = y + 36
    sysb = [
        ("YOU", "partner · manager · article", ["forward a notice, ask a", "question, say yes or no"], "bx", ""),
        ("THE AGENT", "reads skill files first", ["drafts, files pages, cites", "sources · never sends alone"], "bx-agent", "agent"),
        ("THE BRAIN", "pages + graph + timeline", ["hybrid search over markdown", "typed links made on save"], "bx-brain", "brain"),
        ("YOUR TOOLS", "email · portals · tally", ["a person presses send,", "files, pays · not the brain"], "bx", ""),
    ]
    for i, (name, sub, body, cls, tc) in enumerate(sysb):
        x = L + i * (bw + gap)
        g.rect(x, top, bw, bh, cls)
        g.text(x + 22, top + 42, name, f"h {tc}".strip(), maxw=bw - 44)
        g.text(x + 22, top + 70, sub, "s d", maxw=bw - 44)
        g.lines(x + 22, top + 108, body, "s", 26, maxw=bw - 44)
        if i < 3:
            g.path(f"M{x + bw + 3},{top + bh // 2} H{x + bw + gap - 5}")
    y = top + bh

    # ---------- 02 what comes in
    y += 74
    g.section(y, "02 / WHAT COMES IN", "the tools the firm already uses · nothing new to learn")
    cw3, g3, ch = (CW - 60) // 3, 30, 158
    srcs = [
        ("client emails", "notices · questions · files", ["· income-tax + GST notices", "· client questions", "· bank statements, invoices"]),
        ("portal downloads", "gst · income-tax · mca", ["· GSTR-2B, 2A, filed returns", "· 26AS, AIS, demand notices", "· MCA filings, DIN alerts"]),
        ("books + exports", "tally · zoho · excel", ["· trial balance, ledgers", "· purchase + sales registers", "· TDS and payroll sheets"]),
        ("calls + meetings", "notes · recordings", ["· what the client decided", "· positions taken and why", "· who does what, by when"]),
        ("whatsapp forwards", "pasted into the brain", ["· scanned notices", "· photos of bills", "· quick client questions"]),
        ("working papers", "audit · assessment files", ["· checklists and open queries", "· replies already filed", "· past assessment orders"]),
    ]
    top = y + 36
    for i, (name, sub, det) in enumerate(srcs):
        row, col = divmod(i, 3)
        x = L + col * (cw3 + g3)
        yy = top + row * (ch + 22)
        g.rect(x, yy, cw3, ch, "bx-in")
        g.text(x + 22, yy + 40, name, "h", maxw=cw3 - 44)
        g.text(x + 22, yy + 66, sub, "s d", maxw=cw3 - 44)
        g.lines(x + 22, yy + 100, det, "s", 25, maxw=cw3 - 44)
    y = top + 2 * ch + 22

    # ---------- 03 how it is filed
    y += 74
    g.section(y, "03 / HOW IT IS FILED", "one primary home per fact · the folder name decides the page type")
    top = y + 36
    lw, rw, gp = 720, 700, 40
    bh3 = 372
    g.rect(L, top, lw, bh3, "bx-brain")
    g.text(L + 24, top + 40, "THE FOLDER TREE", "lab")
    tree = [
        "brain/",
        "  companies/   one page per client entity (co · LLP · firm)",
        "  people/      promoters · CFOs · client accountants · officers",
        "  projects/    one page per engagement: audit FY25-26 · GSTR-9 · ITR",
        "  concepts/    law, sections, circulars + the firm's own positions",
        "  finance/     rates · due-date calendars · fee schedules",
        "  meetings/    one page per call or visit, dated",
        "  sources/     raw files: notices, returns, statements · never edited",
        "  inbox/       anything the rules cannot place yet",
    ]
    g.lines(L + 24, top + 76, tree, "s", 27, maxw=lw - 48)
    g.hr(top + 326, "rule", L + 24, L + lw - 24)
    g.text(L + 24, top + 352, "keep these names: the brain auto-links only folders it knows", "xs d", maxw=lw - 48)

    rx = L + lw + gp
    g.rect(rx, top, rw, bh3, "bx-brain")
    g.text(rx + 24, top + 40, "ONE CLIENT PAGE · TWO LAYERS", "lab")
    page = [
        ("companies/widget-traders.md", "b"),
        ("type: company · gstin: 27XXXXX0000X1Z5 · fy: apr-mar", "d"),
        ("services: statutory audit · GSTR-9 · ITR", ""),
        ("contacts: [owner](people/r-shah) · [accounts](people/p-iyer)", ""),
        ("open: ASMT-10 notice · reply due 14 nov", ""),
        ("position: ITC claimed on 2B basis since FY24", ""),
        ("<!-- timeline -->", "d"),
        ("2026-10-28  ASMT-10 received · sources/notice-2026-10-28", ""),
        ("2026-09-20  GSTR-3B sep filed · ARN saved", ""),
        ("2026-07-15  statutory audit FY25-26 started", ""),
    ]
    yy = top + 76
    for s, c in page:
        g.text(rx + 24, yy, s, f"s {c}".strip(), maxw=rw - 48)
        yy += 27
    g.hr(top + 326, "rule", rx + 24, rx + rw - 24)
    g.text(rx + 24, top + 352, "top = what is true now · bottom = what happened, when", "xs d", maxw=rw - 48)
    y = top + bh3

    # ---------- 04 the graph wires itself
    y += 74
    g.section(y, "04 / THE GRAPH WIRES ITSELF", "every page save extracts links · zero model calls")
    top = y + 36
    bh4 = 262
    g.rect(L, top, lw, bh4, "bx-brain")
    g.text(L + 24, top + 40, "TYPED EDGES MADE ON SAVE", "lab")
    raw_edges = [
        ("people/r-shah", "works_at", "companies/widget-traders"),
        ("projects/audit-fy25-26", "mentions", "people/p-iyer"),
        ("the-firm", "advises", "companies/widget-traders"),
        ("projects/asmt-10-reply", "source", "sources/notice-2026-10-28"),
        ("meetings/2026-10-30", "attended", "people/r-shah"),
    ]
    edges = [f"{a:<23}─ {t:<9}──▸  {b}" for a, t, b in raw_edges]
    g.lines(L + 24, top + 78, edges, "s", 28, maxw=lw - 48)
    g.text(L + 24, top + 236, "+ a dated timeline entry on every company and person named", "xs d", maxw=lw - 48)

    g.rect(rx, top, rw, bh4, "bx-brain")
    g.text(rx + 24, top + 40, "QUESTIONS SEARCH ALONE CANNOT ANSWER", "lab")
    qs = [
        "· which clients have an open notice this quarter?",
        "· who at this client handles GST, and since when?",
        "· every engagement where we took the 2B position",
        "· what did we tell this client about TDS last year?",
        "· which engagements touch this one supplier?",
    ]
    g.lines(rx + 24, top + 78, qs, "s", 28, maxw=rw - 48)
    g.text(rx + 24, top + 236, "graph walk from one page, 1 to 2 hops, typed by edge", "xs d", maxw=rw - 48)
    y = top + bh4

    # ---------- 05 how one notice moves
    y += 74
    g.section(y, "05 / HOW ONE NOTICE MOVES", "the brain does the work · a CA decides at the gate")
    steps = [
        ("1  NOTICE ARRIVES", ["GST ASMT-10, widget traders", "forwarded by the client"], "bx-in"),
        ("2  FILED", ["under the client's page", "due date on the timeline"], "bx-brain"),
        ("3  FACTS FOUND", ["2B vs books, that period", "our past reply + position"], "bx-brain"),
        ("4  LAW PULLED", ["section · rule · circular", "with the page it came from"], "bx-brain"),
        ("5  DRAFT WRITTEN", ["reply + evidence list", "numbers show their source"], "bx-agent"),
        ("◆ 6 · A CA SAYS YES", ["yes · change it · no", "never files on its own"], "bx-gate"),
        ("⚓ 7  SENT + RECORDED", ["from the firm's own login", "ARN saved on the timeline"], "bx-ok"),
        ("↺ 8  REMEMBERED", ["the position becomes a rule", "next notice drafts faster"], "bx-brain"),
    ]
    sw, sg, sh = 335, 40, 150
    r1 = y + 36
    r2 = r1 + sh + 80
    for i, (h, body, cls) in enumerate(steps):
        row, col = divmod(i, 4)
        x, yy = L + col * (sw + sg), (r1, r2)[row]
        g.rect(x, yy, sw, sh, cls)
        tc = {"bx-gate": "gate", "bx-ok": "ok"}.get(cls, "")
        g.text(x + 20, yy + 42, h, f"h {tc}".strip(), maxw=sw - 40)
        g.lines(x + 20, yy + 80, body, "s", 27, maxw=sw - 40)
        if col < 3:
            g.path(f"M{x + sw + 3},{yy + sh // 2} H{x + sw + sg - 5}")
    x4 = L + 3 * (sw + sg) + sw // 2
    x5 = L + sw // 2
    my = r1 + sh + 40
    g.path(f"M{x4},{r1 + sh + 5} V{my} H{x5} V{r2 - 6}")
    y = r2 + sh

    # ---------- 06 who sees what + where it runs
    y += 74
    g.section(y, "06 / WHO SEES WHAT · WHERE IT RUNS", "one brain per partner or practice group · separation is physical")
    top = y + 36
    tw = 900
    cols = ["", "partner brain", "practice brain", "law pages", "other groups"]
    cwid = [170, 190, 210, 150, 180]
    rows = [
        ["partner", "✓ read + change", "✓ read · approves", "✓ read", "✕"],
        ["manager", "✕", "✓ read · suggests", "✓ read", "✕"],
        ["article", "✕", "✓ read · drafts", "✓ read", "✕"],
        ["client", "✕", "what a CA sends", "✕", "✕"],
        ["outsider", "✕", "✕", "✕", "✕"],
    ]
    rh = 50
    th = rh * (len(rows) + 1)
    g.rect(L, top, tw, th, "bx")
    g.out.append(f'<rect x="{L}" y="{top}" width="{tw}" height="{rh}" class="thead"/>')
    for r, row in enumerate([cols] + rows):
        x = L
        for c, cell in enumerate(row):
            g.text(x + 16, top + r * rh + 32, cell, "lab" if r == 0 else ("s b" if c == 0 else "s"), maxw=cwid[c] - 20)
            x += cwid[c]
        if r:
            g.hr(top + r * rh, "rule", L, L + tw)

    wx = L + tw + 40
    ww = R - wx
    g.rect(wx, top, ww, th, "bx")
    g.text(wx + 22, top + 36, "WHERE IT RUNS", "lab")
    run = [
        ("start", "one file on a firm machine · no server"),
        ("grow", "postgres + pgvector on your own box or a"),
        ("", "managed DB in India · 1000+ files"),
        ("access", "no per-user locks inside one brain today,"),
        ("", "so one brain per partner, no shared keys,"),
        ("", "staff go through the agent, not a key"),
        ("data", "stays on the firm's server · you own it"),
    ]
    yy = top + 68
    for lab, body in run:
        if lab:
            g.text(wx + 22, yy, lab, "xs d")
        g.text(wx + 92, yy, body, "s", maxw=ww - 110)
        yy += 27
    y = top + th

    # ---------- 07 the rhythm
    y += 74
    g.section(y, "07 / THE RHYTHM", "scheduled jobs the brain runs for the firm")
    rhythm = [
        ("EVERY MORNING", "a due list per person: returns, replies, hearings · what is late"),
        ("ALL DAY", "drafts wait in one approval list: yes, change it or no"),
        ("EVERY NIGHT", "sync new files, extract links, embed, flag stale positions"),
        ("EVERY MONDAY", "one memo per partner: filings done, notices open, fees to bill"),
        ("EVERY MONTH", "a health check: dead links, orphan pages, coverage, what was learned"),
    ]
    rrh = 52
    top = y + 36
    g.rect(L, top, CW, rrh * len(rhythm), "bx")
    for i, (lab, body) in enumerate(rhythm):
        yy = top + i * rrh
        if i:
            g.hr(yy, "rule", L, L + CW)
        g.text(L + 22, yy + 33, lab, "lab")
        g.text(L + 260, yy + 33, body, "s", maxw=CW - 280)
    y = top + rrh * len(rhythm)

    # ---------- 08 rollout
    y += 74
    g.section(y, "08 / ROLLOUT IN FIVE STEPS", "one partner first · prove retrieval before adding clients")
    roll = [
        ("1 PILOT", ["one partner's clients", "local brain, the six", "folders above, no server"]),
        ("2 SEED", ["client master from the", "tally or zoho export,", "one markdown page each"]),
        ("3 INGEST", ["two years of notices,", "filings and call notes", "for those clients only"]),
        ("4 MEASURE", ["20 real questions from", "the partner, scored on", "recall · fix schema 1st"]),
        ("5 EXPAND", ["night jobs, email intake", "next partner · postgres", "when the brain outgrows"]),
    ]
    rw5, rg5, rh5 = 268, 30, 150
    top = y + 36
    for i, (h, body) in enumerate(roll):
        x = L + i * (rw5 + rg5)
        g.rect(x, top, rw5, rh5, "bx-agent" if i in (0, 4) else "bx")
        g.text(x + 18, top + 40, h, "h", maxw=rw5 - 36)
        g.lines(x + 18, top + 76, body, "s", 25, maxw=rw5 - 36)
        if i < 4:
            g.path(f"M{x + rw5 + 3},{top + rh5 // 2} H{x + rw5 + rg5 - 5}")
    y = top + rh5

    # ---------- 09 not in the box + non-negotiables
    y += 74
    g.section(y, "09 / NOT IN THE BOX · NON-NEGOTIABLES")
    top = y + 36
    hw = (CW - 40) // 2
    bh9 = 232
    g.rect(L, top, hw, bh9, "bx")
    g.text(L + 22, top + 36, "NOT IN THE BOX · BUILD IT OR KEEP YOUR TOOL", "lab")
    nib = [
        "· no tally, GST-portal or income-tax-portal connector:",
        "  write small deterministic collectors that drop files in",
        "· not a document or practice-management system:",
        "  signed workpapers stay in your DMS, the brain is memory",
        "· no per-user access rules inside one brain: split brains",
        "· no claim about audit-documentation retention standards",
    ]
    g.lines(L + 22, top + 70, nib, "s", 26, maxw=hw - 44)

    nx = L + hw + 40
    g.rect(nx, top, hw, bh9, "bx-never")
    g.text(nx + 22, top + 36, "THE BRAIN NEVER", "lab never")
    never = [
        "✕ files a return or sends a reply without a CA's yes",
        "✕ invents a number, a section or a date",
        "✕ shows a figure without the source it came from",
        "✕ shares a login: one person, one key",
        "✕ lets client data leave the firm's server",
        "✕ keeps passwords, OTPs or DSC PINs in any page",
    ]
    g.lines(nx + 22, top + 70, never, "s", 26, maxw=hw - 44)
    y = top + bh9

    # ---------- example walk
    y += 74
    g.section(y, "EXAMPLE · ONE GST NOTICE, START TO FINISH")
    walk = [
        "1  the client forwards an ASMT-10: GSTR-3B vs 2B mismatch, reply within 30 days",
        "2  the brain files it under widget traders, puts 14 nov on the timeline, pulls the 2B match for that period",
        "3  it finds last year's position on the same supplier and the circular the firm cited then",
        "4  the draft reply and evidence list land in the manager's approval list · she changes two lines",
        "5  the partner says yes · it is filed from the firm's login · ARN and date land on the client timeline",
        "6  monday: the partner's memo shows 1 reply filed, 2 notices still open, follow-up due 28 nov",
    ]
    end = g.lines(L, y + 44, walk, "", 34, maxw=CW)

    # ---------- legend + footer
    fy = end + 24
    g.hr(fy, "rule-fg")
    ly = fy + 52
    items = [("bx-in", "what comes in"), ("bx-brain", "the brain"), ("bx-agent", "the agent"),
             ("bx-gate", "◆ a CA must say yes"), ("bx-ok", "⚓ a result"), ("bx-never", "✕ never")]
    x = L
    for cls, lab in items:
        g.rect(x, ly - 20, 36, 24, cls)
        g.text(x + 48, ly, lab, "s d")
        x += 48 + int(len(lab) * 9.6) + 44
    g.text(L, ly + 44, "↺ repeats · pages are markdown you can read without the brain · the brain is memory, the CA is judgment", "s d")
    g.text(R, ly + 44, "ca firm · brain map", "s d", "end")
    h = ly + 90

    for w_ in g.warn:
        print("WARN", w_)
    title = "A CA firm on one brain"
    html = HEAD.format(title=title, w=W, h=h) + "\n".join(g.out) + "\n" + TAIL
    (HERE / "01-ca-firm-brain.html").write_text(html, encoding="utf-8")
    print("wrote 01-ca-firm-brain.html", W, "x", h)


if __name__ == "__main__":
    poster()
