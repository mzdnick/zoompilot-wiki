# Settings screenshots — capture checklist

The Settings reference (`docs/settings/index.md`) embeds two images per
panel from this directory: comma four (mici) panoramas at the root, and
comma 3/3X (tici/tizi) full-frame panels in `tici/`. Both are rendered
from the release code with the simulator tool in
[contrib/capture-settings.py](../../../contrib/capture-settings.py) —
no device needed.

## Regenerate after a release

1. Clone the zoompilot super-repo at the release branch and set up the
   Python environment:

   ```bash
   git clone --depth 1 --branch main https://github.com/zoompilot/zoompilot
   cd zoompilot
   uv sync --frozen
   uv pip install comma-deps-ncurses comma-deps-imgui \
     comma-deps-bootstrap-icons comma-deps-libusb matplotlib
   ```

2. The `main` branch ships Linux binaries. Build the two macOS native
   pieces in place:

   - `msgq`: copy `SConstruct` and `SConscript` from `commaai/msgq`
     into `msgq_repo/`, then run the venv scons there.
   - `libparams_c.dylib`: the params sources match sunnypilot at the
     release's pinned commit, except `params_keys.h` (zoompilot adds
     keys). Clone sunnypilot at that commit, copy zoompilot's
     `params_keys.h` over, and build with the venv scons. Put the venv
     bin first on `PATH` so the venv capnp (1.0.x) is used, not brew's.

3. Copy `contrib/capture-settings.py` into the zoompilot clone root.
   Edit its `VERSION`, `GIT_BRANCH`, and `GIT_COMMIT` constants for the
   release, then run it once per device:

   ```bash
   PYTHONPATH=. .venv/bin/python capture-settings.py              # comma four
   DEVICE=tici PYTHONPATH=. .venv/bin/python capture-settings.py  # comma 3/3X
   ```

   The mici pass renders each panel as one wide strip (every card);
   the tici pass renders each panel top to bottom in one frame.

4. Copy the eight PNGs from `wiki_captures/` over the files here
   (resample to 480 px tall, `sips --resampleHeight 480 f.png`), and
   the eight from `wiki_captures_tici/` over `tici/` (keep native
   size; they display at column width).

## What the tool renders

- Declared defaults for every setting, plus the zoompilot one-time
  Mazda seed (torque control, self-tune, speed-dependent self-tune,
  tune v2.0) — the state the reference tables document.
- Release metadata in the Software panel, from the constants above.
- No secrets: Dongle ID and serial render as N/A on purpose.

## Device photo fallback

If you have a comma four running `zoompilot/main`, a photo works too:

1. Park with the car off. Most settings need an offroad device.
2. Take the screenshot on the device itself, or photograph the screen
   square-on in dim light (no flash).
3. Crop to the settings card, keep the panel name readable. No status
   bar secrets (pairing codes, dongle IDs) in frame.
4. Save over the matching file here, same name, and commit.

## The panels

| File(s) | Screen to capture |
| --- | --- |
| `steering.png`, `tici/steering.png` | Settings → Steering |
| `cruise.png`, `tici/cruise.png` | Settings → Cruise |
| `models.png`, `tici/models.png` | Settings → Models |
| `visuals.png`, `tici/visuals.png` | Settings → Visuals |
| `toggles.png`, `tici/toggles.png` | Settings → Toggles |
| `device.png`, `tici/device.png` | Settings → Device |
| `software.png`, `tici/software.png` | Settings → Software |
| `developer.png`, `tici/developer.png` | Settings → Developer, default state |

## Notes

- The two devices lay the same settings out differently: the mici
  Visuals panel has 4 toggles while tici has 12 rows, mici puts
  driving personality under Toggles, and the tici alpha toggle still
  reads "sunnypilot Longitudinal Control (Alpha)". That is what the
  devices show; the tables in the reference stay shared.
- On tici, with alpha longitudinal available the Cruise panel shows an
  ICBM "unavailable on this platform" note — ICBM and alpha
  longitudinal are mutually exclusive, and the captures take the
  alpha-on state most installs run.
- If a future release adds a panel, add both files here and one
  `<figure>` pair to `docs/settings/index.md`.
- The strips need the `settings-strip` CSS in
  `docs/stylesheets/custom.css` to scroll sideways; the mici/tici swap
  needs `assets/js/device-switch.js` and the `device-switch` CSS.
