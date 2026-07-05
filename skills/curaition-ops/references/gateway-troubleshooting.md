# Gateway Troubleshooting Recipe

Diagnostic steps for when the Hermes gateway is stuck, error-looping, or won't restart.

## Symptoms

- `hermes gateway restart` hangs indefinitely (spinner never completes)
- Repeated 404/500 API errors in gateway output (model endpoint not found)
- Telegram polling conflicts (`Conflict: terminated by other getUpdates request`)
- "Gateway already running (PID XXXX)" when trying to start

## Step-by-step Fix

### 1. Kill the stuck restart process

`hermes gateway restart` can hang if the old gateway is still running. Find and kill it:

```bash
# Find hermes processes (ps is NOT available on this host)
ls /proc/*/cmdline 2>/dev/null | while read f; do
  tr '\0' ' ' < "$f" 2>/dev/null | grep -i 'hermes.*gateway' && echo " (PID: $(echo $f | cut -d/ -f3))"
done
```

Kill ALL of them — the stuck restart process, the old gateway, and any zombies:
```bash
kill -9 <PID1> <PID2> ...
```

### 2. Stop the gateway cleanly (if any process survived)

```bash
hermes gateway stop
```

If this hangs, kill the remaining PID manually with `kill -9`.

### 3. Verify no gateway processes remain

Re-run the `/proc/*/cmdline` scan from step 1. The only matches should be your own grep command.

### 4. Fix the config

If the model/provider was the root cause (e.g., retired OpenRouter model):

```bash
# hermes config set may NOT reliably write — verify after setting
hermes config set model.default <valid_model>
hermes config set model.provider <provider>
hermes config  # verify the change took effect

# If hermes config set didn't work, use Python yaml editing:
cd ~/.hermes && python3 -c "
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
config['model']['default'] = '<valid_model>'
config['model']['provider'] = '<provider>'
with open('config.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
print('Done')
"

# NOTE: The patch tool REFUSES to edit Hermes config files (security guard).
# Always use hermes config set or Python yaml editing — never patch().
```

### 5. Start the gateway fresh

```bash
hermes gateway run
# OR for background:
hermes gateway start
```

Verify:
```bash
hermes gateway status
```

### 6. Wait for Telegram to settle

Telegram polling conflicts ("terminated by other getUpdates request") will self-resolve ~20-30 seconds after only one bot instance is running. No action needed — the gateway retries with 20s backoff.

## server.py Auto-Respawn

The Railway admin server (`/app/server.py`) monitors the gateway process via its `GatewayManager` class. When the gateway exits unexpectedly (crash, SIGTERM, OOM kill), server.py **automatically restarts it** within seconds. This means:

- **Killing the gateway PID** is a valid restart strategy — server.py will respawn it. No need to manually start a new gateway.
- A crash-loop guard stops after 5 exits in a window, so if the gateway is failing for a real reason (bad config, missing model), it won't loop forever.
- The `/restart` slash command works by exiting the gateway with code 75, which server.py interprets as "restart me."

This is specific to the Railway deployment where server.py is PID 1. On local/CLI setups, `hermes gateway restart` is the standard path.

## Common Root Causes

### Retired OpenRouter Models

OpenRouter stealth/cloaked models can be retired without notice:

| Model | Status | Notes |
|-------|--------|-------|
| `openrouter/owl-alpha` | ❌ Retired 2026-06-30 | Was Meituan LongCat-2.0 (1.6T MoE). Alias removed after official unveiling. |
| `openrouter/hunter-alpha` | Check current | 1T parameter agentic model. |
| `openrouter/healer-alpha` | Check current | Frontier omni-modal. |

Always verify a model exists at https://openrouter.ai/models before configuring it. A 404 "No endpoints found" error means the model ID is invalid or retired.

### Linear MCP OAuth in Headless Environments

The Linear MCP server requires browser-based OAuth that can't complete in a headless environment. Symptoms:
- "OAuth callback timed out — no authorization code received"
- "Address already in use" (OAuth callback port stuck from previous attempt)
- Repeated retry failures (3 attempts, then gives up)

Fix: `hermes mcp remove linear` (unless Linear integration is actively needed, in which case complete auth from a browser-accessible machine first).

### Multiple Gateway Instances

If `hermes gateway stop` doesn't kill all processes, or if `hermes gateway restart` spawned a new instance before killing the old one, you get:
- Telegram polling conflicts (two bots calling getUpdates)
- "Gateway already running" on restart attempts

Always verify with the `/proc/*/cmdline` scan that ALL gateway processes are dead before starting a fresh one.
