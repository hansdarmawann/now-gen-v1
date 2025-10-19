#!/usr/bin/env python3
"""
nowgen: Datetime Extractor and Unique ID Generator

Generates a JSON snapshot of the current time in multiple formats
and various unique identifiers (UUID, ULID, Nano ID).
"""

import argparse
import datetime as dt
import json
import math
import os
import sys
import traceback
import uuid
from typing import Any, Dict, Optional, List

# -----------------------------
# Optional dependency handling
# -----------------------------
MISSING: List[str] = []

# ulid
try:
    import ulid  # type: ignore
    _ULID_OK = True
except Exception:
    _ULID_OK = False
    MISSING.append("ulid-py")

    class _UlidPlaceholder:
        """Fallback ULID generator when library is missing."""
        @staticmethod
        def new():
            return "ULID_LIBRARY_MISSING"

    ulid = _UlidPlaceholder()  # type: ignore

# nanoid
try:
    import nanoid  # type: ignore
    _NANOID_OK = True
except Exception:
    _NANOID_OK = False
    MISSING.append("nanoid")

    class _NanoidPlaceholder:
        """Fallback Nano ID generator when library is missing."""
        @staticmethod
        def generate(size: int = 21):
            return "NANOID_LIBRARY_MISSING"

    nanoid = _NanoidPlaceholder()  # type: ignore

# uuid7 availability (stdlib in Python 3.13+); fallback to uuid6 package
_UUID7_AVAILABLE = hasattr(uuid, "uuid7")
if not _UUID7_AVAILABLE:
    try:
        import uuid6  # type: ignore
        _UUID7_AVAILABLE = True

        def _uuid7():
            """Return a UUIDv7 using uuid6 package."""
            return uuid6.uuid7()  # type: ignore[attr-defined]

    except Exception:
        MISSING.append("uuid6 (for uuid7 on Python < 3.13)")

        def _uuid7():
            return "UUID7_LIBRARY_MISSING"
else:

    def _uuid7():
        """Return a UUIDv7 using stdlib (Python 3.13+)."""
        return uuid.uuid7()  # type: ignore[attr-defined]

# -----------------------------
# Constants
# -----------------------------
NAMESPACE_PROJECT = uuid.UUID("f0e1d2c3-b4a5-6789-0011-223344556677")
NAME_STRING = "nowgen_timestamp_data"

# -----------------------------
# Time helpers
# -----------------------------
def maybe_localize(now_utc: dt.datetime, tz: Optional[str]) -> dt.datetime:
    """Return localized time. If tz is None, use system local tz."""
    if tz:
        try:
            from zoneinfo import ZoneInfo  # py39+
            return now_utc.astimezone(ZoneInfo(tz))
        except Exception:
            pass  # fallback below
    return now_utc.astimezone()


def get_julian_day(dt_utc: dt.datetime) -> float:
    """Return Julian Day (JD) for a UTC datetime with fractional day."""
    y = dt_utc.year
    m = dt_utc.month
    d = dt_utc.day
    hr = dt_utc.hour
    mi = dt_utc.minute
    se = dt_utc.second + dt_utc.microsecond / 1_000_000.0

    if m <= 2:
        y -= 1
        m += 12

    A = math.floor(y / 100.0)
    B = 2 - A + math.floor(A / 4.0)

    day_fraction = (hr + mi / 60.0 + se / 3600.0) / 24.0
    jd = (math.floor(365.25 * (y + 4716))
          + math.floor(30.6001 * (m + 1))
          + d + day_fraction + B - 1524.5)
    return jd


def get_excel_date_value(dt_local: dt.datetime) -> float:
    """Return Excel serial date (Windows 1900 date system)."""
    excel_epoch = dt.datetime(1899, 12, 30, tzinfo=dt_local.tzinfo)
    delta = dt_local - excel_epoch
    return delta.total_seconds() / 86400.0


def extract_datetime_info(tz: Optional[str]) -> Dict[str, Any]:
    """Extract current datetime info and identifiers, grouped by category."""
    now_utc = dt.datetime.now(dt.timezone.utc)
    now_local = maybe_localize(now_utc, tz)
    ts_s = now_utc.timestamp()

    iso_cal = now_local.isocalendar()
    yday = now_local.timetuple().tm_yday

    return {
        "time_formats": {
            "Date in Local Time": now_local.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "Date in UTC": now_utc.strftime("%Y-%m-%d %H:%M:%S+00:00"),
            "ISO 8601": now_utc.isoformat().replace("+00:00", "Z"),
            "RFC 2822": now_local.strftime("%a, %d %b %Y %H:%M:%S %z"),
            "RFC 3339": now_utc.isoformat().replace("+00:00", "Z"),
            "Timezone Name": now_local.tzname(),
            "Timezone Offset": now_local.strftime("%z"),
            "Week Number (00-53)": now_local.strftime("%W"),
            "ISO Week (YYYY-Www)": f"{iso_cal.year}-W{iso_cal.week:02d}",
            "Day of Year (001-366)": f"{yday:03d}",
        },
        "epochs": {
            "UNIX Timestamp": int(ts_s),
            "UNIX Timestamp (Milliseconds)": int(ts_s * 1000),
            "UNIX Timestamp (Microseconds)": int(ts_s * 1_000_000),
        },
        "calendars": {
            "Julian Day": get_julian_day(now_utc),
            "Excel DATEVALUE": get_excel_date_value(now_local),
        },
        "identifiers": {
            "uuid": {
                "v1": str(uuid.uuid1()),
                "v3": str(uuid.uuid3(NAMESPACE_PROJECT, NAME_STRING)),
                "v4": str(uuid.uuid4()),
                "v5": str(uuid.uuid5(NAMESPACE_PROJECT, NAME_STRING)),
                "v7": str(_uuid7()),
            },
            "ulid": str(ulid.new()),
            "nanoid": (
                nanoid.generate()
                if hasattr(nanoid, "generate")
                else "NANOID_LIBRARY_MISSING"
            ),
        },
    }


def write_json(obj: Dict[str, Any], out_dir: str,
               filename: Optional[str]) -> str:
    """Write the collected data to a JSON file."""
    os.makedirs(out_dir, exist_ok=True)
    if not filename:
        epoch = int(dt.datetime.now(dt.timezone.utc).timestamp())
        filename = f"nowgen_{epoch}.json"
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False, sort_keys=True)
    return path


def log_error(exc: Exception, ts_int: int) -> str:
    """Write error traceback to a log file and return its path."""
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, f"error_{ts_int}.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Timestamp: {ts_int}\n")
        f.write(f"Error Type: {type(exc).__name__}\n")
        f.write("=" * 40 + "\n")
        traceback.print_exc(file=f)
    return path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the script."""
    parser = argparse.ArgumentParser(
        description="Generate a JSON file with current time formats "
                    "and assorted IDs."
    )
    parser.add_argument("--out-dir", default="output",
                        help="Directory to save JSON (default: output)")
    parser.add_argument("--filename", default=None,
                        help="Optional JSON filename "
                             "(default: nowgen_[timestamp].json)")
    parser.add_argument("--tz", default=None,
                        help="IANA timezone name (e.g., Asia/Jakarta). "
                             "Defaults to system local.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress extra info messages")
    return parser.parse_args()


def main() -> int:
    """Main entry point for the script."""
    args = parse_args()
    now_utc = dt.datetime.now(dt.timezone.utc)
    ts_int = int(now_utc.timestamp())
    try:
        data = extract_datetime_info(args.tz)
        out_path = write_json(data, args.out_dir, args.filename)
        print(f"Extraction complete. Data saved to {out_path}")
        if MISSING and not args.quiet:
            print("\n*** NOTE: Some optional libraries are missing:")
            for lib in MISSING:
                print(f"   - {lib}")
            print("Install with: pip install -r requirements.txt")
        return 0
    except Exception as e:
        path = log_error(e, ts_int)
        print(f"\nFATAL ERROR: Execution failed. Traceback saved to {path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
