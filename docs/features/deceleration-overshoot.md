---
title: Deceleration Overshoot
---

# Deceleration Overshoot (alpha)

Deceleration overshoot is an optional toggle for [Smart Cruise](smart-cruise.md).
It compensates for the Mazda ECU's slow response to a lower set speed.

## The problem it solves

MRCC, the stock Mazda radar cruise, reacts slowly when you ask it for a
lower speed. Before a curve, the car starts braking later than the
planner expects. The car enters the curve too fast.

## What the toggle does

When a slowdown is coming, zoompilot asks for **more deceleration than
the model wants**, earlier. The overshoot makes up for the ECU's lag, and
the car gets the deceleration the curve actually needs.

## Status

This feature is marked alpha. It shipped in the 2026-07-04 release. If
braking into curves feels too strong with it on, turn the toggle off and
report the route in the
[zoompilot Discord](https://discord.gg/jFWkHC2uhh).

## Design details

The publication path from planner to long controller is described in
[Curve and limit speed planning](../technical/scc-curve-planning.md).
