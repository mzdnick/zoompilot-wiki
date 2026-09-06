---
reviewed: 2026-09
---

# Supported cars

zoompilot steers to zero on any Mazda carrying the 2022-25 CX-5
electric power steering (EPS) motor — factory-fitted, or swapped into
an older Mazda. Fingerprinting identifies the motor and turns the
capability on by itself.

zoompilot runs on every Mazda platform in its support list: the CX-5,
the CX-9, the Mazda 3, and the Mazda 6. The steering motor your car
carries sets the steering envelope, not whether zoompilot runs.

<div id="zp-car-checker" markdown="0"></div>

## Supported vehicles

| Model | Year | Native steer-to-zero | Steer-to-zero with swap | Alpha longitudinal | Pre-seeded torque |
| --- | --- | --- | --- | --- | --- |
| CX-5 | 2022–2025 | ✓ | n/a | ✓ | ✓ |
| | 2017–2021 | — | ✓ | ✓ with swap | ✓ with swap |
| CX-9 | 2021–2023 | — | ✓ | ✓ with swap | ✓ with swap |
| | 2016–2020 | — | ✓ | — | ✓ with swap |
| Mazda 3 | 2017–2018 | — | ✓ | ✓ with swap | ✓ with swap |
| Mazda 6 | 2017–2021 | — | ✓ | ✓ with swap | ✓ with swap |

*Radar and AEB are off while alpha longitudinal is on. The pre-2021
CX-9 keeps it off even with the swap: its radar does not publish the
track frames the port stands in for. The Mazda 3 and Mazda 6 rows are
community-reported, with fewer test miles than the CX-5 and CX-9.*

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
