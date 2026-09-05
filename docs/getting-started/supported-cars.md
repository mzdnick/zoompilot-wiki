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

| Car | Status | Notes |
| --- | --- | --- |
| CX-5 2022–2025 | Full support, primary target | Every zoompilot feature. Steering works down to 0 mph. |
| CX-9 2021–2023 | Full support | Runs on the stock steering envelope with its own factory-matched specs. The 2022-25 CX-5 EPS swap adds steer-to-zero and alpha longitudinal. Speed-dependent torque needs more learning time, because the starting seeds come from a CX-5. |
| Older Mazdas with a swapped 2022-25 CX-5 EPS motor | Supported | The motor is identified by its firmware during fingerprinting. Steering works down to 0 mph, and alpha longitudinal is enabled — radar and AEB off while it is on. |
| CX-5 2017–2021 | Supported | Runs on the stock steering motor and its stock envelope. No steer-to-zero until a 2022-25 CX-5 motor is swapped in. |
| CX-9 2016–2020 | Supported | Stock motor and stock envelope, like the CX-5 2017–2021 row. No steer-to-zero on the stock motor. |
| Mazda 3 2017–2018 | Reported working | Community drives report it runs on the stock motor. Fewer test miles than the CX-5 and CX-9 rows. |
| Mazda 6 2017–2021 | Reported working | Community-reported like the Mazda 3 row: stock motor, stock envelope. |

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
