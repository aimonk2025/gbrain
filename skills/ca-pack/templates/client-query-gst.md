---
template: client-query-gst
version: 1
use: open items in a GST return job, usually 2B mismatches or missing documents
owner: manager
last_reviewed: 2026-11-01
review_every_days: 180
fields: [client_contact_name, client_name, return_type, period, due_date, reply_by, items_table, preparer_name, firm_name]
gate: manager
---
# Client query: {{return_type}} for {{period}}

Dear {{client_contact_name}},

We are preparing the {{return_type}} of {{client_name}} for {{period}}, due on
{{due_date}}. The following items need your input before we can finalise it.

{{items_table}}

For each item, please send the document or confirm the position by
{{reply_by}}. Where a supplier has not reported an invoice, the input tax
credit on it cannot be claimed in this return under the current rules; it can
be claimed once the supplier reports it. We will keep it on the follow-up list.

If we do not hear from you by {{reply_by}}, we will prepare the return without
these items to protect the due date and tell you what was left out.

Regards,
{{preparer_name}}
{{firm_name}}
