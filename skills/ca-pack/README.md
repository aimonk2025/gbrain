# CA Pack: how the brain is set up for a chartered accountancy firm

The pack turns a generic brain into a CA firm's brain. It is a set of reference
pages Claude reads before every job, plus eight skills (`skills/ca-*/SKILL.md`)
that do the work. Nothing here is advice to a client. It is the firm's way of
working, written down once so every job runs the same way.

## pack.yaml and onboarding

`pack.yaml` is the manifest: services, folders, checklists, templates, skills,
scheduled jobs, identity defaults, the demo dataset and the onboarding question
tree. `skills/onboard/SKILL.md` reads it, runs the interview in rounds, writes a
confirmed answers file (`skills/onboard/answers.schema.json`), applies the
answers deterministically, and can load `demo/` to show the brain working before
real data goes in. `test/ca-pack.test.ts` checks the manifest against the files.

## What Claude loads before every CA job, in this order

1. `skills/ca-pack/never-rules.md` (the lines that are never crossed)
2. `skills/ca-pack/folder-schema.md` (where every page lives)
3. `skills/ca-pack/compliance-calendar.md` (due dates; the firm edits this page)
4. The checklist for the job type in `skills/ca-pack/checklists/`
5. The firm's positions in the brain under `concepts/positions/`
6. The template for the output in `skills/ca-pack/templates/` (or the firm's
   newer copy under `templates/` in the brain, which wins when it exists)

Then the skill for the job. If any of the six is missing, the skill says so and
stops. It never fills a gap with a guess.

## The eight skills

| Skill | Fires on | Writes |
|---|---|---|
| `ca-client-onboard` | a new client | client page, contact pages, recurring job pages, engagement letter draft |
| `ca-return-cycle` | a return period opens, or "run this month's returns" | one job page per client per cycle, the morning list, ARN on the timeline |
| `ca-notice-reply` | a notice from any department | notice job page, draft reply with evidence list, filing record |
| `ca-audit-file` | an audit engagement | engagement page, requirement list, workpaper index, issues log, sign-off record |
| `ca-template-fill` | "draft the letter", "fill the template" | a filled document in the approval list, usage logged |
| `ca-monday-memo` | Monday morning, or "partner memo" | one memo per partner under `reports/` |
| `ca-position-check` | "our position on", a new circular | position page read, impact note, affected-client list |
| `ca-fee-review` | "fee review", "client profitability" | per-client fee vs hours table from imported data, fee letter draft, decision record |

## Human gates

Every skill stops at a gate before anything leaves the firm: a CA says yes,
change it, or no. The brain drafts, files pages and keeps the record. A person
presses send, files the return, signs the letter.

## Setup notes for the firm

- Copy the templates you use from `skills/ca-pack/templates/` into `templates/`
  in the brain and edit them there. The brain copy wins. Keep the `version`,
  `use`, `owner` and `last_reviewed` fields current.
- Write the firm's positions as pages under `concepts/positions/` using
  `skills/ca-pack/positions-template.md`. A position without a date and an
  approver is not a position.
- Check `compliance-calendar.md` at the start of every financial year and after
  any notification that moves a date.
- `tasks/`, `templates/` and `strategy/` are the firm's own folders. The brain
  auto-links the standard folders on every save. For these three to link the
  same way, add them to the directory pattern in the engine's link extraction
  (`src/core/link-extraction.ts`, the `DIR_PATTERN` constant) and page typing
  (`src/core/markdown.ts`, `inferType`). One line each.
- Access: the brain has no per-user locks inside one brain. Run one brain per
  partner or practice group. `strategy/` pages are partner-only by that split,
  not by a setting.

## Identifiers the brain may hold, and may not

May hold: entity PAN, GSTIN, TAN, CIN, LLPIN, registration numbers, DSC custody
status (who holds it, till when). These are business identifiers the firm
needs for the work.

Never holds: passwords, portal OTPs, DSC PINs, bank login details, Aadhaar
numbers of individuals, card numbers. See `never-rules.md`.
