#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
AUTOMATIONS_FILE="${CONFIG_DIR}/automations.yaml"
ENTITY_REGISTRY="${CONFIG_DIR}/.storage/core.entity_registry"
REPORT_PATH="${CONFIG_DIR}/scripts/ha_automation_report.md"
AREA_PATTERN='garage|master[ _-]?(bedroom|bathroom)'
BEHAVIOR_PATTERN='night|light|motion|occupancy|illuminance|lux'
NIGHT_LIGHT_PATTERN='night[ _-]?light|smart_night|extra_night|n[1-4]'
if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required. Add jq to the Terminal & SSH add-on's apks setting, then restart the add-on." >&2
  exit 1
fi
if [[ ! -r "$AUTOMATIONS_FILE" ]]; then
  echo "Error: cannot read automation YAML: $AUTOMATIONS_FILE" >&2
  echo "Run this script from the Home Assistant config mounted at /config." >&2
  exit 1
fi
if [[ ! -r "$ENTITY_REGISTRY" ]]; then
  echo "Error: cannot read Home Assistant entity registry: $ENTITY_REGISTRY" >&2
  echo "Run this script from the Home Assistant config mounted at /config." >&2
  exit 1
fi
TEMP_REPORT="$(mktemp "${CONFIG_DIR}/scripts/.ha_automation_report.XXXXXX")"
trap 'rm -f "$TEMP_REPORT"' EXIT

{
  cat <<EOF
# Home Assistant night-light automation report

Generated (UTC): $(date -u '+%Y-%m-%d %H:%M:%S')

This report contains matching automation definitions copied from \`automations.yaml\` and matching automation entity names from the entity registry. It includes triggers, conditions, actions, and modes from the YAML source. The registry's \`disabled_by\` value only describes registry-level disablement; it is not the current on/off state of an automation.

The filter selects automations mentioning a target room and a lighting/motion term, plus named night-light automations and N1-N4 references. Review names and entity IDs before uploading because they may identify rooms or devices in this home.

## Matching automation registry entries

| Entity ID | Name | Disabled by |
| --- | --- | --- |
EOF
  jq -n -r \
    --slurpfile entities "$ENTITY_REGISTRY" \
    --arg area_pattern "$AREA_PATTERN" \
    --arg behavior_pattern "$BEHAVIOR_PATTERN" \
    --arg night_light_pattern "$NIGHT_LIGHT_PATTERN" \
    '
    def cell:
      (. // "" | tostring | gsub("[\t\r\n]"; " ") | gsub("\\|"; "\\\\|"));

    ($entities[0].data.entities // [])[] as $entity
    | select(($entity.entity_id // "") | startswith("automation."))
    | ([
        $entity.entity_id,
        $entity.name,
        $entity.original_name
      ] | map(. // "") | join(" ")) as $search_text
    | select(
        (($search_text | test($area_pattern; "i"))
          and ($search_text | test($behavior_pattern; "i")))
        or ($search_text | test($night_light_pattern; "i"))
      )
    | [
        $entity.entity_id,
        ($entity.name // $entity.original_name // ""),
        ($entity.disabled_by // "no")
      ]
    | map(cell)
    | "| " + join(" | ") + " |"
  '
  cat <<'EOF'

## Matching automation definitions from `automations.yaml`

```yaml
EOF
  awk -v area_pattern="$AREA_PATTERN" \
      -v behavior_pattern="$BEHAVIOR_PATTERN" \
      -v night_light_pattern="$NIGHT_LIGHT_PATTERN" '
    function emit_block() {
      if (block != "" && selected) {
        printf "%s\n", block
        found++
      }
    }

    function mark_line(text, normalized) {
      normalized = tolower(text)
      if (normalized ~ area_pattern) {
        found_area = 1
      }
      if (normalized ~ behavior_pattern) {
        found_behavior = 1
      }
      if (normalized ~ night_light_pattern) {
        found_named_night_light = 1
      }
      selected = (found_area && found_behavior) || found_named_night_light
    }

    /^-[[:space:]]/ {
      emit_block()
      block = $0
      found_area = 0
      found_behavior = 0
      found_named_night_light = 0
      selected = 0
      mark_line($0)
      next
    }

    {
      block = block "\n" $0
      mark_line($0)
    }

    END {
      emit_block()
      if (found == 0) {
        print "# No matching automation definitions found in automations.yaml"
      }
    }
  ' "$AUTOMATIONS_FILE"
  cat <<'EOF'
```

## Optional live automation state query

To report which matching automations are currently on or off and when each last ran, paste this template into Home Assistant's **Developer Tools → Template** and copy its text output into `scripts/ha_automation_states.md`. This is a read-only query and does not require a database dump or API token.

```jinja
{% for s in states.automation | sort(attribute='entity_id') %}
{% set target_area = 'garage' in s.entity_id or 'master_bedroom' in s.entity_id or 'master_bathroom' in s.entity_id %}
{% set target_behavior = 'night' in s.entity_id or 'light' in s.entity_id or 'motion' in s.entity_id or 'occupancy' in s.entity_id or 'illuminance' in s.entity_id or 'lux' in s.entity_id %}
{% if (target_area and target_behavior) or 'smart_night' in s.entity_id or 'extra_night' in s.entity_id or s.entity_id.startswith('automation.n1_') or s.entity_id.startswith('automation.n2_') or s.entity_id.startswith('automation.n3_') or s.entity_id.startswith('automation.n4_') %}
{{ s.entity_id }} | state={{ s.state }} | last_triggered={{ s.attributes.last_triggered or 'never' }} | current={{ s.attributes.current | default(0) }} | mode={{ s.attributes.mode | default('unknown') }}
{% endif %}
{% endfor %}
```

This state query reports current state and recent-run metadata. It does not replace automation traces when investigating why a particular run behaved a certain way.
EOF
} > "$TEMP_REPORT"

mv -- "$TEMP_REPORT" "$REPORT_PATH"
trap - EXIT
echo "Wrote report: $REPORT_PATH"
