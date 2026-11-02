---
name: ca-return-cycle
version: 1.0.0
description: |
  Run the recurring compliance cycle for a CA firm: open one job page per client
  per period from the compliance calendar, copy the checklist, build the morning
  due list by owner, move status forward only, stop at the reviewer gate, record
  the ARN or acknowledgement on the client timeline, add the billing note and
  capture lessons. Covers GST, TDS, ITR, ROC and any row the calendar defines.
triggers:
  - "run this month's returns"
  - "open the return jobs"
  - "return cycle"
  - "due list"
  - "what is late"
  - "mark filed"
tools:
  - search
  - list_pages
  - get_page
  - put_page
  - add_timeline_entry
  - get_timeline
  - submit_job
mutating: true
---

# CA Return Cycle

> **Filing rule:** see [skills/_brain-filing-rules.md](../_brain-filing-rules.md).
> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).

Read before starting: `skills/ca-pack/never-rules.md`,
`skills/ca-pack/folder-schema.md`, the firm's calendar at
`finance/compliance-calendar` (fallback `skills/ca-pack/compliance-calendar.md`),
and the checklist for the service (`concepts/checklists/<service>` in the brain,
fallback `skills/ca-pack/checklists/<service>.md`).

## Contract

This skill guarantees:
- One job page per client per calendar row per period, slug
  `projects/<client>-<service>-<period>`, never a duplicate
- The job opens `lead time` days before due, with the checklist copied in at
  open time and a `due` taken from the calendar, not guessed
- A morning due list per owner: due, waiting on client, late, with job links
- Status moves forward only: open → docs-awaited → in-progress → in-review →
  approved → filed → billed
- `filed` only with an ARN, acknowledgement, token or SRN recorded on the
  client timeline, entered by a person
- A billing note on every filed job
- A lesson page for every reviewer change
- The brain never files anything

## Phases

### Phase 1: Spawn (nightly, or on "open the return jobs")
1. Read the calendar. For each row, compute the periods whose open date
   (`due` minus `lead time`) is today or earlier and whose job does not exist.
2. `list_pages` under `companies/`. For each client whose `services:` includes
   the row's job and whose registration type matches the row, create the job
   page in the schema's job page shape. `owner` and `reviewer` default from
   the client page's manager and partner; the firm can override in
   `strategy/capacity` if that page exists.
3. Copy the checklist into the job page. Add a timeline entry on the client
   page: `- **YYYY-MM-DD** | <service> <period> job opened · due <date>`.
4. If a calendar row's law page is missing or older than 12 months, write
   `calendar row unverified` on each job it spawns and list it in the output.
5. If the brain runs a job queue, `submit_job` the spawn as a nightly job so
   it is idempotent and logged; otherwise run inline.

### Phase 2: Morning due list (every morning, or on "due list")
1. `list_pages` under `projects/` with status not in `filed`, `billed`.
2. Group by owner. Within each: late (due < today), due this week, waiting on
   client (status `docs-awaited` with the date it went there), the rest by due.
3. Write to `reports/due-list/<YYYY-MM-DD-HHMM>.md` and return the list.
   One line per job: due date, client, service, status, days waiting, link.

### Phase 3: Work the job
1. Each checklist step is ticked only with its proof linked on the job page.
   Status changes when the step that defines it is proven: documents in
   `sources/` → `in-progress`; draft and workings in `sources/` → `in-review`.
2. Open items that need the client go out via `ca-template-fill` with
   `templates/client-query-gst` or `templates/document-request`, at the
   manager gate. Status → `docs-awaited` with the date.
3. Where a step applies a firm position, call `ca-position-check` and link
   the position page. If none exists, flag at the gate.

### Phase 4: Review gate
1. ◆ The reviewer reads the job page: checklist complete with proofs, every
   figure in the workings sourced, open items listed. `yes` → status
   `approved` with reviewer and timestamp on the timeline. `change it` → back
   to `in-progress` with the change noted. `no` → stays, with reason.
2. Changes the reviewer made are written to `concepts/lessons/<date>-<short>`
   and linked from the job.

### Phase 5: Filed and billed
1. A person files from the firm's login. On "mark filed <job> <ARN>": record
   `- **YYYY-MM-DD** | <service> <period> filed · ARN <number>` on the client
   timeline and the job timeline, status → `filed`. Without a number, refuse
   and say what is missing.
2. Billing note: `in-retainer` or an amount and the invoice cycle. If the fee
   is outside the retainer and unknown, `fee: not in the brain` and flag.
3. Follow-on jobs the row defines (certificates after a TDS return, e-verify
   after ITR) are opened now with their own due dates.

### Phase 6: Period close
On the last day of the month, list every job of the month by status and write
`reports/return-cycle/<YYYY-MM>.md`: filed on time, filed late with days,
still open with reason, calendar rows unverified.

## Output Format

Spawn:
```
Return cycle: <n> jobs opened for <period>
  <service>: <n> clients · due <date> · <n> unverified calendar rows
  skipped: <n> already open
```

Due list:
```
Due list <date>
<owner>
  LATE   <due>  <client> · <service> <period> · <status> · <link>
  WEEK   <due>  ...
  WAIT   <since> <client> · <service> · waiting <n> days · <link>
```

Mark filed:
```
Filed: <client> · <service> <period> · ARN <number> · recorded on client timeline
  billing: in retainer | <amount>
  follow-on: <job slug> due <date>
```

## Anti-Patterns

- Opening a job with a due date typed by hand instead of read from the calendar
- Two job pages for the same client, service and period
- Ticking a checklist step without its proof linked
- Moving status backwards, or to `filed` without an ARN
- Filing, uploading or sending anything itself
- Marking late items as "in progress" to clean up the list
- Dropping a reviewer's change without writing the lesson

## Tools Used

- `list_pages`: clients and open jobs
- `get_page` / `put_page`: calendar, checklist, job pages, reports
- `add_timeline_entry` / `get_timeline`: open, approved, filed, billed events
- `submit_job`: the nightly spawn when a job queue is available
- `search`: find an existing job before creating one
