# Folder schema for a CA firm's brain

One primary home per fact. The folder decides the page type. Slugs are
lowercase, hyphenated, stable.

> **Filing rule:** see [skills/_brain-filing-rules.md](../_brain-filing-rules.md).

| Folder | One page per | Slug pattern | Holds |
|---|---|---|---|
| `companies/` | client entity (company, LLP, firm, trust, proprietor) | `companies/<client>` | master data, services, fees, contacts, risk, positions, open items, docs index, timeline |
| `people/` | person: promoter, director, CFO, client accountant, assessing officer, our own staff | `people/<name>` | role, which clients, how to reach, what they handle, timeline |
| `projects/` | engagement or recurring job | `projects/<client>-<service>-<period>` or `projects/<client>-<engagement>-<fy>` | owner, reviewer, due, status, checklist progress, open items, template, fee, timeline |
| `projects/notices/` | one notice | `projects/notices/<client>-<form>-<yyyy-mm-dd>` | notice facts, deadline, context, draft, filing record |
| `tasks/` | one open item | `tasks/<client>-<short>` | owner, due, status, which job it belongs to |
| `concepts/law/` | section, rule, circular, notification | `concepts/law/<act>-<ref>` | text summary, source, date checked, what it affects |
| `concepts/positions/` | one firm position | `concepts/positions/<topic>` | the stand, scope, basis, approver, date, clients where applied, superseded-by |
| `concepts/sops/` | one procedure | `concepts/sops/<name>` | steps, who, what proves done |
| `concepts/checklists/` | one job type | `concepts/checklists/<service>` | the firm's edited copy of the pack checklist |
| `concepts/lessons/` | one correction a CA made | `concepts/lessons/<yyyy-mm-dd>-<short>` | what was wrong, what is right, which template or position it changed |
| `templates/` | one template | `templates/<name>` | the firm's edited copy, with version, use, owner, last_reviewed |
| `strategy/` | partner-only pages | `strategy/<name>` | goals, pricing, profitability, capacity, client tiers, decisions, referrals |
| `finance/` | rates and calendars | `finance/compliance-calendar`, `finance/rates-<fy>` | the firm's edited calendar, rate tables, fee bands |
| `meetings/` | one call or visit | `meetings/<yyyy-mm-dd>-<client>` | who, decisions, actions |
| `sources/` | one raw file or export | `sources/<yyyy-mm-dd>-<client>-<what>` | the raw notice, return, statement, export · never edited |
| `reports/` | one generated report | `reports/<category>/<yyyy-mm-dd-hhmm>[-<who>]` | Monday memos, due lists, fee reviews, position impact notes |
| `inbox/` | anything the rules cannot place | `inbox/<yyyy-mm-dd>-<short>` | a signal the schema needs a new home |

## Client page shape (companies/<client>.md)

```markdown
---
type: company
pan: <entity PAN>
gstin: <GSTIN or none>
tan: <TAN or none>
cin: <CIN/LLPIN or none>
fy: apr-mar
registrations: [gst, tds, msme]
books: tally-prime | zoho-books | excel
services: [gstr-1, gstr-3b, tds-q, itr, statutory-audit]
fee_terms: "18,000/month retainer + audit 60,000 · billed quarterly"
risk_tier: A | B | C
partner: people/<partner>
manager: people/<manager>
---
# <Client name>

## What is true now
- services, fee terms, risk notes, payment habit, with [Source: ...]
- contacts: [owner](people/<slug>) · [accounts](people/<slug>)
- positions applied: [itc-2b-basis](concepts/positions/itc-2b-basis)
- open: notices, engagements, documents awaited
- documents: engagement letter version and date · DSC custody till <date>

<!-- timeline -->
## Timeline
- **YYYY-MM-DD** | <event> · [Source: ...]
```

The top is compiled truth. The bottom is dated history. The sentinel
`<!-- timeline -->` separates them; the brain needs it to split the page.

## Job page shape (projects/<client>-<service>-<period>.md)

```markdown
---
type: project
client: companies/<client>
service: gstr-3b
period: 2026-09
owner: people/<article>
reviewer: people/<manager>
due: 2026-10-20
status: open | docs-awaited | in-progress | in-review | approved | filed | billed
checklist: concepts/checklists/gstr-3b
template: templates/client-query-gst
fee: in-retainer | <amount>
---
# <Client> · GSTR-3B · Sep 2026

## Checklist
- [x] books received (2026-10-15) [Source: email from P Iyer, 2026-10-15]
- [ ] 2B vs books match run
...

## Open items
- 2 purchase bills not in 2B · query sent 2026-10-16 · awaiting client

<!-- timeline -->
## Timeline
- **2026-10-15** | books received · 2B pulled
```

Status moves forward only. `filed` requires an ARN or acknowledgement number
on the timeline. `billed` requires an invoice reference.
