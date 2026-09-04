---
title: Alert fixes
---

# Alert fixes and steering override

These changes remove known false alerts in the Mazda port without
touching real fault handling.

## Place hands on wheel alert (2022+)

Log analysis from many drivers proved that `LKAS_BLOCK` does not actually
disengage steering on 2022+ models. Based on that evidence, zoompilot
disables this false alert.

Real faults stay active. Only the false "place hands on wheel" warning is
suppressed.

## Steering override hysteresis

zoompilot adds the same override filter used by Tesla and Rivian. A
pothole or rough patch no longer trips a phantom takeover request, so the
system does not nag you to hold the wheel after a bump.

## Other upstream alert improvements

These arrive with the sunnypilot and openpilot syncs:

- Softer driver monitoring nags.
- The "openpilot unavailable" flash at startup is fixed.
- The false `NO PANDA` flash on screen wake is gone.
- The bogus "Cruise Fault: Restart the Car" on a cold start is gone. The
  fault alert now fires only when the radar genuinely drops out
  mid-drive. See [Troubleshooting](../troubleshooting.md).
