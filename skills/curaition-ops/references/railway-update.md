# Updating Hermes Agent on the Railway Deployment

Step-by-step procedure for upgrading Hermes inside the CurAItion Railway container.

## Environment Constraints

The Railway container (hermes-agent-production-0da7.up.railway.app) has:

| Tool | Available? | Notes |
|------|-----------|-------|
| `hermes update` | ❌ Refuses | `start.sh` stamps `.install_method=docker` on every boot |
| `docker` | ❌ Not installed | Can't pull/restart images from inside |
| `railway` CLI | ⚠️ In npx cache, not on PATH | At `/data/.hermes/home/.npm/_npx/d991ede4b4a6395c/node_modules/@railway/cli/bin/railway`. Requires `railway login` (browser-based) — not practically usable from inside the container. Check Railway variables via the dashboard instead. |
| `gh` CLI | ✅ Available (since GH_TOKEN added) | `GH_TOKEN` is set as a Railway variable. `gh` binary at `/usr/local/bin/gh` (v2.67.0). Works for repo operations, issue/PR management. |
| `ps` / `pgrep` | ❌ Not available | Use `/proc/*/cmdline` scan instead |
| `pip` | ✅ | Works for in-place upgrades |
| `curl` | ✅ | But outbound to GitHub API may time out |

## Container Architecture

- **PID 1**: `python /app/server.py` — Railway admin server (Starlette + reverse proxy)
- **server.py** manages two subprocesses:
  - `hermes gateway` — the messaging gateway (Telegram bot)
  - `hermes dashboard` — the native Hermes web UI on 127.0.0.1:9119
- **Auto-respawn**: server.py monitors the gateway process. On unexpected exit (crash, SIGTERM, OOM kill), it restarts the gateway automatically. A crash-loop guard stops after 5 exits in a window.
- **Persistent volume**: `/data` (RAILWAY_VOLUME_MOUNT_PATH) — survives container restarts. Config, sessions, skills, memories live here.
- **Image layer**: `/app/` and `/opt/hermes-agent/` are part of the image and are rebuilt on redeploy.
- **Template repo**: `curaition/hermes-agent-template` on GitHub, branch `main`. Railway rebuilds on push to main.

## Update Procedure (Ephemeral)

This upgrades the running container but reverts on next Railway redeploy.

### 1. Check current version

```bash
hermes --version
```

Check the latest available version:
```bash
pip index versions hermes-agent 2>&1 | head -5
```

### 2. Upgrade via pip

```bash
pip install --upgrade hermes-agent
```

Verify:
```bash
hermes --version
```

**⚠️ Pitfall: dependency downgrades.** `pip install --upgrade hermes-agent` can downgrade dependencies. For example, upgrading from v0.17.0 to v0.18.0 downgraded `cryptography` from 49.0.0 to 46.0.7 (the new version pins an older range). This is usually safe but worth checking the output for any unexpected downgrades.

### 3. Restart the gateway process

The running gateway still uses the old version. Kill it and server.py will auto-respawn with the new code:

```bash
# Find the gateway PID (exclude slash_worker processes)
for pid in $(ls /proc/*/cmdline 2>/dev/null | sed 's|/proc/||;s|/cmdline||' | grep -E '^[0-9]+$'); do
  cmd=$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null)
  echo "$cmd" | grep -q "hermes gateway" && ! echo "$cmd" | grep -q "slash_worker" && echo "Gateway PID $pid: $cmd"
done

# Kill it
kill <PID>
```

Wait ~5 seconds, then verify the new gateway process appeared:

```bash
for pid in $(ls /proc/*/cmdline 2>/dev/null | sed 's|/proc/||;s|/cmdline||' | grep -E '^[0-9]+$'); do
  cmd=$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null)
  echo "$cmd" | grep -q "hermes gateway" && ! echo "$cmd" | grep -q "slash_worker" && echo "Gateway PID $pid: $cmd"
done
```

### 4. Verify the new version is active

```bash
hermes --version
```

## Making the Upgrade Persistent

The ephemeral pip upgrade reverts on Railway redeploy because the template repo (`curaition/hermes-agent-template`) doesn't pin `hermes-agent` in its `requirements.txt`. The `/app/requirements.txt` only lists admin server deps (starlette, uvicorn, jinja2, etc.).

### From a machine with GitHub access

1. Clone the template repo:
   ```bash
   git clone https://github.com/curaition/hermes-agent-template.git
   cd hermes-agent-template
   ```

2. Add `hermes-agent` to `requirements.txt`:
   ```
   echo "hermes-agent>=0.18.0" >> requirements.txt
   ```

3. Commit and push to main:
   ```bash
   git add requirements.txt
   git commit -m "feat: pin hermes-agent>=0.18.0"
   git push origin main
   ```

4. Railway will auto-rebuild from the push. Verify after rebuild with `hermes --version` inside the container.

### From inside the container (using GH_TOKEN)

With `GH_TOKEN` now set as a Railway variable, the `gh` CLI can be used to make the upgrade persistent from inside the container:

```bash
# Clone, update, push
cd /tmp && gh repo clone curaition/hermes-agent-template
cd hermes-agent-template
echo "hermes-agent>=0.18.0" >> requirements.txt
git add requirements.txt
git commit -m "feat: pin hermes-agent>=0.18.0"
git push origin main
```

## How Hermes Was Originally Installed

The `/opt/hermes-agent/` directory contains the full source tree (pyproject.toml, setup.py, *.py files, egg-info) but hermes-agent is installed as a **regular pip package** at `/usr/local/lib/python3.12/site-packages/` — not as an editable install. The source directory is a build artifact, not the install target. This means `pip install --upgrade` correctly replaces the installed package without conflicting with the source tree.

## server.py Auto-Respawn Details

server.py (`/app/server.py`) uses asyncio subprocess management:

- `GatewayManager` class spawns `hermes gateway` via `asyncio.create_subprocess_exec`
- `_drain()` monitors the process. On unexpected exit:
  - In-band `/restart` (exit code 75) — server.py restarts
  - Crash or OOM — server.py restarts (crash-loop guard: max 5 exits per window)
  - Deliberate `stop()`/`restart()` — no respawn (flagged)
- Killing the gateway process with `SIGTERM` triggers an unexpected-exit respawn
- The gateway PID file (`/data/.hermes/gateway.pid`) is cleared by `start.sh` on every boot
