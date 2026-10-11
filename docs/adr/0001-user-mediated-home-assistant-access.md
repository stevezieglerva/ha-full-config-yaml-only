# ADR 0001: User-mediated Home Assistant access

- Status: Accepted
- Date: 2026-10-11

## Context

The implementation agent has no direct access to the Home Assistant Green instance, UI, API, or runtime state. The local working checkout and the server's config checkout continuously synchronize with this repository's `origin`; the repository's `automations.yaml` is the current tracked automation definition. The user can provide read-only text reports when current runtime or registry evidence is needed.

## Decision

Use this repository and user-provided evidence as the boundary for Home Assistant work. Read configured automation behavior from the current repository YAML; request a server-side text report only for live runtime or registry facts that are not tracked here. Limit changes intended for Home Assistant configuration to YAML unless the user explicitly requests a supporting server-side utility. Treat a push to `origin` as potentially propagating YAML to the server, but do not claim that Home Assistant loaded or validated it without user confirmation.

## Consequences

- The agent cannot inspect live entity states, reload configuration, or validate changes against the running instance.
- Diagnostic output is a point-in-time snapshot, not a live connection to Home Assistant.
- The repo sync path makes current tracked YAML available to the agent and may deliver pushed YAML to the server; it does not expose live entity states or prove a configuration reload succeeded.
- Screenshots are optional. Plain-text reports are preferred for registry, runtime-state, or automation-trace evidence.
