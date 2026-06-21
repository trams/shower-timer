# Stage 1: Design & Implementation Notes

## What was built

A single-page static PWA shower stopwatch. No frameworks, no build step. All app logic
lives in `index.html` (inline CSS + JS); the PWA scaffolding is `manifest.json` and
`sw.js`; `serve.py` provides an HTTPS dev server for on-phone testing.

## File layout

```
index.html              app markup, styles, and logic (inline)
manifest.json           PWA manifest — standalone display, black theme
sw.js                   cache-first service worker (enables install + offline)
icons/
  icon-192.png          home-screen icon (green stopwatch glyph on black)
  icon-512.png
  icon-maskable-512.png safe-zone variant for adaptive icons
serve.py                HTTPS dev server with auto self-signed cert
make_icons.py           one-off icon generator (pure Python, no deps)
.gitignore              excludes cert.pem / key.pem and local settings
```

## Timer logic

- State is a single `startPerf` timestamp (`performance.now()` at Start). Elapsed is
  recomputed from scratch on every tick — not incremented — so the display is immune to
  drift and Chrome's background-tab interval throttling.
- A single **500 ms `setInterval`** drives everything: update display, toggle separator.
- **Display rounding:** seconds are floored to 15 s steps.
  `ss = floor((elapsedSec % 60) / 15) * 15` → values 00, 15, 30, 45.
- **Color thresholds** (hardcoded consts, configurable in a later stage):
  - `THRESHOLD1 = 240 s` (4 min) — green below, yellow above
  - `THRESHOLD2 = 480 s` (8 min) — yellow below, red above
  - Color uses raw elapsed seconds, not the rounded display value.
- **Separator blink:** visibility is toggled each 500 ms tick, producing one full
  on/off cycle per second.

## Battery / display choices

- Black `#000` background — zero emission on OLED panels.
- Font `Courier New` (monospace) with `tabular-nums` to prevent the digits shifting
  width as they change.
- `touch-action: manipulation` + `user-select: none` disable double-tap zoom and text
  selection without blocking single taps.

## Start / Stop button

Start and Stop share a single button (label swaps). The click handler is also the
user-gesture boundary required by two privileged browser APIs:

- `document.documentElement.requestFullscreen()` — enters fullscreen immediately on tap.
  Errors are caught and silently ignored (not all browsers/contexts allow it).
- `navigator.wakeLock.request('screen')` — keeps the screen on while the timer runs.
  Feature-detected (`'wakeLock' in navigator`) and wrapped in try/catch so it degrades
  gracefully on plain HTTP (where the API is unavailable).

Wake lock is re-acquired on `visibilitychange` when `running` is true, because Android
automatically releases it whenever the tab is hidden.

## PWA

Installing to the Android home screen (via "Add to Home Screen") launches the app in
`standalone` mode — no browser chrome, no address bar. This pairs with `requestFullscreen`
for a fully immersive experience.

The service worker (`sw.js`) pre-caches the entire app shell on install and serves it
cache-first, so the app works offline and loads instantly after the first visit.

## Secure context requirement

Wake Lock and Service Workers only work in a **secure context** (HTTPS or `localhost`).
Over a plain `http://LAN-IP` address they silently do nothing. Two options:

1. **`serve.py`** — starts an HTTPS server with a self-signed certificate. Android will
   show a cert warning; tap "Advanced → Proceed" once. Certificate files (`cert.pem`,
   `key.pem`) are git-ignored.
2. **Chrome USB port-forwarding** (`chrome://inspect` → Port forwarding) — forwards
   `localhost:PORT` on the phone to the WSL machine. `localhost` is a secure context with
   no cert warning.

## WSL2 → Android phone (same WiFi)

WSL2 runs behind Windows NAT; its internal IP is not reachable from the WiFi network.
Solution: Windows port proxy forwards a port on the Windows WiFi IP into WSL2.

```powershell
# Run in PowerShell (Admin) on Windows — replace WSL_IP with output of `hostname -I`
netsh interface portproxy add v4tov4 listenport=8443 listenaddress=0.0.0.0 connectport=8443 connectaddress=<WSL_IP>
netsh advfirewall firewall add rule name="WSL2 Shower Timer" dir=in action=allow protocol=TCP localport=8443
```

The WSL2 internal IP changes on reboot; re-run the `portproxy` command each time, or
pin it with a static IP in `.wslconfig`.

## What is deferred (future stages)

- Configurable `threshold1` / `threshold2` via a settings UI
- iOS support
- Sound or vibration alerts at threshold crossings
