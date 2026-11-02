---
template: notice-reply
version: 1
use: a written reply to a notice from GST, income-tax, TDS or MCA authorities
owner: partner
last_reviewed: 2026-11-01
review_every_days: 180
fields: [issuing_office, notice_form, notice_ref, notice_date, service_date, client_name, client_identifier, period, points_and_replies, evidence_list, prayer, authorised_signatory, firm_name, date]
gate: partner
---
# Reply to {{notice_form}} {{notice_ref}} dated {{notice_date}}

To
{{issuing_office}}

Subject: Reply to {{notice_form}} bearing reference {{notice_ref}} dated
{{notice_date}}, served on {{service_date}}, in the matter of {{client_name}}
({{client_identifier}}) for the period {{period}}

Respected Sir / Madam,

With reference to the above notice, {{client_name}} submits as follows.

## Preliminary

The assessee has received the notice on {{service_date}} and submits this
reply within the time allowed. The assessee reserves the right to add to or
amend this reply and requests an opportunity of being heard before any
adverse order is passed.

## Point-wise reply

{{points_and_replies}}

Each paragraph above states the department's point, the facts with the
documents relied on, the legal position with the provision or circular cited,
and the assessee's submission. Where a figure is given, its source document is
listed in the enclosures.

## Enclosures

{{evidence_list}}

## Prayer

{{prayer}}

For {{client_name}}

{{authorised_signatory}}
Authorised signatory

Date: {{date}}
Place:

Prepared with the assistance of {{firm_name}}, Chartered Accountants.
