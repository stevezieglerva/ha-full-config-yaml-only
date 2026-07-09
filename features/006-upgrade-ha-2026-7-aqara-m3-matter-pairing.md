# Aqara M3 Pairing Fix — HA 2024.7.0 → 2026.7.x Upgrade Plan

## Context
Steve can't pair his Aqara Hub M3 with Home Assistant via Matter. Diagnosis is complete and the root cause is confirmed: his HA Core 2024.7.0 runs the Matter integration against **python-matter-server 6.2.2** (Matter 1.2-era, mid-2024). The M3 (global release May 2024, firmware 4.3.7+ required for third-party ecosystems) commissions as a modern Matter bridge that this old server cannot handle — the classic "Discovery timed out / Secure Pairing Failed" failure (same as core issue #134009). Matter itself is already working on his box (9 devices / 71 entities: Eve, ThirdReality, Tapo), so this is purely a version problem, not a setup problem.

The "latest 2026.1.2" in his update dialog is a stale update entity; actual latest is **2026.7.1** (July 3, 2026).

## Target version: 2026.7.x (latest patch)
- 2026.7 ships **Matter Server 9.0** — rewritten on matter.js, Matter 1.5.1 spec, certified stack, dramatically better commissioning reliability. This is the release that makes the M3 pair.
- Anything older (e.g. the offered 2026.1.2) still runs the EOL python-matter-server (final: 8.1.2) with known Aqara-bridge commissioning problems.

## Environment facts (confirmed via Matter diagnostics JSON)
- Home Assistant OS on **aarch64** (64-bit → the 2025.12 32-bit removal does NOT apply; no reflash needed)
- HAOS 12.4 (needs OS update; latest is 18.0; Supervisor marks OS older than last-4 majors unsupported)
- Supervisor 2026.01.1 (already current — auto-updates)
- Recorder: default SQLite, no purge tuning → long schema migration on first boot of each hop
- Custom components: alexa_media 4.10.3, icloud3 3.0.5.2, hacs 2.0.5, cync_lights 1.0.1
- Zigbee via Zigbee2MQTT add-on (separate from Matter path)

## Upgrade strategy: stepped, ≤6 releases per hop (official guidance)
HA keeps YAML→UI migration code for only ~6 releases; official docs say update in increments of ≤6 releases when far behind. Path:

**2024.7.0 → 2025.1.x → 2025.7.x → 2026.1.x → 2026.7.x**

At every hop: full backup → update HACS + custom components → update Core → let recorder migration finish (watch logs/CPU; do not interrupt) → clear Repairs dashboard → next hop. Update **HAOS first** (Settings > System > Updates), before Core hops. Free disk ≥ 2× DB size.

## Config changes needed in this repo (only two real hits)
Grepped the whole config against every breaking change in the span:
1. **`scenes.yaml` — 16 scene entries use mired `color_temp:` (+ `min_mireds`/`max_mireds`)** — removed in 2026.3. Convert to `color_temp_kelvin` (361 mireds ≈ 2770 K, 370 ≈ 2703 K; kelvin = 1,000,000 / mireds) and drop the mired attributes.
2. **`automations.yaml:628` — one `data_template:`** → rename to `data:`.

Not needed (verified absent/safe): `mqtt.publish` `topic_template`/`payload_template` (2025.2 removal), Google Calendar `add_event` (2025.7 removal), `hassio.*` actions (2026.5 raise-on-failure), legacy `platform: template` *sensors* (2026.6 removal — his `template:` block is already modern; the one `platform: template` found is a trigger, which is fine). The 557 `service:` keys and 334 singular `trigger:` keys remain valid in 2026.7 — no rewrite required.

## Breaking changes / gotchas checklist (ordered)
1. **Backup first**; from 2025.1 on, backups are **encrypted by default — save the emergency-kit encryption key immediately** or backups are unrecoverable. Automatic backups default to 04:45.
2. **HAOS 12.4 → 18.x** before Core hops.
3. **HACS 2.0.5 is already the latest release — no update needed.** Note: even 2.0.5 had startup failures on exactly HA 2026.1.2 (hacs #5044); hop to **2026.1.3** to sidestep. Recovery if HACS fails to load: re-run `wget -O - https://get.hacs.xyz | bash -` + restart Core.
4. **Alexa Media Player 4.10.3 → ≥5.15.5** (5.15.5 fixes an HA 2026.7 blocking-call issue; current 5.15.6). A 4.x AMP will not survive the jump. **Expect full Amazon re-auth with 2FA** — school wake-up/departure announcements depend on this; verify after upgrade.
5. **iCloud3 3.0.5.2 → ≥3.5.1** (Apple changed auth in early 2026; old versions can't sign in at all). Expect Apple re-auth/2FA.
6. **cync_lights 1.0.1**: breaks on 2025.3 color-mode enforcement. Migrate to the **official `cync` integration (added 2025.10)** at the 2026.1 hop and remove the custom component; audit automations for Cync entity-ID changes.
7. **Zigbee2MQTT add-on**: update to current 2.x before the 2026.1→2026.7 hop (2026.4 ignores `object_id` in MQTT discovery; old Z2M can produce changed entity IDs). Z2M 2.0 has its own breaking changes — read its changelog at that point.
8. **Recorder migrations**: SQLite = long first boots per hop; don't power-cycle mid-migration.
9. Behavioral changes to audit after landing: template binary sensors returning `None` now read `unknown` not `off` (2025.8); mobile-app zone updates report friendly names not object IDs (2025.11) — check the 192 `device_id:`/tracker-based automations; nested `variables` scoping changed (2025.3/2025.4); Google Calendar entities omit declined events (2024.11) — relevant to school-calendar automations; HomeKit Bridge naming precedence changed (2025.5) — check Apple Home after upgrade.
10. **Matter Server 9.0 migration (at 2026.7)**: auto-migrates data on first start, existing 9 Matter devices are NOT re-commissioned, **no rollback exists**. Take a backup and disable the app watchdog during the first start; if devices show offline afterward, power-cycle them (mDNS re-announce).
11. Automation editor: 2026.7 defaults to purpose-specific triggers — UI change only; classic YAML state triggers unaffected.

## Pairing the M3 (after landing on 2026.7)
1. Aqara app: update M3 firmware to ≥ v4.3.7.
2. Aqara app → Hub M3 device page → **"Third-Party Matter Ecosystems" → Matter Pairing Code** (this per-ecosystem code, NOT the printed QR, is required once the hub is already in Aqara's fabric).
3. HA → Settings > Devices & Services > Add Integration > Matter → "No, it's new" → More options → Matter Accessory → paste code.
4. Keep M3 and HA on the same subnet/VLAN with mDNS + IPv6 link-local working.
5. Expect bridged Zigbee child devices (sensors, switches, plugs, locks, curtains) to appear; **IR blaster and alarm/siren do NOT come through Matter**. Fallback if Matter still misbehaves: pair the M3 via the HomeKit Device integration (exposes more, incl. security system).
6. Note: existing Aqara devices on Zigbee2MQTT stay where they are — moving any to the M3 would change device IDs and break `device_id:`-based automations (187 in automations.yaml).

## Execution scope for this repo (what I'd actually edit)
- `scenes.yaml`: convert 16 mired `color_temp` entries to `color_temp_kelvin`.
- `automations.yaml:628`: `data_template:` → `data:`.
- Write the full upgrade runbook + checklist to `features/006-ha-2026-7-upgrade-aqara-m3.md` so it's tracked in the repo and usable from the HA box.
- Run `scripts/test_yaml_keys.py` (repo's YAML validator) after edits.
- The actual HA OS/Core/add-on updates happen in the HA UI on the live box (manual, with backups) — not from this repo.

## Verification
- After YAML edits: run the repo YAML validator; after each Core hop: check Repairs dashboard + logs for migration completion.
- End state: HA 2026.7.x + Matter Server 9.0.x; M3 commissioned; bridged devices visible under the Matter integration; Alexa announcements and iCloud3 tracking re-authenticated and working.

## Key sources
- https://www.home-assistant.io/blog/2026/07/01/release-20267/ (2026.7, Matter Server 9.0)
- https://www.home-assistant.io/blog/2026/06/23/the-matter-upgrade-youve-been-waiting-for/
- https://github.com/home-assistant/addons/blob/master/matter_server/MIGRATION_FAQ.md
- https://www.home-assistant.io/more-info/unsupported/home_assistant_core_version/ (≤6-release hops)
- https://www.aqara.com/us/product/hub-m3-faq/ (fw 4.3.7+, pairing-code procedure)
- https://github.com/home-assistant/core/issues/134009 (M3 commissioning failure on old stack)
- https://github.com/alandtse/alexa_media_player/releases (5.15.5/5.15.6 for HA 2026.7)
- https://github.com/gcobb321/icloud3/releases (3.5.x Apple auth rework)
- https://www.home-assistant.io/blog/2025/01/03/release-20251/ (backup encryption)
- Per-release breaking changes: home-assistant.io release blogs 2024.8 → 2026.7
