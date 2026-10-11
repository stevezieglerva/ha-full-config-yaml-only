# Claude Code Configuration

This file contains configuration and context for Claude Code when working with this Home Assistant configuration repository.

## Project Overview
This is a Home Assistant configuration repository containing:
- Core configuration files (configuration.yaml, automations.yaml, scripts.yaml, scenes.yaml)
- Blueprint automations for various home automation tasks
- Custom components (Alexa Media and iCloud3)
- Image assets for the Home Assistant interface
- Zigbee2MQTT configuration

## Development Commands
- No specific build or test commands identified yet
- Standard Home Assistant configuration validation can be done through the HA interface

## Home Assistant Access and Deployment
- The working checkout and the Home Assistant server's config checkout continuously synchronize with this repository's `origin`. Treat the local `automations.yaml` as the current tracked automation definition; do not ask Steve to export definitions already present here or assume he must manually pull changes.
- Codex has no direct access to the Home Assistant server, UI, API, or live entity/device/area registry. Ask Steve for a read-only text report only when current runtime state or registry evidence is needed; screenshots are optional.
- For Home Assistant implementation work, modify only YAML configuration files that affect Home Assistant. A push to `origin` may quickly synchronize YAML to the server, so review changes as potentially deployable. Do not claim the configuration was loaded or live-validated without Steve's confirmation.
- Use the current repository YAML to understand configured automation triggers, conditions, and actions. Do not infer live entity IDs, areas, device mappings, runtime state, or whether configuration is loaded from YAML alone. If required live evidence is missing, ask Steve for a read-only text report. Do not request or include credentials, tokens, or unrelated private identifiers in reports.
- Update supporting documentation or agent context only when Steve explicitly requests it.

## GitHub Project
- Repository: `stevezieglerva/ha-full-config-yaml-only`
- Project: [home-assistant Factory](https://github.com/users/stevezieglerva/projects/8/views/2) (owner `stevezieglerva`, project number `8`)
- GitHub project context: `context/github-project.md`
- Workflow status field: `Status`
- Status options: `Todo`, `Elaborate`, `Ready For Agent`, `In Progress`, `Reviewing`, `Deployed`, `Done`
- Work type field: `Work Type`; options: `Feature`, `Task`
- Use the project status for workflow state. Available repository labels: `area:holiday-lights`, `bug`, `documentation`, `duplicate`, `enhancement`, `epic`, `good first issue`, `help wanted`, `invalid`, `priority/P0`, `priority/P1`, `priority/P2`, `question`, `ready-for-agent`, `wontfix`.

## Factory Skills
- Tracker: `GitHub Issues + GitHub Projects`
- Repository: `https://github.com/stevezieglerva/ha-full-config-yaml-only`
- GitHub project context: `context/github-project.md`
- GitHub CLI account: `stevezieglerva`
- Factory parent issue type: `Feature`
- Factory child issue type: `Task`
- Factory epic status: `Elaborate`
- Factory todo status: `Todo`
- Factory ready status: `Ready For Agent`
- Factory in-progress status: `In Progress`
- Factory review status: `Reviewing`
- Factory deployed status: `Deployed`
- Factory done status: `Done`
- Factory priority label: `priority/P1`
- Factory ready label: `ready-for-agent`
- Factory epic label: `epic`
- Factory native issue types: `false`
- Factory status field: `Status`
- Factory work type field: `Work Type`
- Ticket title convention: concise action phrase with no required prefix
- Area labels: `area:holiday-lights`

## Project Structure
- `configuration.yaml` - Main Home Assistant configuration
- `automations.yaml` - Automated tasks and triggers
- `scripts.yaml` - Reusable scripts
- `scenes.yaml` - Predefined scenes
- `secrets.yaml` - Sensitive configuration (not committed)
- `blueprints/` - Automation and script blueprints
- `custom_components/` - Custom Home Assistant integrations
- `image/` - Image assets for the interface
- `zigbee2mqtt/` - Zigbee2MQTT bridge configuration

## Emojis

### Entity and UI Conventions

| Category | Examples | Line References |
|---------|----------|----------------|
| Temperature sensors | 🌡️ | 464, 474 |
| Climate status | 🔥 (heating), ❄️ (cooling) | 200, 221, 228 |
| Washer/laundry | 👚 | 163-173, 378-416 |
| Notifications | ‼️ (alarm), ⁉️ (text), 🚪 (door) | - |
| Sensor Values | "Any Lights" sensor returns area names | 427-428 |
| Message Templates | Door events | 433-447 |
| Mode Indicators | 🏡 Home, 🏝️ Vacation | - |

### Children's Color System

| Child | Color | Line References | Morning Alert | School Status |
|-------|-------|----------------|--------------|---------------|
| Owen | 🟦 Blue | 619-643, 5479 | 🔵 (line 5431) | 🔵📓 (lines 330-343) |
| William | 🟩 Green | 593-617, 5451 | 🟩 (line 5450) | 🟢📓 (lines 344-357) |
| Charlotte | 🩷 Pink | 567-591, 5469 | 🩷 (line 5469) | 🩷📓 (lines 358-371) |

Room motion tracking also uses the same color scheme (lines 567-695).


## Ecosystems
There are three smart home ecosystems: Home Assistant, Apple Home, and Alexa. Some virtual switches (input booleans) are used to enable integration of automations among them. 

### Alexa only devices
- Ceiling fans with lights in: Master, Owen, William, and Charlotte rooms

### Aqara Hub M3 (Matter bridge)
The Zigbee (Zigbee2MQTT) network is saturated and won't accept new devices. An **Aqara Hub M3** bridges select Aqara sensors into HA via the **Matter** integration (added during the 2026.7 upgrade, feature 006). Sensors moved to the M3 get NEW Matter entity IDs and device_ids — device_id-based automations must be repointed when a sensor is re-homed.

Currently on the M3 via Matter:
- **Aqara Back Door** (Dropzone) — `binary_sensor.dropzone_aqara_back_door_door`; replaced old Zigbee `binary_sensor.back_door_contact`
- **Aqara Garage Small** (Garage) — `binary_sensor.garage_aqara_garage_small_door`; replaced the old Zigbee garage-small sensor

Still on Zigbee2MQTT (MQTT): Deck Door, Front Door, Deck Screen Door, Garage Door Large (Third Reality).

### Night motion lighting

- Master Bedroom sources: `binary_sensor.master_bedroom_motion_occupancy`; Bedroom N3 `binary_sensor.master_bedroom_night_light_w_n3_occupancy`, `light.master_bedroom_night_light_w_n3`, and `sensor.master_bedroom_night_light_w_n3_illuminance`; Extra Night Light `binary_sensor.extra_night_light_occupancy`, `light.extra_night_light_light`, and `sensor.extra_night_light_illuminance`.
- Master Bathroom sources: `binary_sensor.master_bathroom_motion_occupancy`; Bathroom N4 `binary_sensor.master_bathroom_night_light_w_n4_occupancy`, `light.master_bathroom_night_light_w_n4`, and `sensor.master_bathroom_night_light_w_n4_illuminance`.
- Garage sources: `binary_sensor.garage_motion_backdoor_occupancy` and `sensor.garage_motion_backdoor_illuminance_lux`; Garage N1 `binary_sensor.garage_night_light_w_n1_occupancy`, `light.garage_night_light_w_n1`, and `sensor.garage_night_light_w_n1_illuminance`; Garage N2 `binary_sensor.garage_night_light_w_n2_occupancy`, `light.garage_night_light_w_n2`, and `sensor.garage_night_light_w_n2_illuminance`.
- The N1–N4 and Extra devices are ThirdReality Matter night lights. N1/N2 are in Garage, N3/Extra are in Master Bedroom, and N4 is in Master Bathroom. Room motion and light occupancy sensors are grouped by their matching room above. The separate `binary_sensor.dropzone_aqara_back_door_door` is in Dropzone.
- `binary_sensor.bedroom_night_motion` combines both room motion sensors and N3, N4, and Extra occupancy. `binary_sensor.garage_night_motion` combines the Garage PIR and N1/N2 occupancy; it excludes the back-door contact.
- Suite lights activate on combined motion when their own illuminance is below 25 lx. Extra retains brightness 64 and its 06:00–06:30 Charlotte school-day activation guard. All three turn off after 15 seconds of clear aggregate motion; the former all-night Extra baseline is removed. The waking-hours ceiling-light routine is unchanged.
- Garage lighting uses the aggregate with the existing night-or-PIR-lux-below-25 gate and 2889 K, then turns off after 60 seconds of aggregate clear. The back-door trigger stays separate with no door-only timer.
- Recency tracking records Bedroom PIR/N3/Extra, Bathroom PIR/N4, and Garage PIR/N1/N2 into their existing separate timestamps. The Motion dashboard keeps separate Bedroom and Bathroom rows, House Mode, Downstairs, and Presence; it has no combined suite row. Waking-hours ceiling-light automation is unchanged.
- `automation.smart_night_light_garage` is outside this implementation by user direction; no definition for it is present in the tracked `automations.yaml`.

Baseline behavior from `main:automations.yaml` before this change (tracked YAML source, not a claim about current HA runtime state):

- Garage automation `1729293256416` (`Garage motion detected`) triggered on the Garage PIR or Dropzone back-door opening. If `sensor.night` was `True` or Garage PIR illuminance was below 25 lx, it turned on the Garage area at 2889 K. Automation `1729456902606` (`Garage no motion`) turned the Garage area off as soon as that PIR reported clear; it had no delay.
- Extra baseline automation `1756087189405` turned Extra on to 10% at 5363 K when `sensor.night` became `True`, and off when it became `False`; it skipped actions during Charlotte's school-day 06:00–06:30 window. Motion automation `1756088697024` turned Extra on to brightness 64 after two seconds of Extra occupancy or immediately on Master Bathroom PIR motion. It required `sensor.night == True`, applied the same school-day guard, and turned Extra off after 15 seconds of clear Extra occupancy. Its log text said “3 minutes,” but the configured delay was 15 seconds.
- The two N3 automations (`1791691014819` / `N3 light on` and `1791692340944` / `N3 off`) referenced the older `smart_night_light_w*` entity IDs rather than the current Matter N3 IDs. The on rule responded to occupancy and turned on the old N3 light; the off rule turned the old N3 light off at civil dawn or after 30 seconds of occupancy clear.
- The generated `scripts/ha_automation_report.md` preserves the matching `automations.yaml` definitions alongside automation registry names. The registry-name list alone does not expose an automation's current state or YAML definition.

## School Schedules

The system includes comprehensive school schedule tracking and automation features:

## Current school schedule 8/2025, Monday - Friday
- William - Wake up 6:15, not awake warning 6:25, leave 6:50
- Charlotte - Wake up 5:55, not awake warning 6:05, leave 6:30
- Owen - Wake up 6:50, not awake warning 7:00, leave 9:00
- Steve Alexa wake-up VSwitch pulses at 5:45 when Charlotte has school
- Alexa school announcements enabled at 5:50 when Charlotte has school



### Core Sensors
- **Daily Status Sensors**: Each child has "Has School Today/Tomorrow" sensors (lines 428-467)
  - 🔵📓 Owen Has School Today/Tomorrow
  - 🟢📓 William Has School Today/Tomorrow  
  - 🩷📓 Charlotte Has School Today/Tomorrow
- **School Year Tracking**: Uses `input_datetime.school_year_begins` and `input_datetime.school_year_ends` to determine active school periods
- **Days Off Calendar**: `calendar.school_days_off` tracks holidays and non-school days

### Automation Features
- **School Day Off Notifications** (line 1522): Alerts when tomorrow is a day off
- **Calendar Change Monitoring** (line 1926): Tracks school calendar updates with school bell sound
- **Alexa School Announcements** (line 3441): Automated wake-up and departure announcements
- **Morning Alerts**: Color-coded notifications for each child's school status
- **TV Management**: Automatically turns off TVs during school hours when house is empty (line 4738)
- **Sleep Monitoring**: Tracks if children are awake for school (line 4632)

### Integration Points
- **Input Booleans**: 
  - `alexa_make_school_wake_announcements`
  - `alexa_make_school_departure_announcements`
  - `school_test` (testing purposes)
- **Scripts**: `school_notifications` script for custom school alerts (line 607)
- **Multi-ecosystem**: Works across Home Assistant, Apple Home, and Alexa platforms

## Claude Processing Notifications
- Play a unique macbook sound when a long running claud process is finished to catch my attention. 
- Send a desktop notification when a long running claud process is finished.
- Send a ios mobile notification when a long running claud process is finished to stephen.v.ziegler@gmail.com

## Allowed commands
- Allow basic bash commands like `ls`, `cd`, `cat`, `echo`, `touch`, `mkdir`, `rm`, `say`, and `cp`.
- Allow git commands like `git status`, `git add`, `git commit`, `git
- allows bash commands for file search and reading like `grep`, `find`, and `cat`.
- Allows oascripts for notifications and sound playback.


# Tests
- Home Assistant uses a custom version of yaml and traditional Yaml parsing will not work for tests
- Run the test_yaml_keys.py script to validate YAML key-value pairs.

# Networking

## Ethernet wired
- From AT&T fiber router 

## Wireless
- asprings-att: WiFi from the AT&T fiber router 
- asprings: Google Wifi mesh

# Routes
Internet (closet) -> ATT router (closet)
ATT router (closet) -> Google Wifi #1 (closet)
Google Wifi #1 (closet) -> backhauled Master room drop
Master room drop -> Master Switch (master)
Master Switch -> Google Wifi #2 (master)
Google Wifi #2 -> Circle VPN (master)
ATT router (closet) -> Living room drop
ATT router (closer) -> Office room drop
ATT router (closer) -> Playroom room drop

Google Wifi #3 (wireless)

Playroom room drop -> Playroom Switch (playroom)
Playroom Switch -> Aqara M3 (playroom)
