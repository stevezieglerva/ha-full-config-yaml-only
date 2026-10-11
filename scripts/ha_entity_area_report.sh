#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
STORAGE_DIR="${CONFIG_DIR}/.storage"
ENTITY_REGISTRY="${STORAGE_DIR}/core.entity_registry"
DEVICE_REGISTRY="${STORAGE_DIR}/core.device_registry"
AREA_REGISTRY="${STORAGE_DIR}/core.area_registry"
REPORT_PATH="${CONFIG_DIR}/scripts/ha_entity_area_report.md"

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required. Add jq to the Terminal & SSH add-on's apks setting, then restart the add-on." >&2
  exit 1
fi

for registry in "$ENTITY_REGISTRY" "$DEVICE_REGISTRY" "$AREA_REGISTRY"; do
  if [[ ! -r "$registry" ]]; then
    echo "Error: cannot read Home Assistant registry: $registry" >&2
    echo "Run this script from the Home Assistant config mounted at /config." >&2
    exit 1
  fi
done

TEMP_REPORT="$(mktemp "${CONFIG_DIR}/scripts/.ha_entity_area_report.XXXXXX")"
trap 'rm -f "$TEMP_REPORT"' EXIT

{
  cat <<EOF
# Home Assistant entity, device, and area report

Generated (UTC): $(date -u '+%Y-%m-%d %H:%M:%S')

This report lists registry entries related to the garage, master bedroom or bathroom, motion/occupancy, illuminance/lux, back doors, and the named night lights. It does not include unique IDs, device IDs, network addresses, or current entity states.

| Entity ID | Display name | Area | Device | Manufacturer | Model | Integration | Disabled by |
| --- | --- | --- | --- | --- | --- | --- | --- |
EOF

  jq -n -r \
    --slurpfile entities "$ENTITY_REGISTRY" \
    --slurpfile devices "$DEVICE_REGISTRY" \
    --slurpfile areas "$AREA_REGISTRY" \
    '
    def cell:
      (. // "" | tostring | gsub("[\t\r\n]"; " ") | gsub("\\|"; "\\\\|"));

    ($devices[0].data.devices // []
      | map({key: .id, value: .})
      | from_entries) as $device_by_id
    | ($areas[0].data.areas // []
      | map({key: .id, value: .name})
      | from_entries) as $area_by_id
    | ($entities[0].data.entities // [])[] as $entity
    | ($device_by_id[($entity.device_id // "")] // {}) as $device
    | ($area_by_id[($entity.area_id // $device.area_id // "")] // "") as $area
    | ($device.name_by_user // $device.name // "") as $device_name
    | ([
        $entity.entity_id,
        $entity.name,
        $entity.original_name,
        $area,
        $device_name
      ] | map(. // "") | join(" ")) as $search_text
    | select(
        ($area | test("garage|master.*(bedroom|bathroom)"; "i"))
        or ($device_name | test("garage.*n[12]|master.*n[34]|extra night light"; "i"))
        or ($search_text | test("garage|master bedroom|master bathroom|back[ _-]?door|motion|occupancy|illuminance|lux|extra night light"; "i"))
      )
    | [
        $entity.entity_id,
        ($entity.name // $entity.original_name // ""),
        $area,
        $device_name,
        ($device.manufacturer // ""),
        ($device.model // ""),
        ($entity.platform // ""),
        ($entity.disabled_by // "no")
      ]
    | map(cell)
    | "| " + join(" | ") + " |"
  '
} > "$TEMP_REPORT"

mv -- "$TEMP_REPORT" "$REPORT_PATH"
trap - EXIT
echo "Wrote report: $REPORT_PATH"
