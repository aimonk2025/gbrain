# Checklist: Notice reply

Used by `ca-notice-reply`. Any department: GST, income-tax, TDS, MCA, PF.

1. [ ] Notice stored raw in `sources/`; form, section, period, DIN or reference number, issuing office, date of issue and date of service recorded (proof: notice job page frontmatter)
2. [ ] Deadline computed from the date of service and the notice's own wording; task opened with the due date minus 3 working days (proof: task link)
3. [ ] Client informed by a CA; acknowledgement date recorded (proof: timeline)
4. [ ] Every point in the notice listed as a row: the department's claim, the amount, our response status (proof: points table)
5. [ ] Facts gathered per point from the client page, past returns, past replies and books (proof: each row has sources)
6. [ ] Firm position checked per point via `ca-position-check`; where none, flagged for the partner (proof: position links or flags)
7. [ ] Law pulled per point from `concepts/law/` with date last checked; gaps flagged (proof: law links)
8. [ ] Evidence list assembled: every document the reply relies on, each on file (proof: evidence table with `sources/` links)
9. [ ] Draft reply filled from `templates/notice-reply` with every figure sourced and every open point marked `not in the brain` (proof: draft link)
10. [ ] ◆ Manager review, then partner says yes (proof: two timeline lines)
11. [ ] ◆ Filed or sent by a person; ARN, acknowledgement or dispatch proof recorded (proof: client timeline)
12. [ ] Follow-up task opened for the hearing date or the department's response window (proof: task link)
13. [ ] Position page updated if the reply took a stand not yet recorded; lesson written if anything changed (proof: links)
