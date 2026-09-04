---
title: Smart Cruise
reviewed: 2026-09
---

# Smart Cruise (curve speed control)

Smart Cruise reduces your set speed before a curve and resumes your
original speed afterward. It is part of the rebuilt Mazda cruise stack,
together with [ICBM](icbm.md) and
[Speed-Limit Assist](speed-limit-assist.md).

## How it slows for curves

Smart Cruise can use two data sources:

- **Vision** — the driving model estimates the road curvature ahead.
- **Maps** — downloaded map data supplies curve geometry. Map-based
  slowdowns became more accurate in the 2026.08 releases, and map hiccups
  no longer trip false warnings.

The latest releases also improved how the planner publishes its target to
the longitudinal controller, so the requested slowdown arrives in time.

## Deceleration overshoot

The Mazda ECU is slow to obey a lower set speed. The optional
[deceleration overshoot](deceleration-overshoot.md) toggle compensates by
requesting a lower speed than the model wants, earlier.

## One set speed, one owner

zoompilot rewrote the sunnypilot cruise systems for Mazda so that one
unified system manages your set speed. Speed-limit assist and smart
cruise work the same way whether the stock radar or openpilot has the gas
and brakes. When a curve or speed zone ends, you get back the exact speed
you set.

## Design details

The full design record is in
[Curve and limit speed planning](../technical/scc-curve-planning.md).
