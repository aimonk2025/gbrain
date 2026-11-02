# Compliance calendar (pack default)

The firm's live copy lives in the brain at `finance/compliance-calendar`. That
page wins. Edit it at the start of every financial year and after any
notification that moves a date. `ca-return-cycle` reads it to spawn jobs.

Dates below are the standard statutory due dates as of the pack date. They are
a starting point, not a source. Verify each one against the current law page
under `concepts/law/` before relying on it. Extensions happen; the brain must
record them as dated timeline entries on this page, never by silently editing
the table.

| Job | Period | Due | Applies to | Lead time (days before due the job opens) |
|---|---|---|---|---|
| GSTR-1 | monthly | 11th of next month | GST clients on monthly filing | 10 |
| GSTR-1 (QRMP) / IFF | quarterly | 13th of month after quarter | GST clients on QRMP | 12 |
| GSTR-3B | monthly | 20th of next month | GST clients on monthly filing | 15 |
| GSTR-3B (QRMP) | quarterly | 22nd or 24th of month after quarter, by state | QRMP clients | 15 |
| TDS deposit | monthly | 7th of next month (30 Apr for March) | deductors | 5 |
| TDS return (24Q, 26Q, 27Q) | quarterly | 31 Jul, 31 Oct, 31 Jan, 31 May | deductors | 20 |
| TDS certificates (Form 16, 16A) | quarterly/annual | 15 days after return due (Form 16: 15 Jun) | deductors | 10 |
| Advance tax | quarterly | 15 Jun, 15 Sep, 15 Dec, 15 Mar | taxpayers above the threshold | 10 |
| ITR, non-audit | annual | 31 Jul | individuals, firms not under audit | 45 |
| Tax audit report (3CA/3CB-3CD) | annual | 30 Sep | audit cases | 60 |
| ITR, audit cases | annual | 31 Oct | audit cases | 30 |
| ITR, transfer pricing cases | annual | 30 Nov | TP cases | 30 |
| GSTR-9 / 9C | annual | 31 Dec | turnover above the threshold | 45 |
| AOC-4 | annual | 30 days from AGM | companies | 20 |
| MGT-7 / MGT-7A | annual | 60 days from AGM | companies | 20 |
| DIR-3 KYC | annual | 30 Sep | every DIN holder | 20 |
| LLP Form 11 | annual | 30 May | LLPs | 20 |
| LLP Form 8 | annual | 30 Oct | LLPs | 20 |
| PT, PF, ESI | monthly | per state / 15th | employers, by registration | 5 |

## How the calendar is used

- `ca-return-cycle` opens one job page per client per row where the client's
  `services` list includes the job and the period applies.
- The job's `due` is the calendar date. The job opens `lead time` days before.
- A date change is recorded as a timeline entry on `finance/compliance-calendar`
  with its source (the notification or circular page), then the table is edited.
- If a row's law page under `concepts/law/` is missing or older than 12 months,
  the skill flags the row at the gate before relying on it.
