# Templates

Pack defaults. Copy the ones the firm uses to `templates/<name>` in the brain
and edit them there. The brain copy wins. `ca-template-fill` reads the
frontmatter first: it refuses a template whose `last_reviewed` is older than
`review_every_days`, and it fills only the fields listed under `fields`.

Field syntax in the body: `{{field}}`. A field with no value in the brain is
left as `{{field: not in the brain}}` and listed at the gate. Claude never
invents a value for a field.
