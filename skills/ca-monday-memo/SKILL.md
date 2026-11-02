---
name: ca-monday-memo
version: 1.0.0
description: |
  Write the Monday memo for each partner of a CA firm from the brain alone:
  filings done last week, notices open with due dates, late and waiting items,
  hours against fees where the billing export exists, fees to bill, templates
  and positions due for review, decisions waiting on the partner. Saved under
  reports/, one memo per partner, numbers only from pages.
triggers:
  - "monday memo"
  - "weekly memo"
  - "partner memo"
  - "weekly summary for the partner"
tools:
  - list_pages
  - get_page
  - put_page
  - get_timeline
  - search
  - get_stats
mutating: true
---

# CA Monday Memo

> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).
> **Reports:** save per [skills/reports/SKILL.md](../reports/SKILL.md) under `reports/monday-memo/`.

Read before starting: `skills/ca-pack/never-rules.md`. Runs Monday morning
by schedule, or on request. One memo per partner, covering that partner's
clients only (the client page's `partner:` field). In a one-partner brain,
one memo.

## Contract

This skill guarantees:
- Every number in the memo traces to a page, a timeline entry or an imported
  export in `sources/`; where the data is not in the brain the line says so
- Seven sections in a fixed order, each present even when empty
- Saved to `reports/monday-memo/<YYYY-MM-DD-HHMM>-<partner>.md` with the
  period covered in frontmatter
- Decisions waiting on the partner listed with the page that needs the answer
- Under one screen: at most 40 lines of body
- No recommendations the pages do not support

## Phases

### Phase 1: Scope
1. `list_pages` under `companies/` where `partner:` is this partner. Collect
   their open jobs under `projects/`, notices under `projects/notices/`, tasks.
2. Period: the previous Monday 00:00 to this Monday 00:00.

### Phase 2: Collect, section by section
1. **Filed last week.** Timeline entries in the period matching `filed ·`.
   Count by service; list late filings with days late.
2. **Notices open.** Notice jobs not `filed`: client, form, due date, days to
   due, gate status. `URGENT` first.
3. **Late and waiting.** From the due list logic in `ca-return-cycle`: late
   jobs with days late and owner; `docs-awaited` older than 7 days with the
   client and what is awaited.
4. **Hours vs fees.** If `sources/` holds a time or billing export for the
   period (the firm imports it; see `ca-fee-review`), show per-client hours,
   fee for the period, and the ratio, worst five first. If no export:
   `hours vs fees: no export imported for <period>`.
5. **Fees to bill.** Jobs `filed` with a billing note and no invoice reference;
   amounts where known, `in-retainer` counted separately.
6. **Review due.** Templates past `last_reviewed + review_every_days` within
   30 days; positions past `review_by` within 30 days; calendar rows whose
   law page is older than 12 months.
7. **Decisions waiting.** Pages with a gate awaiting this partner: engagement
   letters, notice drafts, audit sign-offs, fee proposals, positions awaiting
   approval, risk tiers not set. Each with its link.

### Phase 3: Write and save
1. Write the memo in the output format. Lines are facts with links, not prose.
2. Save under `reports/monday-memo/` with frontmatter `partner`,
   `period_from`, `period_to`, `generated_at`, `sources_missing` (list).
3. Return the memo. Do not send it anywhere; the partner's channel is the
   firm's choice and a person's action.

## Output Format

```markdown
---
type: report
category: monday-memo
partner: people/<partner>
period_from: YYYY-MM-DD
period_to: YYYY-MM-DD
generated_at: YYYY-MM-DDTHH:MM
sources_missing: [billing export <period>]
---
# Monday memo · <partner> · week of <date>

## Filed last week
- <n> returns filed: GSTR-3B <n>, TDS <n>, ITR <n> · late: <n> ([client](link) <n> days)

## Notices open
- URGENT [client](link) · <form> · due <date> (<n> working days) · awaiting partner

## Late and waiting
- LATE [client](link) · <service> <period> · <n> days · owner <name>
- WAIT [client](link) · books for <period> · <n> days

## Hours vs fees (<period>)
- [client](link) · <hours> h · <fee> · <ratio> h per 1,000
- or: no export imported for <period>

## Fees to bill
- [client](link) · <service> <period> · <amount> · filed <date>

## Review due
- template <name> v<n> · owner <name> · due <date>
- position <topic> · review by <date>

## Decisions waiting on you
- [page](link) · what is needed · since <date>
```

## Anti-Patterns

- Estimating hours, fees or ratios when no export is imported
- Dropping an empty section instead of showing it empty
- Including another partner's clients
- Writing advice or praise; the memo reports
- Sending the memo
- Exceeding one screen because every item was listed instead of the top ones with a count

## Tools Used

- `list_pages`: clients, jobs, notices, tasks, templates, positions
- `get_timeline`: filed, approved and waiting events in the period
- `get_page` / `put_page`: pages read, memo written
- `search`: billing and time exports in `sources/`
- `get_stats`: brain health line if the firm wants it in the memo
