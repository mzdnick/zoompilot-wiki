---
title: Alpha longitudinal
reviewed: 2026-09
---

# Alpha longitudinal (work in progress)

Alpha longitudinal lets openpilot take full control of the gas and
brakes, instead of Mazda's stock radar cruise.

<div class="diagram">
<svg viewBox="0 0 800 190" role="img" aria-label="Stock radar cruise versus alpha longitudinal: stock runs radar to PCM with AEB active; alpha runs the vision model and long planner to the PCM with the radar off">
  <defs>
    <marker id="zp-arrow" class="m-dim" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
    <marker id="zp-arrow-a" class="m-acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
  </defs>
  <line class="d-lane" x1="95" y1="12" x2="95" y2="178"/>
  <text x="20" y="51">stock</text>
  <text x="20" y="136">alpha</text>
  <rect class="d-box-stock" x="130" y="29" width="130" height="44"/>
  <text class="d-hi" x="195" y="47" text-anchor="middle">radar</text>
  <text x="195" y="62" text-anchor="middle">AEB · FCW live</text>
  <line class="d-flow" x1="260" y1="51" x2="376" y2="51"/>
  <rect class="d-box-stock" x="380" y="29" width="160" height="44"/>
  <text class="d-hi" x="460" y="47" text-anchor="middle">PCM</text>
  <text x="460" y="62" text-anchor="middle">gas · brakes</text>
  <text x="580" y="55">AEB stays armed</text>
  <rect class="d-box" x="130" y="114" width="130" height="44"/>
  <text class="d-hi" x="195" y="132" text-anchor="middle">vision model</text>
  <text x="195" y="147" text-anchor="middle">drives end to end</text>
  <line class="d-flow-accent" x1="260" y1="136" x2="296" y2="136"/>
  <rect class="d-box-accent" x="300" y="114" width="170" height="44"/>
  <text class="d-hi" x="385" y="132" text-anchor="middle">long planner</text>
  <text x="385" y="147" text-anchor="middle">zoompilot alpha</text>
  <line class="d-flow-accent" x1="470" y1="136" x2="536" y2="136"/>
  <rect class="d-box" x="540" y="114" width="130" height="44"/>
  <text class="d-hi" x="605" y="132" text-anchor="middle">PCM</text>
  <text x="605" y="147" text-anchor="middle">gas · brakes</text>
  <rect class="d-box-stock" x="700" y="114" width="84" height="44"/>
  <text class="d-red" x="742" y="132" text-anchor="middle">radar</text>
  <text class="d-red" x="742" y="147" text-anchor="middle">off</text>
  <line class="d-redline" x1="706" y1="156" x2="778" y2="116"/>
</svg>
</div>

!!! danger "Safety features disabled"

    If alpha longitudinal is enabled, **the car's radar is turned off**.
    Automatic Emergency Braking (AEB) and Forward Collision Alerts are
    **DISABLED** while alpha longitudinal is on.

    If this trade-off is not acceptable to you, do not enable alpha
    longitudinal.

Credit: Alex Frutkin
([@yummydirt](https://github.com/yummydirt)) did the reverse engineering
and implementation for this feature.

## What changes with alpha longitudinal

- openpilot controls acceleration and braking end to end.
- Cruise features such as [Smart Cruise](smart-cruise.md) and
  [Speed-Limit Assist](speed-limit-assist.md) work the same way as with
  the stock radar.
- In experimental mode, zoompilot uses the openpilot model end to end and
  can brake for stop signs and lights.

## Known limitations

- **Experimental models do not often accelerate to the set speed.**
- **Stop and go is improved but not totally fixed.** Cruise may
  disengage after stopping for a lead car.
- **Expect dash errors and safety issues.** This is a work in progress.

## Dash errors while on alpha longitudinal

If your dashboard throws cruise, LKAS, or radar errors, run the
[ECU reset](../how-to/ecu-reset.md), but go straight to the long wait:
park, turn the car completely off for **15 minutes**, then drive again.
A short power-down does not clear this fault.

See also [Troubleshooting](../troubleshooting.md).

## Availability

- CX-5 2022-25: supported since the first zoompilot release.
- Mazdas with a swapped 2022-25 CX-5 EPS, including the CX-9:
  supported since 2026.08.25. A stock CX-9 EPS does not qualify — it
  lacks the steer-to-zero flag.

See [Supported cars](../getting-started/supported-cars.md).

## Design details

The measurement record behind the longitudinal port — radar takeover and
hand-back, the CRZ_INFO checksum, stop-and-go, MRCC state semantics — is
in [Mazda longitudinal](../technical/mazda-longitudinal.md).
