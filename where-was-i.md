# Where Was I

Running journal of work on this Home Assistant config repo. Newest entries on top.

## Journal Entries

### 2026-07-10 — Repoint door automations to Aqara M3 (Matter)

Finished the sensor-swap work started conceptually earlier: the saturated Zigbee network forced the Back Door and Garage Door Small sensors onto an Aqara Hub M3, bridged via Matter, so all config had to move off the old Zigbee IDs. Discovered the real entity IDs from Steve's own commits — HA slugged both sensors after the generic model, and Steve then renamed them to friendly IDs (`binary_sensor.dropzone_aqara_back_door_door`, `binary_sensor.garage_aqara_garage_small_door`). Two Explore agents mapped every reference before touching anything, which surfaced device-based triggers (not just entity_id strings) that would have been missed by a naive grep.

Repointed all 10 references and, rather than just swapping device_ids, converted every `platform: device` trigger/condition to a plain state trigger so a future re-home can't break them again — directly addressing the gotcha flagged in feature 006. Landed as PR #6 (merged, commit 9e33568). Also documented the M3/Matter bridge in CLAUDE.md's Ecosystems section, and produced a styled HTML change report (`aqara-m3-door-sensor-changes.html`) that Steve used to review before I made the edits directly.

**Key decisions**
- Convert device→state triggers (kill device_id fragility) instead of substituting new device_ids.
- Map strictly by entity name; flagged that physical-sensor binding still needs live-registry verification.

**Next steps / open items** (from `~/temp/handoff/2026-07-10-aqara-device-names.md`)
- Verify each renamed entity is bound to the correct *physical* sensor (possible swap mismatch, unconfirmed).
- Delete the temporary "Test automation for Aqara devices".
- Audit sibling entities (battery/temp, e.g. `sensor.aqara_door_and_window_sensor_battery_2`) still on old auto-generated slugs.
- **Deploy:** the live HA box must reload YAML config (or restart) for the merged changes to take effect.

**References:** PR #6; commits 7f76915 → a3c6a0f → 9e33568; memory `aqara-m3-sensor-swap`; feature 006.
