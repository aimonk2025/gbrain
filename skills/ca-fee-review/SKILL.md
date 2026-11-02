---
name: ca-fee-review
version: 1.0.0
description: |
  Partner-only fee and profitability review for a CA firm: import the time and
  billing exports, compute fee against hours per client and per service from
  that data only, compare with the pricing page and client tiers, list
  candidates for revision, draft fee revision letters at the partner gate, and
  record the decision under strategy. Never estimates a number.
triggers:
  - "fee review"
  - "client profitability"
  - "hours vs fees"
  - "which clients lose money"
  - "revise the fee"
tools:
  - search
  - list_pages
  - get_page
  - put_page
  - put_raw_data
  - get_raw_data
  - add_timeline_entry
mutating: true
---

# CA Fee Review

> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).

Read before starting: `skills/ca-pack/never-rules.md`, `strategy/pricing`,
`strategy/client-tiers` and `strategy/profitability` if they exist. This skill
runs only for the partner. If the request comes from anyone else, answer
`fee review is partner-only` and stop; `strategy/` pages are not read for them.

## Contract

This skill guarantees:
- Hours and fees come only from imported exports (time sheets, invoices,
  receipts) stored via `put_raw_data` with the file in `sources/`; no figure
  is estimated, extrapolated or recalled from memory
- Per-client and per-service tables for the period: hours, fees billed, fees
  collected, hours per 1,000 of fee, against the pricing page's bands
- Candidates for revision listed with the rule that triggered them, from the
  pricing page; if the pricing page has no rules, the table is shown and no
  candidates are named
- Fee revision letters drafted via `ca-template-fill` with
  `templates/fee-revision`, each at the partner gate; nothing sent
- Every decision recorded as a dated entry in `strategy/decisions` and on the
  client page timeline; tier changes recorded on `strategy/client-tiers`
- The review saved under `reports/fee-review/`

## Phases

### Phase 1: Import
1. Ask for, or find in `sources/`, the period's exports: time by client and
   staff, invoices by client, receipts by client. Store each with
   `put_raw_data` keyed by `<type>-<period>`, file linked.
2. Validate: every client name in the export maps to a `companies/` slug. Unmapped
   rows are listed and excluded, not guessed into a client.
3. If an export is missing, the section that needs it reads
   `not imported: <type> <period>` and the review proceeds without it.

### Phase 2: Compute
1. Per client: hours (by staff grade if the export has it), fees billed, fees
   collected, outstanding, hours per 1,000 of fee billed. Per service where
   the export carries it.
2. Compare with `strategy/pricing`: retainer band, hourly floor, scope rules.
   Compare with `strategy/client-tiers` for the current tier.
3. Deterministic, from the rows. Show the arithmetic once at the bottom of
   the report so the partner can check it.

### Phase 3: Candidates
1. Apply the pricing page's rules, for example "hours per 1,000 above X for
   two periods" or "scope added without fee change" (scope changes come from
   the client page timeline). Each candidate names the rule and the rows.
2. No rules on the pricing page → show the sorted table, name no candidates,
   and say the pricing page has no revision rules.

### Phase 4: Partner review
1. Save `reports/fee-review/<YYYY-MM-DD-HHMM>.md` and return the summary.
2. ◆ Partner picks: revise (with new terms), hold, drop, re-tier. Each choice
   is written to `strategy/decisions` with date and reason in the partner's
   words, and to the client page timeline.
3. For each `revise`: `ca-template-fill` with `templates/fee-revision`;
   `reasons` comes from the partner's words, never generated. Partner gate on
   the letter. A person sends it.
4. For each `re-tier`: update `strategy/client-tiers` and the client page's
   `risk_tier` or tier field, with the decision link.

## Output Format

```
Fee review · <period> · partner <name>
  imports: time <ok | not imported> · invoices <ok | not imported> · receipts <ok | not imported> · unmapped rows <n>
  clients: <n> · hours <total> · billed <total> · collected <total> · outstanding <total>
  worst five (hours per 1,000 billed):
    [client](link) · <h> h · <fee> · <ratio> · tier <t> · rule: <rule | none>
  candidates: <n> (rules from strategy/pricing) | none: pricing page has no revision rules
  saved: reports/fee-review/<file>
  partner decisions: awaiting | <n> recorded → <n> letters at gate
```

## Anti-Patterns

- Running for anyone but the partner, or reading `strategy/` for them
- Filling a missing export with an estimate or last period's numbers
- Mapping an unknown export row to the nearest client name
- Naming revision candidates without a rule on the pricing page
- Writing the reasons for a fee change itself
- Sending a fee letter, or changing a tier without a decision entry
- Deleting or overwriting an earlier decision

## Tools Used

- `put_raw_data` / `get_raw_data`: exports for the period
- `list_pages` / `get_page`: clients, pricing, tiers, decisions
- `put_page`: report, decisions, tiers, client pages
- `search`: exports already in `sources/`, scope changes on timelines
- `add_timeline_entry`: decisions on client pages
