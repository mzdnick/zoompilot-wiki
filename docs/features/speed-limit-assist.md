---
title: Speed-Limit Assist
---

# Speed-Limit Assist (SLA)

Speed-Limit Assist adjusts your cruise speed automatically when you pass
a speed sign. You confirm the change, or let it stick — the behavior is
configurable.

## Where speed limits come from

SLA has two data sources:

- **Speed sign reading** — the LKAS camera reads speed signs. This
  requires a **nav SD card**. See [Hardware](../getting-started/hardware.md).
- **OpenStreetMap data** — speed limits from the map, used with or
  instead of sign reading.

You can add a positive or negative offset, so the car targets a speed
above or below the limit.

## How confirmation works

Confirming a speed limit is one tap, and the answer sticks. While you are
still deciding, a speed limit prompt does not nudge your set speed. This
is part of the unified cruise rewrite: see
[Smart Cruise](smart-cruise.md).

## Metric cars

Reading speed limits on cars set to km/h was fixed in the 2026.08.25
release. See the [changelog](../releases/changelog.md).

## Design details

- The SLA state machine and its interaction with ICBM:
  [Cruise arbiter](../technical/cruise-arbiter.md)
- How SLA publishes targets to the planner:
  [Curve and limit speed planning](../technical/scc-curve-planning.md)
