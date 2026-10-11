#!/usr/bin/env python3
"""Print read-only Home Assistant illuminance history as CSV.

Run: python3 /config/scripts/query_illuminance_history.py
Periods use UTC; raw averages use samples and statistics average interval means.
"""

from __future__ import annotations

import csv
import math
import sqlite3
import sys
from collections import defaultdict
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TypeAlias

ENTITIES = (
    "sensor.charlotte_night_light_illuminance_lux",
    "sensor.garage_motion_backdoor_illuminance_lux",
    "sensor.kitchen_motion_illuminance_lux",
    "sensor.office_motion_sensor_illuminance_lux",
    "sensor.owen_night_light_illuminance_lux",
    "sensor.william_night_light_illuminance_lux",
)
SOURCES = ("raw_states_daily", "stats_5min_daily", "stats_hourly_monthly")
Key: TypeAlias = tuple[str, str, str]


@dataclass
class Aggregate:
    records: int = 0
    mean_total: float = 0.0
    mean_count: int = 0
    minimum: float | None = None
    maximum: float | None = None


def as_number(value: object) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def period_utc(timestamp: float, date_format: str) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime(date_format)


def add_value(
    groups: dict[Key, Aggregate], source: str, entity: str, period: str,
    mean: float | None, low: float | None, high: float | None,
) -> None:
    row = groups.setdefault((entity, source, period), Aggregate())
    row.records += 1
    if mean is not None:
        row.mean_total += mean
        row.mean_count += 1
    if low is not None:
        row.minimum = low if row.minimum is None else min(row.minimum, low)
    if high is not None:
        row.maximum = high if row.maximum is None else max(row.maximum, high)


def collect_raw_states(
    db: sqlite3.Connection, groups: dict[Key, Aggregate], tables: set[str]
) -> None:
    if not {"states", "states_meta"} <= tables:
        return
    marks = ",".join("?" for _ in ENTITIES)
    sql = f"""
        SELECT m.entity_id, s.last_updated_ts, s.state
        FROM states s JOIN states_meta m ON m.metadata_id = s.metadata_id
        WHERE m.entity_id IN ({marks}) AND s.last_updated_ts IS NOT NULL
    """
    for entity, timestamp, state in db.execute(sql, ENTITIES):
        value = as_number(state)
        if value is not None:
            add_value(groups, "raw_states_daily", entity,
                      period_utc(timestamp, "%Y-%m-%d"), value, value, value)


def collect_statistics(
    db: sqlite3.Connection, groups: dict[Key, Aggregate], tables: set[str],
    table: str, source: str, date_format: str,
) -> None:
    if table not in tables or "statistics_meta" not in tables:
        return
    marks = ",".join("?" for _ in ENTITIES)
    sql = f"""
        SELECT m.statistic_id, s.start_ts, s.mean, s.min, s.max
        FROM {table} s JOIN statistics_meta m ON m.id = s.metadata_id
        WHERE m.statistic_id IN ({marks}) AND s.start_ts IS NOT NULL
    """
    for entity, timestamp, mean, low, high in db.execute(sql, ENTITIES):
        add_value(groups, source, entity, period_utc(timestamp, date_format),
                  as_number(mean), as_number(low), as_number(high))


def print_report(groups: dict[Key, Aggregate]) -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(("entity_id", "source", "period_utc", "records",
                     "mean_lux", "min_lux", "max_lux"))
    for entity in ENTITIES:
        for source in SOURCES:
            rows = sorted((period, data) for (e, s, period), data in groups.items()
                          if e == entity and s == source)
            if not rows:
                writer.writerow((entity, source, "NO DATA", 0, "", "", ""))
                continue
            for period, data in rows:
                mean = (data.mean_total / data.mean_count) if data.mean_count else None
                writer.writerow((
                    entity, source, period, data.records,
                    f"{mean:.2f}" if mean is not None else "",
                    f"{data.minimum:.2f}" if data.minimum is not None else "",
                    f"{data.maximum:.2f}" if data.maximum is not None else "",
                ))


def main() -> int:
    db_path = Path(__file__).resolve().parents[1] / "home-assistant_v2.db"
    if not db_path.is_file():
        print(f"Recorder database not found: {db_path}", file=sys.stderr)
        return 2
    try:
        with closing(sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=5)) as db:
            db.execute("PRAGMA query_only=ON")
            tables = {row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
            groups: dict[Key, Aggregate] = defaultdict(Aggregate)
            collect_raw_states(db, groups, tables)
            collect_statistics(db, groups, tables, "statistics_short_term",
                               "stats_5min_daily", "%Y-%m-%d")
            collect_statistics(db, groups, tables, "statistics",
                               "stats_hourly_monthly", "%Y-%m")
            print_report(groups)
    except sqlite3.Error as error:
        print(f"Could not read recorder database: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
