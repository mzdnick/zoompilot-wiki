---
title: Settings
reviewed: 2026-09
---

# Settings

You manage zoompilot from the **Settings** screen on the device. Every
setting appears below as a card, grouped by panel, with each panel's
settings screen for both devices — comma four strips scroll sideways;
comma 3/3X panels are full-frame. Pick a device once and every panel
follows. The capture tool that regenerates these images lives in
[assets/settings](../assets/settings/README.md).

Type in the search bar to filter the cards, or use the chips to show one
panel at a time. Panels with no matches collapse. The card data lives in
`docs/assets/js/settings-data.js` in this wiki's source, kept next to
the release files that define it — see
[Where the defaults come from](#where-the-defaults-come-from).

<div class="device-switch" data-device-switch role="group" aria-label="Which device's settings screens to show">
  <button type="button" data-device="mici" aria-pressed="true">comma four</button>
  <button type="button" data-device="tici" aria-pressed="false">comma 3/3X</button>
</div>

!!! note "Offroad only"

    Most control settings can only be changed while the car is parked
    with the ignition off. Settings that change how zoompilot talks to
    the car take effect on the next drive.

<div id="zp-settings-controls" class="zp-explorer-controls" markdown="0"></div>
<p id="zp-settings-count" class="zp-explorer-count" markdown="0"></p>
<noscript>

The setting cards on this page need JavaScript. Without it, the same
definitions live in the zoompilot source: the
[settings screen definitions](https://github.com/zoompilot/zoompilot/blob/develop/openpilot/sunnypilot/sunnylink/settings_ui.json)
and the
[params keys](https://github.com/zoompilot/zoompilot/blob/develop/openpilot/common/params_keys.h).

</noscript>

## Defaults on a fresh Mazda install

Fresh installs on Mazdas with a 2022-25 CX-5 EPS are not stock
sunnypilot. zoompilot seeds the torque-control stack once, on the first
start:

| Setting | Seeded value |
| --- | --- |
| Enforce Torque Lateral Control | On |
| Self-Tune | On |
| Speed-Dependent Self-Tune | On |
| Torque Control Tune Version | v2.0 |

The seed runs only once, on any Mazda carrying the 2022-25 CX-5 EPS —
factory-fitted or swapped in — because it keys on that motor's
steer-to-zero flag. After it runs, you can turn any of these off and
zoompilot keeps your choice. Everything else starts at the defaults in
the cards below.

A factory reset clears all settings back to these values. See
[Install](../getting-started/install.md).

## Steering

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/steering.png" alt="The Steering settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/steering.png" alt="The Steering settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

Steering settings control lateral (steering) behavior: MADS, lane
changes, and torque tuning. Some of these settings are covered in more
depth on [Steering improvements](../features/steering.md).

<div class="zp-panel-cards" data-panel="Steering"></div>

## Cruise

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/cruise.png" alt="The Cruise settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/cruise.png" alt="The Cruise settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

Cruise settings control speed and distance behavior. See
[Smart cruise](../features/smart-cruise.md) and
[ICBM](../features/icbm.md) for the features behind these settings.

<div class="zp-panel-cards" data-panel="Cruise"></div>

## Models

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/models.png" alt="The Models settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/models.png" alt="The Models settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

Model behavior settings: steering delay, turn speeds, and camera offset.

<div class="zp-panel-cards" data-panel="Models"></div>

## Visuals

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/visuals.png" alt="The Visuals settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/visuals.png" alt="The Visuals settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

Display-only settings. None of them change how the car drives.

<div class="zp-panel-cards" data-panel="Visuals"></div>

## Toggles

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/toggles.png" alt="The Toggles settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/toggles.png" alt="The Toggles settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

Core on/off switches.

<div class="zp-panel-cards" data-panel="Toggles"></div>

## Device

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/device.png" alt="The Device settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/device.png" alt="The Device settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

Device behavior. See [Connect to comma](https://docs.comma.ai/how-to/connect-to-comma/)
for the hardware basics.

<div class="zp-panel-cards" data-panel="Device"></div>

## Software

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/software.png" alt="The Software settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/software.png" alt="The Software settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

<div class="zp-panel-cards" data-panel="Software"></div>

## Developer

<figure class="settings-strip settings-figure-mici" tabindex="0" aria-label="Settings panel screenshot, scrolls sideways">
  <img src="../assets/settings/developer.png" alt="The Developer settings panel on comma four" loading="lazy">
  <figcaption>comma four</figcaption>
</figure>
<figure class="settings-shot settings-figure-tici">
  <img src="../assets/settings/tici/developer.png" alt="The Developer settings panel on comma 3/3X" loading="lazy">
  <figcaption>comma 3/3X</figcaption>
</figure>

Power-user and debug settings. Test-only items are **not for road use**.

<div class="zp-panel-cards" data-panel="Developer"></div>

## Other panels

The comma 3/3X settings screen lists fifteen panels; the comma four
shows a shorter list with the same driving panels. The seven panels
below have no settings a Mazda owner needs to touch, so this page does
not document them row by row, and neither device's capture above covers
them.

| Panel | What it holds |
| --- | --- |
| Network | Wi-Fi and hotspot settings. |
| sunnylink | sunnypilot's backup, restore, and remote configuration. On by default. |
| Display | Screen comfort: onroad brightness, timeouts, screen saver. |
| OSM | Map data management: downloads, updates, region. Feeds the map-based cruise features; their toggles live on the Cruise panel. |
| Vehicle | Forces a platform fingerprint by hand. zoompilot fingerprints the car itself, so a supported Mazda never needs this — it is the old swap workaround, and a forced platform applies the wrong car specs. |
| Trips | Read-only drive stats: drives, distance, hours. |
| Firehose | comma's route-upload program for model training; shows upload activity. |

On a supported Mazda, the defaults stand. Leave the Vehicle panel alone
unless support asks.

## Where the defaults come from

Mazda seeding is one-time, per install, and gated on the steer-to-zero
EPS flag. The card data on this page mirrors the release sources: the
stored settings and their declared defaults live in
[`common/params_keys.h`](https://github.com/zoompilot/zoompilot/blob/develop/openpilot/common/params_keys.h),
and the settings screen definitions in
[`settings_ui.json`](https://github.com/zoompilot/zoompilot/blob/develop/openpilot/sunnypilot/sunnylink/settings_ui.json).
When a release changes either, edit `docs/assets/js/settings-data.js`
to match.
