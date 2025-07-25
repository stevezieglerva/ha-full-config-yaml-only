# Purpose
Create a consistent behavior for the smart night lights in the house. 

# Implementation
- Created a smart night light script (smart_night_light) in scripts.yaml that:
  - Turns on at a dim setting when the room is dark and it's night time
  - Turns on brightly when motion is detected and the night boolean is true 
  - When motion is no longer detected, returns to dim after a timeout period
  - Does not turn on if the room is already lit (based on illuminance threshold)

- Created individual automations in automations.yaml for:
  - Pantry night light (using pantry motion sensor)
  - Coat closet hall light (using office motion sensor)
  - Garage light (using garage motion sensor)
  - Charlotte's room night light (using integrated motion sensor)
  - Owen's room night light (using integrated motion sensor)
  - William's room night light (using integrated motion sensor)

# Configuration Options
Each night light can be customized with these parameters:
- motion_sensor: The motion sensor that activates the night light
- light_entity: The light to control
- illuminance_sensor: Sensor that detects room brightness
- darkness_threshold: Lux level below which the room is considered dark (25-200 lux)
- dim_brightness: Brightness level when dimmed (1-255)
- bright_brightness: Brightness level when motion detected (1-255)
- timeout: Time in seconds to remain at bright level after motion stops

# How to Add More Night Lights
1. Identify a motion sensor and light to use
2. Determine the appropriate illuminance sensor for the area
3. Add a new automation in automations.yaml following the existing pattern
4. Choose appropriate brightness levels and timeout for the specific area

# Notes
- Uses the existing sensor.night template sensor to determine nighttime
- Different rooms use different darkness thresholds based on their natural lighting
- Automations restart when any trigger fires to ensure consistent behavior