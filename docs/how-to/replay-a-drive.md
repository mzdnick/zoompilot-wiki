# Replay

Replaying is a critical tool for openpilot development and debugging.
A replay simulates a driving session: it publishes the messages logged
during a real drive as if they were live. Use it to inspect a drive,
reproduce a bug, or feed a route into the UI and tools without a car.

The commands below come from an openpilot checkout. They work the same
in a zoompilot checkout. Route names look like
`5beb9b58bd12b691/0000010a--a51155e496`, and you can browse your drives
at [connect.comma.ai](https://connect.comma.ai).

## Setup

Before you replay a remote route, authenticate with your comma account.
This lets the tool download routes from the server:

```bash
python3 openpilot/tools/lib/auth.py
```

## Replaying a route
*Hardware required: none*

Replay the default demo route, or name any route:

```bash
# demo route
openpilot/tools/replay/replay --demo

# one of your routes
openpilot/tools/replay/replay '5beb9b58bd12b691/0000010a--a51155e496'
```

To replay a route you downloaded to disk, point `--data_dir` at the
folder that holds the segment files:

```bash
openpilot/tools/replay/replay '5beb9b58bd12b691/0000010a--a51155e496' \
  --data_dir="/path_to_routes"
```

Useful options (see `replay -h` for all of them):

| Option | What it does |
| --- | --- |
| `-s, --start <seconds>` | start partway into the drive |
| `-x <speed>` | playback speed, 0.2 to 3 |
| `-a` / `-b` | whitelist or blacklist the services to send |
| `--no-loop` | stop at the end instead of looping |
| `--qcam` | load the low-power qcamera video |

To watch the replay in the openpilot UI, keep replay running and start
the UI in a second terminal:

```bash
openpilot/tools/replay/replay <route-name>
cd openpilot/selfdrive/ui && ./ui.py
```

To stream the same messages into plotjuggler instead:

```bash
openpilot/tools/replay/replay <route-name>
openpilot/tools/plotjuggler/juggle.py --stream
```

## Replaying CAN data
*Hardware required: jungle and comma four*

This mode is different: instead of publishing log messages on your PC,
it sends the recorded CAN traffic out over USB, so a real comma device
sees the bus exactly as it looked in the car. This is how you test a
fingerprint or a bug against recorded traffic without driving.

1. Connect a [panda jungle](https://comma.ai/shop/panda-jungle) to your
   PC. The jungle takes up to six comma devices or pandas at once.
2. Connect your comma device (or a spare panda) to the jungle with an
   OBD-C cable.
3. Run the CAN replay. It loops the route over all connected pandas and
   jungles:

```bash
openpilot/tools/replay/can_replay.py <route-name>
```

With no route name, `can_replay.py` uses a default public route. The
device on the jungle boots, fingerprints the replayed car, and runs as
if it were plugged into that car.

## Routes used in these docs

The technical notes cite routes as evidence for each measurement. Those
route IDs are dongle-side segment names in `tools/mazda_long/test_data/`
of the [zoompilot repository](https://github.com/zoompilot/zoompilot),
not public routes, so they cannot be opened at connect.comma.ai. Your
own drives at [connect.comma.ai](https://connect.comma.ai) are public to
your account, and the steps above replay them unchanged.
