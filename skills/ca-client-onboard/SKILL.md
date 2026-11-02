---
name: ca-client-onboard
version: 1.0.0
description: |
  Bring a new client into a CA firm's brain: conflict check, client master page,
  contact pages, services mapped to the compliance calendar, engagement letter
  draft at the partner gate, and the first recurring job pages. A client is not
  onboarded until the engagement letter is signed and the first jobs exist.
triggers:
  - "new client"
  - "onboard client"
  - "add a client"
  - "client onboarding"
tools:
  - search
  - get_page
  - put_page
  - add_link
  - add_timeline_entry
  - file_upload
mutating: true
---

# CA Client Onboard

> **Filing rule:** see [skills/_brain-filing-rules.md](../_brain-filing-rules.md).
> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).

Read before starting, in this order: `skills/ca-pack/never-rules.md`,
`skills/ca-pack/folder-schema.md`, `skills/ca-pack/compliance-calendar.md`
(or the firm's copy at `finance/compliance-calendar`), and
`skills/ca-pack/checklists/client-onboarding.md`.

## Contract

This skill guarantees:
- A conflict check across the brain before any page is written
- One client page under `companies/` in the schema's client page shape, every
  field either sourced or marked `not in the brain`
- One people page per named contact, linked both ways
- Every agreed service mapped to a calendar row, or flagged if no row exists
- The engagement letter drafted via `ca-template-fill` and stopped at the
  partner gate; nothing sent
- Recurring job pages for the current and next period opened via
  `ca-return-cycle` once the letter is signed
- Identifiers stored only as the pack allows: PAN, GSTIN, TAN, CIN; never
  Aadhaar numbers, passwords, OTPs or DSC PINs

## Phases

### Phase 1: Conflict check
1. `search` the entity name, trade names, PAN and GSTIN. `search` each promoter
   and director named.
2. If any hit is an existing client, a counterparty in an open matter, or a
   person page marked as adverse, stop and write the hits to the job page for
   the partner. Do not proceed without a partner line on the timeline.
3. Record the check as a timeline entry on the new client page once created:
   `conflict check: no hits` or `cleared by <partner>`, with date.

### Phase 2: Client master page
1. Slug: `companies/<client>`. If a page exists, this is a re-engagement:
   update, do not recreate, and keep the old timeline.
2. Fill the frontmatter from `folder-schema.md`. Each value carries a source
   in the body: the KYC document in `sources/`, or `[Source: User, onboarding
   call, YYYY-MM-DD]`.
3. Store every KYC document by reference: `file_upload` to `sources/` and
   link it from a `## Documents` list. Never copy an Aadhaar number into a page.
4. `services:` lists only what the partner confirmed. Each entry must match a
   row in the compliance calendar. If a service has no row, write it under
   `## Open` as `no calendar row for <service>` and flag it at the gate.
5. `risk_tier` is the partner's call. If not given, leave `not in the brain`
   and ask at the gate.

### Phase 3: Contacts
1. For each named contact: `search` first. If no page, create
   `people/<name>` with role, which client, what they handle, how to reach.
2. Link from the client page as `[role](people/<slug>)`. The brain creates the
   typed edge on save. Add a timeline entry on the person page:
   `- **YYYY-MM-DD** | contact for [client](companies/<client>) · <role>`.
3. Staff: link the partner and manager pages. Do not create staff pages here;
   they exist from setup.

### Phase 4: Prior-period state
1. Ask for, or read from documents: last returns filed per service, open
   notices, pending assessments, previous auditor.
2. Each item becomes a dated timeline entry with its source. Open notices
   become `ca-notice-reply` jobs immediately; do not wait for the letter.

### Phase 5: Engagement letter
1. Call `ca-template-fill` with `templates/engagement-letter` and the client
   page. Fields with no value stay `{{field: not in the brain}}`.
2. The filled letter goes to the approval list. ◆ Partner gate. Nothing is sent
   by this skill.
3. On `yes` and a signed copy: `file_upload` the signed letter to `sources/`,
   add `engagement letter v<version> signed YYYY-MM-DD` to `## Documents`,
   and a timeline entry.

### Phase 6: First jobs
1. Call `ca-return-cycle` for this client only, for the current and the next
   period of every service in `services:`.
2. Link the job pages from the client page under `## Open`.
3. Tick the onboarding checklist on the client page. Step 12 done means
   onboarded. Timeline entry: `onboarded · <n> services · <n> jobs opened`.

## Output Format

Report to the user, in this shape:

```
Client onboarded: companies/<client>
  conflict check: no hits | cleared by <partner> on <date>
  contacts: <n> people pages (<n> new)
  services: <list> → calendar rows: <n> mapped, <n> missing: <list>
  prior period: <n> timeline entries, <n> open notices → jobs opened
  engagement letter: v<version> · approved by <partner> <date> | awaiting partner
  jobs opened: <n> (<list of slugs>)
  not in the brain: <list of fields left empty>
```

If stopped at a gate, say which gate and what is needed.

## Anti-Patterns

- Creating the client page before the conflict check
- Writing a PAN or GSTIN without the document it came from
- Copying Aadhaar numbers, passwords or DSC PINs from KYC documents into a page
- Listing a service the partner did not confirm because the client "usually needs it"
- Sending the engagement letter, or marking it signed without the signed copy on file
- Opening jobs before the letter is signed, except notice jobs that have a deadline
- Guessing the risk tier

## Tools Used

- `search`: conflict check, existing pages for the entity and contacts
- `get_page` / `put_page`: client and people pages
- `add_link`: only where a link cannot be expressed in markdown
- `add_timeline_entry`: conflict check, documents, prior-period state, onboarding done
- `file_upload`: KYC documents and the signed engagement letter into `sources/`
