# 007 — Fix deprecated `color_temp` (mireds) keys in scenes.yaml

## Context
The HA 2026.7 upgrade removed the mireds-based `color_temp` key from the light
schema in favor of `color_temp_kelvin`. This already surfaced as a hard error in
`script.set_recessed_light` (fixed separately: `color_temp: 400` →
`color_temp_kelvin: 2500`). `scenes.yaml` still contains 16 leftover
`color_temp:` entries plus deprecated `min_mireds` / `max_mireds` bounds. Every
scene entity already stores the kelvin equivalents (`color_temp_kelvin`,
`min_color_temp_kelvin`, `max_color_temp_kelvin`), so the mireds keys are pure
redundant/deprecated duplicates. Removing them prevents the same
"extra keys not allowed" failure when a scene is activated and matches how HA
now re-serializes scenes.

## Change
In `scenes.yaml`, delete the deprecated mireds keys from every `light.*` entity
block. All are duplicates of already-present kelvin keys, so no value
information is lost:

- `color_temp:` — both the populated form (`color_temp: 361` / `color_temp: 370`)
  and the empty null form (`color_temp:`) — 16 occurrences total
- `min_mireds: 154` — deprecated, superseded by `min_color_temp_kelvin: 2000`
- `max_mireds: 500` — deprecated, superseded by `max_color_temp_kelvin: 6493`

Leave untouched:
- `color_temp_kelvin`, `min_color_temp_kelvin`, `max_color_temp_kelvin`
- `color_mode`
- `supported_color_modes` (still lists `color_temp` as a valid mode name — that
  is unrelated to the removed mireds key)
- all other attributes (brightness, hs_color, rgb_color, xy_color, etc.)

Representative locations: lines 7-8 / 15 (Alarm On scene), 120/138/156 (empty
Vacation-on nulls), 307/332 (Garage scenes) — the pattern repeats across all 6
scenes.

## Files
- `scenes.yaml` — only file changed

## Verification
1. Validate YAML keys: `python test_yaml_keys.py` (per CLAUDE.md; standard YAML
   parsers won't handle HA's custom tags).
2. In HA: Developer Tools → YAML → Check Configuration, then Reload Scenes.
3. Activate one previously-affected scene (e.g. "Door open" or "Garage on") from
   Developer Tools → Actions (`scene.turn_on`) and confirm the lights set the
   correct warm-white temperature with no "extra keys not allowed" error.
