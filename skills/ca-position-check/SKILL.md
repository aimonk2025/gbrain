---
name: ca-position-check
version: 1.0.0
description: |
  Answer "what is the firm's position on X" from approved position pages only,
  say when none exists, draft a new position for partner approval, and when a
  new circular, notification or ruling arrives, find the positions and the
  clients it touches through the graph and write an impact note for the
  partner. Never states a position the pages do not hold.
triggers:
  - "our position on"
  - "do we have a stand on"
  - "firm position"
  - "new circular"
  - "does this notification affect"
  - "record a position"
tools:
  - search
  - query
  - get_page
  - put_page
  - traverse_graph
  - get_backlinks
  - add_timeline_entry
mutating: true
---

# CA Position Check

> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).

Read before starting: `skills/ca-pack/never-rules.md` and
`skills/ca-pack/positions-template.md`. Positions live under
`concepts/positions/`. A page there without `approved_by` and `approved_on` is
a draft and is reported as such.

## Contract

This skill guarantees:
- A position is quoted only from a page with `status: current`,
  `approved_by` and `approved_on`; drafts and superseded pages are named as
  such and not applied
- When no page exists, the answer is `no firm position recorded`, followed by
  what the law pages say and an offer to draft one for the partner
- General knowledge is labelled `general, not from the brain` and never
  written into a client document
- A new circular or ruling produces an impact note: the law pages it touches,
  the positions whose `law:` or `watch list` cite them, the clients where
  those positions are applied (from the graph), and a recommended action for
  the partner, with no change made to any position until the partner says yes
- Every position change is a new dated version; nothing is deleted

## Phases

### Phase A: Look up ("our position on X")
1. `search` `concepts/positions/` for the topic and its synonyms; `query` the
   law pages for the section.
2. Current approved page found → answer with the stand, scope, approver, date,
   and the clients where applied. Add nothing.
3. Draft or superseded only → say so, name the page, and do not apply it.
4. Nothing → `no firm position recorded on <topic>`. Summarise what
   `concepts/law/` holds, with page links and their `last checked` dates.
   Anything beyond the pages is labelled `general, not from the brain`. Offer
   Phase B.

### Phase B: Draft a position ("record a position")
1. Create `concepts/positions/<topic>` from the template with
   `status: draft`, no `approved_by`. Fill the stand from the user's words
   with a date, the basis from law pages only, the scope as given.
2. Link it from every job page that raised the question.
3. ◆ Partner gate. On `yes`: set `approved_by`, `approved_on`, `review_by`,
   `status: current`, timeline line. If it replaces an older page, set
   `supersedes` on the new one and `status: superseded` plus `superseded_by`
   on the old one. The old page stays.

### Phase C: Impact of a new circular, notification or ruling
1. Create or update the law page `concepts/law/<act>-<ref>` with the text
   summary, source document in `sources/`, date, and what it changes.
2. `get_backlinks` on the sections it amends or interprets → positions whose
   `law:` cites them. `search` positions whose watch list names the topic.
3. For each position: `traverse_graph` from the position page, direction
   `in`, to the client pages where it is applied, and the open jobs that
   link it.
4. Write `reports/position-impact/<YYYY-MM-DD-HHMM>-<ref>.md`: the change,
   positions touched, clients touched with open jobs, and one of: `no change
   needed`, `position needs review`, `urgent: affects filings due within 30
   days`. Each judgement cites the law page.
5. ◆ Partner reads the note. Any position change goes through Phase B. Open
   jobs touched get a timeline line pointing at the note.

## Output Format

Look up:
```
Position: <topic> · current · approved by <partner> <date> · review by <date>
  stand: <one or two sentences>
  scope: <where it applies, where not>
  basis: <law pages with last-checked dates>
  applied at: <n> clients (<links>)
```
or
```
No firm position recorded on <topic>.
  law pages: <links with dates>
  general, not from the brain: <one line, if offered at all>
  offer: record a position for partner approval
```

Impact note:
```
Impact: <ref> (<date>) · law pages updated: <n>
  positions touched: <n> → <slugs with verdict each>
  clients touched: <n> · open jobs touched: <n> (<n> due within 30 days)
  partner action: <no change | review <slugs> | urgent: <slugs>>
  saved: reports/position-impact/<file>
```

## Anti-Patterns

- Answering a position question from general knowledge and presenting it as the firm's
- Applying a draft or superseded position
- Editing a position page in place after approval; versions supersede
- Changing a position because a circular arrived, before the partner's yes
- Missing clients in the impact note because the search stopped at positions and did not walk the graph
- Writing law into the position page that has no page under `concepts/law/`

## Tools Used

- `search` / `query`: positions, law pages, synonyms
- `get_page` / `put_page`: position pages, law pages, impact notes
- `get_backlinks` / `traverse_graph`: positions citing a section; clients and jobs applying a position
- `add_timeline_entry`: approvals, supersessions, impact notes on affected pages
