# Master Bathroom Fan Schedule

## Summary

Keep the fan off from 6:00 AM through 3:00 PM, then resume the existing recent-upstairs-motion behavior after 3:00 PM.

## Changes

- Update the schedule description to reflect the new operating window.
- Add a 3:00 PM time trigger.
- Turn the fan off at 6:00 AM regardless of motion state.
- Resume motion-based control at 3:00 PM:
  - Turn on if recent upstairs motion is active.
  - Keep it off otherwise.
- Prevent motion events during the restricted period from turning the fan on.

## Tests

- Validate the YAML with the repository’s YAML key test.
- Verify the automation includes 6:00 AM and 3:00 PM transitions.
- Confirm motion does not activate the fan between those times.
- Confirm motion control resumes after 3:00 PM.

## Assumption

“At 3:00 PM” means the fan may resume immediately based on the current motion state.
