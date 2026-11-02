# Position page template (concepts/positions/<topic>.md)

A position is the firm's stand on a question where the law allows more than one
reading, or where practice has settled a method. Without an approver and a
date it is a note, not a position, and `ca-position-check` will not cite it.

```markdown
---
type: concept
kind: position
topic: itc-2b-basis
status: current | superseded
approved_by: people/<partner>
approved_on: 2026-04-02
review_by: 2027-04-01
supersedes: concepts/positions/<older-slug> | none
applies_to: [gstr-3b, gstr-9]
law: [concepts/law/cgst-s16-2-aa, concepts/law/cgst-r36-4]
---
# Position: ITC claimed on GSTR-2B basis

## The stand
One or two sentences. What the firm does, in every case this applies to.
[Source: partner decision, 2026-04-02]

## Scope
Which clients, which returns, which situations. Where it does not apply.

## Basis
The sections, rules, circulars and rulings relied on, each as a link to its
page under `concepts/law/` with the date that page was last checked.

## How it shows in the work
- in the GSTR-3B checklist: step N
- in the notice-reply template: paragraph on 2B reconciliation
- in client queries: the standard wording

## Clients where applied
Links to client pages. The brain keeps this list current from the graph.

## Watch list
Which circulars, notifications or pending cases could change this stand.
`ca-position-check` reads this when a new circular arrives.

<!-- timeline -->
## Timeline
- **2026-04-02** | position approved · [Source: partner meeting, 2026-04-02]
```
