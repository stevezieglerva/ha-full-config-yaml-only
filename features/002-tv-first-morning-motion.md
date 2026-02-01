# Implementation Plan: Turn On TV at First Morning Downstairs Motion

**Plan ID:** 002-tv-first-morning-motion  
**Created:** 2026-02-01  
**Status:** Implemented  
**Implemented:** 2026-02-01  

## Problem Statement

The Sony 65" Bravia TV should automatically turn on when the first downstairs motion is detected after 5:00 AM each morning. This replaces manual TV turn-on during the morning routine.

## Current Behavior

- Downstairs motion is tracked via `input_boolean.recent_downstairs_motiin` (note: intentional misspelling)
- No automation currently turns on the TV based on morning motion
- Existing pattern: Back door opening after 5 AM triggers awake mode using `input_datetime.back_door_first_opened`

## Desired Behavior

- When first downstairs motion detected after 5:00 AM → Turn on Sony 65" Bravia TV
- Only trigger once per morning (reset at midnight)
- Run every day (no weekday/weekend restrictions)
- Follow existing "first event after 5 AM" pattern from back door automation

## Technical Details

**Entities:**
- TV: `media_player.sony_xbr_65x900f` (Sony 65" Bravia)
- Motion tracker: `input_boolean.recent_downstairs_motiin` (existing, misspelled)
- New helper: `input_datetime.first_downstairs_motion_tv` (to be created)

**Existing Pattern Reference:**
- Automation: "🚪 Log First Back Door Open Time After 5 AM" (line ~3801)
- Uses `input_datetime.back_door_first_opened` to track first occurrence
- Resets at midnight via "🔄 Reset daily configs at midnight" automation (line ~2094)

## Implementation Steps

### Step 1: Add input_datetime helper

**File:** `configuration.yaml` line ~1510 (input_datetime section)  
**Action:** Add new helper to track first TV turn-on

**Add after `living_room_most_recent_motion`:**
```yaml
  first_downstairs_motion_tv:
    name: First Downstairs Motion TV
    has_time: true
```

### Step 2: Create automation to turn on TV

**File:** `automations.yaml`  
**Action:** Add new automation after "🚪 Log First Back Door Open Time After 5 AM" (line ~3830)

**New automation:**
```yaml
- id: '[generate-new-id]'
  alias: "📺 Turn On TV at First Morning Downstairs Motion"
  description: 'Turn on Sony 65" Bravia TV when first downstairs motion detected after 5 AM'
  trigger:
  - platform: state
    entity_id: input_boolean.recent_downstairs_motiin
    from: 'off'
    to: 'on'
  condition:
  - condition: time
    after: 05:00:00
  - condition: template
    value_template: '{{ states(''input_datetime.first_downstairs_motion_tv'') == ''00:00:00'' }}'
  action:
  - service: input_datetime.set_datetime
    target:
      entity_id: input_datetime.first_downstairs_motion_tv
    data:
      time: '{{ now().strftime(''%H:%M:%S'') }}'
  - service: media_player.turn_on
    target:
      entity_id: media_player.sony_xbr_65x900f
    data: {}
  mode: single
```

### Step 3: Add reset to midnight automation

**File:** `automations.yaml` line ~2094  
**Automation:** "🔄 Reset daily configs at midnight"  
**Action:** Add reset for new helper

**Add to action section (after `input_datetime.back_door_first_opened` reset):**
```yaml
  - service: input_datetime.set_datetime
    target:
      entity_id: input_datetime.first_downstairs_motion_tv
    data:
      time: 00:00:00
```

## Testing Plan

1. **Helper Creation:** Verify `input_datetime.first_downstairs_motion_tv` appears in Home Assistant UI
2. **First Trigger:** Walk downstairs after 5 AM, verify TV turns on and helper timestamp is set
3. **No Repeat:** Walk downstairs again, verify TV does not turn on again (helper not at 00:00:00)
4. **Midnight Reset:** After midnight, verify helper resets to 00:00:00
5. **Next Day:** Walk downstairs after 5 AM next day, verify TV turns on again

## Notes

- Keeps existing misspelled entity `input_boolean.recent_downstairs_motiin` unchanged
- Follows established pattern from back door automation for consistency
- No weekday/weekend logic - runs every day
- TV entity confirmed from Home Assistant UI: `media_player.sony_xbr_65x900f`
