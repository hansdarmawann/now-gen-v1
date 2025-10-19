# nowgen: Datetime Extractor and Unique ID Generator

`nowgen` is a PEP 8 compliant Python utility designed to extract a comprehensive set of time formats and generate various unique identifiers based on the **current moment**. The output is saved in the **JSON** format inside a dedicated `output/` directory.

## 🛠️ Requirements

The script uses several well-maintained third-party libraries for generating advanced unique IDs like ULID and UUID v7.

-   **Python 3.6+** (Highly compatible with modern versions, including 3.13)

### Installation

It is highly recommended to use a virtual environment.

1.  **Save the files:** Ensure `datetime_extractor.py`, `requirements.txt`, and this `README.md` are in the same directory.
2.  **Install dependencies** using the provided `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

    **NOTE:** If the program fails to run, run the command above first.

## 🚀 How to Use

1.  **Run the script** from your terminal in the project's root directory:

    ```bash
    python datetime_extractor.py
    ```

2.  **View Output:** A folder named `output/` will be created, and the data will be saved to `output/nowgen.json`.

## 📄 Output Data Sample (nowgen.json)

The output captures the exact moment of execution and various formats derived from it.

| Field | Example Value (at 2025-10-19 14:10:28 WIB) | Notes |
| :--- | :--- | :--- |
| **Date in Local Time** | 2025-10-19 14:10:28 WIB | Current time in your local timezone. |
| **Date in UTC** | 2025-10-19 07:10:28+00:00 | Time at Coordinated Universal Time. |
| **ISO 8601** | 2025-10-19T07:10:28.123456Z | Standard international date/time format. |
| **UNIX Timestamp** | 1761894628 | Seconds since the Epoch (Jan 1, 1970). |
| **UNIX Timestamp (Milliseconds)** | 1761894628123 | Timestamp in milliseconds. |
| **UUID v7** | 018247e1-912f-78d1-8178-57a5c89871f3 | Time-ordered, lexicographically sortable ID. |
| **ULID** | 01HF9W58A8A1N8Q9Q5A2B5Q1N8 | Universally Unique Lexicographically Sortable Identifier. |
| **Cuid2** | b6u2o0d9l5a2x4j0n5m1q9h5w6v9n0k1o5p9 | Modern, collision-resistant ID. |