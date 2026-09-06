---
title: EPS swap
reviewed: 2026-09
---

# The EPS swap: a 2022-25 CX-5 steering motor in an older Mazda

zoompilot's steering work is keyed to one part: the electric power
steering (EPS) motor from the 2022–2025 CX-5. Some owners fit that
motor into an older Mazda — a swap. When it is done, zoompilot treats
the car like a 2022-25 CX-5: steering works down to 0 mph, the full
torque envelope opens up, and alpha longitudinal becomes available.

## Why people swap

The older motor holds the car back in three ways:

| | Stock older EPS | Swapped 2022-25 CX-5 EPS |
| --- | --- | --- |
| Minimum steering speed | model-dependent, above 0 | 0 mph |
| Torque envelope | 800/10/25 (the stock openpilot cap) | 1200/12/12, the full curve |
| Alpha longitudinal | not available | available |

For the CX-9 2021 the difference is documented exactly: its stock EPS
firmware (`TC3M-3210X-A-00`) keeps the smaller envelope, and only a
CX-9 with the swapped 2022-25 CX-5 motor gets the full one. The evidence
is in [Mazda fingerprinting](../technical/mazda-fingerprinting.md).

## What this guide does not cover

This page explains **how the software sees a swap**. It does not cover
the mechanical work: which columns fit, wiring, alignment, or torque
specs. That work lives with the swap community — ask in the
[zoompilot Discord](https://discord.gg/jFWkHC2uhh) before you buy
parts. An incorrectly done swap is a steering safety problem before it
is a software question.

## How zoompilot recognizes a swapped car

Identification runs in a fixed order at every startup:

1. **Exact firmware match.** A donor EPS breaks this step on purpose:
   its firmware belongs to the CX-5, not to the car it now sits in.
2. **VIN decode.** The VIN names the chassis through any motor swap.
   For most VINs, this alone identifies the car.
3. **EPS-swap fallback.** Only for export VINs (the JM0 WMI, which
   carries no model year field). It needs two recognized ECUs before
   it trusts the car:
   - an EPS at address `0x730` whose firmware is one of the two
     steer-to-zero versions (`KBST-3210X-A-00` or `KSD5-3210X-C-00`), and
   - an engine ECU at address `0x7e0` whose firmware names exactly one
     Mazda platform.

When the fallback fires, the log names it: *"by engine firmware behind
a steer-to-zero EPS swap"*. A car that passes gets the
`STEER_TO_ZERO_EPS` flag, and everything in the table above follows
from that one flag. The full matching design, including the fallbacks
that were tried and rejected, is in
[Mazda fingerprinting](../technical/mazda-fingerprinting.md).

## After the swap

- **Check recognition.** On the first drive, confirm the device
  recognizes the car. If it does not, or support looks wrong, stop and
  post on the Discord with a route ID (see
  [Share your logs](../troubleshooting.md#share-your-logs)).
- **Expect a learning period.** The self-tune seeds come from a CX-5.
  On any swapped car the learner starts from those and adapts to your
  motor over the first drives. CX-9 owners report the longest
  adaptation; give it miles before judging the feel. See
  [Steering improvements](../features/steering.md) and
  [First drive](../getting-started/first-drive.md).
- **Custom tune stays off.** The learned values beat hand values. See
  [Custom tune](custom-tune.md).
