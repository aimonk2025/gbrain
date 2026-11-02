---
name: onboard
version: 1.0.0
description: |
  Turn a generic brain into an industry brain from a pack manifest. Runs a
  bounded interview in rounds (every unblocked question at once, each with the
  pack's recommended answer), takes facts from the environment before asking,
  ends with a confirmed answers file and a one-page summary at the gate, then
  applies the answers deterministically: folders, calendar, checklists,
  templates, skills, jobs, identity files, config. Optionally loads the pack's
  demo data, shows the brain working, wipes it, and imports the real data.
triggers:
  - "onboard this firm"
  - "onboard the firm"
  - "run onboarding"
  - "install the pack"
  - "onboarding interview"
  - "set up the brain for a client"
tools:
  - get_stats
  - get_health
  - list_pages
  - get_page
  - put_page
  - delete_page
  - put_raw_data
  - add_timeline_entry
  - search
  - traverse_graph
  - sync_brain
mutating: true
---

# Onboard

> **Filing rule:** see [skills/_brain-filing-rules.md](../_brain-filing-rules.md).
> **Convention:** see [skills/conventions/quality.md](../conventions/quality.md).
> **Scheduling:** register jobs per [skills/cron-scheduler/SKILL.md](../cron-scheduler/SKILL.md).
> **Identity:** the four identity files follow [skills/soul-audit/SKILL.md](../soul-audit/SKILL.md); this skill fills them from the pack and the answers instead of a free interview.

The pack is a folder with a `pack.yaml` (for example `skills/ca-pack/pack.yaml`).
The manifest holds the question tree. This skill holds the protocol. Answers
select and toggle parts of the pack; nothing about the brain's shape is
generated.

## Contract

This skill guarantees:
- The question tree comes from the pack manifest and nothing else; no question
  is invented, none is skipped unless its `when` condition is false
- Rounds: every question whose `depends_on` are answered is asked in the same
  round, numbered, each with the pack's default shown as the recommended
  answer; a question that depends on an open question waits for a later round
- Facts before questions: anything the pack marks `facts_from` is read from
  the environment first (identity files, existing pages, the client export)
  and shown as a prefilled answer with its source, never asked cold
- The session ends with `answers.json` (shape in `answers.schema.json`), a
  "what we will build" summary, and the user's explicit confirmation; nothing
  is applied before that
- Apply is deterministic: the same answers file produces the same brain; every
  step writes a proof line to the onboarding report
- The pack's review status is stated at the gate: a pack with empty
  `reviewed_by` is announced as unreviewed content
- The demo loads only pages with the pack's `slug_prefix` and `demo: true`,
  and the wipe removes exactly those
- No secret, API key, password or OTP is ever written to a page or to the
  answers file

## Phases

### Phase 0: Load and check the pack
1. Read `pack.yaml`. Check every file it references exists (`reference`,
   `checklists`, `templates`, `skills`, `demo/dir`). A missing file stops the
   onboarding with the path named.
2. `get_health` and `get_stats`. If the brain already has pages, this is a
   re-onboarding: say so, and later steps update instead of create.
3. State the pack name, version, industry and review status in one line.

### Phase 1: Facts first
For each question with `facts_from`, look before asking:
- Identity files (`USER.md`, `SOUL.md`) and any existing firm page → `firm`
- Existing `people/` pages with a `role` → `staff`, `partners`
- The client export, if a path is given or a likely file sits in `sources/` →
  `client_export`, and per-client services that inform the `services` default
Record each fact as `{ value, source }`. A fact is shown as the prefilled
answer; the user can change it. Never ask for something a file already says.

### Phase 2: Rounds
1. Compute the frontier: questions not yet answered, whose `depends_on` are all
   answered, and whose `when` (if any) evaluates true on current answers.
2. Ask the whole frontier in one message, in this format:

```
Round <n> · <k> questions · <answered>/<total> settled

❓ Q1 · <title>
<the question, with options or fields>
➡️ Recommended: <default, or the prefilled fact with its source>

❓ Q2 · ...
```

3. Wait. Record each answer; note `changed_from_default` when it differs.
   A `default_rule` is evaluated on the answers so far and shown as the
   recommendation with the rule in brackets.
4. Repeat until the frontier is empty. Typical CA pack: three or four rounds.
   Keep the tone plain. This is a setup conversation, not a cross-examination.

### Phase 3: Summary at the gate
Write `## What we will build` from the answers, before touching the brain:
- brains: one, or one per partner (list them)
- folders created, with partner-only ones marked
- calendar rows enabled, with any the user edited
- checklists, templates, skills and jobs enabled, by service
- gates: who reviews what
- what leaves the server under the chosen search mode
- where it runs
- pack review status
- the demo plan, if chosen
Save `answers.json` to `~/.gbrain/onboarding/<pack>-<YYYY-MM-DD-HHMM>.json`
with `confirmed: false`. ◆ Ask for confirmation. On `yes`, set `confirmed`,
`confirmed_by`, `confirmed_at`. On `change`, return to the round that holds
the question. Nothing below runs without `confirmed: true`.

### Phase 4: Apply
Run the effects of every answered question, in manifest order. Each op writes
one proof line to `reports/onboarding/<YYYY-MM-DD-HHMM>.md`.

| op | what it does | proof |
|---|---|---|
| `create_firm_page` | `companies/<firm-slug>` with `role: the-firm` and the firm fields, each sourced | page slug |
| `set_template_fields` | the firm fields recorded on each copied template page's frontmatter under `defaults:` so `ca-template-fill` reads them | template slugs |
| `create_people_pages` | `people/<name>` with `role`; existing pages updated, not replaced | slugs created / updated |
| `select_by_services` | the enabled set: calendar rows whose Job is in a chosen service's `calendar_rows`; checklists, templates, skills, jobs whose `services` intersect the answer or contain `any` | counts per target |
| `split_brains` | when `separate`: one brain per partner; this onboarding continues for the current partner's brain and writes a short runbook for the others | brains listed |
| `exclude_partner_only` | when `shared`: `partner_only` folders and skills are left out of this brain and listed for the partner's own brain | items excluded |
| `set_gates` | writes `concepts/sops/review-gates` with the chain; `ca-*` skills read it | page slug |
| `set_config` | a key in the brain's config file (never a page); `embeddings`, `query_expansion`, `books_systems`, `quiet_hours` | key and value |
| `import_client_master` | `put_raw_data` the export, then one `companies/` page per row with `services`, `partner`, identifiers, each sourced to the export; unmapped columns listed, nothing guessed | rows imported / skipped |
| `write_calendar` | `finance/compliance-calendar` with only the enabled rows, the user's edits, and a timeline entry naming the pack version as the source | page slug, row count |
| `write_page` | a page from the answer, for example `strategy/client-tiers` | slug |
| `set_review_days` | `review_every_days` on every copied template; `review_by` default for new positions in `concepts/sops/review-gates` | values |
| `set_engine` | local file now; for `postgres`, record the step for the operator (`gbrain migrate --to ...`) rather than running it unattended | engine name |
| `load_demo` | Phase 5 | see below |

Then, regardless of answers:
1. Copy enabled checklists to their `target` slugs and enabled templates to
   theirs, each with `source: pack <id> v<version>` in frontmatter.
2. Write the identity files from `templates/`: SOUL.md mission from
   `identity.soul_mission`; USER.md from the firm and staff answers;
   ACCESS_POLICY.md tiers from `identity.access_tiers`; HEARTBEAT.md from the
   enabled jobs. Existing files are backed up with a `.bak-<date>` suffix.
3. Register the enabled jobs through the cron-scheduler skill, staggered,
   outside quiet hours. A job whose skill was not enabled is not registered.
4. Record `schema_choices` in `~/.gbrain/update-state.json`: adopted folders,
   declined services, custom entries.
5. `sync_brain`. Then `get_stats` and write the counts to the report.

### Phase 5: Demo (when chosen)
1. Load every file under the pack's `demo/dir` as a page. Each must carry
   `demo: true` and a slug starting with `slug_prefix`; a file without both is
   refused.
2. Run `demo.queries` in order: `search` queries show the top results with
   sources; `graph` queries run `traverse_graph` from the slug; `skill`
   queries run the named skill on the named page and stop at its gate. Show
   each result as the user will see it in real work.
3. Say plainly what was shown: search, graph, a draft stopped at a gate.
4. Wipe: `delete_page` every page with `demo: true` and the prefix. `list_pages`
   to confirm zero remain. Write the count to the report.

### Phase 6: Real data
If `client_export` was given, `import_client_master` already ran. Otherwise
hand over to `ca-client-onboard` for the first client, and to the pack's
import notes for bulk history. Do not invent a first client.

### Phase 7: Close
Report saved under `reports/onboarding/`. Timeline entry on the firm page:
`onboarded with pack <id> v<version> · <n> services · <n> jobs`. Tell the user
the three things to do next: run the first job, import history, and name the
pack reviewer if `reviewed_by` is empty.

## Output Format

Round:
```
Round 2 · 4 questions · 6/15 settled

❓ Q1 · Do partners share clients
separate | shared
➡️ Recommended: separate (one brain per partner; the brain has no per-user locks)
```

Gate:
```
What we will build · pack ca v1.0.0 · content unreviewed
  brains: 2 (one per partner: <a>, <b>) · this session: <a>
  folders: 17 (strategy partner-only)
  services: 8 → calendar rows 14 · checklists 7 · templates 7 · skills 8 · jobs 5
  gates: manager then partner on returns and notices; partner on letters
  leaves the server: nothing (keyword + graph)
  runs: local file on this machine
  demo: 3 queries, then wiped
answers saved: ~/.gbrain/onboarding/ca-<stamp>.json · confirm to apply? (yes / change Qn)
```

Apply:
```
Applied · 23 steps · report: reports/onboarding/<stamp>
  pages: firm 1 · people 6 · calendar 1 (14 rows) · checklists 7 · templates 7 · tiers 1 · clients 38 (2 rows skipped: no PAN)
  identity: SOUL, USER, ACCESS_POLICY, HEARTBEAT written (backups .bak-<date>)
  jobs: 5 registered · next: nightly-spawn 01:00
  demo: loaded 14 · shown 4 · wiped 14 · remaining 0
  next: run "due list" · import two years of history · name the pack reviewer
```

## Anti-Patterns

- Asking a question the manifest does not contain, or asking all questions in one flat list
- Asking for a fact that a file already holds
- Applying anything before `confirmed: true`
- Generating folders, checklists or templates instead of selecting from the pack
- Writing an API key, password or OTP to a page or the answers file
- Loading demo pages without the prefix, or wiping by any rule other than prefix plus `demo: true`
- Registering a job for a skill that was not enabled
- Running `gbrain migrate` unattended during onboarding
- Hiding that the pack content is unreviewed

## Tools Used

- `get_health` / `get_stats`: before and after
- `list_pages` / `get_page`: facts first, re-onboarding detection, demo wipe check
- `put_page` / `delete_page`: pack pages, identity, client pages, demo load and wipe
- `put_raw_data`: the client export
- `add_timeline_entry`: calendar source, firm onboarded
- `search` / `traverse_graph`: the demo
- `sync_brain`: after apply
