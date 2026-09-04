---
title: Tried and rejected
---

# Tried and rejected

Every technical page here carries a **Tried and rejected** section: the
designs that were built, measured, and replaced. They are written down
on purpose. A rejected idea that is not recorded gets rebuilt.

This page collects all 52 of them in one place, grouped by system. Each
entry is one line; the full reasoning, with the routes behind every
number, lives in the linked page. Routes are the CX-5 2022 test car's
unless stated — see [technical notes](index.md) for what route IDs are.

## Steering (lateral)

### Mazda lateral: evidence and design notes

Full record: [mazda-lateral.md](mazda-lateral.md)

- A winddown faster than 12 counts per frame — the EPS still walks at
  12, and the command just runs ahead of the wheel (gap p99 700 to 800
  counts below 20 mph, max 1400).
- A panda `max_rate_down` looser than the controller's — it rejects
  every frame of a driver-override winddown (route 00000148).
- Scaling `STEER_MAX` down at speed to model the EPS ceiling — it
  rescales every sub-saturation command and invalidates the LAF seeds.
  The ceiling is a separate clamp instead.
- Gating non-delivery on the LKAS_BLOCK bit alone — throws away the
  third to a half the EPS still delivers above 4 m/s.
- Releasing the latch on delivery returning — limit-cycles, because a
  zeroed command has no delivery to observe.
- Gating latch entry on `steeringPressed` — one route spent 203 frames
  blocked with the driver steering along with the request.
- A per-ignition cumulative non-delivery budget — falsified in both
  directions: one route reached 6705 non-delivery frames with no fault,
  another faulted on a third of that spend.
- Alerting the moment the latch fires — every rolling manoeuvre becomes
  a chime.

### Fingerprinting: the engine-only fallback

Full record: [mazda-fingerprinting.md](mazda-fingerprinting.md)

- Naming the chassis from the engine firmware alone behind any
  undecodable VIN — it granted lateral on one recognised ECU plus any
  second address on the bus, which is weaker than upstream's generic
  fuzzy match, and it would have accepted a car whose steering hardware
  was never checked. Replaced by the two-ECU fallback, and it is no
  longer reached on an unknown WMI, an invalid VIN, or VIN_UNKNOWN.

## Cruise (longitudinal)

### Mazda longitudinal (alpha long)

Full record: [mazda-longitudinal.md](mazda-longitudinal.md)

- Adopting a quiet radar on the 50 ms alive window — two masters on a
  stock frame gap, then a session request at speed. Adoption waits the
  full guard.
- Gating the two-master block on availability alone — lateral latched
  on with no exit (route 00000057).
- Raising accFaulted during the boot-phase block — a permanent cruise
  fault toast on every start.
- BIT2 as a settle input — pinned the timer for a whole ignition cycle
  on a second CX-5 2022 whose camera latched BIT2 high at boot.
- `check_relay` on the replaced radar addresses — relay_malfunction on
  every boot.
- Deferring the latched unlatch pulse behind silence or a positive
  nudge — no body response until the pulse.
- A second repulse — stock never pulses twice; no attested shape.
- Emitting a pulse on a gas-pedal release — stock does not, and it once
  latched the camera.
- Holding the stop bits against the throttle until motion — an
  out-of-protocol release.
- Slewing the release command up from -1.024, or pre-ramping toward the
  plan — outside the band the camera accepts.
- A lead-distance cap on the breakaway — only 4 of 34 stock breakaways
  had 0x364 occupied. Too thin to size a second knob the plan already
  encodes.
- Tying the advertised lead to engagement, or advertising a fabricated
  stand-in during a vision gap — a 10.25 m ghost at 22 m/s.
- A byte-exact panda check on 0x364 — it dropped every real-lead frame.
- Reporting `cruiseState.standstill` under op-long — deadlocked every
  stop.
- Relaying the camera's TJA mode fields — dash indicators flapped.
- Pressing RES to release a hold under op-long — stock never does
  (0 of 23 stock releases), and it double-writes CRZ_BTNS.

### Cruise arbiter

Full record: [cruise-arbiter.md](cruise-arbiter.md)

- Four modules interpreting the same press across three processes,
  bridged by wall-clock latches sized to the slowest consumer — every
  shipped bug in the stack was a single press racing the 20 Hz SLA
  cycle, the reconcile window, or the servo state. The phase sweeps in
  `test_icbm_sla_session.py` keep it that way.
- Running the non-pcm session machine in plannerd at 20 Hz — the
  confirm press's own dash step read as a cluster change and dismissed
  the session it created.
- Capping the plan at the cluster when prompting from idle — numerically
  a no-op, but it relabels the plan source.
- Adopting the dash whenever a press happened — an in-transit dash
  destroyed the baseline the servo was about to restore.
- Letting a `-` dismiss leave the baseline in place — the servo
  restored the old baseline 3 s after the driver pressed "slower" in a
  lower zone.
- Dropping the cap on an op-long dismiss without re-anchoring
  `v_cruise` — one tap in a 45 zone released the car to a 70 baseline.
- Latching dial-to-target while a press is still held — it capped
  drivers dialing past the limit.

### ICBM (button servo)

Full record: [icbm.md](icbm.md)

- Taps at ~9 Hz — the ECU drops presses; net progress is half that of
  5 Hz.
- Planning synthesized holds on the 5 mph grid — forged holds never
  snap; all 149 measured stream-driven steps were 1 mph. The native
  grid timing must not size the actuation lead either.
- A 3.0 s restore quiet window — regret improves by 0.8 points over
  1.0 s, while the speed lost to waiting nearly doubles.
- A deadband against the cruise-source target — it stranded the dash
  1 mph under the setpoint after a dropped press.
- The `preActive` route bypassing the quiet window — the servo chased a
  stale target before card had settled the press's own effects.
- Integrating the overshoot behind a blocked emission — a confirm
  prompt banked a gap for its whole 5 s window and the timeout dumped
  it as a SET- burst (user report 2026-08-29).
- Releasing the lever slowly after the source is back on cruise — the
  residual held the dash down and stalled the restore.
- Keying the quiet timer on the overshoot-adjusted command — pinned at
  zero by the lever's own decay (route 126, 4.1 s of extra braking).
- Restoring on target stillness when a vision lookahead is available —
  it restored between bends and fed the next apex (route 126, 3 of 8
  over-ceiling apexes).
- An immediate walk-back after a genuine driver press — reads as a
  fight (route 126 t=341).

### Curve and limit speed planning

Full record: [scc-curve-planning.md](scc-curve-planning.md)

- The lateral-acceleration-percentile heuristic — it used the model's
  velocity plan, so a planned slowdown lowered the prediction below the
  abort threshold mid-braking.
- Geometric curvature from `position.x/y` — same range bias, worse near
  the car.
- An uncapped bias gain (up to 2.07) — wide per-apex spread past 80 m;
  the replay bought no more apexes and added straight-road limiter
  activity.
- Applying the gain above the fitted band — a perfectly reported
  r = 645 m highway bend read as a corner and walked the dash down
  6 mph for nothing.
- Requiring the raw profile to bind before the corrected one may commit
  — on replay it gives back a third of what the gain bought: at 20 m/s
  a real corner enters the 200 m horizon reading 30% of its curvature,
  and corroboration only arrives inside 120 m.
- A trust discount on far kappa, persistence, and a 120 m horizon for
  the highway false commits.
- Publishing -2.0 on openpilot long — it bypassed `A_CRUISE_MIN`
  through the MPC seed.
- Publishing `a_ego` from the map and SLA sources — map curves and map
  limits never braked the real car on stock ACC.
- Freezing the retained map target's distance at commit time — it
  under-requested more the closer the car got.
- Sizing the stock actuation lead from the 5 mph hold grid — forged
  holds never snap.
