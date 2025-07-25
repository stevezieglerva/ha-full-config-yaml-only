# Ceiling Fan Integration

## Overview
This feature adds virtual switches in Home Assistant to track the state of ceiling fans that exist only in the Alexa ecosystem. This allows Home Assistant to be aware of the state of these fans and their lights, enabling integration with other automations.

## Implementation
Virtual switches have been created for:

### Fan Controls
- Master Bedroom Ceiling Fan (`input_boolean.master_bedroom_ceiling_fan`)
- Owen's Bedroom Ceiling Fan (`input_boolean.owen_bedroom_ceiling_fan`)
- William's Bedroom Ceiling Fan (`input_boolean.william_bedroom_ceiling_fan`)
- Charlotte's Bedroom Ceiling Fan (`input_boolean.charlotte_bedroom_ceiling_fan`)

### Light Controls
- Master Bedroom Ceiling Light (`input_boolean.master_bedroom_ceiling_light`)
- Owen's Bedroom Ceiling Light (`input_boolean.owen_bedroom_ceiling_light`)
- William's Bedroom Ceiling Light (`input_boolean.william_bedroom_ceiling_light`)
- Charlotte's Bedroom Ceiling Light (`input_boolean.charlotte_bedroom_ceiling_light`)

## Usage
1. These virtual switches can be toggled in Home Assistant to match the physical state of the ceiling fans/lights
2. They can be integrated with Alexa routines that set the state when the actual fan/light is turned on or off
3. Home Assistant automations can use these switches as conditions or triggers

## Future Enhancements
- Create automations that update these switches based on power consumption patterns
- Add the ability to sync states between Home Assistant and Alexa routines automatically