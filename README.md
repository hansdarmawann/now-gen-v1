# nowgen: Datetime Extractor and Unique ID Generator

`nowgen` is a PEP 8 compliant Python utility designed to extract a comprehensive set of time formats and generate various unique identifiers based on the **current moment**. The output is saved in the **JSON** format inside a dedicated `output/` directory, using the **UNIX timestamp** in the filename for easy versioning.

## 📁 Project Structure

nowgen/
├── datetime_extractor.py     # The main Python script (PEP 8 compliant)
├── requirements.txt          # List of necessary third-party libraries
└── README.md                 # Project documentation and usage guide
└── output/                   # Directory created by the script to store results
    └── nowgen_[UNIX timestamp].json  # The output file (e.g., nowgen_1761895692.json)


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

2.  **View Output:** A folder named `output/` will be created, and the data will be saved to a file named like `output/nowgen_1761895692.json`.

## 📄 Output Data Sample

The output file's name will be based on the exact moment it was run, ensuring every run creates a uniquely named file.

| Field | Example Value |
| :--- | :--- |
| **Output Filename** | `nowgen_1761895692.json` |
| **Date in Local Time** | 2025-10-19 14:14:12 WIB |
| **UNIX Timestamp** | 1761895692 |