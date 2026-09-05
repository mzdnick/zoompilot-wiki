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
- **Maps** — downloaded map data supplies curve geometry. A map hiccup
  does not trip a false warning.

## Deceleration overshoot

MRCC, the stock radar cruise, is slow to obey a lower set speed: before a
curve the car brakes later than the planner expects and enters the curve
too fast. The optional Deceleration Overshoot toggle compensates — when a
slowdown is coming, zoompilot asks for more deceleration than the model
wants, earlier, so the car gets the deceleration the curve actually needs.

The toggle is marked alpha. If braking into curves feels too strong with
it on, turn the toggle off and report the route in the
[zoompilot Discord](https://discord.gg/jFWkHC2uhh).

## One set speed, one owner

zoompilot rewrote the sunnypilot cruise systems for Mazda so that one
unified system manages your set speed. Speed-limit assist and smart
cruise work the same way whether the stock radar or openpilot has the gas
and brakes. When a curve or speed zone ends, you get back the exact speed
you set.

## Design details

The full design record is in
[Curve and limit speed planning](../technical/scc-curve-planning.md).
