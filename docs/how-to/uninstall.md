---
title: Uninstall
reviewed: 2026-09
---

# Uninstall zoompilot

Two clean ways to leave zoompilot, depending on where you want to end
up.

## Back to stock Mazda

Factory-reset the device. A reset removes all custom software and
clears every setting. The car returns to stock Mazda behavior the next
time you drive.

After a reset, follow comma's setup at
[comma.ai/setup](https://comma.ai/setup) if you want to use the device
again.

## Back to another openpilot fork

On the device, choose the custom software option and enter the other
fork's install URL, the same way you installed zoompilot. See
[Install](../getting-started/install.md) for the steps. The recommended path is still a
factory reset first: stale settings from the previous fork cause
hard-to-explain faults. See
[Troubleshooting](../troubleshooting.md#weird-behavior-after-switching-forks).

## One check after leaving alpha longitudinal

If alpha longitudinal was on, the car's radar was off. After you leave
zoompilot, the radar needs a full ignition cycle to come back cleanly.
If cruise stays unavailable after that, run the
[ECU reset](../how-to/ecu-reset.md) and try again.
