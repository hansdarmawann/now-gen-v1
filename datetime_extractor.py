import datetime
import json
import uuid
import math
import os
from typing import Any, Dict

# Third-party libraries for IDs
# Note: These must be installed (see requirements.txt)
try:
    import ulid
    import cuid2
    import nanoid
    import uuid6
except ImportError:
    print("Warning: One or more ID generation libraries (ulid, cuid2, nanoid, uuid6) are not installed.")
    print("Please run 'pip install -r requirements.txt' to install them.")
    
    # Define placeholder classes/functions to allow the rest of the script to run
    class UlidPlaceholder:
        """Placeholder for ulid library."""
        @staticmethod
        def new():
            return 'ULID_LIBRARY_MISSING'
    ulid = UlidPlaceholder

    class Cuid2Placeholder:
        """Placeholder for cuid2 library."""
        @staticmethod
        def create():
            return 'CUID2_LIBRARY_MISSING'
    cuid2 = Cuid2Placeholder

    class NanoidPlaceholder:
        """Placeholder for nanoid library."""
        @staticmethod
        def generate():
            return 'NANOID_LIBRARY_MISSING'
    nanoid = NanoidPlaceholder

    class Uuid6Placeholder:
        """Placeholder for uuid6 library (for UUID v7)."""
        @staticmethod
        def uuid7():
            return 'UUID7_LIBRARY_MISSING'
    uuid6 = Uuid6Placeholder


def get_julian_day(dt_utc: datetime.datetime) -> float:
    """
    Calculates the Julian Day (JD) for a given UTC datetime object.

    Args:
        dt_utc: A datetime object with UTC timezone information.

    Returns:
        The Julian Day as a float.
    """
    # Algorithm based on Fliegel and van Flandern (1968)
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second

    # PEP 8 line continuation uses parentheses
    jd = (367 * year - math.floor(7 * (year + math.floor((month + 9) / 12)) / 4)
          + math.floor(275 * month / 9) + day + 1721013.5
          + (hour + minute / 60 + second / 3600) / 24)

    return jd


def get_excel_date_value(dt_local: datetime.datetime) -> float:
    """
    Calculates the Excel DATEVALUE (number of days since 1/1/1900).

    Args:
        dt_local: A datetime object with local timezone information.

    Returns:
        The Excel serial date value as a float.
    """
    # Excel uses 1/1/1900 as day 1 (with a leap year bug for 1900)
    excel_epoch = datetime.datetime(
        1899, 12, 30, tzinfo=dt_local.tzinfo
    )
    delta = dt_local - excel_epoch
    seconds_in_day = 60 * 60 * 24
    serial = delta.total_seconds() / seconds_in_day

    # Adjust for Excel's 1900 leap year bug
    if dt_local.year > 1900 or (
        dt_local.year == 1900 and dt_local.month > 2
    ):
        serial += 1

    return serial


def extract_datetime_info() -> Dict[str, Any]:
    """Extracts various time formats and unique IDs."""
    now_local = datetime.datetime.now(datetime.timezone.utc).astimezone()
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp_s = now_utc.timestamp()

    # --- Time and Date Extractions ---
    extracted_data = {
        "Date in Local Time": now_local.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "Date in UTC": now_utc.strftime("%Y-%m-%d %H:%M:%S+00:00"),
        "ISO 8601": now_utc.isoformat().replace("+00:00", "Z"),
        "UNIX Timestamp": int(timestamp_s),
        "UNIX Timestamp (Milliseconds)": int(timestamp_s * 1000),
        "Week Number (00-53)": now_local.strftime("%W"),
        "RFC 2822": now_local.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "RFC 3339": now_utc.isoformat().replace("+00:00", "Z"),
        "Julian Day": get_julian_day(now_utc),
        "Excel DATEVALUE": get_excel_date_value(now_local),
    }

    # --- UUID and ID Extractions ---
    extracted_data.update({
        "UUID v1": str(uuid.uuid1()),
        "UUID v2": "N/A: Requires user/group ID for generation (specialized)",
        "UUID v3": "N/A: Requires Namespace UUID and a Name for generation",
        "UUID v4": str(uuid.uuid4()),
        "UUID v5": "N/A: Requires Namespace UUID and a Name for generation",
        "UUID v7": str(uuid6.uuid7()),
        "UUID Decoder": "N/A: Requires an existing UUID to decode",
        "Cuid": "N/A: Use Cuid2 (older library, typically uses JavaScript logic)",
        "Cuid2": cuid2.create(),
        "ULID": str(ulid.new()),
        "Nano ID": nanoid.generate(),
    })

    return extracted_data


def main():
    """Main function to run the extraction and save to JSON."""
    # The first thing we do is get the time, as this drives the output data AND the filename
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp_int = int(now_utc.timestamp())
    
    data = extract_datetime_info()
    
    # Folder and file path setup
    output_dir = "output"
    # New dynamic filename format
    output_filename = f"nowgen_{timestamp_int}.json"
    output_path = os.path.join(output_dir, output_filename)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print(f"Extraction complete. Data saved to {output_path}")


if __name__ == "__main__":
    main()