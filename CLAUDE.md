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

## Deploying (Cloudflare Pages)

Live at **https://shower-timer.pages.dev** (project `shower-timer`, free Cloudflare account).

```bash
npx wrangler login   # once, interactive (browser OAuth)
./deploy.sh          # stages only static assets, then `wrangler pages deploy`
```

`deploy.sh` copies **only** `index.html`, `manifest.json`, `sw.js`, `icons/` into a
temp dir and deploys that. Do NOT `wrangler pages deploy .` from the repo root:
`.assetsignore` is silently ignored for Pages deploys, so it would upload the whole
tree — including the local-only `key.pem` (private TLS key). Keep certs/scripts/docs
out of any deploy.

Cache note: Pages caches per edge node; a deploy only busts caches at nodes hit
afterward, and `*.pages.dev` has no global purge. If a sensitive file is ever
published, **rotate the secret** (don't rely on cache expiry) — e.g. regenerate
the self-signed cert: `rm cert.pem key.pem` (serve.py recreates them).

## What's next (stage 2)

- Configurable thresholds (currently hardcoded: `THRESHOLD1=240s`, `THRESHOLD2=480s`)
- See `docs/01_initial_iteration_spec.md` for the original spec
