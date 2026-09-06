#!/usr/bin/env python3
"""Record the zoompilot install demo from an openpilot checkout.

Runs the real comma setup wizard on this computer and feeds it scripted
touch input. The typed URL and the download are real: `zoompilot/main`
expands to https://installer.comma.ai/zoompilot/main and the app
downloads the real installer binary. See README.md in this directory.

Usage:
  run_install_demo.py tici <openpilot-dir> [output.mp4]   # comma 3 / 3X
  run_install_demo.py mici <openpilot-dir> [output.mp4]   # comma four
"""
import os
import sys
import threading
import time
from pathlib import Path

argv = sys.argv[1:]
if not argv or argv[0] not in ("tici", "mici") or len(argv) < 2:
    print(__doc__)
    sys.exit(2)

DEVICE = argv[0]
OPENPILOT_DIR = Path(argv[1]).resolve()
OUTPUT = Path(argv[2]) if len(argv) > 2 else Path(f"/tmp/zp-demo/{DEVICE}-install-demo.mp4")
if not (OPENPILOT_DIR / "openpilot" / "system" / "ui").exists():
    print(f"not an openpilot checkout: {OPENPILOT_DIR}")
    sys.exit(2)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# env must be set before the app modules load
os.environ.setdefault("RECORD", "1")
os.environ.setdefault("RECORD_OUTPUT", str(OUTPUT))
os.environ.setdefault("FPS", "30")
if DEVICE == "tici":
    os.environ.setdefault("BIG", "1")      # 2160x1080 UI
    os.environ.setdefault("SCALE", "0.7")  # window fits the Mac screen
else:
    os.environ.setdefault("SCALE", "3")    # 536x240 UI -> 1608x720
SCALE_MULT = float(os.environ["SCALE"])

sys.path.insert(0, str(OPENPILOT_DIR))

import pyray as rl  # noqa: E402

# ---------------------------------------------------------------- input --
# The UI polls a handful of pyray calls from one thread (MouseState in
# system/ui/lib/application.py). Replace them with a scripted pointer.
# poll_input_events becomes a no-op, so real mouse input is ignored.

INSTALL_URL = "zoompilot/main"


class Pointer:
    """Scripted pointer in logical UI coordinates."""

    def __init__(self):
        self.lock = threading.Lock()
        self.x = 100.0
        self.y = 100.0
        self.down = False
        self.press_ev = False
        self.release_ev = False

    def move(self, x, y):
        with self.lock:
            self.x, self.y = float(x), float(y)

    def glide(self, x, y, dur):
        steps = max(int(dur / 0.008), 1)
        with self.lock:
            sx, sy = self.x, self.y
        for i in range(1, steps + 1):
            t = i / steps
            self.move(sx + (x - sx) * t, sy + (y - sy) * t)
            time.sleep(dur / steps)

    def press(self):
        with self.lock:
            self.press_ev, self.down = True, True

    def release(self):
        with self.lock:
            self.release_ev, self.down = True, False

    def click(self, x, y, hold=0.12):
        self.move(x, y)
        time.sleep(0.08)
        self.press()
        time.sleep(hold)
        self.release()
        time.sleep(0.1)

    def drag(self, x0, y0, x1, y1, dur=0.7, settle=0.2):
        self.move(x0, y0)
        time.sleep(0.15)
        self.press()
        time.sleep(0.1)
        self.glide(x1, y1, dur)
        time.sleep(settle)
        self.release()
        time.sleep(0.3)


PTR = Pointer()


def _poll_input_events():
    pass


def _get_touch_position(slot=0):
    x, y = PTR.x, PTR.y
    if slot != 0:
        return rl.Vector2(0, 0)
    return rl.Vector2(x * SCALE_MULT, y * SCALE_MULT)


def _is_mouse_button_pressed(button):
    if button == 0:
        with PTR.lock:
            if PTR.press_ev:
                PTR.press_ev = False
                return True
    return False


def _is_mouse_button_released(button):
    if button == 0:
        with PTR.lock:
            if PTR.release_ev:
                PTR.release_ev = False
                return True
    return False


def _is_mouse_button_down(button):
    if button == 0:
        with PTR.lock:
            return PTR.down
    return False


rl.poll_input_events = _poll_input_events
rl.get_touch_position = _get_touch_position
rl.is_mouse_button_pressed = _is_mouse_button_pressed
rl.is_mouse_button_released = _is_mouse_button_released
rl.is_mouse_button_down = _is_mouse_button_down

# ------------------------------------------------------- app + geometry --
from openpilot.system.ui.lib.application import gui_app, FONT_SCALE  # noqa: E402

if DEVICE == "tici":
    from openpilot.system.ui import tici_setup as setup_mod  # noqa: E402
    from openpilot.system.ui.tici_setup import SetupState  # noqa: E402
else:
    from openpilot.system.ui import mici_setup as setup_mod  # noqa: E402

if DEVICE == "tici":
    from openpilot.system.ui.widgets.keyboard import (  # noqa: E402
        KEYBOARD_LAYOUTS, CONTENT_MARGIN, SPACE_KEY, ENTER_KEY)

    def key_center(ch):
        """Center of a lowercase key, same math as Keyboard._render."""
        layout = KEYBOARD_LAYOUTS["lowercase"]
        rect_x = rect_y = CONTENT_MARGIN
        rect_w = 2160 - 2 * CONTENT_MARGIN
        rect_h = 1080 - 2 * CONTENT_MARGIN
        h_space = v_space = 15
        row_y_start = rect_y + 300
        key_height = (rect_h - 300 - 3 * v_space) / 4
        key_max_width = (rect_w - (len(layout[2]) - 1) * h_space) / len(layout[2])
        for row_i, keys in enumerate(layout):
            key_width = min((rect_w - (180 if row_i == 1 else 0) - h_space * (len(keys) - 1)) / len(keys), key_max_width)
            start_x = rect_x + (90 if row_i == 1 else 0)
            for i, key in enumerate(keys):
                if i > 0:
                    start_x += h_space
                if key == SPACE_KEY:
                    w = key_width * 3 + h_space * 2
                elif key == ENTER_KEY:
                    w = key_width * 2 + h_space
                else:
                    w = key_width
                if key == ch:
                    return start_x + w / 2, row_y_start + row_i * (key_height + v_space) + key_height / 2
                start_x += w
        raise KeyError(ch)
else:
    # mici keyboard geometry (MiciKeyboard._lay_out_keys, lowercase layer)
    MI_W, MI_H = 536, 240
    BG_W, BG_H = 520, 170
    BG_X, BG_Y = (MI_W - BG_W) / 2, MI_H - BG_H
    COL_PAD, ROW_PADS, TOUCH_OFF = 33, {0: 44, 1: 33, 2: 44}, 10
    STEP_Y = (BG_H - 2 * COL_PAD) / 2

    def _layer_key(layer_rows, row_pads, ch):
        for row_i, row in enumerate(layer_rows):
            pad = row_pads[row_i]
            y = BG_Y + COL_PAD + row_i * STEP_Y + TOUCH_OFF
            for i, key in enumerate(row):
                x = BG_X + pad + i * ((BG_W - 2 * pad) / (len(row) - 1))
                if key == ch:
                    return x, y
        raise KeyError(ch)

    def key_center(ch):
        rows = [
            list("qwertyuiop"),
            list("asdfghjkl") + [" "],
            ["\0"] + list("zxcvbnm") + ["123"],  # caps first, 123 last
        ]
        return _layer_key(rows, ROW_PADS, ch)

    def special_key_center(ch):
        rows = [
            list("1234567890"),
            list("-/:;()$&@\""),
            ["#+="] + list("~.,?!'#%") + ["abc"],
        ]
        return _layer_key(rows, ROW_PADS, ch)


# ------------------------------------------------------------- driving --
T0 = time.monotonic()


def log(msg):
    print(f"[{time.monotonic() - T0:6.2f}s] {msg}", flush=True)


class Driver:
    def __init__(self, setup):
        self.setup = setup

    def active_name(self):
        try:
            w = gui_app.get_active_widget()
        except Exception:
            w = None
        return type(w).__name__ if w is not None else ""

    def wait_for(self, pred, what, timeout=30):
        end = time.monotonic() + timeout
        reported = False
        while time.monotonic() < end:
            try:
                if pred():
                    log(f"ready: {what}")
                    return True
            except Exception as e:
                if not reported:
                    log(f"predicate error in {what}: {e!r}")
                    reported = True
            time.sleep(0.05)
        log(f"TIMEOUT: {what}")
        return False


def run_tici(d):
    s = d.setup
    W, H = 2160, 1080
    MARGIN, BTN_H = 50, 160
    btn_w = (W - MARGIN * 3) / 2
    cont = (MARGIN * 2 + btn_w + btn_w / 2, H - MARGIN - BTN_H / 2)

    # a bench-powered device shows a low-voltage screen first; this demo
    # starts straight at the software setup
    s.state = SetupState.GETTING_STARTED

    time.sleep(1.2)
    log("getting started: next")
    PTR.click(W - 155, H / 2)

    time.sleep(0.45)
    log("software selection: Custom Software")
    PTR.click(W / 2, 90 * FONT_SCALE + MARGIN * 2 + 230 + 30 + 115)
    time.sleep(0.4)
    log("software selection: Continue")
    PTR.click(*cont)

    d.wait_for(lambda: s.state == SetupState.CUSTOM_SOFTWARE_WARNING, "warning page")
    time.sleep(0.5)
    log("warning: fling to bottom")
    # the Continue button only enables while the scroll offset overshoots
    # the content end, so fling hard, then retry-click as it settles
    PTR.drag(700, 800, 700, 150, dur=0.45)
    log("warning: Continue")
    d.wait_for(lambda: _click_through(lambda: s.state == SetupState.NETWORK_SETUP,
                                      lambda: PTR.click(*cont, hold=0.1), gap=0.12, max_clicks=40),
               "warning continued", timeout=20)

    log("network: waiting for internet check, then Continue")
    d.wait_for(lambda: _click_through(lambda: s.state == SetupState.CUSTOM_SOFTWARE,
                                      lambda: PTR.click(*cont, hold=0.1), gap=0.5, max_clicks=40),
               "URL keyboard", timeout=60)

    d.wait_for(lambda: s.state == SetupState.CUSTOM_SOFTWARE and d.active_name() == "Keyboard",
               "keyboard visible")
    time.sleep(0.6)
    log("typing %s" % INSTALL_URL)
    for ch in INSTALL_URL:
        x, y = key_center(ch)
        PTR.click(x, y, hold=0.1)
        time.sleep(0.16)
        log(f"  typed {ch!r}")
    time.sleep(0.5)
    log("submit URL (enter)")
    PTR.click(*key_center(ENTER_KEY), hold=0.2)

    d.wait_for(lambda: s.state == SetupState.DOWNLOADING and s.download_progress >= 100,
               "download complete", timeout=120)
    log(f"download at {s.download_progress}%")
    time.sleep(3.0)
    log("closing")
    for _ in range(40):
        gui_app.request_close()
        if getattr(gui_app, "_window_close_requested", False):
            break
        time.sleep(0.25)


def _click_through(done, action, gap=1.5, max_clicks=20):
    """Click until done(); clicks on a disabled button are no-ops."""
    clicks = 0
    while clicks < max_clicks:
        if done():
            return True
        action()
        clicks += 1
        deadline = time.monotonic() + gap
        while time.monotonic() < deadline:
            if done():
                return True
            time.sleep(0.1)
    return False


def _scroller_at_end(page, tol=6.0):
    """True when a mici horizontal scroller rests at its last card."""
    try:
        sc = page._scroller  # Scroller wrapper's inner _Scroller
        end = -(sc.content_size - MI_W)
        return sc.scroll_panel.get_offset() <= end + tol
    except Exception:
        return False


def _swipe_to_end(page):
    for _ in range(8):
        if _scroller_at_end(page):
            return True
        PTR.drag(440, 120, 90, 120, dur=0.35)
        time.sleep(0.65)
    return _scroller_at_end(page)


def run_mici(d):
    s = d.setup
    W, H = MI_W, MI_H

    time.sleep(1.2)
    log("start page")
    PTR.click(W / 2, H / 2, hold=0.2)

    d.wait_for(lambda: d.active_name() == "SoftwareSelectionPage", "software selection")
    time.sleep(0.7)
    log("slide to install custom software")
    PTR.drag(438, 180, 110, 180, dur=0.8, settle=0.25)

    d.wait_for(lambda: d.active_name() == "CustomSoftwareWarningPage", "warning page")
    time.sleep(0.7)
    log("warning: swipe left to the end")
    if not _swipe_to_end(s._custom_software_warning_page):
        log("warning: scroller not at end after swipes")
    d.wait_for(lambda: _scroller_at_end(s._custom_software_warning_page), "warning scrolled to end", timeout=8)
    time.sleep(0.4)
    log("warning: next")
    PTR.click(W / 2, 120, hold=0.15)

    d.wait_for(lambda: d.active_name() == "NetworkSetupPage", "network page")
    log("network: waiting for internet, auto-scroll, then choose software")
    d.wait_for(lambda: _scroller_at_end(s._network_setup_page), "network scrolled to end", timeout=30)
    time.sleep(0.4)
    PTR.click(W / 2, 120, hold=0.15)

    d.wait_for(lambda: d.active_name() == "BigInputDialog", "URL dialog", timeout=20)
    time.sleep(0.7)
    log("drag-typing %s" % INSTALL_URL)
    # slide from key to key like a finger, so every drag lands cleanly
    # on its target instead of hovering neighbouring letters
    at = (W / 2, 190)  # neutral spot on the keyboard
    for ch in INSTALL_URL:
        if ch == "/":
            at = _slide(key_center("123"), at)
            time.sleep(0.32)
            at = _slide(special_key_center("/"), at)
            time.sleep(0.32)  # auto-return to letters
        else:
            at = _slide(key_center(ch), at)
        log(f"  typed {ch!r}")
        time.sleep(0.12)
    time.sleep(0.6)
    log("submit URL (enter, top left)")
    PTR.click(40, 40, hold=0.2)

    d.wait_for(lambda: d.active_name() == "DownloadingPage" and s.download_progress >= 100,
               "download complete", timeout=120)
    log(f"download at {s.download_progress}%")
    time.sleep(3.0)
    log("closing")
    for _ in range(40):
        gui_app.request_close()
        if getattr(gui_app, "_window_close_requested", False):
            break
        time.sleep(0.25)


def _slide(target, start):
    """Press at `start`, glide onto the key, release — one keystroke."""
    PTR.move(*start)
    time.sleep(0.08)
    PTR.press()
    time.sleep(0.08)
    PTR.glide(target[0], target[1], 0.24)
    time.sleep(0.14)
    PTR.release()
    time.sleep(0.12)
    return target


# ----------------------------------------------------------------- main --
CLOSE_HOLD_S = 2.5  # keep the window up after the download, for the video


def main():
    for tmp in ("/tmp/installer", "/tmp/installer_url"):
        try:
            os.remove(tmp)
        except FileNotFoundError:
            pass

    # The app closes itself the moment the download completes. Defer the
    # first close request so the video holds the finished download screen.
    orig_close = gui_app.request_close
    hold_until = [None]

    def held_close():
        now = time.monotonic()
        if hold_until[0] is None:
            hold_until[0] = now + CLOSE_HOLD_S
        if now >= hold_until[0]:
            orig_close()

    gui_app.request_close = held_close

    if DEVICE == "tici":
        gui_app.init_window("Setup", 20)  # matches tici_setup.main()
    else:
        gui_app.init_window("Setup")
    setup = setup_mod.Setup()
    gui_app.push_widget(setup)

    driver = Driver(setup)
    script = run_tici if DEVICE == "tici" else run_mici
    threading.Thread(target=script, args=(driver,), daemon=True).start()

    try:
        for _ in gui_app.render():
            pass
    finally:
        setup.close()
        gui_app.close()
    log(f"window closed; recording at {OUTPUT}")


if __name__ == "__main__":
    main()
