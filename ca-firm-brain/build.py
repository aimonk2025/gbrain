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
    g.text(R, 96, "built on gbrain · open source, MIT", "s d", "end")
    g.text(L, 140, "clients, work, knowledge, templates and strategy in one memory an agent can read and write,", "sub")
    g.text(L, 170, "so no due date, position, template version or client fact depends on one person remembering", "sub")
    g.hr(204, "rule-fg")

    # ---------- 01 the system
    y = 262
    g.section(y, "01 / THE SYSTEM", "you speak plainly · the agent reads its skills · the brain keeps the facts")
    bw, gap, bh = 340, 33, 160
    top = y + 36
    sysb = [
        ("YOU", "partner · manager · article", ["forward, ask, assign,", "review, say yes or no"], "bx", ""),
        ("THE AGENT", "reads skill files first", ["drafts, files pages, fills", "templates · never sends alone"], "bx-agent", "agent"),
        ("THE BRAIN", "pages + graph + timeline", ["hybrid search over markdown", "typed links made on save"], "bx-brain", "brain"),
        ("YOUR TOOLS", "email · portals · tally · dms", ["a person presses send,", "files, pays · not the brain"], "bx", ""),
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

    # ---------- 02 what powers it: gbrain
    y += 74
    g.section(y, "02 / WHAT POWERS IT · GBRAIN", "the engine under the poster · every item below is a shipped command or module")
    fw, fg_, fh = (CW - 60) // 3, 30, 266
    feats = [
        ("ENGINES + STORAGE", "pglite · postgres + pgvector",
         ["· PGLite: embedded Postgres in one file, no server",
          "· Postgres + pgvector for scale: Supabase or own",
          "· gbrain migrate --to supabase | pglite, both ways",
          "· markdown is the source of truth, DB is the index",
          "· page versions kept · gbrain revert to any one",
          "· raw data store for exports, files, attachments",
          "· S3, Supabase Storage or local disk for files"], "bx-brain"),
        ("SEARCH", "hybrid · graph-aware · measurable",
         ["· keyword + vector fused by reciprocal rank fusion",
          "· intent classifier: entity, time, event, general",
          "· multi-query expansion, backlink boost, dedup",
          "· keyword-only mode needs no API key at all",
          "· gbrain eval: precision, recall, MRR, nDCG on",
          "  your own 20 questions, A/B two configs",
          "· published benchmark: recall@5 83% to 95%"], "bx-brain"),
        ("KNOWLEDGE GRAPH", "typed links · timeline · zero LLM",
         ["· every page save extracts links: works_at,",
          "  advises, attended, source, mentions, founded",
          "· dated timeline entries per company and person",
          "· gbrain graph-query <slug> --depth 2 --type T",
          "· gbrain orphans: pages nobody links to",
          "· backlink checker and fixer, dead-link audit",
          "· gbrain extract links|timeline over fs or db"], "bx-brain"),
        ("AGENT SURFACE", "one contract · cli + mcp · 26 skills",
         ["· 41 operations defined once, CLI and MCP",
          "  server both generated from that contract",
          "· MCP over stdio for Claude Code, Cursor, any",
          "  client · remote MCP with bearer tokens",
          "· 26 skills: brain-ops, query, enrich, meeting-",
          "  ingestion, citation-fixer, maintain, reports,",
          "  cron-scheduler, data-research, soul-audit"], "bx-agent"),
        ("INGESTION", "files · folders · audio · recipes",
         ["· gbrain import <dir> with resume and workers",
          "· live sync: a watched folder stays indexed",
          "· 3-tier chunking: recursive, semantic, LLM-guided",
          "· audio transcription: Groq Whisper or OpenAI",
          "· recipes: email, calendar, meetings, X, voice",
          "· file upload with path confinement for agents",
          "· data-research: YAML recipe, email to tracker"], "bx-in"),
        ("OPERATIONS", "runs itself · checks itself",
         ["· gbrain autopilot --install: sync, extract, embed",
          "· Minions job queue: retries, backoff, timeouts,",
          "  parent-child fan-out, stall rescue, idempotency",
          "· gbrain doctor --fix: health checks, auto-repair",
          "· brain score 0-100: embeds, links, time, orphans",
          "· gbrain upgrade with migrations + a repair trail",
          "· lint, publish --password (encrypted HTML page)"], "bx-agent"),
    ]
    top = y + 36
    for i, (name, sub, det, cls) in enumerate(feats):
        row, col = divmod(i, 3)
        x = L + col * (fw + fg_)
        yy = top + row * (fh + 22)
        g.rect(x, yy, fw, fh, cls)
        g.text(x + 20, yy + 38, name, "h", maxw=fw - 40)
        g.text(x + 20, yy + 62, sub, "s d", maxw=fw - 40)
        g.lines(x + 20, yy + 94, det, "xs", 22, maxw=fw - 40)
    y = top + 2 * fh + 22 + 40
    g.rect(L, y - 24, CW, 84, "ex")
    g.text(L + 22, y + 6, "gbrain init  ·  gbrain import ./brain  ·  gbrain query \"open notices this quarter\"  ·  gbrain graph-query widget-traders --depth 2", "s", maxw=CW - 44)
    g.text(L + 22, y + 36, "gbrain autopilot --install  ·  gbrain jobs submit  ·  gbrain doctor --fix  ·  gbrain eval  ·  gbrain serve  (MCP for the agent)", "s", maxw=CW - 44)
    y += 60

    # ---------- 03 what the brain holds: five domains
    y += 74
    g.section(y, "03 / WHAT THE BRAIN HOLDS", "five domains · one primary home per fact · the folder decides the page type")
    top = y + 36
    dw, dg, dh = 272, 25, 276
    domains = [
        ("CLIENTS", "companies/ · people/",
         ["· entity master: PAN, GSTIN,", "  FY, registrations", "· services engaged + fees", "· contacts and their roles",
          "· risk tier, history, notes", "· every notice, filing, call"], "bx-brain", "brain"),
        ("WORK", "projects/ · tasks/",
         ["· one page per engagement", "· recurring compliance jobs", "· tasks: owner, due, status",
          "· checklists ticked per job", "· review gates and sign-off", "· billing note when done"], "bx-agent", "agent"),
        ("KNOWLEDGE", "concepts/",
         ["· acts, rules, circulars", "· the firm's own positions", "· SOPs: how we do each job",
          "· checklists per service", "· past rulings relied on", "· lessons from corrections"], "bx-brain", "brain"),
        ("TEMPLATES", "templates/",
         ["· engagement letters", "· reply and representation", "  formats, audit reports",
          "· onboarding kits, MIS packs", "· one page per template:", "  version, use, owner"], "bx-brain", "brain"),
        ("STRATEGY", "strategy/ (partner only)",
         ["· firm goals, service mix", "· pricing + fee realisation", "· client profitability",
          "· staffing and capacity", "· growth and referral plan", "· decisions and why"], "bx-gate", "gate"),
    ]
    for i, (name, sub, body, cls, tc) in enumerate(domains):
        x = L + i * (dw + dg)
        g.rect(x, top, dw, dh, cls)
        g.text(x + 18, top + 40, name, f"h {tc}".strip(), maxw=dw - 36)
        g.text(x + 18, top + 66, sub, "s d", maxw=dw - 36)
        g.hr(top + 84, "rule", x + 18, x + dw - 18)
        g.lines(x + 18, top + 112, body, "xs", 24, maxw=dw - 36)
    y = top + dh + 34
    g.text(L, y, "also: meetings/ one page per call · finance/ rates and due-date calendars · sources/ raw files, never edited · inbox/ unplaced items", "s d", maxw=CW)
    g.text(L, y + 28, "companies, people, projects, concepts, meetings, finance and sources auto-link out of the box", "xs d", maxw=CW)
    g.text(L, y + 50, "tasks/, templates/ and strategy/ are the firm's own folders · one pattern line makes them link the same way", "xs d", maxw=CW)
    y += 50

    # ---------- 03 the client master
    y += 74
    g.section(y, "04 / THE CLIENT MASTER · ONE PAGE PER CLIENT", "top = true now · bottom = history")
    top = y + 36
    lw, rw, gp = 720, 700, 40
    bh3 = 426
    g.rect(L, top, lw, bh3, "bx-brain")
    g.text(L + 24, top + 40, "companies/widget-traders.md", "s b")
    page = [
        ("type: company · pan: XXXXX0000X · gstin: 27XXXXX0000X1Z5", "d"),
        ("fy: apr-mar · regd: gst, tds, msme · books: tally prime", "d"),
        ("services: gstr-1/3b monthly · tds quarterly · itr · audit", ""),
        ("fees: 18,000/month retainer + audit 60,000 · billed quarterly", ""),
        ("contacts: [owner](people/r-shah) · [accounts](people/p-iyer)", ""),
        ("risk: medium · late documents in q4 · pays within 30 days", ""),
        ("position: ITC claimed on 2B basis since FY24", ""),
        ("open: ASMT-10 reply due 14 nov · audit FY25-26 fieldwork", ""),
        ("docs: engagement letter v3 (2026) · dsc with firm till mar", ""),
        ("<!-- timeline -->", "d"),
        ("2026-10-28  ASMT-10 received · sources/notice-2026-10-28", ""),
        ("2026-10-20  GSTR-3B sep filed · ARN saved · invoice raised", ""),
    ]
    yy = top + 74
    for s_, c in page:
        g.text(L + 24, yy, s_, f"s {c}".strip(), maxw=lw - 48)
        yy += 26
    g.hr(top + 380, "rule", L + 24, L + lw - 24)
    g.text(L + 24, top + 406, "numbers come from your billing and books exports · the brain links them", "xs d", maxw=lw - 48)

    rx = L + lw + gp
    g.rect(rx, top, rw, bh3, "bx-brain")
    g.text(rx + 24, top + 40, "WHAT HANGS OFF THE CLIENT PAGE", "lab")
    hang = [
        "people/r-shah · people/p-iyer        who we talk to, about what",
        "projects/wt-gstr3b-2026-10           this month's return job",
        "projects/wt-audit-fy25-26            the audit engagement",
        "projects/wt-asmt10-reply             the notice reply",
        "templates/engagement-letter          v3 · signed 2026-04",
        "concepts/positions/itc-2b-basis      the stand we take",
        "meetings/2026-10-30-widget-traders   last call, decisions",
        "sources/notice-2026-10-28.pdf        the raw notice",
        "tasks/wt-*                           open items by owner",
    ]
    g.lines(rx + 24, top + 76, hang, "s", 27, maxw=rw - 48)
    g.hr(top + 380, "rule", rx + 24, rx + rw - 24)
    g.text(rx + 24, top + 406, "every link above is a typed edge · ask the graph, not a folder search", "xs d", maxw=rw - 48)
    y = top + bh3

    # ---------- 04 the work engine
    y += 74
    g.section(y, "05 / THE WORK ENGINE", "recurring compliance + one-off engagements + tasks · the morning list is built from this")
    top = y + 36
    bh4 = 420
    g.rect(L, top, lw, bh4, "bx-agent")
    g.text(L + 24, top + 40, "THE COMPLIANCE CALENDAR · finance/calendar.md", "lab")
    cal = [
        ("GSTR-1", "11th monthly", "every GST client"),
        ("GSTR-3B", "20th monthly", "every GST client"),
        ("TDS deposit", "7th monthly", "deductors"),
        ("TDS return", "31 jul · oct · jan · may", "deductors"),
        ("advance tax", "15 jun · sep · dec · mar", "taxpayers above limit"),
        ("tax audit", "30 sep", "audit cases"),
        ("ITR", "31 jul · 31 oct (audit)", "all"),
        ("GSTR-9 / 9C", "31 dec", "turnover above limit"),
        ("AOC-4 · MGT-7", "30 · 60 days from AGM", "companies"),
    ]
    yy = top + 76
    for a, b, c in cal:
        g.text(L + 24, yy, a, "s b", maxw=170)
        g.text(L + 214, yy, b, "s", maxw=270)
        g.text(L + 494, yy, c, "s d", maxw=lw - 518)
        yy += 27
    g.hr(top + 336, "rule", L + 24, L + lw - 24)
    g.lines(L + 24, top + 362, ["dates live on one page you edit when the law changes · the brain",
                                "spawns one job per client per cycle and puts it on the timeline"], "xs d", 22, maxw=lw - 48)

    g.rect(rx, top, rw, bh4, "bx-agent")
    g.text(rx + 24, top + 40, "ONE JOB · projects/wt-gstr3b-2026-10.md", "lab")
    job = [
        ("client: widget-traders · service: GSTR-3B · period: sep 2026", "d"),
        ("owner: article a · reviewer: manager m · due: 20 oct", ""),
        ("status: in review · started 12 oct · docs received 15 oct", ""),
        ("checklist: concepts/checklists/gstr3b (9 of 11 ticked)", ""),
        ("open: 2 purchase bills not in 2B · ask client", ""),
        ("template: templates/client-query-gst v2", ""),
        ("fee: in retainer · bill with quarter", ""),
        ("<!-- timeline -->", "d"),
        ("2026-10-15  books received · 2B pulled · match run", ""),
        ("2026-10-18  draft 3B ready · sent to reviewer ◆", ""),
    ]
    yy = top + 76
    for s_, c in job:
        g.text(rx + 24, yy, s_, f"s {c}".strip(), maxw=rw - 48)
        yy += 26
    g.hr(top + 336, "rule", rx + 24, rx + rw - 24)
    g.lines(rx + 24, top + 362, ["views the brain gives you: by client · by staff · by service line",
                                 "· by due date · what is late · what is waiting on the client"], "xs d", 22, maxw=rw - 48)
    y = top + bh4

    # ---------- 05 knowledge + template strategy
    y += 74
    g.section(y, "06 / KNOWLEDGE + TEMPLATE STRATEGY", "the firm's way of working, written once, used by every job")
    top = y + 36
    bh5 = 330
    g.rect(L, top, lw, bh5, "bx-brain")
    g.text(L + 24, top + 40, "KNOWLEDGE · concepts/", "lab")
    kn = [
        "law/         sections, rules, circulars · with source + date checked",
        "positions/   the stand we take, when, why · who approved it",
        "sops/        how we onboard, run an audit, reply to a notice",
        "checklists/  per service: GSTR-3B, TDS, ITR, audit, ROC",
        "lessons/     every correction a CA makes becomes a line here",
        "",
        "a page says 'not covered' when the firm has no position yet",
        "stale check: anything older than its review date is flagged",
    ]
    g.lines(L + 24, top + 76, kn, "s", 27, maxw=lw - 48)
    g.text(L + 24, top + 308, "the agent reads these before drafting · the draft cites the page it used", "xs d", maxw=lw - 48)

    g.rect(rx, top, rw, bh5, "bx-brain")
    g.text(rx + 24, top + 40, "TEMPLATES · templates/ · one page per template", "lab")
    tp = [
        "engagement-letter      v3 · use: new client · owner: partner",
        "client-query-gst       v2 · use: 2B mismatch · owner: manager",
        "asmt-10-reply          v4 · use: 3B vs 2B notice · reviewed sep",
        "audit-report-pvt       v6 · use: pvt ltd audit · reviewed apr",
        "representation-letter  v2 · use: every audit · owner: partner",
        "monthly-mis            v1 · use: retainer clients · owner: m",
        "",
        "the agent fills a template from the client page, never by hand",
    ]
    g.lines(rx + 24, top + 76, tp, "s", 27, maxw=rw - 48)
    g.text(rx + 24, top + 308, "a change a CA makes twice becomes the next version · usage logs on the client", "xs d", maxw=rw - 48)
    y = top + bh5

    # ---------- 06 strategy and the partner view
    y += 74
    g.section(y, "07 / STRATEGY · THE PARTNER VIEW", "the private layer · reads everything, is read by no one else")
    top = y + 36
    bh6 = 290
    g.rect(L, top, lw, bh6, "bx-gate")
    g.text(L + 24, top + 40, "STRATEGY PAGES · strategy/", "lab gate")
    st = [
        "goals-2026        revenue, service mix, clients to add or drop",
        "pricing           retainer bands, hourly floor, scope rules",
        "profitability     fees vs hours per client · from your billing export",
        "capacity          who is loaded when · season plan · hiring",
        "client-tiers      A/B/C by fee, risk, payment habit",
        "decisions         what we decided, when, why · never deleted",
        "referrals         who sends work, who we send to",
    ]
    g.lines(L + 24, top + 76, st, "s", 27, maxw=lw - 48)
    g.text(L + 24, top + 272, "numbers are imported, not invented · every figure keeps its source file", "xs d", maxw=lw - 48)

    g.rect(rx, top, rw, bh6, "bx-gate")
    g.text(rx + 24, top + 40, "QUESTIONS THE PARTNER ASKS THE BRAIN", "lab gate")
    pq = [
        "· which clients take the most hours for the least fee?",
        "· who is overloaded in the september audit season?",
        "· which service line grew this year, which shrank?",
        "· which clients have an open notice or a late payment?",
        "· what did we decide about scope creep in march, and why?",
        "· which templates have not been reviewed in a year?",
        "· which positions do we take that a new circular affects?",
    ]
    g.lines(rx + 24, top + 76, pq, "s", 27, maxw=rw - 48)
    g.text(rx + 24, top + 272, "answers cite pages · the brain says 'not in the brain' instead of guessing", "xs d", maxw=rw - 48)
    y = top + bh6

    # ---------- 07 how work moves
    y += 74
    g.section(y, "08 / HOW ANY PIECE OF WORK MOVES", "a return, a notice, a new client, an advisory ask · same eight steps")
    steps = [
        ("1  WORK ARRIVES", ["return due · notice · ask", "new client · partner idea"], "bx-in"),
        ("2  FILED", ["under client + engagement", "owner, due date, status"], "bx-brain"),
        ("3  CONTEXT FOUND", ["client history + position", "law, SOP, past lessons"], "bx-brain"),
        ("4  TEMPLATE PULLED", ["the right version", "filled from the client page"], "bx-brain"),
        ("5  WORK PREPARED", ["draft, working, checklist", "every number shows source"], "bx-agent"),
        ("◆ 6 · A CA REVIEWS", ["yes · change it · no", "never files on its own"], "bx-gate"),
        ("⚓ 7  DONE + LOGGED", ["sent or filed by a person", "timeline + billing note"], "bx-ok"),
        ("↺ 8  REMEMBERED", ["lesson, template version,", "position, client note"], "bx-brain"),
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

    # ---------- 08 who sees what + where it runs
    y += 74
    g.section(y, "09 / WHO SEES WHAT · WHERE IT RUNS", "one brain per partner or practice group · separation is physical")
    top = y + 36
    tw = 900
    cols = ["", "strategy", "clients + work", "knowledge", "other groups"]
    cwid = [160, 180, 220, 190, 150]
    rows = [
        ["partner", "✓ read + change", "✓ read · approves", "✓ read + change", "✕"],
        ["manager", "✕", "✓ read · suggests", "✓ read · suggests", "✕"],
        ["article", "✕", "✓ read · drafts", "✓ read", "✕"],
        ["client", "✕", "what a CA sends", "✕", "✕"],
        ["outsider", "✕", "✕", "✕", "✕"],
    ]
    rh = 58
    th = rh * (len(rows) + 1)
    g.rect(L, top, tw, th, "bx")
    g.out.append(f'<rect x="{L}" y="{top}" width="{tw}" height="{rh}" class="thead"/>')
    for r, row in enumerate([cols] + rows):
        x = L
        for c, cell in enumerate(row):
            g.text(x + 16, top + r * rh + 36, cell, "lab" if r == 0 else ("s b" if c == 0 else "s"), maxw=cwid[c] - 20)
            x += cwid[c]
        if r:
            g.hr(top + r * rh, "rule", L, L + tw)

    wx = L + tw + 40
    ww = R - wx
    g.rect(wx, top, ww, th, "bx")
    g.text(wx + 22, top + 34, "WHERE IT RUNS", "lab")
    run = [
        ("start", "one file on a firm machine · no server"),
        ("grow", "postgres + pgvector on your own box or a"),
        ("", "managed DB in India · 1000+ files"),
        ("access", "no per-user locks inside one brain today,"),
        ("", "so one brain per partner, no shared keys,"),
        ("", "staff go through the agent, not a key"),
        ("data", "pages and the DB stay on the firm's server"),
        ("leaves", "chunk text to the embedding API (OpenAI),"),
        ("", "queries to a small model for expansion ·"),
        ("", "turn both off: keyword + graph, none out"),
    ]
    yy = top + 64
    for lab, body in run:
        if lab:
            g.text(wx + 22, yy, lab, "xs d")
        g.text(wx + 92, yy, body, "s", maxw=ww - 110)
        yy += 27
    y = top + th

    # ---------- 09 the rhythm
    y += 74
    g.section(y, "10 / THE RHYTHM", "scheduled jobs the brain runs for the firm")
    rhythm = [
        ("EVERY MORNING", "a due list per person: returns, replies, hearings, client docs awaited · what is late"),
        ("ALL DAY", "drafts and workings wait in one approval list: yes, change it or no"),
        ("EVERY NIGHT", "sync new files, extract links, embed, spawn next cycle's jobs, flag stale positions"),
        ("EVERY MONDAY", "one memo per partner: filings done, notices open, hours vs fees, fees to bill"),
        ("EVERY MONTH", "client profitability, template review list, health check: dead links, orphans, coverage"),
        ("EVERY QUARTER", "strategy review from the pages: goals vs actuals, capacity for next season, tiers"),
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

    # ---------- 10 rollout
    y += 74
    g.section(y, "11 / ROLLOUT IN FIVE STEPS", "one partner first · prove retrieval before adding clients")
    roll = [
        ("1 PILOT", ["one partner's clients", "local brain, the folders", "above, no server yet"]),
        ("2 SEED", ["client master from the", "tally, zoho and billing", "exports · one page each"]),
        ("3 LOAD", ["calendar, checklists,", "templates, positions and", "two years of history"]),
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

    # ---------- 11 not in the box + never
    y += 74
    g.section(y, "12 / NOT IN THE BOX · NON-NEGOTIABLES")
    top = y + 36
    hw = (CW - 40) // 2
    bh9 = 258
    g.rect(L, top, hw, bh9, "bx")
    g.text(L + 22, top + 36, "NOT IN THE BOX · BUILD IT OR KEEP YOUR TOOL", "lab")
    nib = [
        "· no tally, GST-portal or income-tax-portal connector:",
        "  small collectors drop exports into sources/ on a schedule",
        "· not a billing, time-sheet or document system: those stay,",
        "  the brain imports their exports and links the facts",
        "· no per-user access rules inside one brain: split brains",
        "· no local embedding model yet: semantic search uses the",
        "  OpenAI embedding API · keyword + graph mode needs nothing",
    ]
    g.lines(L + 22, top + 70, nib, "s", 26, maxw=hw - 44)

    nx = L + hw + 40
    g.rect(nx, top, hw, bh9, "bx-never")
    g.text(nx + 22, top + 36, "THE BRAIN NEVER", "lab never")
    never = [
        "✕ files a return or sends a reply without a CA's yes",
        "✕ invents a number, a section, a date or a fee",
        "✕ shows a figure without the source it came from",
        "✕ shares a login: one person, one key",
        "✕ lets client data leave the firm's server",
        "✕ keeps passwords, OTPs or DSC PINs in any page",
        "✕ answers from outside the brain without saying so",
    ]
    g.lines(nx + 22, top + 70, never, "s", 26, maxw=hw - 44)
    y = top + bh9

    # ---------- example walk
    y += 74
    g.section(y, "EXAMPLE · ONE MONTH FOR ONE CLIENT, START TO FINISH")
    walk = [
        "1  1 oct: the night job spawns widget traders' GSTR-3B job for september, owner article a, due 20 oct",
        "2  the morning list shows it · on 15 oct books arrive, the brain pulls 2B, runs the match, two bills are missing",
        "3  the agent fills client-query-gst v2 from the client page · the manager says yes · the client replies in a day",
        "4  the draft 3B and workings go to the manager ◆ · she changes one head · the partner files it from the firm login",
        "5  ARN, date and 'bill with quarter' land on the client timeline · the correction becomes a lesson line",
        "6  28 oct: an ASMT-10 arrives · filed under the client, template v4 pulled, last year's position found, reply due 14 nov",
        "7  monday memo: 1 return filed, 1 notice open, 11 hours on a retainer client this month, fee realisation flagged",
    ]
    end = g.lines(L, y + 44, walk, "", 34, maxw=CW)

    # ---------- legend + footer
    fy = end + 24
    g.hr(fy, "rule-fg")
    ly = fy + 52
    items = [("bx-in", "what comes in"), ("bx-brain", "the brain"), ("bx-agent", "the agent · work"),
             ("bx-gate", "◆ partner only · a CA must say yes"), ("bx-ok", "⚓ a result"), ("bx-never", "✕ never")]
    x = L
    for cls, lab in items:
        g.rect(x, ly - 20, 36, 24, cls)
        g.text(x + 48, ly, lab, "s d")
        x += 48 + int(len(lab) * 9.6) + 44
    g.text(L, ly + 44, "↺ repeats · pages are markdown you can read without gbrain · the brain is memory, the CA is judgment", "s d")
    g.text(R, ly + 74, "built on gbrain · github.com/garrytan/gbrain · MIT", "s d", "end")
    h = ly + 118

    for w_ in g.warn:
        print("WARN", w_)
    title = "A CA firm on one brain: the whole practice"
    html = HEAD.format(title=title, w=W, h=h) + "\n".join(g.out) + "\n" + TAIL
    (HERE / "01-ca-firm-brain.html").write_text(html, encoding="utf-8")
    print("wrote 01-ca-firm-brain.html", W, "x", h)


if __name__ == "__main__":
    poster()
