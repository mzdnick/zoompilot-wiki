# Changelog

zoompilot release notes. The release channel is `zoompilot/main`; the
site header always shows the current release commit.

<!-- Generated from the site repo's src/data/changelog.js by
     scripts/sync-wiki.mjs (`npm run sync:wiki`). Edit the data file
     there, not this page: manual edits to the releases below are
     lost on the next sync. -->

## 2026.08.25-8 (2026-08-25)

- **Fingerprint Mazdas on VIN and EPS.** Supports more Mazda models more reliably by using the VIN for fingerprinting. EPS fingerprinting determines whether an EPS-swapped car can steer to zero. By [@mzdnick](https://github.com/mzdnick).
- **zoompilot branding in the UI.** By [@mzdnick](https://github.com/mzdnick).
- **Speed-limit assist on metric cars.** Fixed reading speed limits on cars set to km/h.
- **Updated speed-dependent torque seeds.** Refreshed the seeds using my latest learned values. Self-tune may converge a little faster now.
- **Comma 4 toggles for new sunnypilot features.** Screensaver and road edge lane change.
- **Synced sunnypilot as of 2026-08-24.** See the [sunnypilot docs](https://docs.sunnypilot.ai).
  - **Block lane changes at road edge.** Prevents a lane change from activating when the road's edge is detected.
  - **Jerk-aware steering.** A torque controller that tries to solve for jerky steering. This doesn't seem to improve anything for Mazdas; it hurts performance because speed-dependent torque already solves for this.
  - **Support for comma's chestnut eGPU.**
  - The driving path changes color with what the car is doing and keeps its width when you override with gas or steering.
  - The “openpilot unavailable” flash at startup is fixed.
  - New screensaver function.
  - Switching models no longer asks to reset calibration.
  - AGNOS 19.6.
- **Alpha longitudinal only.**
  - Improved stop and go, but not totally fixed. Cruise may disengage after stopping for a lead car.
  - The bogus “Cruise Fault: Restart the Car” on a cold start is gone. The fault alert now only fires when the radar genuinely drops out mid-drive.
  - Fixed canceling cruise whilst braking. Thank you [@mzdnick](https://github.com/mzdnick).
  - Alpha longitudinal enabled on EPS-swapped models (CX-9).

## 2026.08.02-5 — Alpha longitudinal handoff (2026-08-02)

More reliable handoff when you override acceleration with the pedal, and more reliable stop and hold.


## 2026.08.01-4 — First release on the zoompilot channel (2026-08-01)

zoompilot has its own home, its own build, and the biggest batch of changes yet.

- **New home, new install URL.** The fork lives at zoompilot/zoompilot and installs from `zoompilot/main`. If you are already running zoompilot you don't need to do anything: your device repoints itself on its next start.
- **Prebuilt releases.** Every release is built ahead of time on a real comma device, so installing no longer means sitting through the better part of an hour of compiling.
- **Alpha longitudinal on the CX-5.** openpilot can drive the gas and brakes on the 2022+ CX-5. Read section 05 first: it shuts the stock radar down, which takes automatic emergency braking and forward collision alerts with it.
- **Torque control out of the box.** Fresh installs on 22+ EPS Mazdas arrive with torque control, self-tune, and speed-dependent self-tune already on.
- **Fresher steering seeds.** The CX-5 2022 starting values come straight off my car's learned data, so a new install steers like a tuned car much sooner.
- **Cruise buttons, rebuilt.** The speed you set is the speed you get back after every curve and speed zone, down to the exact number. Confirming a speed limit is one tap and the answer sticks. Press a button mid-adjustment and zoompilot hands control straight back. Big changes hold the button down the way you would.
- **Cruise features under one roof.** Speed-limit assist and smart cruise now work the same way whether the stock radar or openpilot has the gas and brakes, and a speed limit prompt no longer nudges your set speed while you are still deciding.
- **Latest sunnypilot and openpilot.** New alert sounds and softer driver monitoring nags. Lane changes arm right away if your blinker is already on. Map-based curve slowdowns are more accurate, map hiccups no longer trip false warnings, the false NO PANDA flash on screen wake is gone, and you can switch software branches from the device screen.
- **Leaner install.** Setup no longer downloads a 1.8GB driving model the device never uses.

## 2026-07-04 — Smart cruise and EPS swaps

Curve slowdowns get usable, and older Mazdas with a 2022+ rack join in.

- **Smart cruise decel overshoot.** New alpha toggle. The Mazda ECU is slow to obey a lower set speed, so this asks for more than the model wants and gets the deceleration the curve needs.
- **ICBM fixes.** Fixed set-speed desync with the stock ECU and the target-chasing oscillation. Button presses are suppressed while you press yours, and pacing adapts to how far the target is.
- **EPS swap support.** 2022+ racks in older Mazdas fingerprint by the rack's firmware and steer to a stop.
- **Upstream sync.** Merged sunnypilot master and the opendbc upstream into zoompilot.

## Upstream release notes

zoompilot syncs from sunnypilot and openpilot. Their release notes live
in the repository:

- [`RELEASES.md`](https://github.com/zoompilot/zoompilot/blob/develop/RELEASES.md) —
  upstream openpilot release notes
- [`CHANGELOG.md`](https://github.com/zoompilot/zoompilot/blob/develop/CHANGELOG.md) —
  upstream sunnypilot changelog

