---
title: Logs and privacy
reviewed: 2026-09
---

# Logs and privacy

zoompilot records every drive. This page says what is recorded, what
leaves the device, and which switches control it. The full sharing
procedure is in
[Share your logs](../troubleshooting.md#share-your-logs).

## What is recorded

A drive is stored as a **route**, cut into one-minute **segments**. Each
segment holds the full internal log (**rlog**), the camera video, and
small **qlog**/**qcamera** copies made for fast upload — the video you
see in [comma connect](https://connect.comma.ai). The file formats are
described in [Logging](logs.md).

## What leaves the device

The device uploads when it has internet, at home Wi-Fi or a hotspot:

| Data | Upload | Controlled by |
| --- | --- | --- |
| qlogs and qcamera video | automatic while **Onroad Uploads** is on | Settings → Device → Onroad Uploads (default **on**) |
| Full raw logs (rlogs) and full video | only when you request it from the route's **Files** page in comma connect | your action, per route |
| Driver camera recording | off by default | Settings → Toggles → Record and Upload Driver Camera |
| Microphone audio | off by default | Settings → Toggles → Record and Upload Microphone Audio |

Turning **Onroad Uploads** off stops automatic uploads. Routes stay on
the device until cleaned up. You can browse and download routes
directly on your network with the **copyparty Service** toggle
(Settings → Developer, needs Show Advanced Controls).

## What a shared route shows

When you make a route public in comma connect, anyone who has its ID
can view it. A route contains **GPS position, speed, and timestamps**,
plus the camera video. It does not contain your name, but a home
address can be obvious from where a drive starts or ends.

Practical rules from the sharing procedure:

- Start and end your drives at public places.
- Share only routes you are comfortable making public.
- Mark a route **Preserved** so cleanup does not remove it while it is
  being reviewed.

Routes you want gone can be deleted from comma connect.

## What zoompilot itself sends

zoompilot adds no telemetry of its own. It is a fork of openpilot, and
it uses the same route logging and the same comma connect services as
upstream. The source is public at
[github.com/zoompilot/zoompilot](https://github.com/zoompilot/zoompilot).
