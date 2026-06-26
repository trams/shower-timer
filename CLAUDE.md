# Shower Timer

Static PWA stopwatch for Android. No framework, no build step.

## Project state (stage 1 complete)

All core logic is done. See `docs/02_stage1_design.md` for full design notes.

Key files: `index.html` (inline CSS+JS), `manifest.json`, `sw.js`, `icons/`, `serve.py`.

## Running locally

```bash
# Desktop smoke test (no wake lock / PWA install)
python3 -m http.server 8000 --bind 0.0.0.0

# On-phone test (wake lock + PWA — requires HTTPS)
python3 serve.py   # prints LAN URL; accept self-signed cert on Android
```

## WSL2 → Android (same WiFi)
Our WSL is configured with mirroring networking so above commands should work

## Deploying (Cloudflare Pages — Git integration)

Live at **https://shower-timer.pages.dev** (project `shower-timer`, free Cloudflare account).

**Every push to `main` auto-deploys** — the CF Pages project is connected to the GitHub repo
(`trams/shower-timer`), so there is no manual deploy step. PRs/branches get preview URLs.

Build settings (configured in the Cloudflare dashboard, since this is a no-build static site):
- **Framework preset:** None
- **Build command:** `mkdir -p _site && cp index.html manifest.json sw.js _site/ && cp -r icons _site/`
- **Build output directory:** `_site`

The build command stages **only** the static PWA assets into `_site`, so `docs/`, `serve.py`,
and other tracked files are not published. (Certs `cert.pem`/`key.pem` are gitignored, so they
are never in the repo or a deploy.)

> Note: the project is now Git-connected. Cloudflare does not allow Direct-Upload
> (`wrangler pages deploy`) against a Git-connected project, so the old `deploy.sh` no longer
> applies — deploy by pushing to `main`.

Cache note: Pages caches per edge node; a deploy only busts caches at nodes hit
afterward, and `*.pages.dev` has no global purge. If a sensitive file is ever
published, **rotate the secret** (don't rely on cache expiry) — e.g. regenerate
the self-signed cert: `rm cert.pem key.pem` (serve.py recreates them).

## What's next (stage 2)

- Configurable thresholds (currently hardcoded: `THRESHOLD1=240s`, `THRESHOLD2=480s`)
- See `docs/01_initial_iteration_spec.md` for the original spec
