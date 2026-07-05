# GBrain Capability Sync

The capability-sync cron job keeps GBrain's record of Hermes skills current. It runs autonomously (no user present) and must complete fully within a single turn.

## Inventory Parsing

`hermes skills list` has **no `--json` flag**. Parse the table output:

```bash
hermes skills list 2>&1 | grep -E '^\│' | awk -F'│' '{gsub(/ /,"",$2); print $2}' | grep -v '^$' | sort
```

**Truncation gotcha:** Skill names longer than ~22 chars are truncated with `…` in the table (e.g. `audiocraft-audio-gene…`). To resolve full names:
- Cross-reference against existing GBrain pages (slugs in `mcp_gbrain_list_pages` use full names).
- Or run `hermes skills inspect <prefix>` which suggests full matches (but this is slow — 60s timeout per call).
- The safest approach: compare the truncated list against the EXISTING GBrain pages list — existing slugs already have full names, so only genuinely new skills need resolution.

## GBrain put_page Contract

- **Required params:** `slug` (string) + `content` (string). A call missing `content` fails with `invalid_params`.
- **Content shape:** Full markdown document beginning with YAML frontmatter:
  ```yaml
  ---
  title: <Skill Name>
  type: capability
  tags: [hermes-capability]
  category: <category>
  source: <builtin|local|hub|github>
  enabled: true
  ---
  <one-paragraph description>
  ```
- **Tagging:** Putting `tags: [hermes-capability]` in frontmatter tags the page automatically — no separate `add_tag` call needed.
- **Slug convention:** `hermes/capabilities/<skill-name>` (skill name with hyphens, no underscores).
- **Index page:** `hermes/capabilities/index` — lists all current slugs, total count, and `last_synced` ISO-8601 timestamp.

## Sequential Upsert (Cron Constraint)

`execute_code` is **BLOCKED in cron**. Must call `mcp_gbrain_put_page` once per skill, sequentially. Batch 10 parallel calls per assistant turn to stay efficient within the sequential constraint.

## Tombstone Pattern for Stale Pages

When a skill exists in GBrain but is no longer in the live inventory (Status=disabled or removed):

1. Do **NOT** hard-delete the page.
2. Re-write it via `mcp_gbrain_put_page` with `status: removed` and `enabled: false` added to frontmatter. Keep the rest of the page body intact.
3. Exclude `hermes/capabilities/index` from tombstoning — the index is always rewritten fresh.

**Note:** If the stale page was already tombstoned in a previous sync, `put_page` returns `status: skipped` (content unchanged). This is expected — the tombstone is already in place.

## Response Semantics

- `status: created_or_updated` — page was written or updated successfully.
- `status: skipped` — content hash unchanged from what's already stored. No action needed.

## Reconciliation Workflow

1. `hermes skills list` → parse table → build CURRENT set (enabled skills only).
2. `mcp_gbrain_list_pages(tag='hermes-capability')` → get EXISTING pages.
3. STALE = EXISTING slugs under `hermes/capabilities/<x>` where `<x>` NOT in CURRENT, excluding `index`.
4. Upsert all CURRENT skills (one `put_page` per skill).
5. Tombstone all STALE skills (one `put_page` per stale skill).
6. Write index page with full CURRENT list + count + timestamp.

## Common Full-Name Mappings

Truncated table names → full skill names (as of 2026-07-05):

| Truncated | Full |
|-----------|------|
| `audiocraft-audio-gene…` | `audiocraft-audio-generation` |
| `evaluating-llms-harne…` | `evaluating-llms-harness` |
| `hermes-agent-skill-au…` | `hermes-agent-skill-authoring` |
| `songwriting-and-ai-mu…` | `songwriting-and-ai-music` |
| `test-driven-developme…` | `test-driven-development` |
