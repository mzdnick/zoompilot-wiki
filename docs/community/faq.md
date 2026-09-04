---
title: FAQ
hide:
  - toc
---

# Frequently asked questions

Answers to the questions that come up most often. This page will grow —
ask on the [Discord](https://discord.gg/jFWkHC2uhh) if your question is
missing.

## Is my Mazda supported?

zoompilot targets the 2022+ EPS motor. Full support: CX-5 2022–2025
and CX-9 2021–2023. Older Mazdas with a swapped 2022-25 CX-5 EPS motor
are also supported. See [Supported cars](../getting-started/supported-cars.md).

## What hardware do I need?

A comma four and the Mazda harness kit from the
[comma shop](https://comma.ai/shop). The comma 3X works for development,
but the comma four is the supported device. See
[Hardware](../getting-started/hardware.md).

## How much does zoompilot cost?

zoompilot is free and open source. You pay for the hardware: the comma
device and the harness kit.

## How do I install or update zoompilot?

Install from `zoompilot/main` on the device. Every release is prebuilt,
so updates install in minutes, not hours of compiling. zoompilot checks
for updates when it has Wi-Fi. See
[Install](../getting-started/install.md).

## Why do I need a nav SD card?

The LKAS camera reads speed-limit signs through the nav SD card, and map
data powers map-based curve slowdowns. Without it, you lose sign reading
and part of [Speed-Limit Assist](../features/speed-limit-assist.md).

## What happens to AEB with alpha longitudinal?

It is disabled. Alpha longitudinal turns off the car's radar, which takes
automatic emergency braking and forward collision alerts with it. See
[Alpha longitudinal](../features/alpha-longitudinal.md).

## Do fresh installs need tuning?

No. Fresh installs on 2022+ EPS Mazdas arrive with torque control,
self-tune, and speed-dependent self-tune already on. The steering
improves as self-tune learns your motor. See
[First drive](../getting-started/first-drive.md).

## Why does the steering feel different at different speeds?

The EPS behaves differently at low and high speed, so zoompilot learns
separate torque values across seven speed ranges and applies the right
one for your current speed. See
[Steering improvements](../features/steering.md).

## Can I change the set speed with my cruise buttons?

Yes. zoompilot rebuilds the cruise button behavior: the speed you set is
the speed you get back after curves and speed zones. With
[ICBM](../features/icbm.md) you get custom step sizes, and speed-limit
prompts let you confirm with one tap. See
[Settings](../settings/index.md#cruise).

## What is experimental mode?

Experimental mode lets the driving model drive end to end, so the car can
brake for stop signs and lights. It needs zoompilot to control the gas
and brakes, so on Mazda it appears once alpha longitudinal is on.
zoompilot recommends it with alpha longitudinal. See
[Alpha longitudinal](../features/alpha-longitudinal.md).

## I switched forks. Should I factory reset?

Yes, it is recommended. A reset clears stale settings from the previous
fork. See [Install](../getting-started/install.md).

## Does zoompilot upload my drives?

Route logs upload while the device has internet, so maintainers can help
you after an incident. You can turn this off under Settings → Device →
Onroad Uploads. Driver camera and microphone recording are off by
default. See [Settings](../settings/index.md#toggles).

## Will it drain my car's battery?

The device shuts itself down after 30 hours offroad by default. You can
change the limit under Settings → Device → Max Time Offroad. See
[Settings](../settings/index.md#device).

## Is zoompilot affiliated with Mazda, comma.ai, or sunnypilot?

No. zoompilot is a community fork. Mazda, comma.ai, and the sunnypilot
project neither endorse it nor have anything to do with it. See
[About & credits](../about.md).

## How can I help?

Share drives and route IDs on the
[Discord](https://discord.gg/jFWkHC2uhh), report issues, or work on code
and docs. See [How to give feedback](feedback.md) and
[Contribute](contribute.md).
