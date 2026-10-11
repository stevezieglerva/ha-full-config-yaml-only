# ADR 0002: Read-only Home Assistant registry report script

- Status: Accepted
- Date: 2026-10-11

## Context

The implementation agent needs entity, device, and area metadata to work on Home Assistant changes, but has no direct server access. The user can run a script from the Terminal & SSH add-on and upload its text output to the repository.

## Decision

Provide `scripts/ha_entity_area_report.sh`, a read-only Bash script that uses `jq` to read Home Assistant's entity, device, and area registry files under `.storage`. It writes `scripts/ha_entity_area_report.md` and selects garage, master bedroom and bathroom, motion, occupancy, illuminance, lux, back-door, and Extra Night Light matches.

The report includes entity IDs, display names, areas, device names, manufacturer/model, integration, and disabled status. It intentionally omits registry unique IDs, device IDs, connection identifiers, and live entity states. The script uses `jq -n` so it does not wait for terminal input.

## Consequences

- The script requires `jq` in the Terminal & SSH add-on and read access to the three registry files.
- It reads Home Assistant's internal registry JSON files, whose format may change across Home Assistant versions.
- The filter is intentionally broad: motion and illuminance matches outside the named rooms can appear in the report.
- Automation entities may appear by ID and name, but the registry does not contain automation triggers or actions. Use screenshots or another user-run export to provide those details.
- Entity IDs and display/device names are included verbatim and may contain local network information. Review and redact reports before future uploads.
- The Markdown report is a point-in-time snapshot. Regenerate it when current registry information is needed.
