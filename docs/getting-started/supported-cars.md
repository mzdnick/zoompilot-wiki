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

## Supported Mazda vehicles

| Model | Year | Steer-to-zero | Alpha longitudinal |
| :---: | :---: | :---: | :---: |
| CX-5 | 2022–2025 | ✓ | ✓ |
| CX-5 | 2017–2021 | ✓ with swap | ✓ with swap |
| CX-9 | 2021–2023 | ✓ with swap | ✓ with swap |
| CX-9 | 2016–2020 | ✓ with swap | — |
| Mazda 3 | 2017–2018 | ✓ with swap | ? |
| Mazda 6 | 2017–2021 | ✓ with swap | ? |

- **✓** — works as the car ships.
- **✓ with swap** — works once a 2022-25 CX-5 EPS motor is swapped in.
  See [EPS swap](../technical/eps-swap.md).
- **—** — a hard limit. The pre-2021 CX-9's radar does not publish the
  track data the port stands in for, so alpha longitudinal stays off
  even with the swap.
- **?** — expected to work, not yet validated on that platform. The
  Mazda 3 and Mazda 6 are community-reported only, with fewer test
  miles than the CX-5 and CX-9.

While alpha longitudinal is on, the stock radar and AEB are off.

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
