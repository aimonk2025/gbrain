---
name: ca-audit-file
version: 1.0.0
description: |
  Run an audit engagement's memory for a CA firm: engagement page, planning
  and requirement list, a workpaper index that points at the firm's document
  system, an issues log, representations, the reviewing partner's sign-off
  and the record of what was signed. The brain holds the index, the findings
  and the history; signed workpapers stay in the DMS.
triggers:
  - "start the audit"
  - "audit engagement"
  - "audit file"
  - "working papers index"
  - "issues log"
  - "management letter points"
tools:
  - search
  - get_page
  - put_page
  - add_timeline_entry
  - list_pages
  - file_upload
mutating: true
---

# CA Audit File

> **Filing rule:** see [skills/_brain-filing-rules.md](../_brain-filing-rules.md).
> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).

Read before starting: `skills/ca-pack/never-rules.md`,
`skills/ca-pack/folder-schema.md`, and for tax audits
`skills/ca-pack/checklists/tax-audit.md`. The firm's audit programme, if it has
one under `concepts/sops/audit-programme`, wins over the generic phases below.

## Contract

This skill guarantees:
- One engagement page `projects/<client>-audit-<fy>` with scope, team,
  dates, materiality as set by the partner, status
- A requirement list sent via `ca-template-fill` with
  `templates/document-request`, tracked item by item
- A workpaper index: one row per area with the DMS reference, preparer,
  reviewer, status. The brain never becomes the DMS
- An issues log: every finding with amount, area, evidence link, client
  response, resolution, and whether it goes to the management letter
- Representations obtained via the template before sign-off
- ◆ Reviewing partner sign-off recorded before anything is signed; the brain
  records UDIN and date after a person signs
- Timeline entries on the client page at start, fieldwork, sign-off

## Phases

### Phase 1: Engagement page
1. `search` for last year's engagement page. Carry forward: open points, prior
   issues, prior management letter, areas that needed the most time.
2. Create `projects/<client>-audit-<fy>`. Frontmatter: `client`,
   `audit_type` (statutory, tax, internal, other), `fy`, `partner`,
   `manager`, `team`, `planned_start`, `planned_signoff`, `materiality`
   (partner's number with date, else `not in the brain`), `status`.
3. Timeline on the client page: `audit <fy> started`.

### Phase 2: Planning and requirements
1. Build the requirement list from last year's list plus changes in the
   client page (new registrations, new services, open notices).
2. Send via `ca-template-fill` with `templates/document-request` at the
   manager gate. Track each item: requested, received (with `sources/` link),
   not applicable (with the client's note).
3. Risk notes: the partner's areas of focus, written with date and source.

### Phase 3: Workpaper index
1. One row per audit area: area, DMS reference (path or document id in the
   firm's document system), preparer, reviewer, status (open, prepared,
   reviewed), date.
2. The brain stores the index and findings. It does not store the signed
   workpapers; it links to where they live. A row without a DMS reference is
   not `prepared`.
3. For tax audits, the 3CD clause table from the checklist sits on the same
   page.

### Phase 4: Issues log
1. Every finding: area, description, amount, evidence (link to `sources/` or
   DMS reference), client response with date, resolution (adjusted, waived
   with reason, carried), management letter (yes or no).
2. Where a finding touches a firm position, call `ca-position-check` and link.
3. Issues with an amount above materiality are listed first and flagged to
   the partner the day they are logged.

### Phase 5: Representations and sign-off
1. `ca-template-fill` with `templates/representation-letter`; the
   `representations` field is built from the issues log and the standard set
   the firm keeps under `concepts/sops/`. Partner gate. Signed copy to
   `sources/` with a link.
2. ◆ Reviewing partner reads the index (all rows reviewed), the issues log
   (all resolved or carried with reason) and the representations. `yes` →
   status `approved-for-signing`, timeline line.
3. A person signs and generates the UDIN. On "signed <job> <UDIN> <date>":
   record both on the client and job timelines, status → `signed`. The brain
   never records a UDIN it was not given.

### Phase 6: Close
1. Management letter points compiled from the issues log into a draft via the
   firm's template if one exists, else a plain list for the partner.
2. Carry-forward list written for next year's engagement.
3. Lessons from reviewer changes to `concepts/lessons/`.

## Output Format

```
Audit: <client> · <type> <fy> · partner <name> · status <status>
  requirements: <n> received / <n> requested · <n> outstanding (oldest <n> days)
  workpapers: <n> reviewed / <n> prepared / <n> areas · <n> rows without DMS reference
  issues: <n> open · <n> above materiality · <n> for management letter
  representations: not yet | signed <date>
  sign-off: awaiting partner | approved <date> | signed · UDIN <number> <date>
```

## Anti-Patterns

- Storing signed workpapers in the brain instead of indexing the DMS
- Marking an area `prepared` with no DMS reference
- Setting materiality itself
- Logging a finding without its evidence link
- Closing an issue as "waived" without the reason and the partner's line
- Recording a UDIN or a signing date the person did not give
- Starting fieldwork without carrying forward last year's open points

## Tools Used

- `search` / `list_pages`: prior engagements, client history, positions
- `get_page` / `put_page`: engagement page, issues log, carry-forward
- `file_upload`: requirement replies, representation letter, evidence
- `add_timeline_entry`: started, fieldwork, approved, signed
