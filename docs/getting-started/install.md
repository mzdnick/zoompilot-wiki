# Install zoompilot

!!! warning "Before you install"

    zoompilot is experimental software. You drive the car, follow the law,
    and carry all the risk. Read the [safety page](../safety.md) first.

## Recommended: factory reset first

Factory-reset the device before installing. This clears stale settings
from previous forks and prevents odd behavior after switching.

## Install steps

<div class="diagram">
<svg viewBox="0 0 800 130" role="img" aria-label="Install flow: comma device, enter the zoompilot/main URL, download and boot, then first drive">
  <defs>
    <marker id="zp-arrow" class="m-dim" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
    <marker id="zp-arrow-a" class="m-acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
  </defs>
  <rect class="d-box" x="20" y="38" width="150" height="48"/>
  <text class="d-hi" x="95" y="58" text-anchor="middle">comma 3X / 3</text>
  <text x="95" y="74" text-anchor="middle">finish setup</text>
  <line class="d-flow" x1="170" y1="62" x2="246" y2="62"/>
  <rect class="d-box-accent" x="250" y="38" width="210" height="48"/>
  <text class="d-hi" x="355" y="58" text-anchor="middle">custom software</text>
  <text x="355" y="74" text-anchor="middle">zoompilot/main</text>
  <line class="d-flow-accent" x1="460" y1="62" x2="526" y2="62"/>
  <rect class="d-box" x="530" y="38" width="130" height="48"/>
  <text class="d-hi" x="595" y="58" text-anchor="middle">download</text>
  <text x="595" y="74" text-anchor="middle">boot · a few min</text>
  <line class="d-flow" x1="660" y1="62" x2="706" y2="62"/>
  <rect class="d-box-accent" x="710" y="38" width="74" height="48"/>
  <text class="d-hi" x="747" y="66" text-anchor="middle">drive</text>
</svg>
</div>

1. Power on the comma device and finish the standard setup until it asks
   for software.
2. Choose the custom software option.
3. Enter this URL:

    ```
    zoompilot/main
    ```

4. Let the device download and boot the release. The first boot can take
   a few minutes.

That is the whole install. There is nothing to configure on a computer.

## Branches

| Branch | URL | What it is |
| --- | --- | --- |
| `main` | `zoompilot/main` | Prebuilt releases. Built ahead of time on a real comma device, so installing does not need an hour of compiling on the device. |
| `develop` | `zoompilot/develop` | Daily work. Less tested; use only if you follow development. |

## What a fresh install enables

On 2022+ EPS Mazdas, a fresh install arrives with these already on:

- Torque control
- Self-tune
- Speed-dependent self-tune

You can change everything on the device. See
[First drive](first-drive.md) for the recommended settings.

## Switching from another fork

You can enter `zoompilot/main` over an existing fork install. A factory
reset is still the cleaner path. If you already run zoompilot, updates
arrive on their own: the device repoints itself on its next start.

## Next steps

- [First drive](first-drive.md) — recommended settings and first engagement
- [Safety](../safety.md) — read before driving
- [Troubleshooting](../troubleshooting.md) — if something looks wrong
