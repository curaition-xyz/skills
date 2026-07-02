# Activation Format — "What We're Watching Next"

The "What We're Watching Next" (Partner Pulse) and "What We're Tracking Next" (Market Pulse) sections must be activation-ready — not passive observation lists. Every forward-looking signal must give the reader something they can DO, not just something to "watch."

## The Three-Part Format (MANDATORY)

Each signal must contain all three components:

### 1. The Signal (What + When + Trigger)

A specific, measurable observation with a clear time-bound trigger condition. Not "monitor X" — instead: "If X is still doing Y by [date], then Z."

**Good:**
> If Kyanfitt's vulnerability-led content scales beyond 20 items by Issue #3 (April 6), it validates a new athlete archetype worth recruiting against.

**Bad:**
> We'll continue to monitor vulnerability content trends across the ecosystem.

### 2. The Prompt (Copy-Paste CurAItion Query)

A ready-to-run query the reader can paste into Claude (with CurAItion MCP access) to investigate the signal further right now. Present in a styled code block.

```
Ask Claude: "Using CurAItion, search the Gymshark Partner Ecosystem
(org_id: 297e242a, project_id: 83472bde) for all content where 'mental health'
or 'vulnerability' appears as a theme in the last 14 days. Show me the top 10
by engagement with source links and which athletes created them."
```

**Rules for prompts:**
- Include the org_id and project_id (abbreviated) so the query is self-contained
- Specify the exact data the reader should ask for (themes, entities, time window)
- Keep under 4 lines
- Make them genuinely useful — not performative

### 3. The Brief Starter (Executable Creative Idea)

A 3-5 line creative concept that could be turned into a brief, RFP, or format experiment. Include: format, talent, timing, and one specific hook.

**Example:**
> **Format:** 4-part Instagram carousel series — "The Real Reason I Train"
> **Talent:** Kyanfitt + Abbie Dennison + 2 athletes from the rising cohort
> **Hook:** Each athlete shares their non-physical motivation in a 15-second talking-head clip. No product shots. Raw audio. Gymshark logo only in the final frame.
> **Timing:** Post Monday 7am when mental-health content engagement peaks.
> **Measure:** Compare engagement rate vs standard product carousel over 7 days.

**Rules for brief starters:**
- Must be specific enough that a creative team could start work from it
- Must reference a specific athlete, format, or content pattern from the data
- Must include a timing or trigger condition
- Must include a success metric (even if rough)
- Should feel like "I wish I'd thought of that" not "I already know this"

## HTML Template

```html
<h3>Signal [N]: [Title]</h3>

<p>[The Signal — 2-3 sentences with specific data point and trigger condition]</p>

<div class="callout">
  <div class="callout-label">Run This Now</div>
  <p class="callout-text" style="font-family: monospace; font-size: 13px;">
    Ask Claude: "[CurAItion query the reader can copy-paste]"
  </p>
</div>

<p><strong>Brief starter:</strong> [Format] — "[Working title]"<br>
<strong>Talent:</strong> [Specific athletes or creator types]<br>
<strong>Hook:</strong> [The specific creative angle]<br>
<strong>Timing:</strong> [When to publish and why]<br>
<strong>Measure:</strong> [What success looks like]</p>
```

## What NOT To Do

```html
<!-- WRONG: Passive observation -->
<p>We'll continue to monitor trends in vulnerability content across the ecosystem.</p>

<!-- WRONG: Generic advice -->
<p>Consider leveraging this trend in upcoming campaigns.</p>

<!-- WRONG: No specific data, no prompt, no brief -->
<p>Watch for more mental health content from athletes in the next issue.</p>
```
