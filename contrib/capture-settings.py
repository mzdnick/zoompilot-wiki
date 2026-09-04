#!/usr/bin/env python3
"""Render the eight mici settings panels embedded in the zoompilot wiki to PNG.

Lives in the wiki repo (contrib/). Copy it into a zoompilot super-repo
clone to run it — see docs/assets/settings/README.md.

Based on selfdrive/ui/tests/screenshot_layouts.py, but captures a fresh
Mazda install: declared defaults plus the one-time torque-control seed,
and the four stock panels the upstream tool does not capture.

Usage:
  cd /path/to/zoompilot   (super-repo root)
  cp /path/to/wiki/contrib/capture-settings.py .
  PYTHONPATH=. SCALE=3 .venv/bin/python capture-settings.py

SCALE=3 keeps the hidden window inside the Mac screen; larger scales
make the centered window position overflow and AppKit aborts.
"""
import os

os.environ["BIG"] = "0"
os.environ.setdefault("SCALE", "4")

import pyray as rl

from pathlib import Path
from opendbc.car.structs import car
from openpilot.cereal import custom
from openpilot.common.params import Params
from openpilot.common.prefix import OpenpilotPrefix

GIT_COMMIT = "393a506e61b5e3c74ebd58258c729ef247480950"
GIT_BRANCH = "main"
VERSION = "2026.08.25-8"

OUTPUT_DIR = Path(__file__).parent / "wiki_captures"
SETTLE_FRAMES = 30


def setup_params():
  params = Params()

  cp = car.CarParams.new_message(
    enableBsm=True,
    brand="mazda",
    openpilotLongitudinalControl=True,
    alphaLongitudinalAvailable=True,
    steerControlType="torque",
  )
  params.put("CarParamsPersistent", cp.to_bytes())

  cp_sp = custom.CarParamsSP.new_message(
    intelligentCruiseButtonManagementAvailable=True,
  )
  params.put("CarParamsSPPersistent", cp_sp.to_bytes())

  # zoompilot seeds these once on steer-to-zero Mazdas (2022+ CX-5, CX-9,
  # EPS swaps) — the wiki's "Defaults on a fresh Mazda install" table.
  params.put_bool("EnforceTorqueControl", True)
  params.put_bool("LiveTorqueParamsToggle", True)
  params.put_bool("SpeedDependentTorqueToggle", True)
  params.put("TorqueControlTune", 2.0)  # v2.0

  # Documented defaults the UI would otherwise render as off.
  params.put_bool("Mads", True)
  params.put_bool("MadsMainCruiseAllowed", True)
  params.put_bool("MadsUnifiedEngagementMode", True)
  params.put_bool("OpenpilotEnabledToggle", True)
  params.put("SpeedLimitMode", 1)    # information
  params.put("SpeedLimitPolicy", 3)  # map data priority
  params.put("LongitudinalPersonality", 1)  # standard

  # Release metadata so the Software panel shows this build.
  params.put("Version", VERSION)
  params.put("GitBranch", GIT_BRANCH)
  params.put("GitCommit", GIT_COMMIT)

  # No DongleId / HardwareSerial: fresh, unpaired device shows N/A, and
  # the wiki capture checklist forbids secrets in frame.


def setup_ui_state():
  from openpilot.selfdrive.ui.ui_state import ui_state

  ui_state.params = Params()
  ui_state.CP = car.CarParams.new_message(
    enableBsm=True,
    brand="mazda",
    openpilotLongitudinalControl=True,
    alphaLongitudinalAvailable=True,
    steerControlType="torque",
  )
  ui_state.CP_SP = custom.CarParamsSP.new_message(
    intelligentCruiseButtonManagementAvailable=True,
  )
  ui_state.started = False
  ui_state.has_longitudinal_control = True
  ui_state.has_icbm = True
  ui_state.is_metric = False
  ui_state.is_sp_release = False


def capture(widget, filename, frames=SETTLE_FRAMES):
  from openpilot.system.ui.lib.application import gui_app

  # Render at the scaled framebuffer size; widgets draw in logical
  # coordinates, so mirror gui_app's own push/scalef sequence.
  scale = gui_app._scale

  if hasattr(widget, '_trigger_animate_in'):
    widget._trigger_animate_in = False
  if hasattr(widget, '_pos_filter'):
    widget._pos_filter.x = 0.0

  # Keep alpha opaque: blend RGB normally, but force alpha to stay at dst (1.0 from clear)
  GL_FUNC_ADD = 0x8006
  rl.rl_set_blend_factors_separate(
    0x0302, 0x0303,  # RGB: GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
    0x0000, 0x0001,  # Alpha: GL_ZERO, GL_ONE (preserves dst alpha = 1.0)
    GL_FUNC_ADD, GL_FUNC_ADD,
  )

  def render_pass(rt, rect, n):
    for _ in range(n):
      rl.begin_texture_mode(rt)
      rl.clear_background(rl.BLACK)
      rl.rl_push_matrix()
      rl.rl_scalef(scale, scale, 1.0)
      rl.begin_blend_mode(rl.BLEND_CUSTOM_SEPARATE)
      widget.render(rect)
      rl.end_blend_mode()
      rl.rl_pop_matrix()
      rl.end_texture_mode()
      rl.begin_drawing()
      rl.end_drawing()

  # First lay out at the logical device size so the card scroller sizes
  # its content, then re-render as a panorama wide enough for every card.
  logical_rect = rl.Rectangle(0, 0, gui_app.width, gui_app.height)
  warmup = rl.load_render_texture(gui_app._scaled_width, gui_app._scaled_height)
  render_pass(warmup, logical_rect, frames)
  rl.unload_render_texture(warmup)

  content_w = gui_app.width
  scroller = getattr(widget, '_scroller', None)
  if scroller is not None and getattr(scroller, '_content_size', 0) > content_w:
    content_w = scroller._content_size
  content_w = int(content_w + 4)
  content_w += content_w % 2

  rt = rl.load_render_texture(int(content_w * scale), gui_app._scaled_height)
  wide_rect = rl.Rectangle(0, 0, float(content_w), float(gui_app.height))
  if hasattr(widget, '_pos_filter'):
    widget._pos_filter.x = 0.0
  render_pass(rt, wide_rect, frames)

  image = rl.load_image_from_texture(rt.texture)
  rl.image_flip_vertical(image)

  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  path = str(OUTPUT_DIR / filename)
  rl.export_image(image, path)

  rl.unload_image(image)
  rl.unload_render_texture(rt)
  print(f"  {filename} ({int(content_w * scale)}x{gui_app._scaled_height})")


def main():
  with OpenpilotPrefix():
    setup_params()

    rl.set_config_flags(rl.FLAG_WINDOW_HIDDEN)

    from openpilot.system.ui.lib.application import gui_app
    gui_app.init_window("capture_wiki_settings", fps=30)

    setup_ui_state()

    from openpilot.selfdrive.ui.sunnypilot.mici.layouts.steering import SteeringLayoutMici
    from openpilot.selfdrive.ui.sunnypilot.mici.layouts.cruise import CruiseLayoutMici
    from openpilot.selfdrive.ui.sunnypilot.mici.layouts.models import ModelsLayoutMici
    from openpilot.selfdrive.ui.sunnypilot.mici.layouts.visuals import VisualsLayoutMici
    from openpilot.selfdrive.ui.mici.layouts.settings.toggles import TogglesLayoutMici
    from openpilot.selfdrive.ui.mici.layouts.settings.device import DeviceLayoutMici
    from openpilot.selfdrive.ui.mici.layouts.settings.software import SoftwareLayoutMici
    from openpilot.selfdrive.ui.mici.layouts.settings.developer import DeveloperLayoutMici

    print("Capturing screenshots...")
    for cls, name in [
      (SteeringLayoutMici, "steering.png"),
      (CruiseLayoutMici, "cruise.png"),
      (ModelsLayoutMici, "models.png"),
      (VisualsLayoutMici, "visuals.png"),
      (TogglesLayoutMici, "toggles.png"),
      (DeviceLayoutMici, "device.png"),
      (SoftwareLayoutMici, "software.png"),
      (DeveloperLayoutMici, "developer.png"),
    ]:
      widget = cls()
      widget.show_event()
      capture(widget, name)

    gui_app.close()
    print(f"\nDone — {OUTPUT_DIR}/")


if __name__ == "__main__":
  main()
