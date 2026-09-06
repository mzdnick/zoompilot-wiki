---
reviewed: 2026-09
---

# Install zoompilot

<div class="zp-build" markdown>
Install URL: `zoompilot/main` <span class="zp-stamp">· build 393a506e61 · 2026-08-25</span>
</div>

!!! warning "Before you install"

    zoompilot is experimental software. You drive the car, follow the law,
    and carry all the risk. Read the [safety page](../safety.md) first.

## Recommended: factory reset first

Factory-reset the device before installing. This clears stale settings
from previous forks and prevents odd behavior after switching.

## Install steps

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

## Watch the install

<details class="zp-demo">
<summary>Two short clips — the setup, the URL, the download</summary>
<figure class="zp-clip">
  <video controls preload="metadata" playsinline src="../assets/demo/install-comma-3-3x.mp4" aria-label="Demo: installing zoompilot on a comma 3/3X"></video>
  <figcaption>comma 3/3X — choose custom software, type the URL, download</figcaption>
</figure>
<figure class="zp-clip">
  <video controls preload="metadata" playsinline src="../assets/demo/install-comma-four.mp4" aria-label="Demo: installing zoompilot on comma four"></video>
  <figcaption>comma four — slide to install custom software, type the URL, download</figcaption>
</figure>
<p>The clips run the real setup wizard. The typed URL and the download are real.</p>
</details>

## Branches

| Branch | URL | What it is |
| --- | --- | --- |
| `main` | `zoompilot/main` | Prebuilt releases. Built ahead of time on a real comma device, so installing does not need an hour of compiling on the device. |
| `develop` | `zoompilot/develop` | Daily work. Less tested; use only if you follow development. |

## What a fresh install enables

On Mazdas with a 2022-25 CX-5 EPS, a fresh install arrives with these
already on:

- Speed-dependent self-tune
- Steer-to-zero steering
- Full range of EPS steering torque

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
