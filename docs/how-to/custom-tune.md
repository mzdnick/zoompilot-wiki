---
title: Custom tune
reviewed: 2026-09
---

# Custom tune: what it is, and why it stays off

The Steering panel has three ways to produce torque values: self-tune
(the default), a hand-entered custom tune, and a manual real-time
override. This page explains what each one does, so the settings stop
being a mystery. The short version first:

!!! warning "Recommended off"

    Keep **Enable Custom Tuning** and **Manual Real-Time Tuning** off.
    The learned values are better than hand values on every measured
    axis. See [First drive](../getting-started/first-drive.md).

## The default: self-tune

With torque control, self-tune, and speed-dependent self-tune on,
zoompilot learns your motor while you drive:

- Driving is sorted into **seven speed bands**, and each band gets its
  own learned values. See
  [Steering improvements](../features/steering.md).
- Each band stores two numbers: the **lateral acceleration factor**
  (how much torque a request is worth) and the **friction** (the
  baseline torque that fights the motion).
- The learner only accepts sane results: values are clipped to a band
  around the CX-5 seeds. Fresh installs start from those seeds, so the
  first drive already steers well.
- Learned values are cached on the device and restored on the next
  boot. A cache that fails its checks is thrown out whole, so a bad
  value never half-survives a restart.

The full learner design, with every constant and route, is in
[Lateral tune](../technical/lateral-tune.md).

## What the custom knobs do

| Setting | What it does |
| --- | --- |
| Enable Custom Tuning | Replaces the learned values with two fixed numbers you enter: **Lateral Acceleration Factor** (0.1–5.0, default 2.5) and **Friction** (0.0–1.0, default 0.1). |
| Manual Real-Time Tuning | Forces your fixed values onto every frame, overriding self-tune even while it runs. Needs Enable Custom Tuning. |
| Torque Control Tune Version | Picks the controller generation: v0.0, v1.0, or v2.0. Mazda steer-to-zero cars are seeded with v2.0. Leave it there. |

A fixed tune cannot adapt. It uses one gain and one friction at every
speed, on a motor whose behavior changes with speed — and whose output
scale even steps down at one measured speed. The tuned path rescales
exactly at that step; interpolating plain values across it is measured
at about +18% too much torque below the step and −19% too little above
it. See [Lateral tune](../technical/lateral-tune.md).

There is also a cautionary tale. One hand-tuning attempt raised the
controller gains by 21% and railed the EPS ceiling in the 25–32 mph
band — the exact wobble it was trying to fix — and was reverted. Small
hand changes hit the envelope faster than they feel like they would.

## If you still want to try

1. Enable **Enable Custom Tuning** under Settings → Steering.
2. Set **Lateral Acceleration Factor** and **Friction**. Change one
   value at a time, in small steps.
3. Turn on **Manual Real-Time Tuning** only if you want the values to
   win over self-tune on every frame.

Test on quiet roads. If the steering wobbles, feels heavy, or the
dashboard throws errors, turn custom tuning back off.

## Getting back to stock behavior

Turn **Enable Custom Tuning** off. Self-tune resumes with its cached
values; nothing was lost while custom tuning was on. A factory reset
clears everything back to the seeded defaults (self-tune on,
speed-dependent on, tune version v2.0). See
[Settings](../settings/index.md#defaults-on-a-fresh-mazda-install).
