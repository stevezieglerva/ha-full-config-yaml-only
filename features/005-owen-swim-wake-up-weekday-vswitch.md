# Owen Early Swim Wake-Up — Weekday Guard + Alexa VSwitch

## Context

The "🏊‍♂️ Owen not awake for early swim" automation fires at 4:50 AM whenever Owen's room motion sensor is inactive — but it has no weekday restriction (could fire on weekends) and no Alexa hook. The fix adds a Mon–Fri guard and replaces/supplements the phone notification with a momentary vswitch pulse that Alexa can react to.

## Changes

### 1. New `input_boolean` in `configuration.yaml` (after line 1188)

Add after `vswitch_alexa_launch_fully_kiosk_bravia_65`:

```yaml
vswitch_announce_owen_swim_wake_up:
  name: "🏊‍♂️🔵 VSwitch Announce Owen Swim Wake Up"
  initial: off
  icon: mdi:swim
```

Entity ID: `input_boolean.vswitch_announce_owen_swim_wake_up`

### 2. Modify automation in `automations.yaml` (lines 5949–5975)

**Condition block changes:**
- Add weekday guard (Mon–Fri)
- Remove `owen_on_wifi` condition (no longer needed)
- Keep room occupancy check

**Action block changes:**
- Keep existing phone notification
- Add: turn on `vswitch_announce_owen_swim_wake_up`, wait 5 seconds, turn it off

Final automation:
```yaml
- id: '1750731652197'
  alias: "🏊‍♂️ Owen not awake for early swim"
  description: ''
  trigger:
  - platform: time
    at: 04:50:00
  condition:
  - condition: time
    weekday:
    - mon
    - tue
    - wed
    - thu
    - fri
  - type: is_not_occupied
    condition: device
    device_id: 236765636ad6b4830327b44e7b9ab4ca
    entity_id: 77ac37fbd504457b6317913dc74dc3ad
    domain: binary_sensor
    for:
      hours: 0
      minutes: 5
      seconds: 0
  action:
  - service: notify.mobile_app_iphone703
    metadata: {}
    data:
      message: "💤 Owen hasn't woke up!"
      data:
        sound: alarm-clock.wav
  - service: input_boolean.turn_on
    target:
      entity_id: input_boolean.vswitch_announce_owen_swim_wake_up
  - delay:
      seconds: 5
  - service: input_boolean.turn_off
    target:
      entity_id: input_boolean.vswitch_announce_owen_swim_wake_up
  mode: single
```

## Verification

1. Reload HA configuration after saving
2. Confirm `input_boolean.vswitch_announce_owen_swim_wake_up` appears in entity list
3. Expose to Alexa via the Alexa integration
4. Create an Alexa routine: trigger = vswitch turns on → action = announcement
5. On a weekday, manually trigger the automation → phone notification fires + vswitch pulses on/off
6. On a weekend, confirm automation does not fire
