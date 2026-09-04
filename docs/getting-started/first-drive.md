---
reviewed: 2026-09
---

# First drive

You can manage almost everything directly on the device. This page walks
through the recommended setup from the zoompilot author, then how to
engage.

## Recommended setup

1. **Factory-reset before installing.** Clear out stale settings from
   previous forks. See [Install](install.md).
2. **Pick a driving model.** The author runs Firehose. DTRv6 is a
   community favorite, and CD210 works well with alpha longitudinal.
3. **Enable self-tune.** Make sure torque control, self-tune, and
   speed-dependent self-tune are on. Fresh installs on 2022+ EPS Mazdas
   already have them on.
4. **Leave custom tune off.** Keep custom tune and manual real-time off.
   The learned values are better than hand tuning.

## Before you engage

- Clean the windscreen in front of the road camera.
- Mount the device high and centered on the windshield.
- Make sure driver monitoring can see your face.
- Read the [safety page](../safety.md). Know how to cancel: brake pedal
  or the cancel button.

## Engaging

zoompilot engages like openpilot: set the cruise with the stock steering
wheel controls while driving above the minimum speed. On 2022+ EPS Mazdas
the minimum speed is 0 mph, so the car can steer from a stop.

What to expect on a first drive:

- Steering should feel confident at low speed and calm on the highway.
  The speed-dependent torque learns your specific motor over the first
  drives.
- Self-tune keeps improving the steering in the background. You do not
  need to touch anything.
- Nags stay honest. zoompilot suppresses the known false alerts, like
  the "place hands on wheel" warning on 2022+ models. See
  [Alert fixes](../features/alerts.md).
- If anything feels wrong, cancel and pull the [troubleshooting
  page](../troubleshooting.md).

## After the drive

Check [community/feedback](../community/feedback.md) to report how the
car drives. Driving feedback with routes attached is the most useful
contribution there is.
