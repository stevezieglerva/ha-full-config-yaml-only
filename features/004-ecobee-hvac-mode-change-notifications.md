# Ecobee HVAC Mode Change Notifications

## Context
The Ecobee HVAC mode has been changing unexpectedly (e.g., switching from heat_cool to cool-only). To help debug when and why this happens, we need notifications when the HVAC mode changes on either thermostat.

## Approach
Add **two new automations** to `automations.yaml` — one for downstairs, one for upstairs — that fire when the HVAC mode (state) changes on each climate entity.

### Automation 1: Downstairs Ecobee HVAC Mode Changed
- **Trigger:** `state` platform on `climate.downstairs_ecobee`
- **Action:** `notify.mobile_app_iphone703` with message including:
  - Which ecobee changed (Downstairs)
  - New mode (`trigger.to_state.state`)
  - Previous mode (`trigger.from_state.state`)
  - Current ecobee temperature (`sensor.downstairs_ecobee_current_temperature`)
  - Outside temperature (`sensor.ktta_temperature`)

### Automation 2: Upstairs Ecobee HVAC Mode Changed
- Same pattern using `climate.upstairs_ecobee`
- Upstairs current temp via `state_attr('climate.upstairs_ecobee', 'current_temperature')`
- Outside temperature via `sensor.ktta_temperature`

### Message Format
```
🔔 Downstairs Ecobee mode changed: heat_cool → cool
Ecobee temp: 72°F | Outside: 85°F
```

### Key Entities
- `climate.downstairs_ecobee` / `climate.upstairs_ecobee`
- `sensor.downstairs_ecobee_current_temperature` (downstairs current temp)
- `state_attr('climate.upstairs_ecobee', 'current_temperature')` (upstairs current temp)
- `sensor.ktta_temperature` (outside temp)
- `notify.mobile_app_iphone703`

### File Modified
- `automations.yaml` — append two new automations at the end

## Verification
- Check YAML validity with `test_yaml_keys.py`
- Manually toggle an ecobee mode in HA to confirm notification fires
