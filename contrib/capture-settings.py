#!/usr/bin/env python3
"""Render the eight mici settings panels embedded in the zoompilot wiki to PNG.

Based on selfdrive/ui/tests/screenshot_layouts.py, but captures a fresh
Mazda install: declared defaults plus the one-time torque-control seed,
and the four stock panels the upstream tool does not capture.

Usage:
  cd /path/to/zoompilot   (super-repo root)
  PYTHONPATH=. SCALE=4 .venv/bin/python capture_wiki_settings.py
"""
import os

DEVICE = os.getenv("DEVICE", "mici")  # mici (comma four) or tici (comma 3/3X)
BIG_UI = DEVICE == "tici"
os.environ["BIG"] = "1" if BIG_UI else "0"
os.environ.setdefault("SCALE", "0.75" if BIG_UI else "3")

import pyray as rl

from pathlib import Path
from opendbc.car.structs import car
from openpilot.cereal import custom
from openpilot.common.params import Params
from openpilot.common.prefix import OpenpilotPrefix

GIT_COMMIT = "393a506e61b5e3c74ebd58258c729ef247480950"
GIT_BRANCH = "main"
VERSION = "2026.08.25-8"

OUTPUT_DIR = Path(__file__).parent / ("wiki_captures_tici" if BIG_UI else "wiki_captures")
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
  # models.py reads this with a positional default that lands on `block`,
  # so it must exist or the blocking read raises on a fresh params DB
  params.put("LagdToggleDelay", 0.2)

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

  # First lay out at the logical device size so the scroller sizes its
  # content. The mici panels are one-card-per-screen horizontal
  # scrollers, so re-render as a panorama wide enough for every card;
  # the tici panels are vertical lists, so extend the frame downward.
  logical_rect = rl.Rectangle(0, 0, gui_app.width, gui_app.height)
  warmup = rl.load_render_texture(gui_app._scaled_width, gui_app._scaled_height)
  render_pass(warmup, logical_rect, frames)
  rl.unload_render_texture(warmup)

  content_w, content_h = gui_app.width, gui_app.height
  scroller = getattr(widget, '_scroller', None)
  if BIG_UI:
    # scroller_tici computes its content height inline; mirror it
    if scroller is not None and getattr(scroller, '_items', None):
      items = [i for i in scroller._items if i.is_visible]
      h = sum(i.rect.height for i in items) + scroller._spacing * len(items)
      if not scroller._pad_end:
        h -= scroller._spacing
      if h > content_h:
        content_h = h
      # rows can still grow (text wrap) during the final pass
      content_h += 48
  else:
    if scroller is not None and getattr(scroller, '_content_size', 0) > content_w:
      content_w = scroller._content_size
  content_w = int(content_w + 4)
  content_w += content_w % 2
  content_h = int(content_h + 4)
  content_h += content_h % 2

  rt = rl.load_render_texture(int(content_w * scale), int(content_h * scale))
  wide_rect = rl.Rectangle(0, 0, float(content_w), float(content_h))
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
  print(f"  {filename} ({int(content_w * scale)}x{int(content_h * scale)})")


def main():
  with OpenpilotPrefix():
    setup_params()

    rl.set_config_flags(rl.FLAG_WINDOW_HIDDEN)

    from openpilot.system.ui.lib.application import gui_app
    gui_app.init_window("capture_wiki_settings", fps=30)

    setup_ui_state()

    if BIG_UI:
      from openpilot.selfdrive.ui.sunnypilot.layouts.settings.steering import SteeringLayout
      from openpilot.selfdrive.ui.sunnypilot.layouts.settings.cruise import CruiseLayout
      from openpilot.selfdrive.ui.sunnypilot.layouts.settings.models import ModelsLayout
      from openpilot.selfdrive.ui.sunnypilot.layouts.settings.visuals import VisualsLayout
      from openpilot.selfdrive.ui.layouts.settings.toggles import TogglesLayout
      from openpilot.selfdrive.ui.sunnypilot.layouts.settings.device import DeviceLayoutSP
      from openpilot.selfdrive.ui.sunnypilot.layouts.settings.software import SoftwareLayoutSP
      from openpilot.selfdrive.ui.sunnypilot.layouts.settings.developer import DeveloperLayoutSP
      panels = [
        (SteeringLayout, "steering.png"),
        (CruiseLayout, "cruise.png"),
        (ModelsLayout, "models.png"),
        (VisualsLayout, "visuals.png"),
        (TogglesLayout, "toggles.png"),
        (DeviceLayoutSP, "device.png"),
        (SoftwareLayoutSP, "software.png"),
        (DeveloperLayoutSP, "developer.png"),
      ]
    else:
      from openpilot.selfdrive.ui.sunnypilot.mici.layouts.steering import SteeringLayoutMici
      from openpilot.selfdrive.ui.sunnypilot.mici.layouts.cruise import CruiseLayoutMici
      from openpilot.selfdrive.ui.sunnypilot.mici.layouts.models import ModelsLayoutMici
      from openpilot.selfdrive.ui.sunnypilot.mici.layouts.visuals import VisualsLayoutMici
      from openpilot.selfdrive.ui.mici.layouts.settings.toggles import TogglesLayoutMici
      from openpilot.selfdrive.ui.mici.layouts.settings.device import DeviceLayoutMici
      from openpilot.selfdrive.ui.mici.layouts.settings.software import SoftwareLayoutMici
      from openpilot.selfdrive.ui.mici.layouts.settings.developer import DeveloperLayoutMici
      panels = [
        (SteeringLayoutMici, "steering.png"),
        (CruiseLayoutMici, "cruise.png"),
        (ModelsLayoutMici, "models.png"),
        (VisualsLayoutMici, "visuals.png"),
        (TogglesLayoutMici, "toggles.png"),
        (DeviceLayoutMici, "device.png"),
        (SoftwareLayoutMici, "software.png"),
        (DeveloperLayoutMici, "developer.png"),
      ]

    print("Capturing screenshots...")
    for cls, name in panels:
      widget = cls()
      widget.show_event()
      capture(widget, name)

    gui_app.close()
    print(f"\nDone — {OUTPUT_DIR}/")


if __name__ == "__main__":
  main()
