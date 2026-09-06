# What is zoompilot?

zoompilot is a [Mazda-optimized fork](https://zoompilot.ai) of
[sunnypilot](https://sunnypilot.ai), which is itself a fork of
[openpilot](https://comma.ai) by comma.ai. It runs on a comma device. Its
Mazda work tunes openpilot to what the car's own hardware can actually
do — measured, not assumed.

## What zoompilot changes

zoompilot keeps openpilot's safety model and adds Mazda-specific work.
Today it spans:

1. **Steering** — the full torque curve of the 2022-25 CX-5 EPS, learned
   across seven speed ranges. See [Steering improvements](../features/steering.md).
2. **Cruise** — one unified system owns your set speed: ICBM, Speed-Limit
   Assist, and Smart Cruise. See
   [Radar cruise enhancements](../features/smart-cruise.md).
3. **Sensors** — the forward radar, blind-spot monitors, and speed-limit
   signs are wired into openpilot. See
   [Sensor readouts](../features/sensor-readouts.md).
4. **Alpha longitudinal** — openpilot drives gas and brakes instead of the
   stock radar cruise. Work in progress, with real trade-offs. See
   [Alpha longitudinal](../features/alpha-longitudinal.md).

## Who builds it

zoompilot is a community project. Alex Frutkin
([@yummydirt](https://github.com/yummydirt)) did the reverse engineering
and implementation for alpha longitudinal. Contributors including
[@mzdnick](https://github.com/mzdnick) added VIN and EPS fingerprinting.
The source lives at [github.com/zoompilot/zoompilot](https://github.com/zoompilot/zoompilot).
zoompilot stands on openpilot and sunnypilot. Full credits are on the
[About & credits](../about.md) page.
