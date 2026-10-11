#!/usr/bin/env python3
"""Report weekday on-transitions for the kids' HA light entities.

Run: python3 /config/scripts/query_kids_light_on_history.py
Reports local times for Sep 14–25, 2026. Events may be automation-driven;
input_boolean ceiling-light trackers may not reflect direct device feedback.
"""

from __future__ import annotations

import csv
import sqlite3
import sys
from collections import defaultdict
from contextlib import closing
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import TypeAlias
from zoneinfo import ZoneInfo

LOCAL_ZONE = ZoneInfo("America/New_York")
START = datetime(2026, 9, 14, tzinfo=LOCAL_ZONE)
END = datetime(2026, 9, 26, tzinfo=LOCAL_ZONE)
KID_LIGHTS: dict[str, tuple[str, ...]] = {
    "Charlotte": (
        "input_boolean.charlotte_bedroom_ceiling_light",
        "light.charlotte_night_light_light",
    ),
    "Owen": (
        "input_boolean.owen_bedroom_ceiling_light",
        "light.owen_night_light_light",
        "light.owen_night_light_light_2",
    ),
    "William": (
        "input_boolean.william_bedroom_ceiling_light",
        "light.william_night_light_light",
    ),
}
Key: TypeAlias = tuple[str, str]


def query_on_events(
    db: sqlite3.Connection,
) -> dict[Key, list[datetime]]:
    entity_to_child = {
        entity: child for child, entities in KID_LIGHTS.items() for entity in entities
    }
    marks = ",".join("?" for _ in entity_to_child)
    sql = f"""
        SELECT m.entity_id, s.last_updated_ts
        FROM states s
        JOIN states_meta m ON m.metadata_id = s.metadata_id
        JOIN states old ON old.state_id = s.old_state_id
        WHERE m.entity_id IN ({marks})
          AND s.state = 'on' AND old.state = 'off'
          AND s.last_updated_ts >= ? AND s.last_updated_ts < ?
        ORDER BY s.last_updated_ts
    """
    params = (*entity_to_child, START.timestamp(), END.timestamp())
    events: dict[Key, list[datetime]] = defaultdict(list)
    for entity, timestamp in db.execute(sql, params):
        local_time = datetime.fromtimestamp(timestamp, LOCAL_ZONE)
        if local_time.weekday() < 5:
            events[(entity_to_child[entity], entity)].append(local_time)
    return events


def median_time(events: list[datetime]) -> str:
    minute = round(median([time.hour * 60 + time.minute for time in events])) % 1440
    return f"{minute // 60:02d}:{minute % 60:02d}"


def print_report(events: dict[Key, list[datetime]]) -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(("record_type", "child", "entity_id", "event_count",
                     "median_time_local", "date_local", "weekday", "time_local", "note"))
    for child, entities in KID_LIGHTS.items():
        for entity in entities:
            points = sorted(events.get((child, entity), []))
            prediction = median_time(points) if points else ""
            note = (
                "No retained off-to-on transitions; check Recorder retention."
                if not points else "Transitions may be automation-driven."
            )
            writer.writerow(("summary", child, entity, len(points), prediction,
                             "", "", "", note))
            for timestamp in points:
                writer.writerow(("event", child, entity, "", "",
                                 timestamp.strftime("%Y-%m-%d"),
                                 timestamp.strftime("%A"),
                                 timestamp.strftime("%H:%M"), ""))


def main() -> int:
    db_path = Path(__file__).resolve().parents[1] / "home-assistant_v2.db"
    if not db_path.is_file():
        print(f"Recorder database not found: {db_path}", file=sys.stderr)
        return 2
    try:
        with closing(sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=5)) as db:
            db.execute("PRAGMA query_only=ON")
            events = query_on_events(db)
            print_report(events)
    except sqlite3.Error as error:
        print(f"Could not read recorder database: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
