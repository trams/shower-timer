#!/usr/bin/env bash
# Deploy ONLY the static PWA assets to Cloudflare Pages (project: shower-timer).
# Stages files into a temp dir so non-public files (certs, scripts, docs) can
# never be uploaded. Requires `npx wrangler login` to have been run once.
set -euo pipefail
cd "$(dirname "$0")"

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

cp index.html manifest.json sw.js "$STAGE"/
cp -r icons "$STAGE"/

npx --yes wrangler pages deploy "$STAGE" \
  --project-name=shower-timer \
  --branch=main \
  --commit-dirty=true
