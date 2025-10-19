# nowgen: Datetime Extractor and Unique ID Generator

`nowgen` is a PEP 8–compliant Python utility that extracts a comprehensive set of time formats and generates various unique identifiers based on the **current moment**.  
The results are saved as **JSON** in the `output/` directory, with filenames based on the **UNIX timestamp** for easy versioning.

---

## 📁 Project Structure

```
nowgen/
├── nowgen.py                 # The main Python script (PEP 8 compliant)
├── requirements.txt          # Third-party dependencies
├── README.md                 # Project documentation and usage guide
├── output/                   # Stores generated results
│   └── nowgen_[UNIX timestamp].json  # Example output
└── log/                      # Created automatically if errors occur
    └── error_[UNIX timestamp].log    # Error logs
```

---

## 🛠️ Requirements

- **Python 3.8+** (works with latest versions, including 3.13)
- Third-party libraries:
  - [`ulid-py`](https://pypi.org/project/ulid-py/) – ULID generator  
  - [`nanoid`](https://pypi.org/project/nanoid/) – Nano ID generator  
  - [`uuid6`](https://pypi.org/project/uuid6/) – UUIDv7 support for Python < 3.13  

### Installation

It is strongly recommended to use a virtual environment.

1. **Clone/Copy files:** Ensure `nowgen.py`, `requirements.txt`, and this `README.md` are in the same directory.  
2. **Install dependencies** using:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Use

Run the script from your terminal in the project’s root directory:

```bash
python nowgen.py
```

### Optional Arguments
- `--tz <TIMEZONE>` : Use a specific IANA timezone (e.g. `Asia/Jakarta`). Defaults to system local.  
- `--out-dir <DIR>` : Choose output folder (default: `output/`).  
- `--filename <NAME>` : Specify custom filename (default: `nowgen_[timestamp].json`).  
- `--quiet` : Suppress library-missing notices.  

---

## 📄 Example Output (Grouped JSON)

```json
{
    "time_formats": {
        "Date in Local Time": "October 19, 2025 2:45 PM",
        "Date in UTC": "October 19, 2025 7:45 AM",
        "ISO 8601": "2025-10-19T14:45:10+07:00",
        "RFC 2822": "Sun, 19 Oct 2025 14:45:10 +0700",
        "RFC 3339": "2025-10-19T14:45:10+07:00",
        "Timezone Name": "WIB",
        "Timezone Offset": "+0700",
        "Week Number": "43",
        "ISO Week": "2025-W42",
        "Day of Year": "292"
    },
    "epochs": {
        "UNIX Timestamp": 1760880901,
        "UNIX Timestamp (Milliseconds)": 1760880901987,
        "UNIX Timestamp (Microseconds)": 1760880901987654
    },
    "calendars": {
        "Julian Day": 2460967.823,
        "Excel DATEVALUE": 45949
    },
    "identifiers": {
        "uuid": {
            "v1": "d35c37b6-8e8e-11ef-918f-0242ac110002",
            "v3": "01dbdfd1-02af-3a36-838f-d4f17c5221f4",
            "v4": "1a08f607-46ce-45a3-88d0-04b47216dbd3",
            "v5": "44a34e57-d16c-56cb-b7c5-2a7dfaa51d6a",
            "v7": "018e1d20-c6c1-7d4c-b449-6e1fc0e40b09"
        },
        "ulid": "01JC3N5P2K93TVE3JW7FKYJ4Y3",
        "nanoid": "V1jFGxW4V7tPf..."
    }
}
```

---

## 📊 Data Description

| Section       | Field                    | Description                                   | Value Example |
|---------------|--------------------------|-----------------------------------------------|---------------|
| **time_formats** | Date in Local Time       | Human-readable local time                     | `October 19, 2025 2:45 PM` |
|               | Date in UTC              | Human-readable UTC time                       | `October 19, 2025 7:45 AM` |
|               | ISO 8601                 | Standardized ISO 8601 format                  | `2025-10-19T14:45:10+07:00` |
|               | RFC 2822                 | RFC 2822 email timestamp format               | `Sun, 19 Oct 2025 14:45:10 +0700` |
|               | RFC 3339                 | Internet date-time standard                   | `2025-10-19T14:45:10+07:00` |
|               | Timezone Name            | Abbreviation of local timezone                | `WIB` |
|               | Timezone Offset          | Numeric UTC offset                            | `+0700` |
|               | Week Number              | Week of the year (00–53)                      | `43` |
|               | ISO Week                 | ISO year-week format                          | `2025-W42` |
|               | Day of Year              | Ordinal day of the year (001–366)             | `292` |
| **epochs**   | UNIX Timestamp            | Seconds since 1970-01-01 UTC                  | `1760880901` |
|               | UNIX Timestamp (ms)      | Milliseconds since epoch                      | `1760880901987` |
|               | UNIX Timestamp (µs)      | Microseconds since epoch                      | `1760880901987654` |
| **calendars** | Julian Day               | Astronomical Julian Day Number                | `2460967.823` |
|               | Excel DATEVALUE          | Excel serial date number (days since 1900-01-01) | `45949` |
| **identifiers** | UUID v1                 | Time-based UUID (includes MAC)                | `d35c37b6-8e8e-11ef-918f-0242ac110002` |
|               | UUID v3                  | Name-based UUID (MD5)                         | `01dbdfd1-02af-3a36-838f-d4f17c5221f4` |
|               | UUID v4                  | Random UUID                                   | `1a08f607-46ce-45a3-88d0-04b47216dbd3` |
|               | UUID v5                  | Name-based UUID (SHA-1)                       | `44a34e57-d16c-56cb-b7c5-2a7dfaa51d6a` |
|               | UUID v7                  | Time-ordered UUID                             | `018e1d20-c6c1-7d4c-b449-6e1fc0e40b09` |
|               | ULID                     | Lexicographically sortable ID                 | `01JC3N5P2K93TVE3JW7FKYJ4Y3` |
|               | Nano ID                  | Compact URL-safe random string                | `V1jFGxW4V7tPf...` |

---

## ⚠️ Error Logging

If an error occurs during execution (for example, a missing dependency or an internal Python exception), the script will:

1. Print a message like:

```
FATAL ERROR: Execution failed. Traceback saved to log/error_1761895692.log
```

2. Create a `log/` directory (if it does not exist).  
3. Save a detailed traceback in a file named `error_[UNIX timestamp].log`.

---

## 🔗 References

- [time.lol](https://time.lol) — Interactive time and epoch conversion playground  
- [uuid.lol](https://uuid.lol) — UUID playground and decoder  
