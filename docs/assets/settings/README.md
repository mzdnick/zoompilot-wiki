# Settings screenshots — capture checklist

The Settings reference (`docs/settings/index.md`) embeds one image per
panel from this directory. The images are panoramas of the comma four
(mici) settings screens: every card of the panel in one strip. They are
rendered from the release code with the simulator tool in
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
   release, then:

   ```bash
   PYTHONPATH=. SCALE=3 .venv/bin/python capture_wiki_settings.py
   ```

4. Copy the eight PNGs from `wiki_captures/` over the files here, and
   resample to 480 px tall (`sips --resampleHeight 480 f.png`).

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

| File | Screen to capture |
| --- | --- |
| `steering.png` | Settings → Steering |
| `cruise.png` | Settings → Cruise |
| `models.png` | Settings → Models |
| `visuals.png` | Settings → Visuals |
| `toggles.png` | Settings → Toggles |
| `device.png` | Settings → Device |
| `software.png` | Settings → Software |
| `developer.png` | Settings → Developer, default state |

## Notes

- If a future release adds a panel, add its file here and one
  `<figure class="settings-strip">` block to
  `docs/settings/index.md`.
- The strips need the `settings-strip` CSS in
  `docs/stylesheets/custom.css` to scroll sideways.
