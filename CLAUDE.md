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
     │ 1. Entity Names: Emojis are directly added to entity names in the configuration files. For example:                                 │
     │   - Temperature sensors: 🌡️ (lines 464, 474)                                                                                       │
     │   - Climate status: 🔥 (heating), ❄️ (cooling) (lines 200, 221, 228)                                                                │
     │   - Washer/laundry: 👚 (lines 163-173, 378-416)                                                                                     │
     │   - Notifications: ‼️ (alarm), ⁉️ (text), 🚪 (door)                                                                                 │
     │ 2. Sensor Values: Some sensors include emojis in their returned values, like the "Any Lights" sensor that returns area names with   │
     │ lights on (lines 427-428).                                                                                                          │
     │ 3. Message Templates: Emojis are used in notification templates, like for door events (lines 433-447).                              │
     │ 4. Mode Indicators: Emojis are used in house modes like 🏡 Home, 🏝️ Vacation, etc. 

 │ 1. Children's Color Associations:                                                                                                         │ │
│ │   - 🟦 Blue for Owen (lines 619-643, 5479)                                                                                                │ │
│ │   - 🟩 Green for William (lines 593-617, 5451)                                                                                            │ │
│ │   - 🩷 Pink for Charlotte (lines 567-591, 5469)                                                                                           │ │
│ │ 2. School Indicators:                                                                                                                     │ │
│ │   - 🔵📓 Owen's school status (lines 330-343)                                                                                             │ │
│ │   - 🟢📓 William's school status (lines 344-357)                                                                                          │ │
│ │   - 🩷📓 Charlotte's school status (lines 358-371)                                                                                        │ │
│ │ 3. Morning Notifications:                                                                                                                 │ │
│ │   - 🔵 Owen is up (line 5431)                                                                                                             │ │
│ │   - 🟩 William is up (line 5450)                                                                                                          │ │
│ │   - 🩷 Charlotte is up (line 5469)                                                                                                        │ │
│ │ 4. Room Motion Tracking:                                                                                                                  │ │
│ │   - Uses the same color scheme for tracking motion (lines 567-695)  


## Ecosystems
There are three smart home ecosystems: Home Assistant, Apple Home, and Alexa. Some virtual switches (input booleans) are used to enable integration of automations among them. 

## Claude Processing Notifications
- Play a unique macbook sound when a long running claud process is finished to catch my attention. 