# Launch Fully Kiosk Browser on Sony Bravia 65

## Goal
Create a Home Assistant script that turns on the Sony Bravia 65" TV and launches the Fully Kiosk Browser app.

## Details
- **TV Entity:** `media_player.bravia_4k_vh22` (Sony Living Room TV 65 Remote)
- **App ID:** `de.ozerov.fully`
- **App Name:** Fully Kiosk Browser

## Script Behavior
1. Turn on the TV using `media_player.turn_on`
2. Launch Fully Kiosk Browser using `media_player.play_media` with:
   - `media_content_id: de.ozerov.fully`
   - `media_content_type: app`

## Existing Pattern
Follows the same pattern as `launch_hulu_on_sony_bravia_tv` in `scripts.yaml` (line ~545), which uses the same two-step turn on + play_media approach for a different TV entity.

## Verification
- Run `python test_yaml_keys.py` to validate YAML structure after adding the script
