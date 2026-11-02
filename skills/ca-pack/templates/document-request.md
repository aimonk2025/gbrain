---
template: document-request
version: 1
use: the first information request for any job (onboarding, audit, ITR, assessment)
owner: manager
last_reviewed: 2026-11-01
review_every_days: 365
fields: [client_contact_name, client_name, job_name, document_table, send_by, send_to, preparer_name, firm_name]
gate: manager
---
# Information required: {{job_name}} for {{client_name}}

Dear {{client_contact_name}},

To proceed with {{job_name}}, we need the following. Items are grouped by
priority; the first group holds up everything else.

{{document_table}}

Please send soft copies to {{send_to}} by {{send_by}}. Where a document does
not exist or does not apply, a short note saying so is enough. We will confirm
receipt of each item and tell you what is still open.

Regards,
{{preparer_name}}
{{firm_name}}
