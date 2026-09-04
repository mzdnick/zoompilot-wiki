---
title: ECU reset
reviewed: 2026-09
---

# ECU reset (the 15-minute power-down)

A full power-down clears fault state in the car's electronic control
units. When a dashboard error appears, this is the first thing to try,
and it fixes most one-off faults.

## When to use it

- The dashboard throws cruise, LKAS, or radar errors.
- Cruise stays unavailable after you flipped
  [alpha longitudinal](../features/alpha-longitudinal.md) on or off.
- Something behaved oddly right after switching forks or updating.

## The procedure

1. Park, then turn the car **completely off**.
2. Leave it off for **15 minutes**. The wait matters: a short off period
   does not power the ECUs down fully, and the fault state survives.
3. Start the car and drive again. The errors should be gone.

## If the error comes back

A fault that survives an ECU reset, or returns every drive, is not a
one-off. Do not keep resetting and driving. Capture evidence instead:

1. Update to the latest `zoompilot/main` release first.
2. Share a route from that drive, following
   [Share your logs](../troubleshooting.md#share-your-logs).
3. Post the route ID and the exact dashboard message on the
   [Discord](https://discord.gg/jFWkHC2uhh).
