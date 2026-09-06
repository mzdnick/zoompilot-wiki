# Install demo recordings

Recorded demos for the [Install guide](../../docs/getting-started/install.md).
Each recording shows the real device setup flow: the user picks custom
software, types `zoompilot/main`, and starts the download.

- `tici-install-demo.mp4` — comma 3 / comma 3X (tici/tizi UI, 2160x1080)
- `mici-install-demo.mp4` — comma four / mici UI (536x240, shown at 3x)

The mp4 files are not committed. They are too heavy for the wiki repo.
Keep them here locally, or upload them to the video host when the wiki
embeds them.

## How the recordings are made

No real device is used. The setup app from an openpilot checkout runs on
this computer, and a driver script feeds it scripted touch input. The
setup app is comma's own first-boot wizard, so the screens match what a
real device shows. The typed URL and the download are real:

- `zoompilot/main` expands to `https://installer.comma.ai/zoompilot/main`.
- The app downloads the real zoompilot installer binary (~2 MB) and
  shows real download progress.

### Software used

- openpilot checkout with a working Python env (pyray). Tested with
  `~/ZCodeProject/openpilot-upstream` (upstream master). The setup
  wizard code in zoompilot's tree is the same flow with older API names,
  so the screens are identical.
- `openpilot/system/ui/tici_setup.py` — comma 3/3X setup wizard.
- `openpilot/system/ui/mici_setup.py` — comma four setup wizard.
- The app's built-in `RECORD=1` mode writes lossless frames to ffmpeg.
  No screen capture is involved; every frame comes from the app itself.

### Input

`run_install_demo.py` replaces the four pyray input calls the UI polls
(`get_touch_position`, `is_mouse_button_pressed/released/down`) with a
scripted pointer. Real mouse input is ignored, so the recording cannot
be disturbed. Typing taps the on-screen keys. The mici keyboard is a
drag-to-select keyboard, so the driver drags to each letter and
releases, exactly like a finger swipe.

## Run

```sh
# comma 3 / 3X — 2160x1080 window at 0.7 scale, 20 fps
python3 contrib/demo/run_install_demo.py tici ~/ZCodeProject/openpilot-upstream

# comma four — 536x240 window at 3x scale
python3 contrib/demo/run_install_demo.py mici ~/ZCodeProject/openpilot-upstream
```

Each run needs internet. The output mp4 path prints at start; pass a
third argument to change it. `/tmp/installer` and `/tmp/installer_url`
are written on success — the driver removes them before each run.

The window needs an active display. If it fails with `Failed to
determine Monitor`, the Mac display is asleep — wake it first
(`caffeinate -u -t 3`), and run long recordings under `caffeinate -d`.

## Shot list

comma 3/3X (tici_setup):

1. Getting started — tap the right-edge arrow
2. Choose Software to Use — pick Custom Software, Continue
3. Custom software warning — swipe to the bottom, Continue
4. Connect to Wi-Fi — Continue without Wi-Fi (internet check passes)
5. Enter URL keyboard — type `zoompilot/main`, tap enter
6. Downloading... — real progress to 100%, window closes

comma four (mici_setup):

1. start
2. slide to install custom software (drag the knob left)
3. caution page — swipe up, next
4. connect to internet — choose software (internet check passes)
5. custom software URL — drag-type `zoompilot/main`, tap enter
6. downloading... — real progress to 100%, window closes

## Decisions and notes

- The demo runs comma's setup wizard, not zoompilot's fork UI, because
  the install flow happens before any fork code runs. This is the same
  app a real device boots into.
- comma 3 (tici) is not yet supported by zoompilot, so the big-UI
  recording stands for the 3X. The setup flow is the same for both;
  only the download resolution differs on a real device.
- The demo skips the low-voltage screen a bench-powered device shows
  first: the driver starts the wizard at the software setup. The
  safety page still carries the advice about powering the device in
  a car.
- The installer download is ~2 MB, so progress reaches 100% in about a
  second on fast internet. The driver holds the window open ~2.5 s
  after the download so the video ends on the finished download screen.
- Suggested post-processing before publishing: trim the first ~1.5 s of
  idle time, add a caption card with the install URL. wiki pages can
  embed short mp4s hosted on Cloudflare Pages (25 MB per file limit) or
  a video host.
