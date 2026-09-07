---
title: Glossary
---

# Glossary

Short definitions for the words this wiki uses. Abbreviations shown in
small-caps tooltips across the wiki come from the same list.

## The stack

**openpilot** — the open source driver assistance system by comma.ai.
The base everything here builds on.

**sunnypilot** — a feature-rich fork of openpilot. zoompilot's direct
parent.

**zoompilot** — a Mazda-optimized fork of sunnypilot. See
[What is zoompilot?](../getting-started/what-is-zoompilot.md).

**comma device** — the hardware openpilot runs on: the comma 3
(codename tici), the comma 3X (codename tizi), or the comma four
(codename mici). See [Hardware](../getting-started/hardware.md).

**panda** — the car-interface board inside the comma device. It
enforces the safety model on the wire.

**jungle** — a [panda jungle](https://comma.ai/shop/panda-jungle):
a test board that takes up to six comma devices or pandas, used to
replay recorded CAN traffic into devices.

## Car terms

**ACC** — adaptive cruise control. Keeps a set speed and a gap to the
car ahead.

**counts** — the raw torque units the EPS speaks. The 2022-25 CX-5 EPS
can apply about 1148 counts at neighborhood speeds, falling to 620 on
the highway.

**EPS** — electric power steering. The motor that turns the front
wheels. zoompilot's work is keyed to the 2022–25 CX-5 EPS motor; see
[EPS swap](../technical/eps-swap.md).

**PCM** — powertrain control module. The car's engine and transmission
computer; it executes gas and brake requests.

**MRCC** — Mazda Radar Cruise Control, Mazda's stock adaptive cruise.

**LKAS** — Lane Keeping Assist System, the stock lane centering.

**BSM** — blind spot monitoring.

**AEB** — automatic emergency braking. Disabled while
[alpha longitudinal](../features/alpha-longitudinal.md) is on, because
the radar is off.

**FCW** — forward collision warning. Disabled together with AEB under
alpha longitudinal.

**VIN** — vehicle identification number. zoompilot decodes it to
identify the platform. See
[Mazda fingerprinting](../technical/mazda-fingerprinting.md).

**WMI** — world manufacturer identifier, the first three VIN
characters (JM1, JM3, 3MZ, JM0 on Mazdas).

## How zoompilot drives

**fingerprint** — the identification of your car from VIN and ECU
firmware. Decides what zoompilot is allowed to do.

**steer-to-zero flag** — `STEER_TO_ZERO_EPS`: the flag that marks the
2022-25 CX-5 motor, wherever it is fitted. Unlocks 0 mph steering, the
full torque envelope, and alpha longitudinal.

**torque envelope** — what the EPS may be asked for: 1200/12/12 on the
steer-to-zero motor (scale, units per frame, frame rate), 800/10/25 on
the stock older motor. See
[Mazda lateral](../technical/mazda-lateral.md).

**speed bands** — the seven speed ranges the learner tunes separately,
from parking speeds to highway. See
[How it works](../getting-started/how-it-works.md).

**self-tune** — the background learner that measures your motor's
torque values while you drive. See
[Custom tune](../how-to/custom-tune.md).

**LAF** — lateral acceleration factor. How much torque a unit of
lateral acceleration is worth; the main learned number.

**MADS** — Modular Assistive Driving System: steering can stay engaged
without cruise.

**UEM** — unified engagement mode: one pedal action engages steering
and cruise together.

**ICBM** — Intelligent Cruise Button Management: zoompilot presses
your cruise buttons for you. See [ICBM](../features/icbm.md).

**SLA** — Speed Limit Assist. See
[Speed-Limit Assist](../features/speed-limit-assist.md).

**SCC** — Smart Cruise Control: the curve- and limit-aware cruise speed
planner. See [Smart Cruise](../features/smart-cruise.md).

**op-long** — shorthand for openpilot longitudinal: zoompilot commands
gas and brakes itself instead of the stock radar cruise. The
experimental form is
[alpha longitudinal](../features/alpha-longitudinal.md).

**dashcamOnly** — an upstream status: the car is recognized, but lane
keeping stays off. It clears on supported zoompilot cars.

**alpha longitudinal** — zoompilot's experimental mode: openpilot
drives gas and brakes, the stock radar is off. See
[Alpha longitudinal](../features/alpha-longitudinal.md).

**NNLC** — neural network lateral control. Exists for Mazda, but the
tuned torque controller is the tested path.

## Data

**route** — one drive, as recorded. Identified by an ID like
`5beb9b58bd12b691/0000010a--a51155e496`. Routes open at
[connect.comma.ai](https://connect.comma.ai).

**segment** — a one-minute slice of a route.

**rlog / qlog** — the full log and its small decimated copy. See
[comma's logging docs](https://docs.comma.ai/concepts/logs/).

**qcamera** — the low-resolution video that comma connect plays.

**LKAS_BLOCK** — the Mazda blocking state behind the false
"place hands on wheel" alert on the 2022-25 CX-5 EPS. See
[Alert fixes](../features/alerts.md).

**CRZ_INFO** — the Mazda CAN message (0x21b) that carries the
accelerator command. Central to the
[longitudinal record](../technical/mazda-longitudinal.md).

**DTR** — a community driving model; DTRv6 is a popular pick in the
Models panel. See [First drive](../getting-started/first-drive.md).
