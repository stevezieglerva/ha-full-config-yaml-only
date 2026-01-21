# Ecobee Sleep Mode Management

## Problem Statement
Currently, the ecobee thermostats can switch to "Away" mode overnight when motion stops, even though people are sleeping in the house. This causes uncomfortable temperature changes during sleep.

## Requirements
- Use `input_boolean.sleeping` to determine sleep state
- Prevent ecobee from switching to "Away" mode when sleeping
- Set both ecobees to "Sleep" mode immediately when `input_boolean.sleeping` turns on
- Return both ecobees to "Home" mode immediately when `input_boolean.awake` turns on
- Ecobee has Home, Away, and Sleep comfort settings configured

## Background
- `input_boolean.sleeping` is set by "Shut down the house" automation
- `input_boolean.awake` is manually triggered in the morning
- Two automations currently switch ecobees to "Away" mode:
  1. "🔲 Notify house appears empty" (line 1768) - both ecobees
  2. "❄️ Turn off Upstairs Ecobee since empty" (line 4497) - upstairs only
- Ecobee device IDs:
  - Upstairs: `abebc99ac3bcf057336b1f0ef5e4d0c8` (entity: `b9cdfe91458734f5b458b1a7525f2f8a`)
  - Downstairs: `e107fd237c3ce1ff46b28fd9730fb308` (entity: `3830dc0f63623ab1bc8ce328082975c8`)

## Proposed Solution
1. Add `input_boolean.sleeping` condition to prevent "Away" mode during sleep
2. Create automation to set ecobees to "Sleep" mode when sleeping
3. Create automation to set ecobees to "Home" mode when awake

## Task Breakdown

### Task 1: Prevent "Away" mode when sleeping - House empty automation
- **Objective**: Modify "🔲 Notify house appears empty" automation to not run when sleeping
- **Implementation**: Add condition checking `input_boolean.sleeping` is 'off'
- **Location**: `automations.yaml` line ~1768
- **Demo**: When `input_boolean.sleeping` is on, house appearing empty will not switch ecobees to Away mode

### Task 2: Prevent "Away" mode when sleeping - Upstairs empty automation
- **Objective**: Modify "❄️ Turn off Upstairs Ecobee since empty" automation to not run when sleeping
- **Implementation**: Add condition checking `input_boolean.sleeping` is 'off'
- **Location**: `automations.yaml` line ~4497
- **Demo**: When `input_boolean.sleeping` is on, upstairs appearing empty will not switch ecobee to Away mode

### Task 3: Set ecobees to Sleep mode when going to bed
- **Objective**: Create automation that sets both ecobees to "Sleep" comfort setting when sleeping
- **Implementation**: 
  - Trigger: `input_boolean.sleeping` changes from 'off' to 'on'
  - Action: Set both upstairs and downstairs ecobee to "sleep" option
- **Location**: New automation in `automations.yaml`
- **Demo**: When "Shut down the house" runs and sets sleeping=on, both ecobees switch to Sleep mode

### Task 4: Set ecobees to Home mode when waking up
- **Objective**: Create automation that sets both ecobees to "Home" comfort setting when awake
- **Implementation**:
  - Trigger: `input_boolean.awake` changes from 'off' to 'on'
  - Action: Set both upstairs and downstairs ecobee to "home" option
- **Location**: New automation in `automations.yaml`
- **Demo**: When awake button is pressed, both ecobees switch to Home mode

### Task 5: Update KIRO.md documentation
- **Objective**: Document the sleep mode management system
- **Implementation**: Add section explaining how `input_boolean.sleeping` controls ecobee behavior
- **Location**: `.kiro/steering/KIRO.md`
- **Demo**: Documentation clearly explains the sleep mode automation system
