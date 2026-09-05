# Hardware

## Comma device

zoompilot runs on a **comma 3X** or a **comma four**. A hardware clone
of either also works, but only if the clone is identical. Some clones
omit parts that zoompilot needs, such as a driver monitoring camera.
Those clones are not supported.

The parts list below ships with the comma four.

## What you need for a Mazda

The parts for a supported Mazda are one kit from the
[comma shop](https://comma.ai/shop):

- 1 Mazda connector
- 1 OBD-C cable (2 ft)
- 1 comma four
- 1 comma power v3
- 1 harness box
- 1 mount

## Optional extras

| Item | Why | Needed for |
| --- | --- | --- |
| Nav SD card | Lets the LKAS camera read speed-limit signs and supplies map data | [Speed-Limit Assist](../features/speed-limit-assist.md) sign reading, map-based Smart Cruise |
| Chestnut eGPU | External GPU for big driving models | Large models that no longer fit on-device |

!!! tip "Nav SD card"

    The nav SD card is the cheapest way to unlock features you already
    own hardware for. Speed sign reading through the LKAS camera requires
    it.

## Physical install

comma.ai documents the physical install at
[comma.ai/setup](https://comma.ai/setup). Pick your Mazda model and follow
the harness guide. After the device is mounted and powered, continue with
[Install zoompilot](install.md).
