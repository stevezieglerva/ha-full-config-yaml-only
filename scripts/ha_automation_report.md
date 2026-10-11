# Home Assistant night-light automation report

Generated (UTC): 2026-10-11 14:04:13

This report contains matching automation definitions copied from `automations.yaml` and matching automation entity names from the entity registry. It includes triggers, conditions, actions, and modes from the YAML source. The registry's `disabled_by` value only describes registry-level disablement; it is not the current on/off state of an automation.

The filter selects automations mentioning a target room and a lighting/motion term, plus named night-light automations and N1-N4 references. Review names and entity IDs before uploading because they may identify rooms or devices in this home.

## Matching automation registry entries

| Entity ID | Name | Disabled by |
| --- | --- | --- |
| automation.garage_motion_detected | Garage motion detected | no |
| automation.garage_no_motion | Garage no motion | no |
| automation.record_recent_garage_light_level | 📝 Record recent garage light level | no |
| automation.vacation_night_lights_on | Vacation night lights on | no |
| automation.vacation_lights_off | Vacation night lights off | no |
| automation.turn_on_master_bedroom_tv_late_night | Turn off Master Bedroom TV late night | no |
| automation.pantry_night_light | Pantry night light | no |
| automation.smart_night_light_pantry | Smart Night Light - Pantry | no |
| automation.smart_night_light_coat_closet | Smart Night Light - Coat Closet | no |
| automation.smart_night_light_garage | Smart Night Light - Garage | no |
| automation.smart_night_light_charlotte_room | Smart Night Light - Charlotte Room | no |
| automation.smart_night_light_owen_room | Smart Night Light - Owen Room | no |
| automation.smart_night_light_william_room | Smart Night Light - William Room | no |
| automation.turn_on_master_bedroom_light_when_night_and_occupied | Turn on master bedroom light when night and occupied | no |
| automation.alert_garage_back_door_light_off_at_switch | 💡❌ Alert - Garage Back Door Light Off at Switch | no |
| automation.alert_garage_tool_light_off_at_switch | 💡❌ Alert - Garage Tool Light Off at Switch | no |
| automation.nightly_master_bathroom_fan | Master bathroom fan outlet schedule | no |
| automation.extra_night_light | Extra night light | no |
| automation.extra_night_light_motion_control | Extra night light - Motion control | no |
| automation.n3_light_on | N3 light on | no |
| automation.n3_off | N3 off | no |

## Matching automation definitions from `automations.yaml`

```yaml
- id: '1729293256416'
  alias: Garage motion detected
  description: ''
  triggers:
  - type: occupied
    device_id: 77b1c91800c080836f21f5086b6b1637
    entity_id: e9b79a0705db7c31f403d50ba412c0c0
    domain: binary_sensor
    trigger: device
  - entity_id: binary_sensor.dropzone_aqara_back_door_door
    from: 'off'
    to: 'on'
    trigger: state
  conditions:
  - condition: or
    conditions:
    - condition: state
      entity_id: sensor.night
      state: 'True'
    - condition: numeric_state
      entity_id: sensor.garage_motion_backdoor_illuminance_lux
      below: 25
  actions:
  - metadata: {}
    data:
      color_temp_kelvin: 2889
    target:
      area_id: garage
    action: light.turn_on
  mode: single
- id: '1729456902606'
  alias: Garage no motion
  description: ''
  trigger:
  - type: not_occupied
    platform: device
    device_id: 77b1c91800c080836f21f5086b6b1637
    entity_id: e9b79a0705db7c31f403d50ba412c0c0
    domain: binary_sensor
  condition: []
  action:
  - service: light.turn_off
    metadata: {}
    data: {}
    target:
      area_id: garage
  mode: single
- id: '1730058846069'
  alias: "\U0001F4DD Record recent garage light level"
  description: ''
  trigger:
  - platform: time_pattern
    seconds: /30
  condition: []
  action:
  - service: input_number.set_value
    target:
      entity_id: input_number.recent_garage_light_level
    data:
      value: '{{ states(''sensor.garage_motion_backdoor_illuminance_lux'') | float
        }}'
  mode: single
- id: '1731374918834'
  alias: Log back door light on
  description: ''
  trigger:
  - platform: device
    type: turned_on
    device_id: b95c94a8b8cdad187c610f1f0b3fd356
    entity_id: 5aba52409b2df46871b28bd7c588c84f
    domain: light
  condition: []
  action:
  - service: logbook.log
    metadata: {}
    data:
      name: Garage Back Door Light
      message: Turned on
      entity_id: light.garage_back_door_light
  mode: single
- id: '1731374985678'
  alias: Log Back Door Light offp
  description: ''
  trigger:
  - platform: device
    type: turned_off
    device_id: b95c94a8b8cdad187c610f1f0b3fd356
    entity_id: 5aba52409b2df46871b28bd7c588c84f
    domain: light
  condition: []
  action:
  - service: logbook.log
    metadata: {}
    data:
      name: Garage Back Door Light
      message: Light turned off
      entity_id: light.garage_back_door_light
  mode: single
- id: '1732470642008'
  alias: "\U0001F3B6 Door open"
  description: chime when the doors open and then I'm out of warning if it's left
    open
  trigger:
  - platform: state
    entity_id:
    - sensor.any_door_open
    from: 'False'
    to: 'True'
  condition: []
  action:
  - choose:
    - conditions:
      - condition: state
        entity_id: binary_sensor.dropzone_aqara_back_door_door
        state: 'on'
      sequence:
      - service: input_boolean.turn_on
        metadata: {}
        data: {}
        target:
          entity_id: input_boolean.back_door_opened_recently
    - conditions:
      - type: is_open
        condition: device
        device_id: 9e390a614d30fa2788bbc0b2677695fa
        entity_id: 04c10c2cfad9f91306b93a7446560b38
        domain: binary_sensor
      sequence:
      - service: input_boolean.turn_on
        metadata: {}
        data: {}
        target:
          entity_id:
          - input_boolean.front_door_opened_recently
    - conditions:
      - type: is_open
        condition: device
        device_id: 67ea44ea7a2992266ef085c35b5bb0b2
        entity_id: 8eac68d685601dd2c7827ba9f0b83a97
        domain: binary_sensor
      sequence:
      - service: input_boolean.turn_on
        metadata: {}
        data: {}
        target:
          entity_id:
          - input_boolean.deck_door_opened_recently
    - conditions:
      - type: is_open
        condition: device
        device_id: 2838551eb36c440364ff5b2c486f4a23
        entity_id: c9df7503c1f20615ae8caa0a78418a5d
        domain: binary_sensor
      sequence:
      - service: input_boolean.turn_on
        metadata: {}
        data: {}
        target:
          entity_id: input_boolean.deck_screen_door_opened_recently
    - conditions:
      - condition: state
        entity_id: binary_sensor.garage_aqara_garage_small_door
        state: 'on'
      sequence:
      - service: input_boolean.turn_on
        metadata: {}
        data: {}
        target:
          entity_id: input_boolean.garage_door_small_opened_recently
  - service: media_player.turn_on
    metadata: {}
    data: {}
    target:
      entity_id: media_player.office_homepod
  - choose:
    - conditions:
      - condition: state
        entity_id: binary_sensor.office_motion_sensor_occupancy
        state: 'off'
      sequence:
      - service: media_player.volume_set
        metadata: {}
        data:
          volume_level: 1
        target:
          entity_id: media_player.office_homepod
  - service: media_player.play_media
    metadata: {}
    data:
      media_content_id: media-source://media_source/local/app_sounds/door-chime.mp3
      media_content_type: music
    target:
      entity_id: media_player.office_homepod
  - service: media_player.volume_set
    metadata: {}
    data:
      volume_level: 0.5
    target:
      entity_id: media_player.office_homepod
  mode: restart
- id: '1732740272360'
  alias: Vacation night lights on
  description: ''
  triggers:
  - entity_id:
    - sensor.night
    to: 'True'
    trigger: state
  conditions:
  - condition: state
    entity_id: input_select.house_mode
    state: "\U0001F3DD️ Vacation"
  actions:
  - metadata: {}
    target:
      entity_id: scene.vacation_lights_on
    enabled: true
    action: scene.turn_on
  - metadata: {}
    data: {}
    target:
      entity_id: input_boolean.vswitch_vacation_night
    action: input_boolean.turn_on
  - metadata: {}
    data: {}
    target:
      entity_id:
      - light.butlers_pantry_light
      - light.kitchen_sink_light
      - light.coat_closet_hall
    action: light.turn_on
  - type: turn_on
    device_id: 8ca1474cea6a4122af672bd220ed9ce6
    entity_id: da6f242407f98532354fcdab4aedd601
    domain: remote
  mode: single
- id: '1732740416569'
  alias: Vacation night lights off
  description: ''
  triggers:
  - at: '23:00:00'
    trigger: time
  conditions:
  - condition: state
    entity_id: input_select.house_mode
    state: "\U0001F3DD️ Vacation"
  actions:
  - metadata: {}
    target:
      entity_id: scene.vacation_lights_off
    enabled: true
    action: scene.turn_on
  - metadata: {}
    data: {}
    target:
      entity_id: input_boolean.vswitch_vacation_night
    action: input_boolean.turn_off
  - metadata: {}
    data: {}
    target:
      entity_id:
      - light.butlers_pantry_light
      - light.coat_closet_hall
      - light.kitchen_sink_light
    action: light.turn_off
  mode: single
- id: '1737892048242'
  alias: "\U0001F333 Backyard lights"
  description: ''
  trigger:
  - platform: state
    entity_id: binary_sensor.dropzone_aqara_back_door_door
    from: 'off'
    to: 'on'
  - type: opened
    platform: device
    device_id: 67ea44ea7a2992266ef085c35b5bb0b2
    entity_id: 8eac68d685601dd2c7827ba9f0b83a97
    domain: binary_sensor
  - type: opened
    platform: device
    device_id: 2838551eb36c440364ff5b2c486f4a23
    entity_id: c9df7503c1f20615ae8caa0a78418a5d
    domain: binary_sensor
  - platform: device
    type: turned_on
    device_id: b95c94a8b8cdad187c610f1f0b3fd356
    entity_id: 5aba52409b2df46871b28bd7c588c84f
    domain: light
  - platform: state
    entity_id: binary_sensor.garage_aqara_garage_small_door
    from: 'off'
    to: 'on'
  - platform: state
    entity_id:
    - input_boolean.steve_on_wifi
    from: 'off'
    to: 'on'
  - platform: state
    entity_id:
    - input_boolean.katharine_on_wifi
    from: 'off'
    to: 'on'
  condition:
  - condition: state
    entity_id: sensor.night
    state: 'True'
  - condition: device
    type: is_off
    device_id: c879297a402a20b452c50410c40b72d2
    entity_id: 7cef3ced64efa588838c6c0d36d16d98
    domain: switch
  action:
  - type: turn_on
    device_id: c879297a402a20b452c50410c40b72d2
    entity_id: 7cef3ced64efa588838c6c0d36d16d98
    domain: switch
  - service: input_boolean.turn_on
    metadata: {}
    data: {}
    target:
      entity_id: input_boolean.vswitch_deck_lights
    enabled: false
  - delay:
      hours: 0
      minutes: 5
      seconds: 0
      milliseconds: 0
  - type: turn_off
    device_id: c879297a402a20b452c50410c40b72d2
    entity_id: 7cef3ced64efa588838c6c0d36d16d98
    domain: switch
  - delay:
      hours: 0
      minutes: 0
      seconds: 1
      milliseconds: 0
  - type: turn_on
    device_id: c879297a402a20b452c50410c40b72d2
    entity_id: 7cef3ced64efa588838c6c0d36d16d98
    domain: switch
  - delay:
      hours: 0
      minutes: 5
      seconds: 0
      milliseconds: 0
  - type: turn_off
    device_id: c879297a402a20b452c50410c40b72d2
    entity_id: 7cef3ced64efa588838c6c0d36d16d98
    domain: switch
  - service: input_boolean.turn_off
    metadata: {}
    data: {}
    target:
      entity_id: input_boolean.vswitch_deck_lights
    enabled: false
  mode: restart
- id: '1743816219648'
  alias: Turn off Master Bedroom TV late night
  description: ''
  trigger:
  - platform: time
    at: 01:00:00
  - platform: time
    at: 01:30:00
  condition: []
  action:
  - service: media_player.volume_set
    metadata: {}
    data:
      volume_level: 0
    target:
      entity_id: media_player.master_bedroom_tv
  - delay:
      hours: 0
      minutes: 0
      seconds: 5
      milliseconds: 0
  - service: media_player.media_pause
    metadata: {}
    data: {}
    target:
      entity_id: media_player.bravia_vu31
  - delay:
      hours: 0
      minutes: 1
      seconds: 0
      milliseconds: 0
  - condition: state
    entity_id: media_player.master_bedroom_tv
    attribute: volume_level
    state: 0
  - type: turn_off
    device_id: dfcd8127c11f911f3dfda80156d1b162
    entity_id: 739c2382be3ad952e3aeed8e2c7eea57
    domain: remote
    enabled: true
  mode: restart
- id: '1747592805843'
  alias: "\U0001F6B6‍♀️‍➡️Most recent room motions"
  description: Records the most recent motion of various motion detectors
  trigger:
  - type: occupied
    platform: device
    device_id: 73b0e9f01107a7254f075391c15b3ca3
    entity_id: 46110b9ab6ad4190ca4bde8d99b7386d
    domain: binary_sensor
    id: charlotte
  - type: occupied
    platform: device
    device_id: 71ccf4e7c04c9f999b4d4e69de0ec325
    entity_id: 41a502ce172a9fc7aaa3cde86c62039c
    domain: binary_sensor
    id: william
  - type: occupied
    platform: device
    device_id: 236765636ad6b4830327b44e7b9ab4ca
    entity_id: 77ac37fbd504457b6317913dc74dc3ad
    domain: binary_sensor
    id: owen
  - type: occupied
    platform: device
    device_id: 4045ad03705b1a1db194ca6220ef6210
    entity_id: 70103ab535967624969f508590e4012b
    domain: binary_sensor
    id: bathroom
  - type: occupied
    platform: device
    device_id: 71eeaaccdfbcb19ec501fb586f2dfdc7
    entity_id: 932a7aecdf9969ecfaf3e7b558bc24aa
    domain: binary_sensor
    id: bedroom
  - platform: state
    entity_id:
    - binary_sensor.office_motion_sensor_occupancy
    from: 'off'
    to: 'on'
    id: office
  - platform: state
    entity_id:
    - binary_sensor.kitchen_motion_occupancy
    from: 'off'
    to: 'on'
    id: kitchen
  - platform: state
    entity_id:
    - binary_sensor.dropzone_motion_occupancy
    from: 'off'
    to: 'on'
    id: dropzone
  - platform: state
    entity_id:
    - binary_sensor.garage_motion_backdoor_occupancy
    from: 'off'
    to: 'on'
    id: garage
  - platform: state
    entity_id:
    - binary_sensor.playroom_motion_occupancy
    from: 'off'
    to: 'on'
    id: playroom
  - platform: state
    entity_id:
    - binary_sensor.pantry_night_light_occupancy_3
    from: 'off'
    to: 'on'
    id: pantry
  - platform: state
    entity_id:
    - binary_sensor.living_room_motion_occupancy
    from: 'off'
    to: 'on'
    id: livingroom
  - type: occupied
    platform: device
    device_id: 541858278f8e0f3bfab5b64b39701cbe
    entity_id: 35849acbafd284cc880dae68ccd797e5
    domain: binary_sensor
    id: office
  condition: []
  action:
  - choose:
    - conditions:
      - condition: trigger
        id:
        - charlotte
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.charlotte_room_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - william
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.william_room_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - owen
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.owen_room_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - bedroom
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.master_bedroom_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - bathroom
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.master_bathroom_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - office
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.office_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - kitchen
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.kitchen_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - dropzone
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.dropzone_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - garage
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.garage_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - playroom
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.playroom_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - pantry
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.pantry_most_recent_motion
    - conditions:
      - condition: trigger
        id:
        - livingroom
      sequence:
      - service: input_datetime.set_datetime
        metadata: {}
        data:
          datetime: '{{ now().strftime(''%Y-%m-%d %H:%M:%S'') }}'
        target:
          entity_id: input_datetime.living_room_most_recent_motion
  mode: single
- id: '1747595318129'
  alias: "\U0001F305 Morning awake notifications"
  description: ''
  trigger:
  - type: occupied
    platform: device
    device_id: 71ccf4e7c04c9f999b4d4e69de0ec325
    entity_id: 41a502ce172a9fc7aaa3cde86c62039c
    domain: binary_sensor
    id: william
  - type: occupied
    platform: device
    device_id: 236765636ad6b4830327b44e7b9ab4ca
    entity_id: 77ac37fbd504457b6317913dc74dc3ad
    domain: binary_sensor
    id: owen
  - type: occupied
    platform: device
    device_id: 73b0e9f01107a7254f075391c15b3ca3
    entity_id: 46110b9ab6ad4190ca4bde8d99b7386d
    domain: binary_sensor
    id: charlotte
  - type: occupied
    platform: device
    device_id: 71eeaaccdfbcb19ec501fb586f2dfdc7
    entity_id: 932a7aecdf9969ecfaf3e7b558bc24aa
    domain: binary_sensor
    id: bedroom
  - type: occupied
    platform: device
    device_id: 4045ad03705b1a1db194ca6220ef6210
    entity_id: 70103ab535967624969f508590e4012b
    domain: binary_sensor
    id: bathroom
  condition:
  - condition: or
    conditions:
    - condition: state
      entity_id: schedule.kids_awake
      state: 'on'
    - condition: state
      entity_id: input_boolean.upstairs_room_motion_alerts
      state: 'on'
  action:
  - choose:
    - conditions:
      - condition: trigger
        id:
        - owen
      sequence:
      - condition: state
        entity_id: timer.owen_suppress_motion_alert
        state: idle
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F7E6 Owen is up"
          data:
            sound: ussd.caf
      - service: timer.start
        metadata: {}
        data: {}
        target:
          entity_id: timer.owen_suppress_motion_alert
    - conditions:
      - condition: trigger
        id:
        - william
      sequence:
      - condition: state
        entity_id: timer.william_suppress_motion_alert
        state: idle
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F7E9 William is up"
          data:
            sound: shake.caf
      - service: timer.start
        metadata: {}
        data: {}
        target:
          entity_id: timer.william_suppress_motion_alert
    - conditions:
      - condition: trigger
        id:
        - charlotte
      sequence:
      - condition: state
        entity_id: timer.charlotte_suppress_motion_alert
        state: idle
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001FA77 Charlotte is up"
          data:
            sound: short_double_high.caf
      - service: timer.start
        metadata: {}
        data: {}
        target:
          entity_id: timer.charlotte_suppress_motion_alert
    - conditions:
      - condition: trigger
        id:
        - bathroom
      sequence:
      - condition: state
        entity_id: timer.master_bathroom_suppress_motion_alert
        state: idle
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F6BD Bathroom motion"
          data:
            sound: short_double_low.caf
      - service: timer.start
        metadata: {}
        data: {}
        target:
          entity_id: timer.master_bathroom_suppress_motion_alert
    - conditions:
      - condition: trigger
        id:
        - bedroom
      sequence:
      - condition: state
        entity_id: timer.master_bedroom_suppress_motion_alert
        state: idle
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F6CC Bedroom motion"
          data:
            sound: ct-busy.caf
      - service: timer.start
        metadata: {}
        data: {}
        target:
          entity_id: timer.master_bedroom_suppress_motion_alert
        enabled: true
  mode: single
- id: '1748791088177'
  alias: Pantry night light
  description: ''
  trigger:
  - platform: state
    entity_id:
    - binary_sensor.pantry_night_light_occupancy_3
    from: 'off'
    to: 'on'
    id: motion
  - platform: state
    entity_id:
    - binary_sensor.pantry_night_light_occupancy_3
    from: 'on'
    to: 'off'
    id: empty
  condition: []
  action:
  - choose:
    - conditions:
      - condition: trigger
        id:
        - motion
      sequence:
      - service: light.turn_on
        metadata: {}
        data:
          brightness_pct: 100
        target:
          entity_id: light.pantry_night_light_light_3
    - conditions:
      - condition: trigger
        id:
        - empty
      sequence:
      - service: light.turn_off
        metadata: {}
        data: {}
        target:
          entity_id: light.pantry_night_light_light_3
  mode: single
- id: '1751062870540'
  alias: "\U0001F415 Maggie Upstairs Motion Detection"
  description: Monitors upstairs rooms for motion when the toggle is on and sends
    notifications
  trigger:
  - type: occupied
    platform: device
    device_id: 73b0e9f01107a7254f075391c15b3ca3
    entity_id: 46110b9ab6ad4190ca4bde8d99b7386d
    domain: binary_sensor
    id: charlotte
  - type: occupied
    platform: device
    device_id: 71ccf4e7c04c9f999b4d4e69de0ec325
    entity_id: 41a502ce172a9fc7aaa3cde86c62039c
    domain: binary_sensor
    id: william
  - type: occupied
    platform: device
    device_id: 236765636ad6b4830327b44e7b9ab4ca
    entity_id: 77ac37fbd504457b6317913dc74dc3ad
    domain: binary_sensor
    id: owen
  - type: occupied
    platform: device
    device_id: 4045ad03705b1a1db194ca6220ef6210
    entity_id: 70103ab535967624969f508590e4012b
    domain: binary_sensor
    id: bathroom
  - type: occupied
    platform: device
    device_id: 71eeaaccdfbcb19ec501fb586f2dfdc7
    entity_id: 932a7aecdf9969ecfaf3e7b558bc24aa
    domain: binary_sensor
    id: bedroom
  condition:
  - condition: state
    entity_id: input_boolean.maggie_upstairs_monitor
    state: 'on'
  action:
  - choose:
    - conditions:
      - condition: trigger
        id:
        - charlotte
      sequence:
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F415 Maggie detected in Charlotte's room!"
          data:
            push:
              sound: dog-bark.wav
    - conditions:
      - condition: trigger
        id:
        - william
      sequence:
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F415 Maggie detected in William's room!"
          data:
            push:
              sound: dog-bark.wav
    - conditions:
      - condition: trigger
        id:
        - owen
      sequence:
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F415 Maggie detected in Owen's room!"
          data:
            push:
              sound: dog-bark.wav
    - conditions:
      - condition: trigger
        id:
        - bathroom
      sequence:
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F415 Maggie detected in the master bathroom!"
          data:
            push:
              sound: dog-bark.wav
    - conditions:
      - condition: trigger
        id:
        - bedroom
      sequence:
      - service: notify.mobile_app_iphone703
        metadata: {}
        data:
          message: "\U0001F415 Maggie detected in the master bedroom!"
          data:
            push:
              sound: dog-bark.wav
  - condition: state
    entity_id: input_boolean.alexa_maggie_alert
    state: 'on'
  - service: input_boolean.turn_on
    metadata: {}
    data: {}
    target:
      entity_id: input_boolean.alexa_maggie_alert
  - delay:
      hours: 0
      minutes: 0
      seconds: 10
      milliseconds: 0
  - service: input_boolean.turn_off
    metadata: {}
    data: {}
    target:
      entity_id: input_boolean.alexa_maggie_alert
  mode: single
- id: smart_night_light_pantry
  alias: Smart Night Light - Pantry
  description: Controls the pantry night light with smart behavior
  trigger:
  - platform: state
    entity_id: binary_sensor.pantry_night_light_occupancy_3
  - platform: state
    entity_id: sensor.night
  - platform: homeassistant
    event: start
  - platform: numeric_state
    entity_id: sensor.kitchen_motion_illuminance_lux
    below: 5
  action:
  - service: script.smart_night_light
    data:
      motion_sensor: binary_sensor.pantry_night_light_occupancy_3
      light_entity: light.pantry_night_light_light_3
      illuminance_sensor: sensor.kitchen_motion_illuminance_lux
      darkness_threshold: 25
      dim_brightness: 20
      bright_brightness: 255
      timeout: 60
  mode: restart
- id: smart_night_light_charlotte
  alias: Smart Night Light - Charlotte Room
  description: Controls Charlotte's room night light with smart behavior
  trigger:
  - platform: state
    entity_id: binary_sensor.charlotte_night_light_occupancy
  - platform: state
    entity_id: sensor.night
  - platform: homeassistant
    event: start
  - platform: numeric_state
    entity_id: sensor.charlotte_night_light_illuminance_lux
    below: 5
  action:
  - service: script.smart_night_light
    data:
      motion_sensor: binary_sensor.charlotte_night_light_occupancy
      light_entity: light.charlotte_night_light_light
      illuminance_sensor: sensor.charlotte_night_light_illuminance_lux
      darkness_threshold: 25
      dim_brightness: 15
      bright_brightness: 100
      timeout: 60
  mode: restart
- id: smart_night_light_owen
  alias: Smart Night Light - Owen Room
  description: Controls Owen's room night light with smart behavior
  trigger:
  - platform: state
    entity_id: binary_sensor.owen_night_light_occupancy
  - platform: state
    entity_id: sensor.night
  - platform: homeassistant
    event: start
  - platform: numeric_state
    entity_id: sensor.owen_night_light_illuminance_lux
    below: 5
  action:
  - service: script.smart_night_light
    data:
      motion_sensor: binary_sensor.owen_night_light_occupancy
      light_entity: light.owen_night_light_light
      illuminance_sensor: sensor.owen_night_light_illuminance_lux
      darkness_threshold: 25
      dim_brightness: 15
      bright_brightness: 100
      timeout: 60
  mode: restart
- id: smart_night_light_william
  alias: Smart Night Light - William Room
  description: Controls William's room night light with smart behavior
  trigger:
  - platform: state
    entity_id: binary_sensor.william_night_light_occupancy
  - platform: state
    entity_id: sensor.night
  - platform: homeassistant
    event: start
  - platform: numeric_state
    entity_id: sensor.william_night_light_illuminance_lux
    below: 5
  action:
  - service: script.smart_night_light
    data:
      motion_sensor: binary_sensor.william_night_light_occupancy
      light_entity: light.william_night_light_light
      illuminance_sensor: sensor.william_night_light_illuminance_lux
      darkness_threshold: 25
      dim_brightness: 15
      bright_brightness: 100
      timeout: 60
  mode: restart
- id: wheres_maggie_alexa_alert
  alias: "\U0001F415 Where's Maggie Alexa Alert"
  description: Triggered by Alexa routine to announce Maggie location based on recent
    motion
  trigger:
  - platform: state
    entity_id: input_boolean.wheres_maggie_trigger
    to: 'on'
  condition: []
  action:
  - variables:
      most_recent_location: '{{ states(''sensor.maggie_s_most_recent_location'') }}'
      second_most_recent_location: '{{ states(''sensor.maggie_s_second_most_recent_location'')
        }}'
  - choose:
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''charlotte'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_charlotte
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''william'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_william
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''owen'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_owen
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''master_bathroom'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_master_bathroom
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''master_bedroom'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_master_bedroom
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''pantry'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_pantry
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''office'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_office
    - conditions:
      - condition: template
        value_template: '{{ most_recent_location == ''unknown'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_no_recent_motion
  - delay: 00:00:02
  - choose:
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''charlotte'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_charlotte
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''william'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_william
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''owen'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_owen
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''master_bathroom'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_master_bathroom
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''master_bedroom'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_master_bedroom
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''pantry'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_pantry
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''office'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_office
    - conditions:
      - condition: template
        value_template: '{{ second_most_recent_location == ''unknown'' }}'
      sequence:
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.maggie_location_no_recent_motion
  - service: input_boolean.turn_off
    target:
      entity_id: input_boolean.wheres_maggie_trigger
  - delay: 00:00:05
  - service: input_boolean.turn_off
    target:
      entity_id:
      - input_boolean.wheres_maggie_trigger
      - input_boolean.maggie_location_charlotte
      - input_boolean.maggie_location_william
      - input_boolean.maggie_location_owen
      - input_boolean.maggie_location_master_bathroom
      - input_boolean.maggie_location_master_bedroom
      - input_boolean.maggie_location_pantry
      - input_boolean.maggie_location_office
      - input_boolean.maggie_location_no_recent_motion
  mode: single
- id: '1753482248994'
  alias: Turn on master bedroom light when night and occupied
  description: ''
  trigger:
  - type: occupied
    platform: device
    device_id: 71eeaaccdfbcb19ec501fb586f2dfdc7
    entity_id: 932a7aecdf9969ecfaf3e7b558bc24aa
    domain: binary_sensor
  condition:
  - condition: time
    before: '23:30:00'
    after: '17:00:00'
  - condition: state
    entity_id: sensor.night
    state: 'True'
  action:
  - service: input_boolean.turn_on
    metadata: {}
    data: {}
    target:
      entity_id: input_boolean.master_bedroom_ceiling_light
  mode: single
- id: william_room_night_mode
  alias: "\U0001F7E9 William's Room - Night Mode Control"
  description: Controls William's night light based on night sensor state
  trigger:
  - platform: state
    entity_id: sensor.night
  condition: []
  action:
  - choose:
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'True'
      sequence:
      - service: light.turn_on
        data:
          brightness: 26
        target:
          entity_id: light.william_night_light_light
      - service: logbook.log
        data:
          name: William's Night Light
          message: 'Night mode ON: Light set to 10% brightness'
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'False'
      sequence:
      - service: light.turn_off
        target:
          entity_id: light.william_night_light_light
        data: {}
      - service: logbook.log
        data:
          name: William's Night Light
          message: 'Night mode OFF: Light turned off'
  mode: single
- id: owen_room_motion_brightness
  alias: "\U0001F7E6 Owen's Room - Motion Brightness Control"
  description: Controls Owen's night light brightness based on motion detection
  trigger:
  - platform: state
    entity_id:
    - binary_sensor.owen_night_light_occupancy_2
    to: 'on'
    id: motion_detected
  - platform: state
    entity_id:
    - binary_sensor.owen_night_light_occupancy_2
    to: 'off'
    id: motion_cleared
  condition:
  - condition: state
    entity_id: sensor.night
    state: 'True'
  action:
  - choose:
    - conditions:
      - condition: trigger
        id: motion_detected
      sequence:
      - service: light.turn_on
        data:
          brightness: 255
        target:
          entity_id: light.owen_night_light_light_2
      - service: logbook.log
        data:
          name: Owen's Night Light
          message: 'Motion detected: Light set to 100% brightness'
    - conditions:
      - condition: trigger
        id: motion_cleared
      sequence:
      - delay:
          minutes: 3
      - service: light.turn_on
        data:
          brightness: 26
        target:
          entity_id: light.owen_night_light_light_2
      - service: logbook.log
        data:
          name: Owen's Night Light
          message: 'No motion for 3 minutes: Light returned to 10% brightness'
  mode: restart
- id: william_room_motion_brightness
  alias: "\U0001F7E9 William's Room - Motion Brightness Control"
  description: Controls William's night light brightness based on motion detection
  trigger:
  - platform: state
    entity_id: binary_sensor.william_night_light_occupancy
    to: 'on'
    id: motion_detected
  - platform: state
    entity_id: binary_sensor.william_night_light_occupancy
    to: 'off'
    id: motion_cleared
  condition:
  - condition: state
    entity_id: sensor.night
    state: 'True'
  - condition: state
    entity_id: light.william_night_light_light
    state: 'on'
  action:
  - choose:
    - conditions:
      - condition: trigger
        id: motion_detected
      sequence:
      - service: light.turn_on
        target:
          entity_id: light.william_night_light_light
        data:
          brightness: 255
      - service: logbook.log
        data:
          name: William's Night Light
          message: 'Motion detected: Light set to 100% brightness'
    - conditions:
      - condition: trigger
        id: motion_cleared
      sequence:
      - delay:
          minutes: 3
      - service: light.turn_on
        target:
          entity_id: light.william_night_light_light
        data:
          brightness: 26
      - service: logbook.log
        data:
          name: William's Night Light
          message: 'No motion for 3 minutes: Light returned to 10% brightness'
  mode: restart
- id: charlotte_room_motion_brightness
  alias: "\U0001F9E1 Charlotte's Room - Motion Brightness Control"
  description: Controls Charlotte's night light brightness based on motion detection
  trigger:
  - platform: state
    entity_id: binary_sensor.charlotte_night_light_occupancy
    to: 'on'
    id: motion_detected
  - platform: state
    entity_id: binary_sensor.charlotte_night_light_occupancy
    to: 'off'
    id: motion_cleared
  condition:
  - condition: state
    entity_id: sensor.night
    state: 'True'
  - condition: state
    entity_id: light.charlotte_night_light_light
    state: 'on'
  - condition: template
    value_template: "{{ not (\n  is_state('sensor.charlotte_has_school_today', 'True')\n
      \ and now().strftime('%H:%M') >= '06:00'\n  and now().strftime('%H:%M') <= '06:30'\n)
      }}"
  action:
  - choose:
    - conditions:
      - condition: trigger
        id: motion_detected
      sequence:
      - service: light.turn_on
        target:
          entity_id: light.charlotte_night_light_light
        data:
          brightness: 255
      - service: logbook.log
        data:
          name: Charlotte's Night Light
          message: 'Motion detected: Light set to 100% brightness'
    - conditions:
      - condition: trigger
        id: motion_cleared
      sequence:
      - delay:
          minutes: 3
      - condition: template
        value_template: "{{ not (\n  is_state('sensor.charlotte_has_school_today',
          'True')\n  and now().strftime('%H:%M') >= '06:00'\n  and now().strftime('%H:%M')
          <= '06:30'\n) }}"
      - service: light.turn_on
        target:
          entity_id: light.charlotte_night_light_light
        data:
          brightness: 26
      - service: logbook.log
        data:
          name: Charlotte's Night Light
          message: 'No motion for 3 minutes: Light returned to 10% brightness'
  mode: restart
- id: charlotte_room_night_mode
  alias: "\U0001F9E1 Charlotte's Room - Night Mode Control"
  description: Controls Charlotte's night light based on night sensor state
  trigger:
  - platform: state
    entity_id: sensor.night
  condition:
  - condition: template
    value_template: "{{ not (\n  is_state('sensor.charlotte_has_school_today', 'True')\n
      \ and now().strftime('%H:%M') >= '06:00'\n  and now().strftime('%H:%M') <= '06:30'\n)
      }}"
  action:
  - choose:
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'True'
      sequence:
      - service: light.turn_on
        target:
          entity_id: light.charlotte_night_light_light
        data:
          brightness: 26
      - service: logbook.log
        data:
          name: Charlotte's Night Light
          message: 'Night mode ON: Light set to 10% brightness'
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'False'
      sequence:
      - service: light.turn_off
        target:
          entity_id: light.charlotte_night_light_light
      - service: logbook.log
        data:
          name: Charlotte's Night Light
          message: 'Night mode OFF: Light turned off'
  mode: single
- id: owen_room_night_mode
  alias: "\U0001F7E6 Owen's Room - Night Mode Control"
  description: Controls Owen's night light based on night sensor state
  trigger:
  - platform: state
    entity_id: sensor.night
  condition: []
  action:
  - choose:
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'True'
      sequence:
      - service: light.turn_on
        target:
          entity_id:
          - light.owen_night_light_light_2
        data:
          brightness: 26
      - service: logbook.log
        data:
          name: Owen's Night Light
          message: 'Night mode ON: Light set to 10% brightness'
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'False'
      sequence:
      - service: light.turn_off
        target:
          entity_id:
          - light.owen_night_light_light_2
        data: {}
      - service: logbook.log
        data:
          name: Owen's Night Light
          message: 'Night mode OFF: Light turned off'
  mode: single
- id: '1691234500002'
  alias: "\U0001F4A1❌ Alert - Garage Back Door Light Off at Switch"
  description: Alert when Garage Back Door Light has been turned off at the switch
  trigger:
  - platform: state
    entity_id:
    - binary_sensor.garage_back_door_light_off_at_switch
    from: Ok
    to: 'on'
  condition: []
  action:
  - service: notify.mobile_app_iphone703
    data:
      message: "\U0001F4A1❌ Garage Back Door Light has been turned off at the switch"
      data:
        push:
          sound: alarm.caf
  - service: input_boolean.turn_on
    target:
      entity_id: input_boolean.alexa_garage_back_door_light_off
    data: {}
  - delay:
      seconds: 5
  - service: input_boolean.turn_off
    target:
      entity_id: input_boolean.alexa_garage_back_door_light_off
    data: {}
  - service: logbook.log
    data:
      name: Garage Back Door Light
      message: Detected as off at the switch
      entity_id: binary_sensor.garage_back_door_light_off_at_switch
  mode: single
- id: '1691234500003'
  alias: "\U0001F4A1❌ Alert - Garage Tool Light Off at Switch"
  description: Alert when Garage Tool Light has been turned off at the switch
  trigger:
  - platform: state
    entity_id:
    - binary_sensor.garage_tool_light_off_at_switch
    from: Ok
    to: 'on'
  condition: []
  action:
  - service: notify.mobile_app_iphone703
    data:
      message: "\U0001F4A1❌ Garage Tool Light has been turned off at the switch"
      data:
        push:
          sound: alarm.caf
  - service: input_boolean.turn_on
    target:
      entity_id: input_boolean.alexa_garage_tool_light_off
    data: {}
  - delay:
      seconds: 5
  - service: input_boolean.turn_off
    target:
      entity_id: input_boolean.alexa_garage_tool_light_off
    data: {}
  - service: logbook.log
    data:
      name: Garage Tool Light
      message: Detected as off at the switch
      entity_id: binary_sensor.garage_tool_light_off_at_switch
  mode: single
- id: '1755364533742'
  alias: Master bathroom fan outlet schedule
  description: Runs the fan from midnight to 2 AM, keeps it off from 2 AM to 6 AM,
    then follows recent upstairs motion.
  triggers:
  - at: 00:00:00
    id: midnight
    trigger: time
  - at: 02:00:00
    id: two-am
    trigger: time
  - at: 06:00:00
    id: six-am
    trigger: time
  - entity_id: input_boolean.recent_upstairs_motion
    from: 'off'
    to: 'on'
    id: motion
    trigger: state
  - entity_id: input_boolean.recent_upstairs_motion
    from: 'on'
    to: 'off'
    id: no-motion
    trigger: state
  conditions: []
  actions:
  - choose:
    - conditions:
      - condition: trigger
        id: midnight
      sequence:
      - type: turn_on
        device_id: 1270cc0ff83d07446858eb388339b38b
        entity_id: 65d9be250ff0d6342c1e9aff462cb072
        domain: switch
      - action: switch.turn_on
        metadata: {}
        target:
          entity_id: switch.master_bathroom_master_bathroom_fan
        data: {}
    - conditions:
      - condition: trigger
        id: two-am
      sequence:
      - type: turn_off
        device_id: 1270cc0ff83d07446858eb388339b38b
        entity_id: 65d9be250ff0d6342c1e9aff462cb072
        domain: switch
      - action: switch.turn_off
        metadata: {}
        target:
          entity_id: switch.master_bathroom_master_bathroom_fan
        data: {}
    - conditions:
      - condition: trigger
        id: six-am
      - condition: state
        entity_id: input_boolean.recent_upstairs_motion
        state: 'on'
      sequence:
      - type: turn_on
        device_id: 1270cc0ff83d07446858eb388339b38b
        entity_id: 65d9be250ff0d6342c1e9aff462cb072
        domain: switch
      - action: switch.turn_on
        metadata: {}
        target:
          entity_id: switch.master_bathroom_master_bathroom_fan
        data: {}
    - conditions:
      - condition: trigger
        id: six-am
      - condition: state
        entity_id: input_boolean.recent_upstairs_motion
        state: 'off'
      sequence:
      - type: turn_off
        device_id: 1270cc0ff83d07446858eb388339b38b
        entity_id: 65d9be250ff0d6342c1e9aff462cb072
        domain: switch
      - action: switch.turn_off
        metadata: {}
        target:
          entity_id: switch.master_bathroom_master_bathroom_fan
        data: {}
    - conditions:
      - condition: trigger
        id: motion
      - condition: time
        after: 06:00:00
      sequence:
      - type: turn_on
        device_id: 1270cc0ff83d07446858eb388339b38b
        entity_id: 65d9be250ff0d6342c1e9aff462cb072
        domain: switch
      - action: switch.turn_on
        metadata: {}
        target:
          entity_id: switch.master_bathroom_master_bathroom_fan
        data: {}
    - conditions:
      - condition: trigger
        id: no-motion
      - condition: time
        after: 06:00:00
      sequence:
      - type: turn_off
        device_id: 1270cc0ff83d07446858eb388339b38b
        entity_id: 65d9be250ff0d6342c1e9aff462cb072
        domain: switch
      - action: switch.turn_off
        metadata: {}
        target:
          entity_id: switch.master_bathroom_master_bathroom_fan
        data: {}
  mode: restart
- id: '1756087189405'
  alias: Extra night light
  description: Controls Charlotte's night light based on night sensor state
  trigger:
  - platform: state
    entity_id: sensor.night
  condition:
  - condition: template
    value_template: "{{ not (\n  is_state('sensor.charlotte_has_school_today', 'True')\n
      \ and now().strftime('%H:%M') >= '06:00'\n  and now().strftime('%H:%M') <= '06:30'\n)
      }}"
  action:
  - choose:
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'True'
      sequence:
      - service: light.turn_on
        metadata: {}
        data:
          brightness_pct: 10
          kelvin: 5363
        target:
          entity_id: light.extra_night_light_light
      - service: logbook.log
        data:
          name: Extra Night Light
          message: 'Night mode ON: Light set to 10% brightness'
    - conditions:
      - condition: state
        entity_id: sensor.night
        state: 'False'
      sequence:
      - service: light.turn_off
        target:
          entity_id:
          - light.extra_night_light_light
        data: {}
      - service: logbook.log
        data:
          name: Charlotte's Night Light
          message: 'Night mode OFF: Light turned off'
  mode: single
- id: '1756088697024'
  alias: Extra night light - Motion control
  description: Controls Charlotte's night light brightness based on motion detection
  triggers:
  - type: occupied
    device_id: 1e1606390f508b7c47a5e337af23f999
    entity_id: c825c080b0125f16455144fa049bf048
    domain: binary_sensor
    id: motion_detected
    for:
      hours: 0
      minutes: 0
      seconds: 2
    trigger: device
  - type: not_occupied
    device_id: 1e1606390f508b7c47a5e337af23f999
    entity_id: c825c080b0125f16455144fa049bf048
    domain: binary_sensor
    id: motion_cleared
    enabled: true
    trigger: device
  - trigger: occupancy.detected
    target:
      entity_id: binary_sensor.master_bathroom_motion_occupancy
    options:
      behavior: each
      for: 00:00:00
    id: motion_detected
  conditions:
  - condition: state
    entity_id: sensor.night
    state: 'True'
  - condition: template
    value_template: "{{ not (\n  is_state('sensor.charlotte_has_school_today', 'True')\n
      \ and now().strftime('%H:%M') >= '06:00'\n  and now().strftime('%H:%M') <= '06:30'\n)
      }}"
  actions:
  - choose:
    - conditions:
      - condition: trigger
        id:
        - motion_detected
      sequence:
      - target:
          entity_id:
          - light.extra_night_light_light
        data:
          brightness: 64
        action: light.turn_on
      - data:
          name: Extra Night Light
          message: 'Motion detected: Light set to 100% brightness'
        action: logbook.log
    - conditions:
      - condition: trigger
        id: motion_cleared
      sequence:
      - delay:
          hours: 0
          minutes: 0
          seconds: 15
          milliseconds: 0
      - condition: template
        value_template: "{{ not (\n  is_state('sensor.charlotte_has_school_today',
          'True')\n  and now().strftime('%H:%M') >= '06:00'\n  and now().strftime('%H:%M')
          <= '06:30'\n) }}"
      - target:
          entity_id:
          - light.extra_night_light_light
        data: {}
        action: light.turn_off
      - data:
          name: Extra Night Light
          message: 'No motion for 3 minutes: Light returned to 10% brightness'
        action: logbook.log
  mode: restart
- id: charlotte_school_morning_lights
  alias: "\U0001F338 Charlotte School Morning Lights"
  description: Sets Charlotte's morning lights to green, yellow, and red before turning
    them off at departure time
  triggers:
  - at: 06:00:00
    id: green
    trigger: time
  - at: 06:05:00
    id: yellow
    trigger: time
  - at: 06:10:00
    id: red
    trigger: time
  - at: 06:30:00
    id: 'off'
    trigger: time
  conditions:
  - condition: state
    entity_id: sensor.charlotte_has_school_today
    state: 'True'
  actions:
  - choose:
    - conditions:
      - condition: trigger
        id: green
      sequence:
      - target:
          entity_id:
          - light.charlotte_night_light_light
          - light.extra_night_light_light
        data:
          brightness_pct: 100
          rgb_color:
          - 0
          - 255
          - 0
        action: light.turn_on
    - conditions:
      - condition: trigger
        id: yellow
      sequence:
      - target:
          entity_id:
          - light.charlotte_night_light_light
          - light.extra_night_light_light
        data:
          brightness_pct: 100
          rgb_color:
          - 255
          - 255
          - 0
        action: light.turn_on
    - conditions:
      - condition: trigger
        id: red
      sequence:
      - target:
          entity_id:
          - light.charlotte_night_light_light
          - light.extra_night_light_light
        data:
          brightness_pct: 100
          rgb_color:
          - 255
          - 0
          - 0
        action: light.turn_on
    - conditions:
      - condition: trigger
        id: 'off'
      sequence:
      - action: light.turn_on
        metadata: {}
        target:
          entity_id:
          - light.extra_night_light_light
          - light.charlotte_night_light_light
        data:
          color_temp_kelvin: 2411
      - target:
          entity_id:
          - light.charlotte_night_light_light
          - light.extra_night_light_light
        action: light.turn_off
  mode: restart
- id: '1791691014819'
  alias: N3 light on
  description: ''
  triggers:
  - trigger: occupancy.detected
    target:
      entity_id: binary_sensor.smart_night_light_w_occupancy_2
    options:
      behavior: each
      for: 00:00:00
  conditions: []
  actions:
  - action: light.turn_on
    metadata: {}
    target:
      entity_id: light.smart_night_light_w_2
    data: {}
  mode: single
- id: '1791692340944'
  alias: N3 off
  description: ''
  triggers:
  - trigger: sun.dawn
    options:
      type: civil
  - trigger: occupancy.cleared
    target:
      entity_id: binary_sensor.smart_night_light_w_occupancy
    options:
      behavior: each
      for:
        hours: 0
        minutes: 0
        seconds: 30
  conditions: []
  actions:
  - action: light.turn_off
    metadata: {}
    target:
      entity_id: light.smart_night_light_w
    data: {}
  mode: single
```

## Optional live automation state query

To report which matching automations are currently on or off and when each last ran, paste this template into Home Assistant's **Developer Tools → Template** and copy its text output into `scripts/ha_automation_states.md`. This is a read-only query and does not require a database dump or API token.

```jinja
{% for s in states.automation | sort(attribute='entity_id') %}
{% set target_area = 'garage' in s.entity_id or 'master_bedroom' in s.entity_id or 'master_bathroom' in s.entity_id %}
{% set target_behavior = 'night' in s.entity_id or 'light' in s.entity_id or 'motion' in s.entity_id or 'occupancy' in s.entity_id or 'illuminance' in s.entity_id or 'lux' in s.entity_id %}
{% if (target_area and target_behavior) or 'smart_night' in s.entity_id or 'extra_night' in s.entity_id or s.entity_id.startswith('automation.n1_') or s.entity_id.startswith('automation.n2_') or s.entity_id.startswith('automation.n3_') or s.entity_id.startswith('automation.n4_') %}
{{ s.entity_id }} | state={{ s.state }} | last_triggered={{ s.attributes.last_triggered or 'never' }} | current={{ s.attributes.current | default(0) }} | mode={{ s.attributes.mode | default('unknown') }}
{% endif %}
{% endfor %}
```

This state query reports current state and recent-run metadata. It does not replace automation traces when investigating why a particular run behaved a certain way.
