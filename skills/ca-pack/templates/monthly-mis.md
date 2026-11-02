---
template: monthly-mis
version: 1
use: the monthly compliance and status note sent to a retainer client
owner: manager
last_reviewed: 2026-11-01
review_every_days: 180
fields: [client_name, month, filings_table, open_notices_table, documents_awaited_table, upcoming_due_table, notes, preparer_name, firm_name]
gate: manager
---
# {{client_name}}: compliance status for {{month}}

## Filed this month

{{filings_table}}

## Open notices and assessments

{{open_notices_table}}

## Awaiting from you

{{documents_awaited_table}}

## Due in the next 45 days

{{upcoming_due_table}}

## Notes

{{notes}}

Every figure above is taken from filed returns, acknowledgements or your
records as received by us. Please tell us within 7 days if anything here does
not match your records.

{{preparer_name}}
{{firm_name}}
