Overall goal
Build a static web page with javascript which implements a simple bathroom shower stopwatch for Android phone

## UI and basic logic
The top part shows the time elapsed `elapsed_time` in minutes-seconds mm:ss
Seconds are shows only with 15 seconds precision: 00, 15, 30, 45
Every seconds the `:` separator blinks indicating that the stopwatch is active

The time will be shows in one of 3 colors
1. green when `elapsed_time` <= `theshold1`
2. yellow when `threshold1` < `elapsed_time` <= `threshold2`
3. red for `elapsed_time` > `threshold2`

`threshold1` < `threshold2`
For simplicity in the begging we can hard code them to 4 minutes and 8 minutes respectively
(in the next stage we will add an ability to configure)

The bottom part is one button
When the stopwatch is not active the button says "Start" and it starts a stopwatch from zero
(resetting the previous one if needed)
When the stopwatch is active the button says "Stop"

The background is black. We want to use minimal amount of battery. Black should not waste energy
on modern OLED screens

## High level design decisions
1. Use pure javascript for now. Consider a framework later
2. Single static page
3. Android only: do not worry about ios for now
4. Keep the screen on when active
5. (if possible) fullscreen mode
6. Consider PWA

## Fullscreen on Android
```
document.documentElement.requestFullscreen();
// must be called inside a click/tap handler
```

## Keep the screen on
```
let wakeLock = null;
async function keepAwake() {
  wakeLock = await navigator.wakeLock.request('screen');
}
// call from a button tap
```
this might require adding a button. Check whether we can benefit from Start button here

## Alternative to a full screen
From another Claude session
```If you add a web manifest and "install" the page to your home screen as a PWA, it launches in standalone mode (no browser chrome) automatically, which often feels better than calling requestFullscreen() every session. Worth considering depending on the app.```

# Testing
Run a basic python http server on 0.0.0.0 and let me know. I can connect and try
TODO: Research Chrome tools and ability to simulate an Android Chrome locally