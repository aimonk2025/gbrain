---
template: engagement-letter
version: 1
use: new client, or a change in scope or fee for an existing client
owner: partner
last_reviewed: 2026-11-01
review_every_days: 365
fields: [firm_name, firm_address, client_name, client_address, client_pan, services, period_from, period_to, fee_terms, billing_cycle, partner_name, partner_membership_no, date]
gate: partner
---
# Engagement letter

{{firm_name}}
{{firm_address}}

Date: {{date}}

To
{{client_name}}
{{client_address}}
PAN: {{client_pan}}

Subject: Terms of engagement for professional services

Dear Sir / Madam,

Thank you for engaging {{firm_name}}. This letter sets out the scope of our
services, our respective responsibilities and the fee terms, for the period
{{period_from}} to {{period_to}}.

## Scope of services

{{services}}

Each service listed is performed in accordance with the applicable law and the
standards issued by the Institute of Chartered Accountants of India. Services
not listed are outside this engagement and may be agreed separately.

## Your responsibilities

You will provide complete and accurate books, records, documents and
explanations within the timelines we communicate for each filing. Statutory
due dates depend on timely receipt of information. Where information is
received late, we will inform you of the consequence before acting.

## Our responsibilities

We will prepare and, where instructed, file the returns and documents in scope,
keep you informed of due dates, and bring to your attention any matter that
in our professional judgement requires your decision. Every filing is reviewed
by a chartered accountant of the firm before it is submitted.

## Fees

{{fee_terms}}, billed {{billing_cycle}}. Out-of-pocket expenses and government
fees are charged at actuals. Fees are exclusive of applicable taxes.

## Confidentiality and data

Your information is kept on the firm's own systems and is used only for the
services in scope. It is not shared with third parties except as required by
law or with your written consent.

## Term

This engagement continues until ended by either party with 30 days' written
notice. Work in progress at the date of termination is billed on a
time-and-materials basis.

Please sign and return a copy of this letter to confirm your acceptance.

Yours faithfully,

{{partner_name}}
Partner, {{firm_name}}
Membership No. {{partner_membership_no}}

Accepted on behalf of {{client_name}}:

Name: ____________________ Designation: ____________________ Date: ____________
