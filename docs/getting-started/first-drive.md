---
reviewed: 2026-09
---

# First drive

This page walks through the recommended setup from the zoompilot author,
then how to engage.

## Recommended setup

1. **Pick a driving model.** New installs default to Firehose, also
   the author's pick. DTRv6 is a community favorite, and CD210 works
   well with alpha longitudinal.
2. **Trust the learned tune.** Keep self-tune on. Keep custom tune and
   manual real-time off. The learned values are better than hand
   tuning. On Mazdas with a 2022-25 CX-5 EPS, a fresh install already
   has the steering toggles on — see [Install](install.md).

## Before you engage

- Clean the windscreen in front of the road camera.
- Mount the device high and centered on the windshield.
- Make sure driver monitoring can see your face.
- Read the [safety page](../safety.md). Know how to cancel: brake pedal
  or the cancel button.

## Engaging

zoompilot engages like openpilot: set the cruise with the stock steering
wheel controls while driving above the minimum speed. On Mazdas with a
2022-25 CX-5 EPS the minimum speed is 0 mph, so the car can steer from
a stop.

What to expect on a first drive:

- Steering should feel confident at low speed and calm on the highway.
  The speed-dependent torque learns your specific motor over the first
  drives.
- Self-tune keeps improving the steering in the background. You do not
  need to touch anything.
- Nags stay honest. zoompilot suppresses the known false alerts, like
  the "place hands on wheel" warning on a 2022-25 CX-5 EPS. See
  [Alert fixes](../features/alerts.md).
- If anything feels wrong, cancel and pull the [troubleshooting
  page](../troubleshooting.md).

## After the drive

Check [community/feedback](../community/feedback.md) to report how the
car drives. Driving feedback with routes attached is the most useful
contribution there is.
