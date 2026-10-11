# ADR 0003: Text export for automation review

- Status: Accepted
- Date: 2026-10-11

## Context

The entity registry report identifies automation entities and their registry metadata, but it does not expose triggers, conditions, actions, or the current automation state. Screenshots are a poor fit for reviewing long automation definitions, and a recorder database dump is unnecessary for understanding configured behavior.

## Decision

Use `scripts/ha_automation_report.sh` on the Home Assistant config directory to generate a Markdown report containing matching entries from the entity registry and matching automation definitions from `automations.yaml`. For current on/off and last-triggered values, use the included read-only Home Assistant template query and save its text output alongside the report.

Do not include credentials or tokens. The registry table omits registry unique IDs and device IDs. Selected YAML definitions may contain device IDs or opaque trigger IDs that are part of the configured automation; review them before uploading. Do not treat registry disable metadata as the automation's current on/off state.

## Consequences

- Automation behavior can be reviewed through text shared in Git without screenshots.
- The exporter requires `jq` and read access to `automations.yaml` and `.storage/core.entity_registry`.
- The YAML excerpt is a point-in-time view of configured definitions; current states are a separate point-in-time query.
- A trace is still needed when investigating the details of a particular automation run.
