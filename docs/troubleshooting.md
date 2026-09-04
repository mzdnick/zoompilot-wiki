---
title: Troubleshooting
hide:
  - toc
---

# Troubleshooting

Starter fixes for the most common problems. For anything else, ask on the
[Discord](https://discord.gg/jFWkHC2uhh) with your release version and a
route ID.

## Before you troubleshoot

Work through these three steps first. They fix most reports.

1. **Update zoompilot.** Run the latest `zoompilot/main` release. Fixes
   are not backported to older releases.
2. **Check your settings.** Compare against the
   [Settings reference](settings/index.md). In particular, check that
   torque control, self-tune, and speed-dependent self-tune are on, and
   custom tuning is off.
3. **Remove customizations.** If you patched the code or changed fork
   branches, retest on a clean `zoompilot/main` install before you
   report. See [Install](getting-started/install.md).

## Share your logs

Most bug reports need a route. zoompilot records every drive as a route,
and you can share one from [comma connect](https://connect.comma.ai).
This process is adapted from the
[sunnypilot docs](https://github.com/sunnypilot/user-docs) (MIT).

To prepare a route for review:

1. Park where you have Wi-Fi, or a strong hotspot signal, and let the
   device upload. Keep **Onroad Uploads** on (see
   [Settings](settings/index.md#device)).
2. Open [comma connect](https://connect.comma.ai), select the route, and
   open **Files**. Under **All logs**, upload the remaining raw logs and
   wait for the uploads to finish. Reviewers need the complete raw logs.
3. Open **More info** and turn on **Preserved**, so the route is not
   cleaned up.
4. Open **More info**, turn on **Public access**, and copy the **route
   ID**. Post the route ID on the Discord with a short description.

!!! note "Public routes"

    A public route is visible to anyone who has its ID. It contains GPS
    position, speed, and timestamps. Start and end your drives at public
    places, and share only routes you are comfortable making public.

For what the logs contain, see [Logging](how-to/logs.md).

## Dashboard errors (cruise, LKAS, or radar)

If your dashboard throws cruise, LKAS, or radar errors, especially with
[alpha longitudinal](features/alpha-longitudinal.md) on:

1. Turn the car completely off.
2. Leave it off for **15 minutes** so the ECU resets.
3. Drive again.

## "Cruise Fault: Restart the Car" on a cold start

A bug fired this alert falsely on cold starts. It is fixed since
2026.08.25-8: the alert now fires only when the radar genuinely drops out
mid-drive. Update to the latest release. See the
[changelog](releases/changelog.md).

## False "NO PANDA" flash on screen wake

Fixed in the 2026.08 releases. Update zoompilot.

## Wrong speed limits on a km/h car

Reading speed limits on cars set to km/h is fixed since 2026.08.25-8.
Update, and check that the nav SD card is inserted for sign reading. See
[Speed-Limit Assist](features/speed-limit-assist.md).

## Cruise blocked after flipping alpha longitudinal

Alpha longitudinal applies its change at a standstill: zoompilot waits
until you are parked, gives the radar back to the car, and then restarts.
After you turn alpha longitudinal **off**, the radar may need a full
ignition cycle to come back cleanly. If cruise stays unavailable:

1. Park and turn the car fully off.
2. Start it again and drive once with zoompilot not engaged.
3. If the error stays, follow the dashboard-error reset above.

See [Alpha longitudinal](features/alpha-longitudinal.md).

## Weird behavior after switching forks

Factory-reset the device, then install `zoompilot/main` fresh. Stale
settings from a previous fork cause hard-to-explain faults. See
[Install](getting-started/install.md).

## Steering feels weak or wobbly

- Check that torque control, self-tune, and speed-dependent self-tune are
  on, and custom tune is off. See
  [Settings](settings/index.md#steering) and
  [First drive](getting-started/first-drive.md).
- Give self-tune a few drives. Fresh installs start from learned CX-5
  seeds, but your motor still needs some miles.
- CX-9 owners: speed-dependent torque takes longer to learn, because the
  starting seeds come from a CX-5.

## zoompilot will not engage

Check, in order:

1. **Enable zoompilot** is on. It is the master switch under Settings →
   Toggles. It is on by default, but it turns everything passive when
   off.
2. The car is in a state that allows engagement: driver door closed,
   seatbelt on, and stock cruise able to set. See
   [First drive](getting-started/first-drive.md).
3. Your car is supported. zoompilot targets the 2022+ EPS motor. The
   device fingerprints on VIN and EPS firmware; EPS swaps are identified
   by motor firmware. See
   [Supported cars](getting-started/supported-cars.md).
4. The engagement conditions for your model are met. The CX-5 steers
   from 0 mph; stock-radar cars keep their stock stop-and-go limits. See
   [Supported cars](getting-started/supported-cars.md).

## Where to get more help

- [zoompilot Discord](https://discord.gg/jFWkHC2uhh) — post your release
  version, car, and route ID.
- [zoompilot issues](https://github.com/zoompilot/zoompilot/issues)
- [How to give feedback](community/feedback.md)
