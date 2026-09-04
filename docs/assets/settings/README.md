# Settings screenshots — capture checklist

The Settings reference (`docs/settings/index.md`) embeds one screenshot
per panel from this directory. The current files are generated
placeholders; replace them one by one with real captures from a
**comma four** running `zoompilot/main`. Keep the file name and the
1280×720-ish 16:9 crop, and nothing else needs to change.

## How to capture

1. Park with the car off. Most settings need an offroad device.
2. Take the screenshot on the device itself, or photograph the screen
   square-on in dim light (no flash).
3. Crop to the settings panel, 16:9. No status bar secrets (pairing
   codes, dongle IDs) in frame.
4. Save over the matching file here, same name, and commit.

## The panels

| File | Screen to capture |
| --- | --- |
| `steering.svg` | Settings → Steering, with the MADS and torque rows visible |
| `cruise.svg` | Settings → Cruise, with ICBM and Speed-Limit Assist rows visible |
| `models.svg` | Settings → Models |
| `visuals.svg` | Settings → Visuals |
| `toggles.svg` | Settings → Toggles, with Enable zoompilot visible |
| `device.svg` | Settings → Device, with Onroad Uploads and Max Time Offroad visible |
| `software.svg` | Settings → Software |
| `developer.svg` | Settings → Developer, **without** any test toggles switched on |

## Notes

- Do not capture the Developer panel with Alpha Longitudinal enabled —
  the default state is what the reference documents.
- If a future release adds a panel, add its file here and one `![](...)`
  line to `docs/settings/index.md`.
