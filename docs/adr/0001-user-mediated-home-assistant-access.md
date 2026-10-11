# ADR 0001: User-mediated Home Assistant access

- Status: Accepted
- Date: 2026-10-11

## Context

The implementation agent has no direct access to the Home Assistant Green instance. The user can provide screenshots, run commands on the server, and commit diagnostic text reports to this repository. Home Assistant configuration changes are delivered through version-controlled files that the user pulls onto the server.

## Decision

Use this repository and user-provided evidence as the boundary for Home Assistant work. Ask the user to run any server-side diagnostics and share the resulting report through Git or screenshots. Limit changes intended for Home Assistant configuration to YAML unless the user explicitly requests a supporting server-side utility.

## Consequences

- The agent cannot inspect live entity states, reload configuration, or validate changes against the running instance.
- Diagnostic output is evidence for review, not a live connection to Home Assistant.
- Changes requiring runtime validation must be pulled and applied by the user, who can then provide screenshots or a new report.
