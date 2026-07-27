# Installing the CurAItion skills

**Who this is for:** anyone joining the CurAItion editorial workflow. No technical
knowledge needed. If you can install an app and click through a settings menu,
you can do this.

**How long:** about 15 minutes, most of it waiting for a login screen.

---

## What you are installing

A **skill** is a set of instructions that teaches Claude how to do one specific
job the way we do it. You do not run a skill like an app. You just ask Claude for
something, and it picks up the right skill on its own.

There are eleven. You do not need to remember them — this is here so the names
mean something when you see them in a menu.

| Skill | What it does |
|---|---|
| `cultural-scout` | Sweeps our library for the most interesting story of the day |
| `click-bait-scout` | Same job, but for whatever is breaking on the live web right now |
| `user-needs-classifier` | Works out *why* a reader would care about a story |
| `story-packager` | Locks a story down into one agreed brief the writers share |
| `linkedin-writer` | Turns that brief into a LinkedIn post in our voice |
| `substack-writer` | Turns that brief into a Substack "Drop" article |
| `carousel-producer` | Turns a story into Instagram carousel slides |
| `digest` | Builds a full HTML newsletter |
| `gymshark-partner-pulse` | The Gymshark athlete-ecosystem briefing |
| `gymshark-market-pulse` | The Gymshark competitor briefing |
| `curaition-ops` | Internal operations helper |

They chain together — scout, then classify, then package, then write — but **each
one also works entirely on its own.** You never have to run them in order. Ask
for a LinkedIn post and you will get one.

---

## Before you start

You need **three** things. Check all three now; it saves backtracking.

**1. The Claude desktop app.** Download it from
[claude.ai/download](https://claude.ai/download) and sign in with your CurAItion
work email.

> ⚠️ **Read this before you sign in — it is the one mistake that cannot be
> undone.** If you already have *any* Claude account on your work email, sign in
> to that one. Do **not** create a second account, and do not click "Sign up" to
> get around a login problem. Registering a second time against an email that is
> already linked permanently locks the account, and we cannot fix it from our
> side — support has to. If you are stuck at the login screen, use **"Forgot
> password"** on the address you already have. Always. That is the fix, every
> time.

**2. A Claude Pro or Max plan.** Skills work on Free too, but the CurAItion
skills lean on code execution and long documents, so Pro is the realistic floor.
Rick or Ben will confirm which you are on.

**3. Ten minutes where nobody needs anything from you.** There is a login
redirect in step 3 that will fail if you wander off mid-way.

---

## Step 1 — Switch on the two settings that make skills work

Do this at **[claude.ai](https://claude.ai)** in your web browser, not in the
desktop app. Settings live on your account, so anything you change here applies
to the desktop app too.

1. Click your **name or initials**, bottom-left.
2. Click **Settings**.
3. Click **Capabilities**.
4. Turn **ON**: **Code execution and file creation**.
5. Turn **ON**: **Skills**.

Both must be on. **Skills cannot run without code execution** — that is not
optional, it is how they work. If you only turn one on, nothing will happen and
there will be no error message to tell you why.

---

## Step 2 — Install the skills on your account

**You install these yourself, on your own account.** Custom skills are private to
whoever uploads them, so everybody does this once.

### Get the files

Download the eleven `.zip` files from the
[latest release](https://github.com/curaition-xyz/skills/releases/latest), or use
the folder Rick or Ben sends you.

**Do not unzip them.** Claude wants each zip exactly as downloaded. If you
double-click one and upload the folder that comes out, it will be rejected.

### Upload them

For each of the eleven:

1. At claude.ai, click your name → **Settings** → **Customize** → **Skills**.
2. Click **+ Add** (or **+ Create skill**).
3. Choose **upload a zip file**.
4. Pick one `.zip`.
5. Claude reads it and shows the skill's name and description. Confirm.
6. Repeat for the other ten.

It is repetitive. There is no bulk upload. Put a podcast on.

When you are done, all eleven should be listed and toggled **ON**.

> **If you are ever moved onto a Claude Team or Enterprise plan**, this step
> changes: an Organization Owner uploads the eleven once under *Organization
> settings → Skills*, and they appear for everyone automatically. Nobody
> installs anything individually. Until then, the steps above are the way.

---

## Step 3 — Connect CurAItion

This is the step people skip, and then wonder why the scouts return nothing.

**The skills are the instructions. CurAItion is the data.** Without this
connection, `cultural-scout` has no library to sweep and `digest` has nothing to
build a newsletter from. They will not crash — they will just come back
empty-handed, which is more confusing than an error.

1. At claude.ai, go to **Settings** → **Connectors**.
2. Click **Add custom connector**.
3. Paste this address exactly:

   ```
   https://mcp.curaition.xyz
   ```

4. Click **Add**, then **Connect**.
5. A CurAItion login window opens. Sign in with your work email.
6. It returns you to Claude and the connector shows as **Connected**.

> If the login window opens and then hangs, close it and click **Connect**
> again. If it fails a second time, stop and message Rick — do not create a new
> account to get past it. See the warning in *Before you start*.

---

## Step 4 — Check it actually works

Open the **desktop app**. Quit it fully and reopen it first, so it picks up
everything you just changed.

Type this:

> Use the cultural-scout skill to find today's story.

**What good looks like:** it takes a minute or two, tells you it is searching
across domains, and comes back with a handful of story candidates with links you
can click.

**What a problem looks like:**

| What you see | What it means | What to do |
|---|---|---|
| "I don't have access to that skill" | Skills are off, or not installed | Redo Step 1, then check Step 2 |
| It answers instantly from general knowledge, no links | It ignored the skill | Say: *"Use the cultural-scout skill"* explicitly |
| It runs but finds nothing, or mentions no data | CurAItion is not connected | Redo Step 3 |
| Nothing happens at all | The app is stale | Quit the desktop app completely and reopen |

---

## Using them day to day

**You do not need to name the skill.** Ask for what you want and Claude picks:

> - *"What should we post about today?"* → `cultural-scout`
> - *"What's blowing up right now?"* → `click-bait-scout`
> - *"Write the LinkedIn post"* → `linkedin-writer`
> - *"Build me a culture and food digest"* → `digest`

**Name it when you want to be sure.** *"Use the story-packager skill on this"*
removes all doubt. Worth doing when you know exactly what you want.

**You can start anywhere in the chain.** The full run is scout → classify →
package → write, and it produces the most considered result. But if you already
have a story and just want the post, ask for the post. The writer will handle it
and tell you it worked from a rough brief rather than a full package.

**One thing they will never do: make a fact up.** Every claim traces back to a
real source with a link. If a skill cannot support a claim, it says so rather
than filling the gap. If you ever see a number without a source, tell Rick —
that is a bug, not a quirk.

---

## Things worth knowing

**We all write in one voice.** There is a single shared tone-of-voice guide built
into the skills. You do not need to configure it or paste house-style rules into
your prompt.

**British English, no em dashes.** Enforced automatically. If you see American
spelling in an output, that is a bug worth reporting.

**Skills are not shared chats.** Installing them does not give anyone visibility
of your conversations.

**Gymshark work is separate.** The two `gymshark-*` skills use client data and a
different voice. They are deliberately walled off from the CurAItion editorial
skills, and the scouts exclude Gymshark content from our own posts.

---

## If you are stuck

Message Rick or Ben with:

1. Which step number you reached.
2. What you saw on screen, ideally a screenshot.
3. Whether you are in the desktop app or the browser.

**Do not** create a second Claude account, and do not re-register to get past a
login problem. It permanently locks the account and needs Anthropic support to
undo. "Forgot password" is always the right move.

---

<details>
<summary><b>For whoever maintains this</b> (technical — everyone else can stop here)</summary>

### Building the bundles

```bash
cd ~/Projects/skills
python3 scripts/build-bundles.py     # → dist/*.zip, one per skill
python3 scripts/build-bundles.py --check   # validate without building
```

The build checks every skill has a `SKILL.md` whose frontmatter `name:` matches
its folder, since Claude rejects a zip otherwise.

### Why the build step exists

`skills/_voice/` holds **one** copy of the tone-of-voice guide and the voice
lint, shared by the six editorial-chain skills. That works in a repo checkout,
where they reach it as `../_voice/`.

It does not survive packaging: Claude takes one skill folder per zip, so a
packaged skill has no siblings. The build therefore **copies `_voice/` into each
chain skill's bundle**. The repo keeps the single source; the distributable
carries a copy per bundle. Edit `skills/_voice/`, rebuild, and every bundle
updates together.

The skills check `_voice/` inside the folder first, then `../_voice/` beside it,
so one `SKILL.md` works in both layouts. `digest` and the two Gymshark skills are
excluded — they carry their own client voice on purpose.

### Distribution

Cut a GitHub release and attach `dist/*.zip`:

```bash
git tag -a vX.Y.Z -m "CurAItion Skills vX.Y.Z"
git push origin vX.Y.Z
gh release create vX.Y.Z --repo curaition-xyz/skills --notes "…" dist/*.zip
```

The repo is private, so the release is visible to org members only. Someone
outside the GitHub org gets a 404 rather than a login prompt — if a link looks
dead, check their membership before you check the URL.

**Today everyone installs individually**, because custom skills are private to
the account that uploads them. On a Claude **Team or Enterprise** plan that
changes: an *Organization Owner* — the Owner role specifically, not an Admin —
uploads once under **Organization settings → Skills**, where the same page holds
both the **Code execution and file creation** / **Skills** toggles and the
upload. Provisioned skills are then enabled by default for everyone and appear
under each member's *Customize → Skills*. Worth revisiting if the team grows;
eleven manual uploads per person stops being trivial somewhere around the third
hire.

### After changing a skill

Bundles do not auto-update. Rebuild, cut a new release, and tell people which
bundle changed so they re-upload just that one. Batch changes where you can —
nobody wants a re-upload every week.

</details>

---

*CurAItion Intelligence Desk · last updated 27 July 2026*
