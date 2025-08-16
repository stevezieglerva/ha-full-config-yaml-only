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