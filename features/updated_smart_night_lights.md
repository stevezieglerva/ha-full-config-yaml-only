# Smart Night Lights - Updated Implementation

## Purpose
Provide smart night light functionality in Owen's, William's, and Charlotte's rooms with automatic brightness control based on time of day and motion detection.

## Requirements

1. Night lights should turn ON automatically when:
   - The `input_boolean.night` changes from `false` to `true`
   - At 10% brightness level

2. Night lights should turn OFF automatically when:
   - The `input_boolean.night` changes from `true` to `false`

3. Motion-based brightness control:
   - When motion is detected AND `input_boolean.night` is `true`:
     - Increase brightness to 100%
     - After 1 minute of no motion, return to 10% brightness

## Implementation

- Create separate individual automations for each night light location:
  - Owen's room night light
  - William's room night light
  - Charlotte's room night light

- Each location will have two automations:
  1. Night mode control automation:
     - Triggers on state change of `input_boolean.night`
     - Turns light on/off based on night boolean state
     - Sets initial brightness to 10% when turning on

  2. Motion-based brightness control automation:
     - Triggers on motion detection
     - When motion detected AND night mode is active:
       - Sets brightness to 100%
       - After 1 minute of no motion, returns to 10% brightness

## Light Entities

- Owen's room: `light.owens_smart_night_light`
- William's room: `light.williams_smart_night_light`
- Charlotte's room: `light.charlottes_smart_night_light`

## Motion Sensors

- Owen's room: `binary_sensor.owens_room_motion`
- William's room: `binary_sensor.williams_room_motion`
- Charlotte's room: `binary_sensor.charlottes_room_motion`