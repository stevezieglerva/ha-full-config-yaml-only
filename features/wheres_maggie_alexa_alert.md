# Purpose
Announce a guess of Maggie's location in the Alexa ecosystem using a virtual switch in Home Assistant given the timers of recent motion detected upstairs or in the pantry.

# Desired Behavior
- User asks "Alexa, where's Maggie?"
- Alexa routine triggers a change in a wheres maggie virtual switch in HA 
- HA detects that the switch has changed and checks the last motion detected upstairs or in the pantry
- There are several "Minutes since <motion in room>" sensors that track the last motion detected in each room
- check for the room that has the most recent motion detected
- check for the roo that has the 2nd most recent motion detected
- Trigger a room-specific virtual switch for the room with the most recent motion detected
- wait 2 seconds
- Trigger a room-specific virtual switch for the room with the 2nd most recent motion detected


# tasks
Give the desired behavior, create the necessary virtual switches, automations, and scripts to implement the feature.

