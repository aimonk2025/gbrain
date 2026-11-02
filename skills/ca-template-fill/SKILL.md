---
name: ca-template-fill
version: 1.0.0
description: |
  Fill a versioned template from brain pages for a CA firm: pick the template
  by use case, refuse stale versions, pull every field from the client page and
  the job page, leave missing fields visibly empty, put the result in the
  approval list at the gate the template names, and log usage on the client
  and the template. Never invents a value.
triggers:
  - "fill the template"
  - "draft the letter"
  - "use the template"
  - "which template"
  - "template review due"
tools:
  - search
  - list_pages
  - get_page
  - put_page
  - add_timeline_entry
  - file_upload
mutating: true
---

# CA Template Fill

> **Filing rule:** see [skills/_brain-filing-rules.md](../_brain-filing-rules.md).
> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).

Read before starting: `skills/ca-pack/never-rules.md` and
`skills/ca-pack/templates/README.md`. Templates live at `templates/<name>` in
the brain; the pack copies under `skills/ca-pack/templates/` are fallbacks.

## Contract

This skill guarantees:
- The template chosen by its `use:` line, with the brain copy preferred over
  the pack copy; if two templates match, both are named and the user picks
- A template whose `last_reviewed` plus `review_every_days` is in the past is
  refused with the owner named; it is not filled
- Only fields listed in the template's `fields:` are filled; every value comes
  from a named page or the user's statement with a date
- A missing value renders as `{{field: not in the brain}}`, listed at the gate
- The filled document is saved to `sources/` and linked from the job page and
  the client page; it goes to the approval list at the gate the template's
  `gate:` names
- Usage logged on the client timeline and on the template page
- Nothing is sent by this skill

## Phases

### Phase 1: Pick
1. From the request and the job page, match the `use:` line of templates under
   `templates/`, then `skills/ca-pack/templates/`. One match → proceed. Many →
   list them with their `use:` lines and stop. None → say so and offer the
   nearest; never improvise a letter.
2. Read the frontmatter. If `last_reviewed + review_every_days < today`, stop:
   `template <name> v<version> is past review (owner: <owner>)`.

### Phase 2: Gather
1. For each field in `fields:`, take the value from, in order: the job page,
   the client page, the people pages linked from it, the firm page
   (`strategy/firm` or `companies/<firm>`), the user's words in this
   conversation with a date. Record the source per field on the job page.
2. Table fields (`items_table`, `points_and_replies`, `document_table`,
   `filings_table`) are built from the job page's own tables. If the job page
   has no such table, the field is `not in the brain`.
3. Dates are written in full (`14 November 2026`). Amounts carry the currency
   and the source.

### Phase 3: Fill
1. Replace each `{{field}}`. Missing → `{{field: not in the brain}}`.
2. No other text changes. The template's wording is the firm's; the skill does
   not "improve" it. Wording changes are a new template version by the owner.
3. Save to `sources/<yyyy-mm-dd>-<client>-<template>-v<version>.md` (or the
   format the firm asks for), link from the job page and the client page.

### Phase 4: Gate
1. Put the document in the approval list for the role in `gate:`. ◆ The
   reviewer sees the document, the field sources, and the list of missing
   fields. `yes` → status `approved`. `change it` → the change is applied by
   the reviewer, not guessed, and if the change is to template wording, a
   lesson is written and the template owner is told.
2. The person sends or signs. The brain does not.

### Phase 5: Log
1. Client timeline: `- **YYYY-MM-DD** | <template> v<version> prepared for
   <job> · approved by <name>` once approved.
2. Template page timeline: `used for <client> · <job>`; a monthly count
   feeds the Monday memo's template review list.

## Output Format

```
Template: <name> v<version> (<brain | pack>) · gate: <role>
  fields: <n> filled from pages · <n> from user · <n> not in the brain: <list>
  saved: sources/<file> · linked from projects/<job>, companies/<client>
  next: awaiting <role> | approved by <name> <date>
```

Refusal:
```
Not filled: <name> v<version> is past review (last reviewed <date>, owner <owner>)
```

## Anti-Patterns

- Picking a template by name similarity instead of its `use:` line
- Filling a template past its review date "just this once"
- Inventing a value for a missing field, or copying one from another client
- Rewording the template body
- Adding fields the template does not declare
- Sending the document
- Skipping the usage log

## Tools Used

- `list_pages` / `search`: templates and their `use:` lines
- `get_page`: template, job page, client page, people pages
- `put_page`: job page field sources, approval status
- `file_upload`: the filled document into `sources/`
- `add_timeline_entry`: usage on client and template pages
