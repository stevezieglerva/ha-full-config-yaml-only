# House Mode and Alarm Mode Analysis

This document provides a comprehensive analysis of the house mode helper and alarm functionality in the Home Assistant configuration, identifying overlaps and potential improvements.

## House Mode Helper (`input_select.house_mode`)

The house_mode helper acts as a central occupancy state controller for the home automation system, with four distinct states:

1. **🚶Home** - The house is occupied
2. **🔲 Away** - The house is unoccupied
3. **🏝️ Vacation** - The house is in vacation mode
4. **🔐 Armed Home** - The house is occupied but secured

### Automations Using House Mode

#### Home Mode (🚶Home) Automations:
- **Office lights and lamp on with motion** (id: 1729124978730)
  - Turns on office lights when motion is detected
  - Has different behaviors based on time of day (working hours vs. evening)

- **Office light off when empty** (id: 1729125593991)
  - Turns off office lights when no motion is detected

- **Kitchen lights on at night**
  - Controls kitchen lights when illumination is below 25 lux at night

- **Kitchen lights on with motion**
  - Turns on kitchen lights when motion is detected and light level is low

- **Late night light control**
  - Controls downstairs lights during late night hours

- **Midnight scene**
  - Activates a scene at 00:30

- **Set house to away**
  - Changes house_mode from "Home" to "Away" when no recent motion is detected

#### Away Mode (🔲 Away) Automations:
- **Set house to home**
  - Changes house_mode from "Away" to "Home" when motion is detected

- **Garage door security alert**
  - Sends notifications when the garage door opens

#### Vacation Mode (🏝️ Vacation) Automations:
- **Vacation night lights on**
  - Turns on specific lights when it gets dark

- **Vacation night lights off**
  - Turns off vacation lights at 23:00

- **Garage door security alert** (same as mentioned above)
  - Works in multiple modes including "Vacation"

#### Armed Home Mode (🔐 Armed Home) Automations:
- **Garage door security alert**
  - Also works when house_mode is "Armed Home"

### House Mode Transitions

The system has automatic transitions between modes:
- From **Home** to **Away**: When no motion is detected for a period of time
- From **Away** to **Home**: When motion is detected after being away

The other modes (Vacation and Armed Home) appear to be manually set, as there are no automations that automatically transition to these states.

## Alarm Functionality

Rather than having a separate dedicated alarm_mode helper, the system uses:

1. **Alarm Scenes**:
   - `scene.alarm_on` - Activates specific lights when security events occur
   - Scene contains bright lighting for kitchen sink, butler's pantry, and garage areas

2. **Security Notifications**:
   - Mobile alerts with alarm sounds for various events
   - Uses push notification with alarm.caf sound

3. **Armed Home Mode**:
   - A security-focused state within the house_mode helper
   - Used for security monitoring while the house is occupied

## Overlap and Integration Analysis

The overlap primarily exists in how security functions are managed:

1. **House Mode States with Security Purpose**:
   - The "🔐 Armed Home" state is essentially a security mode within the house_mode helper
   - The "🔲 Away" state triggers security notifications for certain events
   - The "🏝️ Vacation" state combines both occupancy information and security requirements

2. **Security Event Handling**:
   - When the house_mode is set to "Away", "Vacation", or "Armed Home" and a garage door opens, the system:
     - Sends a notification: "‼️ Alarm triggered while you're not home!"
     - Activates the alarm_on scene (turns on specific lights)

3. **Scene Activation**:
   - The `scene.alarm_on` scene is triggered based on house_mode states, showing they're integrated
   - This creates a coupling between occupancy state and security response

## Recommendations for Consolidation

Based on the current configuration, here's how the system could be improved to reduce overlap and streamline functionality:

1. **Clarify Purpose of Each Mode**:
   - **House Mode**: Focus purely on occupancy status (Home/Away/Vacation)
   - **Security Mode**: Create a separate helper specifically for security states

2. **Proposed Structure**:
   - **House Mode Helper** (`input_select.house_mode`):
     - 🚶 Home - House is occupied, normal operations
     - 🔲 Away - House is temporarily unoccupied
     - 🏝️ Vacation - House is unoccupied for extended period

   - **New Security Mode Helper** (`input_select.security_mode`):
     - 🔓 Disarmed - No security monitoring
     - 🔐 Armed Home - Security active while home
     - 🚨 Armed Away - Full security while away
     - 🏝️ Vacation Security - Extended away security features

3. **Automation Transitions**:
   - When house_mode changes to "Away", security_mode could automatically change to "Armed Away"
   - When house_mode changes to "Vacation", security_mode could change to "Vacation Security"
   - When house_mode changes to "Home", security_mode could prompt for desired state

4. **Benefits of Separation**:
   - Clearer distinction between occupancy state and security state
   - More flexible security options (can be armed while home without changing occupancy)
   - Easier to expand security features independently
   - Reduced confusion in automation conditions

This separation would allow security to be enabled while home without affecting other home automations, and would make the system more modular while reducing state overlap.

## Implementation Considerations

If implementing these changes, consider:

1. Creating a new `input_select.security_mode` helper in configuration.yaml
2. Updating existing automations to reference the appropriate helper based on purpose
3. Creating transition automations that sync the two helpers when appropriate
4. Migrating security-specific functionality to use the new helper

This approach provides a cleaner separation of concerns while maintaining all current functionality.