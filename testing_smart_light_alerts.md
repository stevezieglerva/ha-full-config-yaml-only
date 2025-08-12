# Testing Smart Light Off at Switch Alerts

This document provides instructions for testing the "Alert when smart lights are turned off at the switch" feature.

## Feature Overview

The feature detects when smart bulbs have been turned off at the physical switch (making them unavailable to Home Assistant) and provides:

1. Mobile notifications with sound alerts
2. Alexa virtual switches that can be used in Alexa routines for voice announcements

## Test Procedure

### Step 1: Configuration Validation

1. Restart Home Assistant to load the new configuration
2. Check for any configuration errors in the logs
3. Verify the new binary sensors appear in the States panel:
   - `binary_sensor.butlers_pantry_light_off_at_switch`
   - `binary_sensor.coat_closet_hall_light_off_at_switch`
   - `binary_sensor.garage_back_door_light_off_at_switch`
   - `binary_sensor.garage_tool_light_off_at_switch`
   - `binary_sensor.kitchen_sink_light_off_at_switch`
   - `binary_sensor.office_lamp_light_off_at_switch`

4. Verify the new input booleans appear in the States panel:
   - `input_boolean.alexa_butlers_pantry_light_off`
   - `input_boolean.alexa_coat_closet_hall_light_off`
   - `input_boolean.alexa_garage_back_door_light_off`
   - `input_boolean.alexa_garage_tool_light_off`
   - `input_boolean.alexa_kitchen_sink_light_off`
   - `input_boolean.alexa_office_lamp_light_off`

### Step 2: Simulation Testing

Since we can't easily make lights unavailable without physically turning off their switches, we can test by temporarily modifying the binary sensor template to simulate an unavailable state:

1. Go to Developer Tools > Template
2. Copy and paste this template to simulate the Butler's Pantry light being off at the switch:

```yaml
{% set last_updated = now() - timedelta(minutes=35) %}
{% set minutes_since = ((now() - last_updated).total_seconds() / 60) | int %}
{{ minutes_since > 30 }}
```

3. If the template returns `true`, it means our detection logic works correctly.

### Step 3: Test Mobile Notifications

1. Manually trigger the automations to test notifications:
   - Go to Developer Tools > Services
   - Select the `automation.trigger` service
   - Enter the entity_id of one automation (e.g., `automation.alert_butlers_pantry_light_off_at_switch`) 
   - Trigger the automation and check if you receive a mobile notification with the alarm sound

### Step 4: Test Alexa Integration

1. Set up Alexa routines:
   - Open the Alexa app
   - Create a new routine for each smart light
   - Set the trigger as "Smart Home" > Select the virtual switch (e.g., "Butler's Pantry Light Off")
   - Set the action to announce: "The [light name] has been turned off at the switch. Please turn it back on for smart home control."

2. Manually trigger each input_boolean to test the Alexa announcements:
   - Go to Developer Tools > Services
   - Select the `input_boolean.turn_on` service
   - Enter entity_id (e.g., `input_boolean.alexa_butlers_pantry_light_off`)
   - Trigger the service and verify that your Alexa device makes the announcement

### Step 5: Real-World Testing

For actual testing with physical switches:

1. Physically turn off one of the smart lights at its switch
2. Wait 30+ minutes
3. Verify that you receive both a mobile notification and an Alexa announcement
4. Turn the switch back on and verify the light becomes available in Home Assistant

## Troubleshooting

If notifications are not working:
- Check that the binary sensors are detecting unavailable status correctly
- Verify that the automations are triggered when the binary sensor state changes
- Check mobile app notification settings
- Verify that Alexa routines are properly configured

If sensor detection is not working:
- Ensure the light entity names in the binary sensor templates are correct
- Check that the light entities report "unavailable" status when physically turned off

## Adjusting Detection Time

The current configuration is set to detect lights that have been unavailable for more than 30 minutes. If you want to adjust this timing:

1. Modify the binary_sensor templates in configuration.yaml
2. Change the value in this line: `{{ minutes_since > 30 }}` 
3. Lower the number for faster detection or raise it to reduce false positives