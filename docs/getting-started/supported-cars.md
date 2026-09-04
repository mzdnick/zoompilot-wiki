---
reviewed: 2026-09
---

# Supported cars

zoompilot runs on any Mazda with the 2022-25 CX-5 electric power
steering (EPS) motor — factory-fitted, or swapped into an older Mazda.
Support depends on which steering motor your car has, not just the model
year.

<div id="zp-car-checker" markdown="0"></div>

## Supported vehicles

| Car | Status | Notes |
| --- | --- | --- |
| CX-5 2022–2025 | Full support, primary target | Every zoompilot feature. Steering works down to 0 mph. |
| CX-9 2021–2023 | Full support | Factory-matched specs included. Speed-dependent torque needs more learning time, because the starting seeds come from a CX-5. |
| Older Mazdas with a swapped 2022-25 CX-5 EPS motor | Supported | The motor is identified by its firmware during fingerprinting. Steering works down to 0 mph, and alpha longitudinal is enabled. |

## How EPS swaps are detected

zoompilot fingerprints your car from the VIN first, then from the EPS
firmware. The EPS fingerprint tells zoompilot whether the car can steer to
zero. This is how an older Mazda with a swapped motor gets full steering.
The design notes are in
[Mazda fingerprinting](../technical/mazda-fingerprinting.md).

## Upstream support tables

For the upstream compatibility table and required harness parts per car,
see [`docs/CARS.md`](https://github.com/zoompilot/zoompilot/blob/develop/docs/CARS.md)
in the zoompilot repository. It follows the openpilot support table format.

!!! note "Not sure about your car?"

    Ask in the [zoompilot Discord](https://discord.gg/jFWkHC2uhh). Include
    your model year and, if you can, whether the EPS motor is original.
