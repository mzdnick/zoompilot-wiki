---
title: ECU reset
reviewed: 2026-09
---

# ECU reset

A full power-down clears fault state in the car's electronic control
units. When a dashboard error appears, this is the first thing to try.
Start with a short power-down: it clears most one-off faults.

## When to use it

- The dashboard throws cruise, LKAS, or radar errors.
- Cruise stays unavailable after you flipped
  [alpha longitudinal](../features/alpha-longitudinal.md) on or off.
- Something behaved oddly right after switching forks or updating.

## The procedure

1. Park, then turn the car **completely off**.
2. Leave it off for **one minute**, then start the car and drive again.
   A short power-down clears most one-off faults.
3. If the error is still there, park and turn the car off again, this
   time for **15 minutes**. Some faults survive a short power-down and
   clear only once the car has sat long enough for its modules to shut
   down fully. The radar fault that [alpha
   longitudinal](../features/alpha-longitudinal.md) can latch is one of
   them; the mechanism is on the
   [technical notes](../technical/mazda-longitudinal.md#fsc-settle-gate).

## If the error comes back

A fault that survives an ECU reset, or returns every drive, is not a
one-off. Do not keep resetting and driving. Capture evidence instead:

1. Update to the latest `zoompilot/main` release first.
2. Share a route from that drive, following
   [Share a route](../troubleshooting.md#share-a-route).
3. Post the route ID and the exact dashboard message on the
   [Discord](https://discord.gg/jFWkHC2uhh).
