---
name: daily-drop
description: >-
  Orchestrate the CurAItion daily publishing run end-to-end: scout (cultural +
  click-bait in parallel), editorial sign-off on a candidate shortlist,
  user-needs classification, story packaging, adversarial fact and link
  verification, parallel rendering (Substack Drop, LinkedIn post + first
  comment, IG carousel + LinkedIn carousel PDF, IG caption), a cross-asset
  editor gate, delivery to the shared "The Drop" Google Drive folder in a
  dated subfolder, and an issue-log writeback to GBrain. One command per day:
  "run the daily drop", "publish today's drop", "run the daily publishing
  chain". Resolves the canonical editorial spec from GBrain at run time and
  degrades explicitly when a connector or stage skill is unavailable. Facts
  are frozen and verified before any writing happens; nothing ships that
  fails a gate.
---

# CurAItion Daily Drop (Orchestrator)

One invocation produces one publishable issue: the Substack Drop, the
LinkedIn post with its prepared first comment, the IG carousel with caption,
the LinkedIn carousel PDF, and a run report, all delivered to Google Drive.
This skill decides nothing editorial by itself: the canonical spec lives in
GBrain, the stage skills own their crafts, and the human owns the story
choice.

**The one rule that outranks everything: no fabrication.** Every fact is
cited, every citation is verified against its source before a single word of
copy is written, and every gate must pass before delivery. A failed gate
never ships; it escalates.

## Canonical sources (resolve at run start)

Pull these before doing anything else. GBrain is canonical; the bundled
snapshot is the fallback, and using the fallback must be flagged in the run
report.

| Source | What it owns |
|---|---|
| GBrain `curaition/daily-publishing-prompt` | the whole editorial spec: outputs, formats, carousel technical spec, anti-AI-detection rules |
| GBrain `curaition/carousel-slide-density` | slide density rules + canonical reach-ranked hooks |
| GBrain `curaition/the-drop` | the issue log: issue count, published titles/subtitles/captions (the calibration corpus) |
| GBrain `people/ben-oliver-voice` | Ben's register for repost comments (not used for the assets themselves) |
| `references/publishing-spec-snapshot.md` | offline snapshot of the above, dated; use only when GBrain is unreachable |

The daily-content-generator project files (`CurAItion Tone of Voice TOV.docx`,
`Newsletter example TOVs.docx`, the logo files) are the brand substrate the
canonical prompt names as pre-reads; the skills bundle their operational
copies (`_voice/`, carousel assets), so the docx files need re-reading only
when checking for drift.

**If a canonical GBrain page and a stage skill's SKILL.md disagree, the
GBrain page wins.** Note the disagreement in the run report so the skill gets
updated.

## Connectors this run needs

CurAItion MCP (scouting, corpus), GBrain MCP (canonical spec + issue log),
Google Drive MCP (delivery), WebSearch/WebFetch (verification). Optional:
the `curaition_publish_substack` tool on the CurAItion connector (super-admin
principals only) lets Stage 7 create the Substack draft directly. At run
start, check each is present. Missing connector handling:

- No CurAItion → halt before scouting; nothing to scout from. Tell the user.
- No GBrain → run from the snapshot, flag every place the snapshot decided.
- No Google Drive → produce everything locally, deliver files into the
  conversation, and say delivery to Drive did not happen.
- No WebFetch/WebSearch → **halt before writing.** Verification is not
  optional; an unverified issue does not get drafted.

## Staging

All intermediates live in `daily-drafts/<YYYY-MM-DD>/` (the scouts' default).
Slug: kebab-case of the chosen title, e.g. `the-batman-problem`.

## The run

### Stage 0 — Pre-production checks

1. `curaition_get_stats`: confirm domain counts, and the canary check —
   `effective_org_id: null`, `external_safe: true`. A failed canary halts the
   run (library scope is not safe).
2. `curaition_list_content` sorted by published_at descending, limit 20 — the
   recency picture.
3. Read the issue log for the next issue number and the last 7 issues (the
   portfolio context the classifier and writers use).

### Stage 1 — Scout (parallel)

Run **cultural-scout** and **click-bait-scout** as parallel subagents, each
producing its standard story-candidate handoff into the staging folder. The
scouts own the domain sweep (all eligible domains — the canonical prompt's
mandatory 19-domain sweep lives inside their protocols; do not skip it or
let them skip it).

### Stage 2 — Editorial sign-off (the human checkpoint)

Present a shortlist to the user with AskUserQuestion: the top candidate from
each scout (and a strong runner-up if one is close), each with its headline
hypothesis, why-now, surprise factor, and mode. The user picks the story.

Unattended (no answer available, e.g. a scheduled run): pick the candidate
with the stronger corroboration and brand-safety margin, state the choice
and reasoning at the top of the run report, and continue. Never silently
pick.

### Stage 3 — Classify and package

1. **user-needs-classifier** on the chosen candidate (portfolio balance uses
   the last 7 issues from the issue log).
2. **story-packager** consolidates candidate + classification into
   `story-package-<date>.json` (its own validator must pass). `brand_safety:
   unsafe` halts the run, per the packager's rules.

### Stage 4 — Verify (the anti-hallucination gate)

Before any writing. For every fact in the package's `facts[]`, spawn
verification work that:

1. Takes each citation. For a URL: fetch it with **WebFetch** (never curl or
   a script) and ask one question: does this page state or support the
   specific claim? For a CurAItion `content_id`: `curaition_get_content` and
   check the claim against the analysis.
2. Records a verdict per citation — `verified` | `mismatch` | `dead` |
   `unreachable` — and per fact: `verified` (≥1 verified citation) |
   `failed` (all citations dead or mismatched) | `unreachable`.
3. Writes `verification-<date>.json` in the staging folder:

```json
{
  "package": "story-package-<date>.json",
  "verified_at": "<ISO timestamp>",
  "facts": [
    {"fact_id": "f1", "verdict": "verified",
     "citations": [{"url": "https://…", "status": "verified",
                     "note": "states the 90% figure directly"}]}
  ]
}
```

Then run `python scripts/check_verification.py verification-<date>.json
--package story-package-<date>.json`. It must exit 0: every fact covered,
no `failed` fact still in play.

Handling failures: a `failed` fact is removed from the writers' working set
(note it in the run report). If a failed fact is loadbearing for the thesis,
go back to Stage 2 with the second candidate rather than shipping a hollow
story. `unreachable` facts (paywall, timeout) survive only if the fact has
another verified citation; otherwise treat as failed.

Verified URLs become the **link allowlist**: the only URLs any draft may
contain.

### Stage 5 — Render (parallel where possible)

Order matters only where the contract does: the Drop must exist before the
LinkedIn post (subtitle mirror). Carousel and caption can run alongside the
Drop.

1. **substack-writer** → `<slug>-substack-drop.md` (its lint must pass) +
   the paste-ready `<slug>-substack-drop.html` twin (the writer's
   `drop_to_html.py`) — raw markdown pasted into Substack loses links; the
   rendered HTML keeps them.
2. **linkedin-writer** (after 1) → `<slug>-linkedin.md` +
   `<slug>-linkedin-first-comment.md` (lints pass, `--drop` supplied).
3. **carousel-producer** → `carousel-<slug>.json` (slide_lint passes) →
   rendered IG PNGs + LinkedIn PNGs + PDF.
4. **IG caption** → `<slug>-ig-caption.md`: one line, declarative, ends with
   a relevant emoji (`--channel ig-caption` lint).

Every writer works from the package + verification manifest only. A writer
that wants a fact outside the package stops and says so; nobody researches
mid-render.

### Stage 6 — Editor gate (fresh eyes)

Run a **fresh subagent** that has not written any of the assets, with the
rubric: same thesis across all assets; no claim outside `facts[]`; lift never
stated as flat fact; voice against the tone guide and the published corpus
(does this read like Issues 44-51 or like a machine?); carousel hook against
the canonical hooks; caption format. It returns pass, or per-asset notes.

Then the mechanical cross-check:

```
python scripts/cross_check.py daily-drafts/<date>/ --slug <slug>
```

which enforces: LinkedIn line 1 == Drop subtitle; the post ends "Full
breakdown in the comments"; hashtag contracts (post and first comment); Drop
has a subtitle, no sources block, ≤1000 words; every link in every draft is
on the verified allowlist; no em dash or double hyphen anywhere; caption is
one emoji-terminated line; carousel passes density rules.

Failures go back to the owning writer with the notes, **maximum two revision
loops per asset**; a third failure escalates to the user with the draft and
the unresolved notes. Never ship a marginal asset to hit the schedule.

### Stage 7 — Deliver

**Substack draft first (when the tool is in the session).** If the CurAItion
connector exposes `curaition_publish_substack` (super-admin principals only;
`curaition_describe_tools` with `name_filter: "substack"` tells you), the run
creates the Substack draft itself instead of leaving the paste for a human:

1. After the Stage 6 editor gate has passed, call it with `dry_run: true`
   (`title` = the Drop title with its terminal full stop, `subtitle` = the Drop
   subtitle, `body_html` = the paste-ready `<slug>-substack-drop.html`,
   `issue_number` = this issue). It validates and reports block counts
   without creating anything. A validation error here is a real defect in the
   HTML twin (dialect, em dash, double hyphen): fix the draft, do not work
   around it.
2. Same call with `dry_run: false`. It returns the draft editor URL and the
   slug Substack assigned (or a clearly labelled predicted slug). The draft is
   DRAFT only; the tool cannot publish or schedule. Record the editor URL and
   slug in the run report.
3. The LinkedIn first comment must carry the **real** slug: if it differs from
   the `https://curaition.substack.com/p/<slug>` placeholder the
   linkedin-writer used, rewrite `<slug>-linkedin-first-comment.md` with the
   returned slug, re-run `voice_lint.py --channel first-comment`, and say so
   in the run report. If the response says the slug is predicted, keep the
   "confirm the live URL before posting the comment" item in the eyeball
   list.

Failure handling: `ERR_ACCESS_DENIED` with the refresh hint means the stored
Substack session cookie has expired (the expected failure mode; a super-admin
refreshes `SUBSTACK_SESSION_TOKEN` on the Render `mcp-server` service). Any
other non-validation failure is reported verbatim in the run report. In both
cases, and whenever the tool is simply absent from the session, the existing
PASTE-READY flow applies unchanged: the `.html` twin goes to Drive and the
human pastes it; the first comment keeps the placeholder slug and the run
report flags it.

**Instagram publish handoff (when publishing through CurAItion).** The
carousel's route to Instagram is CurAItion's asset pipeline, and the run's
job ends at INGEST — a human presses publish. Verified live on Issue 52:

1. Ingest the 9 rendered slides via multipart
   **`POST /api/assets/prerendered`** on the CurAItion API (slide 1 first;
   `caption` = the IG caption; `hashtags_json` = a JSON array string;
   `X-Organization-ID` header required for API-key callers). This is the
   ONLY correct route: it sets `metadata.prerendered = true`, which is the
   flag the publish renderer checks before preserving artwork — any other
   create path (the generic `/api/assets`, any `curaition_asset_catalog`
   create) omits it and the deck is **silently redrawn** at publish time.
   There is no MCP tool for this endpoint today; call the API directly, or
   leave ingestion to the human when no API access is in the session.
2. **`cta_url` sequencing:** the Substack public URL is baked into the IG
   caption at publish, and the real slug exists only once the Substack post
   is LIVE (the Stage 7 draft is not live). So ingest with `cta_url`
   **null** — never a guessed slug; a wrong link is worse than a missing
   one — and put "set cta_url from the live Substack URL before publishing
   Instagram" in the run report's eyeball list. Order is always: publish
   Substack → set cta_url → publish Instagram.
3. Successful ingest IS the media-spec compliance proof (aspect 0.8–1.91,
   width ≤1440, ≤8MB after JPEG, 2–10 slides — the 1080×1350 canvas is
   0.8000 exactly). Validation runs at ingest only; the publish path never
   re-checks geometry. The asset lands in `review` status and waits
   indefinitely.
4. The publish itself (`POST /api/assets/{id}/publish`) is a **human
   action, never the run's**: `dry_run: false` is live and irreversible,
   and its dry run proves only S3 reachability and slide count, not the
   media spec or the Instagram token. Record the asset id and status in
   the run report; stop there.

**LinkedIn carousel is a manual upload.** There is no automated LinkedIn
publish anywhere downstream (placeholder platform row, no publisher class).
The PDF in Drive is for a human to upload via LinkedIn's document icon —
say so in the run report rather than implying an automated post.

Google Drive: the **"The Drop"** folder inside the **"Output" shared
drive** (folder ID `1H-nlMyc-jWxm13mSMzEn2ckB3N6yIZci` — the ID survived
the move into the shared drive; verify with `get_file_metadata` and ask the
user rather than recreating the folder if it ever stops resolving):

1. Create subfolder `<YYYY-MM-DD>/` under it (skip if it exists).
2. Upload: the Drop (`.md` **and** its paste-ready `.html`), LinkedIn post
   + first comment (`.md`), IG caption (`.txt` or `.md`), all 9 IG PNGs,
   the LinkedIn PDF, the `story-package-<date>.json`,
   `verification-<date>.json`, and `run-report-<date>.md`.
3. Also deliver the four text assets and the run report into the
   conversation so the user can review without opening Drive.

**Binary upload caveat (learned in the 23 Aug dry run):** the Drive MCP
`create_file` base64 path is unreliable for binaries — base64 relayed
through the model gets corrupted. Upload text/JSON via the MCP connector;
for PNGs and the PDF, stage them to the connected computer and upload
through the connected Chrome into the Drive folder, verifying byte sizes
against the source afterwards. If no browser bridge is available, deliver
binaries into the conversation only and say Drive got the text assets.

### Stage 8 — Issue-log writeback

Append the new issue to GBrain `curaition/the-drop`: `get_page` with
`include_content: true`, add the new issue entry at the top of the issue
list (same fields as existing entries: title, subtitle, scout, story
summary, key entities, IG caption), update the "Issues live" count, and
`put_page` the round-tripped content. This keeps tomorrow's run — and the
classifier's portfolio balance — current without anyone editing GBrain by
hand.

### The run report

`run-report-<date>.md`, delivered with the assets:

- which candidate won and why (and, unattended, that the choice was made
  without sign-off);
- verification summary: facts verified / failed / unreachable, with the
  removed facts listed;
- every gate result, every revision loop, anything inferred or degraded
  (snapshot used, connector missing, placeholder Substack URL, Substack
  draft created by the tool or left to the paste flow, and why);
- publish-handoff state: the Substack draft editor URL + slug, the
  CurAItion asset id in `review` (or "not ingested" and why), and the two
  standing human steps — publish Substack then set `cta_url` before the
  Instagram publish; upload the LinkedIn PDF manually;
- what the user should eyeball before posting (the 2-3 highest-risk spots).

## Running without the stage skills

This orchestrator prefers the named skills but does not require them: each
stage's contract is an artifact (story-candidate, user-needs, story-package,
drafts), and any stage whose skill is absent is performed inline from the
artifact contracts and the canonical spec, flagged in the run report. The
one stage that can never be skipped or absorbed silently is Stage 4:
verification is the licence to publish.

## Reference files

- `scripts/check_verification.py` — verification manifest gate (Stage 4).
- `scripts/cross_check.py` — mechanical cross-asset gate (Stage 6).
- `references/publishing-spec-snapshot.md` — dated snapshot of the canonical
  GBrain pages, for offline runs only.

---

*CurAItion Intelligence Desk · Daily Drop orchestrator · scout → sign-off →
package → verify → render → gate → deliver · GBrain is canonical · v1.2*
*Changelog v1.2: Stage 7 gains the Instagram publish handoff, verified live on Issue 52: ingest via `POST /api/assets/prerendered` only (the flag-setting route — any other create path lets the publish renderer silently redraw the deck), `cta_url` null until the Substack post is live (publish Substack → set cta_url → publish Instagram), ingest as the media-spec compliance proof, and the publish call itself always a human action. LinkedIn stated plainly as a manual PDF upload (no automated path exists). Run report now carries the publish-handoff state.*
*Changelog v1.1: Stage 7 creates the Substack draft via `curaition_publish_substack` when the session has it (super-admin only, draft-only), confirms the real slug into the LinkedIn first comment, and falls back to the PASTE-READY flow when absent.*
