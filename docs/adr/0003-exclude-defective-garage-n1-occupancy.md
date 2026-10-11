# ADR 0003: Exclude defective Garage N1 occupancy

- Status: Accepted
- Date: 2026-10-11

## Context

`binary_sensor.garage_night_light_w_n1_occupancy` repeatedly reported Detected/Clear cycles while the Garage was empty, including approximately 20-second occupancy periods. Masking the sensor did not stop the behavior, and a device power cycle did not remediate it. This is operational evidence from the running Home Assistant installation; the repository has no live Home Assistant access.

## Decision

Treat the N1 occupancy signal as defective for automation purposes. Exclude it from Garage motion state, motion recency, elapsed-occupancy tracking, dashboard indicators, and motion-driven lighting decisions. Retain `light.garage_night_light_w_n1` in the configuration and existing Garage light targets so the light remains available and controllable. Continue using Garage Motion Backdoor, Garage Night Light-W N2 occupancy, and the Dropzone back-door contact as trusted Garage lighting inputs.

## Consequences

- False N1 occupancy events no longer create trusted Garage motion or turn on Garage lights.
- N1 occupancy is no longer represented as a trusted Motion dashboard signal.
- The N1 light remains controllable, including when targeted with other Garage lights.
- The N1 occupancy entity may still exist in Home Assistant as a raw diagnostic entity, but it is not used by this configuration.
- Home Assistant UI configuration validation and runtime behavior remain pending user confirmation.

## Alternatives considered

- Masking the occupancy sensor: rejected because repeated false cycles continued.
- Power cycling the device: rejected because the behavior persisted after the cycle.
- Removing, disabling, factory-resetting, or re-pairing the smart-light device: rejected because the light capability is still required and those actions exceed this decision's scope.
- Retaining N1 as a trusted motion source: rejected because the observed false events can trigger incorrect motion state, recency, and lighting behavior.
