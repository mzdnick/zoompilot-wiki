# Logging

zoompilot inherits openpilot's logging. A drive is stored as a route of
one-minute chunks called segments. A route starts on the rising edge of
ignition and ends on the falling edge.

This page is about the tools and the file formats. For what uploads and
the privacy switches, see [Logs and privacy](logs-and-privacy.md).

## Where routes live

On the device, routes are stored under `/data/media/0/realdata/`, one
folder per route. [Connecting to the device](connect-to-comma.md) over
SSH gets you there.

Routes also upload to your comma account, where
[connect.comma.ai](https://connect.comma.ai/) plays the video and shows
the drive. When you ask for help in the
[zoompilot Discord](https://discord.gg/jFWkHC2uhh), include the route
name — see [how to give feedback](../community/feedback.md).

comma's [logreader](https://github.com/commaai/openpilot/blob/master/openpilot/tools/lib/logreader.py)
is the Python library for reading logs, and
[openpilot/tools](https://github.com/commaai/openpilot/tree/master/openpilot/tools)
holds the replay and plotting tools. See [Replay](replay-a-drive.md)
for the common cases.

## Log types

For each segment, openpilot records the following log types:

### rlog.zst

rlogs contain all the messages passed amongst openpilot's processes.
See [openpilot/cereal/services.py](https://github.com/commaai/openpilot/blob/master/openpilot/cereal/services.py)
for a list of all the logged services. They're a zstd archive of the
serialized [Cap'n Proto](https://capnproto.org/) messages.

### camera video files

Each camera stream is H.265 encoded and written to its respective file.

* `fcamera.hevc` is the narrow road camera (the main forward camera)
* `ecamera.hevc` is the wide road camera
* `dcamera.hevc` is the cabin camera

### qlog.zst & qcamera.ts

qlogs are a decimated subset of the rlogs. Check out
[openpilot/cereal/services.py](https://github.com/commaai/openpilot/blob/master/openpilot/cereal/services.py)
for the decimation.

qcameras are H.264 encoded, lower res versions of the fcamera.hevc.
The video shown in [comma connect](https://connect.comma.ai/) is from
the qcameras.

qlogs and qcameras are designed to be small enough to upload instantly
on slow internet, yet useful enough for most analysis and debugging.
