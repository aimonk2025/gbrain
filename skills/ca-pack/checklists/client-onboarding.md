# Checklist: Client onboarding

Used by `ca-client-onboard`. A client is not onboarded until step 12.

1. [ ] Conflict check: the entity and its promoters searched across the brain; no conflict, or partner cleared it (proof: search note, partner line)
2. [ ] Entity identifiers collected: PAN, GSTIN, TAN, CIN/LLPIN as applicable (proof: client page frontmatter, source documents in `sources/`)
3. [ ] KYC documents listed and stored by reference; no Aadhaar numbers copied into pages (proof: docs index)
4. [ ] Contacts recorded as people pages with role and what they handle (proof: links on client page)
5. [ ] Services agreed, listed in `services:`; each mapped to a calendar row (proof: client page, calendar rows named)
6. [ ] Fee terms recorded with billing cycle (proof: `fee_terms`)
7. [ ] Books system and access route recorded: Tally, Zoho, Excel; who sends exports and when (proof: client page)
8. [ ] Prior-period status: last returns filed, open notices, pending assessments, previous auditor if any (proof: timeline entries with sources)
9. [ ] Risk tier set by the partner with reason (proof: `risk_tier` and a timeline line)
10. [ ] Engagement letter drafted from the template and put in the approval list (proof: `ca-template-fill` output link)
11. [ ] ◆ Partner says yes on the engagement letter; signed copy filed (proof: `sources/`, client page docs line)
12. [ ] Recurring job pages opened for the current and next period via `ca-return-cycle` (proof: job links on client page)
