---
template: fee-revision
version: 1
use: a fee revision proposal to an existing client after a fee review
owner: partner
last_reviewed: 2026-11-01
review_every_days: 365
fields: [client_contact_name, client_name, current_fee_terms, proposed_fee_terms, effective_from, reasons, scope_changes, partner_name, firm_name, date]
gate: partner
---
# Revision of professional fees

Date: {{date}}

Dear {{client_contact_name}},

We write regarding the professional fees for the services {{firm_name}}
provides to {{client_name}}.

Current terms: {{current_fee_terms}}
Proposed terms: {{proposed_fee_terms}}, effective {{effective_from}}

{{reasons}}

{{scope_changes}}

We value the relationship and are happy to discuss. Unless we hear otherwise,
the revised terms will apply to work from {{effective_from}}, and we will send
a short amendment to the engagement letter for signature.

Yours sincerely,

{{partner_name}}
Partner, {{firm_name}}
