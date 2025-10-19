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

Each run creates a new JSON file with this structure:

```json
{
    "time_formats": {
        "Date in Local Time": "2025-10-19 21:35:01 WIB",
        "Date in UTC": "2025-10-19 14:35:01+00:00",
        "ISO 8601": "2025-10-19T14:35:01.987654Z",
        "RFC 2822": "Sun, 19 Oct 2025 21:35:01 +0700",
        "RFC 3339": "2025-10-19T14:35:01.987654Z",
        "Timezone Name": "WIB",
        "Timezone Offset": "+0700",
        "Week Number (00-53)": "42",
        "ISO Week (YYYY-Www)": "2025-W42",
        "Day of Year (001-366)": "292"
    },
    "epochs": {
        "UNIX Timestamp": 1760880901,
        "UNIX Timestamp (Milliseconds)": 1760880901987,
        "UNIX Timestamp (Microseconds)": 1760880901987654
    },
    "calendars": {
        "Julian Day": 2460725.106,
        "Excel DATEVALUE": 45666.898
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

## 🔑 Supported Identifiers

| Identifier | Description | Sortable? | Notes |
|------------|-------------|-----------|-------|
| **UUID v1** | Timestamp + MAC address | ✅ (time-based) | Leaks machine ID, rarely recommended |
| **UUID v3** | Name-based (MD5 hash) | ❌ | Deterministic given namespace + name |
| **UUID v4** | Random | ❌ | Most common for randomness |
| **UUID v5** | Name-based (SHA-1 hash) | ❌ | Deterministic given namespace + name |
| **UUID v7** | Unix time + randomness | ✅ (time-ordered) | Modern standard, recommended |
| **ULID** | Time + randomness (Crockford Base32) | ✅ | Lexicographically sortable |
| **Nano ID** | URL-safe random string | ❌ | Small, fast, customizable length |

---

## ⚠️ Error Logging

If an error occurs during execution (for example, a missing dependency or an internal Python exception), the script will:

1. Print a message like:

```
FATAL ERROR: Execution failed. Traceback saved to log/error_1761895692.log
```

2. Create a `log/` directory (if it does not exist).  
3. Save a detailed traceback in a file named `error_[UNIX timestamp].log`.

### Example log file (`log/error_1761895692.log`):

```
Timestamp: 1761895692
Error Type: ImportError
========================================
Traceback (most recent call last):
  File "nowgen.py", line 25, in <module>
    import ulid
ModuleNotFoundError: No module named 'ulid'
```
