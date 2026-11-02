---
name: ca-notice-reply
version: 1.0.0
description: |
  Handle a notice from any department (GST, income-tax, TDS, MCA, PF) for a CA
  firm's client: store the raw notice, compute the deadline, build the
  point-wise facts, positions, law and evidence, draft the reply from the
  template with every figure sourced, stop at manager then partner gates,
  record the filing and the follow-up, and update positions and lessons.
triggers:
  - "notice received"
  - "reply to this notice"
  - "show cause notice"
  - "demand notice"
  - "ASMT-10"
  - "143(1)"
  - "assessment notice"
tools:
  - search
  - query
  - get_page
  - put_page
  - add_timeline_entry
  - traverse_graph
  - file_upload
mutating: true
---

# CA Notice Reply

> **Filing rule:** see [skills/_brain-filing-rules.md](../_brain-filing-rules.md).
> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).

Read before starting: `skills/ca-pack/never-rules.md`,
`skills/ca-pack/folder-schema.md`, `skills/ca-pack/checklists/notice-reply.md`,
and the template `templates/notice-reply` (fallback
`skills/ca-pack/templates/notice-reply.md`).

## Contract

This skill guarantees:
- The raw notice stored in `sources/` before anything else is written
- One job page `projects/notices/<client>-<form>-<yyyy-mm-dd>` with form,
  section, period, reference number, issuing office, issue and service dates
- The deadline computed from the service date and the notice wording, with a
  task three working days earlier, and the partner told if fewer than five
  working days remain
- A points table: every claim in the notice as a row with amount, facts,
  position, law, evidence and status
- A draft reply with every figure sourced and every open point marked
  `not in the brain`; no invented section, circular or figure
- Two gates: manager, then partner. Nothing filed or sent by the brain
- Filing recorded with ARN or acknowledgement on the client timeline, a
  follow-up task for the hearing or response window
- Position pages and lessons updated when the reply took a stand

## Phases

### Phase 1: Intake
1. `file_upload` the notice to `sources/<yyyy-mm-dd>-<client>-<form>`.
2. Create the job page. Frontmatter: `client`, `department`, `form`,
   `section`, `period`, `reference` (DIN or notice number), `issuing_office`,
   `issued_on`, `served_on`, `due`, `owner`, `reviewer`, `partner`, `status`.
3. Deadline: count from `served_on` per the notice's own words (days or a
   named date). Write the computation on the page. Open `tasks/<client>-notice-
   reply` with due = deadline minus three working days. If fewer than five
   working days remain, put `URGENT` first in the output and on the task.
4. Timeline on the client page: `- **<served_on>** | <form> received · <ref>
   · reply due <date>`. The CA informs the client; record the acknowledgement
   date when given.

### Phase 2: Points table
1. Read the notice. One row per point the department makes: claim, period,
   amount demanded or proposed, provision cited by the department.
2. For each row, in order:
   - Facts: `get_page` the client page, `get_timeline` for the period,
     `search` past returns, workings and prior replies in `sources/` and
     `projects/notices/`. Each fact gets a `[Source: ...]`.
   - Position: call `ca-position-check` for the topic. Link the position page
     or write `no firm position recorded` and flag.
   - Law: `search` `concepts/law/` for the sections and circulars involved.
     Link each with its `last checked` date. If a law page is missing or older
     than 12 months, write `law page missing or stale` and flag. Do not quote
     law from memory into the draft.
   - Evidence: list every document the response relies on, each as a link to
     `sources/`. A document not on file is an open item with an owner.
3. Status per row: `ready`, `open: <what is missing>`.

### Phase 3: Draft
1. Call `ca-template-fill` with `templates/notice-reply`. The
   `points_and_replies` field is built from the table: for each row, the
   department's point, the facts with sources, the legal position with the
   provision, the submission. Open rows render as
   `[not in the brain: <what is missing>]` in the draft, never as a guess.
2. `evidence_list` is the evidence table. `prayer` comes from the firm's
   position page or the partner; if neither, `not in the brain`.
3. Save the draft as a file in `sources/` linked from the job page. Status →
   `in-review`.

### Phase 4: Gates
1. ◆ Manager: reads the points table and the draft. `yes` → status
   `partner-review`. `change it` → changes noted, back to draft.
2. ◆ Partner: `yes` → `approved`, timeline line with name and time. Both lines
   must exist before step 5.
3. Any change at either gate becomes a lesson page and, where it is a stand,
   a position page update via `ca-position-check`.

### Phase 5: Filed and followed up
1. A person files on the portal or dispatches the reply. On "mark filed <job>
   <ARN or acknowledgement>": record it on the client and job timelines,
   status → `filed`. Without a number or dispatch proof, refuse.
2. Open `tasks/<client>-notice-followup` for the hearing date if given, else
   for the department's response window from the notice or 30 days.
3. If the reply took a stand not yet recorded, draft the position page from
   `skills/ca-pack/positions-template.md` for the partner's approval.

## Output Format

```
Notice: <client> · <form> <ref> · served <date> · reply due <date> (<n> working days) [URGENT]
  job: projects/notices/<slug> · task: tasks/<slug>
  points: <n> total · <n> ready · <n> open
    1. <claim> · <amount> · position: <slug | none recorded> · law: <n> pages (<n> stale) · evidence: <n>/<n> on file
  draft: sources/<file> · gaps: <list of not-in-the-brain items>
  gate: awaiting manager | awaiting partner | approved by <name> <date>
```

After filing:
```
Filed: <client> · <form> <ref> · ARN <number> · follow-up task due <date>
  positions updated: <list | none> · lessons: <list | none>
```

## Anti-Patterns

- Drafting before the raw notice is in `sources/` and the deadline is on a task
- Computing the deadline from the issue date when the notice counts from service
- Quoting a section, rule or circular that has no page under `concepts/law/`
- Stating the firm's position without a dated, approved position page
- Filling a gap with a plausible figure or a "typical" reply paragraph
- Sending or filing the reply, or marking it filed without the number
- Treating a reply as done without the follow-up task

## Tools Used

- `file_upload`: the raw notice, the draft, the evidence
- `get_page` / `put_page`: job page, client page, position pages, lessons
- `search` / `query`: past replies, returns, law pages, workings
- `get_timeline`: the client's history for the period
- `traverse_graph`: other clients affected by the same issue when a position changes
- `add_timeline_entry`: received, approved, filed, follow-up
