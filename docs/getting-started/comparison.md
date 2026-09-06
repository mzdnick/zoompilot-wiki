---
title: Which fork, and why
---

# Which fork, and why

zoompilot is a fork of [sunnypilot](https://github.com/sunnypilot/sunnypilot),
which is a fork of [openpilot](https://github.com/commaai/openpilot).
A fork keeps everything its parent has. So zoompilot keeps every
sunnypilot feature, and adds the Mazda work on top.

This page compares what each project does on a supported Mazda today.
It is the deep version of the
[comparison on zoompilot.ai](https://zoompilot.ai); every zoompilot
row has a measurement record behind it on this wiki.

## Side by side

| Capability | openpilot | sunnypilot | zoompilot |
| --- | :-: | :-: | :-: |
| LKAS + ACC on the 2022-25 CX-5 | ✓ | ✓ | ✓ |
| Unified cruise management (ICBM) | — | ✓ | ✓ |
| Speed-Limit Assist and curve-speed Smart Cruise | — | ✓ | ✓ |
| Speed-dependent torque across seven learned bands | — | — | ✓ |
| EPS-rail-aware limits and cliff-exact friction | — | — | ✓ |
| Torque commands per frame | 10 | 10 | 12 |
| Measured steer-to-zero on the 2022-25 CX-5 EPS | — | — | ✓ |
| Steer-to-zero on an EPS swap, with your car's own specs | — | — | ✓ |
| VIN + EPS fingerprinting (finds a swapped-in motor) | — | — | ✓ |
| Mazda alpha longitudinal | — | — | ✓ experimental |
| Mazda sensors wired in: radar, blind spots, speed signs | — | — | ✓ |
| Mazda alert fixes (LKAS_BLOCK, override hysteresis) | — | — | ✓ |

## What the rows mean

**The shared rows.** Upstream openpilot already drives the 2022-25 CX-5. It caps every steering command at one flat 800 counts, sends at
most 10 commands per frame, and asks for lane keeping only above
25 mph. That envelope is safe, but it belongs to a spec sheet, not to
the measured steering rack in your car.

**The sunnypilot rows.** ICBM, Speed-Limit Assist, and Smart Cruise
are sunnypilot features. zoompilot inherits them and reworks their
Mazda parts — ICBM is rebuilt as a button servo measured against the
real ECU, for example. On an EPS swap, sunnypilot reaches steer-to-zero
one way: select the CX-5 2022-25 platform by hand. That applies the
CX-5 steering ratio, wheelbase, and mass to a car that is not a CX-5.
See [ICBM](../features/icbm.md) and
[Smart Cruise](../features/smart-cruise.md).

**The zoompilot rows.** Everything else comes from measuring the car.
The torque curve follows the EPS's real ceiling, which falls from about
1148 counts in town to 620 on the highway. The seven learned speed
bands replace one setting for all speeds. Fingerprinting reads the VIN
and the EPS firmware, which is how a swapped-in 2022-25 CX-5 EPS motor
gets
recognized — and why the swap row above stays matched to your car's own
specs. See [steering](../features/steering.md) and
[fingerprinting](../technical/mazda-fingerprinting.md).

**Alpha longitudinal** is zoompilot's experimental full cruise control.
While it is on, the stock radar is silenced and AEB is off. That is a
real trade, and it is written down everywhere the feature is. See
[safety](../safety.md).

## What you give up

- **Car coverage.** Upstream supports many makes and models. zoompilot
  supports one brand: the Mazda platforms in its list. Steer-to-zero
  follows the 2022-25 CX-5 EPS, factory-fitted or swapped in; every
  other Mazda in the list runs on its stock motor's envelope. If your
  car is not one of them, run upstream — see
  [supported cars](supported-cars.md).
- **Maturity.** zoompilot is a young fork with a narrow focus. Upstream
  has thousands of car-miles of broad testing that a young fork cannot
  claim.
- **AEB while alpha longitudinal is on.** The radar is the trade. Do
  not run alpha longitudinal if that is not acceptable to you.

## Who should run what

- **Any brand of car** → openpilot. It is the upstream everything else
  builds on.
- **A supported car, and you want ICBM or Smart Cruise** → sunnypilot.
- **A supported Mazda** → zoompilot. Every Mazda in the list runs; the
  2022-25 CX-5 EPS adds steer-to-zero and alpha longitudinal wherever
  it is fitted, factory or swapped. That motor is the case this whole
  wiki measures.

Stock Mazda cruise and lane keeping return as soon as zoompilot is off.
To leave zoompilot, factory-reset the device, or enter another fork's
URL under the custom software option. See [Install](install.md).
