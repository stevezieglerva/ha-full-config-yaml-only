# Implementation Plan: Ecobee Sleep Mode Management

**Plan ID:** 001-sleeping-ecobee  
**Created:** 2026-01-31  
**Status:** Implemented  
**Implemented:** 2026-01-31

## Problem Statement

The ecobee thermostats currently switch to "Away" mode overnight when motion stops, even though people are sleeping in the house. This causes uncomfortable temperature changes during sleep.

## Current Behavior

- When house motion stops → "🔲 Notify house appears empty" automation switches both ecobees to "Away" mode
- When upstairs motion stops → "❄️ Turn off Upstairs Ecobee since empty" automation switches upstairs ecobee to "Away" mode
- These automations run regardless of whether people are sleeping
- `input_boolean.sleeping` is set to 'on' by "Shut down the house" automation (manually triggered before bed)
- `input_boolean.awake` is manually toggled in the morning

## Desired Behavior

- When `input_boolean.sleeping` is 'on', prevent ecobees from switching to "Away" mode
- When going to bed (sleeping turns 'on'), immediately set both ecobees to "Sleep" comfort setting
- When waking up (awake turns 'on'), immediately set both ecobees to "Home" comfort setting

## Technical Details

**Ecobee Device IDs:**
- Upstairs: `abebc99ac3bcf057336b1f0ef5e4d0c8` (entity: `b9cdfe91458734f5b458b1a7525f2f8a`)
- Downstairs: `e107fd237c3ce1ff46b28fd9730fb308` (entity: `3830dc0f63623ab1bc8ce328082975c8`)

**Comfort Settings:**
- Home - Normal occupied temperature
- Away - Energy-saving when house empty
- Sleep - Nighttime temperature

**Automations to Modify:**
1. "🔲 Notify house appears empty" (line ~1769) - controls both ecobees
2. "❄️ Turn off Upstairs Ecobee since empty" (line ~4549) - controls upstairs ecobee

## Implementation Steps

### Step 1: Add sleeping condition to "Notify house appears empty" automation

**File:** `automations.yaml` line ~1769  
**Change:** Add condition to prevent running when sleeping

**Current conditions:**
```yaml
condition:
  - condition: state
    entity_id: sensor.late_night
    state: 'False'
```

**New conditions:**
```yaml
condition:
  - condition: state
    entity_id: sensor.late_night
    state: 'False'
  - condition: state
    entity_id: input_boolean.sleeping
    state: 'off'
```

**Test:** Manually set `input_boolean.sleeping` to 'on', wait for house motion to stop, verify ecobees do not switch to "Away" mode

---

### Step 2: Add sleeping condition to "Turn off Upstairs Ecobee since empty" automation

**File:** `automations.yaml` line ~4549  
**Change:** Add condition to prevent running when sleeping

**Current conditions (partial):**
```yaml
condition:
  - condition: state
    entity_id: schedule.upstairs_ecobee_schedule
    state: 'on'
  - condition: state
    entity_id: input_boolean.alexa_cool_upstairs
    state: 'off'
  - condition: numeric_state
    entity_id: sensor.ktta_temperature
    above: 70
  - condition: state
    entity_id: input_boolean.heat_wave
    state: 'off'
    alias: "Confirm 🥵 Heat Wave is off because that will keep AC going"
```

**Add new condition:**
```yaml
  - condition: state
    entity_id: input_boolean.sleeping
    state: 'off'
```

**Test:** Manually set `input_boolean.sleeping` to 'on', wait for upstairs motion to stop, verify upstairs ecobee does not switch to "Away" mode

---

### Step 3: Create automation to set ecobees to Sleep mode

**File:** `automations.yaml`  
**Change:** Add new automation

**New automation:**
```yaml
- id: '[generate-new-id]'
  alias: "🌙 Set Ecobees to Sleep Mode"
  description: ''
  trigger:
  - platform: state
    entity_id:
    - input_boolean.sleeping
    from: 'off'
    to: 'on'
  condition: []
  action:
  - device_id: abebc99ac3bcf057336b1f0ef5e4d0c8
    domain: select
    entity_id: b9cdfe91458734f5b458b1a7525f2f8a
    type: select_option
    option: sleep
  - device_id: e107fd237c3ce1ff46b28fd9730fb308
    domain: select
    entity_id: 3830dc0f63623ab1bc8ce328082975c8
    type: select_option
    option: sleep
  mode: single
```

**Test:** Run "Shut down the house" automation, verify both ecobees immediately switch to "Sleep" comfort setting

---

### Step 4: Create automation to set ecobees to Home mode

**File:** `automations.yaml`  
**Change:** Add new automation

**New automation:**
```yaml
- id: '[generate-new-id]'
  alias: "☀️ Set Ecobees to Home Mode"
  description: ''
  trigger:
  - platform: state
    entity_id:
    - input_boolean.awake
    from: 'off'
    to: 'on'
  condition: []
  action:
  - device_id: abebc99ac3bcf057336b1f0ef5e4d0c8
    domain: select
    entity_id: b9cdfe91458734f5b458b1a7525f2f8a
    type: select_option
    option: home
  - device_id: e107fd237c3ce1ff46b28fd9730fb308
    domain: select
    entity_id: 3830dc0f63623ab1bc8ce328082975c8
    type: select_option
    option: home
  mode: single
```

**Test:** Manually toggle `input_boolean.awake` to 'on', verify both ecobees immediately switch to "Home" comfort setting

---

## Testing Plan

### Test 1: Prevent Away mode during sleep (house empty)
1. Set `input_boolean.sleeping` to 'on'
2. Wait for `sensor.recent_house_motion` to change from 'True' to 'False'
3. Verify "🔲 Notify house appears empty" automation does not run
4. Verify both ecobees remain in current comfort setting (not "Away")

### Test 2: Prevent Away mode during sleep (upstairs empty)
1. Set `input_boolean.sleeping` to 'on'
2. Wait for `input_boolean.recent_upstairs_motion` to change from 'on' to 'off'
3. Verify "❄️ Turn off Upstairs Ecobee since empty" automation does not run
4. Verify upstairs ecobee remains in current comfort setting (not "Away")

### Test 3: Sleep mode activation
1. Trigger "Shut down the house" automation (toggle `input_boolean.shutting_down_house_for_night`)
2. Verify `input_boolean.sleeping` changes to 'on'
3. Verify both ecobees immediately switch to "Sleep" comfort setting
4. Check ecobee displays show "Sleep" mode active

### Test 4: Home mode activation
1. Toggle `input_boolean.awake` from 'off' to 'on'
2. Verify both ecobees immediately switch to "Home" comfort setting
3. Check ecobee displays show "Home" mode active
4. Verify `input_boolean.sleeping` is 'off'

### Test 5: Normal Away mode still works when awake
1. Ensure `input_boolean.sleeping` is 'off'
2. Wait for house motion to stop
3. Verify "🔲 Notify house appears empty" automation runs
4. Verify both ecobees switch to "Away" mode

## Rollback Plan

If issues occur:
1. Remove the `input_boolean.sleeping` conditions from both automations
2. Delete the two new automations ("🌙 Set Ecobees to Sleep Mode" and "☀️ Set Ecobees to Home Mode")
3. Restart Home Assistant
4. Ecobees will return to previous behavior (switching to Away when motion stops)

## Success Criteria

- ✅ Ecobees do not switch to "Away" mode when `input_boolean.sleeping` is 'on'
- ✅ Both ecobees switch to "Sleep" mode when going to bed
- ✅ Both ecobees switch to "Home" mode when waking up
- ✅ Normal "Away" mode behavior works when not sleeping
- ✅ No errors in Home Assistant logs
- ✅ Comfortable sleep temperature maintained overnight

## Notes

- This feature was originally documented in `features/2026-01-20-ecobee-sleep-mode-management.md` but not implemented
- The KIRO.md steering document already includes documentation for this feature
- Ecobee comfort settings (Home/Away/Sleep) must be pre-configured in the ecobee thermostats
