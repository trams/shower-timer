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

WSL2 is not directly reachable from the phone. Run this on **Windows (PowerShell Admin)**
after every WSL restart (WSL IP changes on reboot):

```powershell
netsh interface portproxy add v4tov4 listenport=8443 listenaddress=0.0.0.0 connectport=8443 connectaddress=<WSL_IP>
netsh advfirewall firewall add rule name="WSL2 Shower Timer" dir=in action=allow protocol=TCP localport=8443
```

Get current WSL IP: `hostname -I | awk '{print $1}'`

## What's next (stage 2)

- Configurable thresholds (currently hardcoded: `THRESHOLD1=240s`, `THRESHOLD2=480s`)
- See `docs/01_initial_iteration_spec.md` for the original spec
