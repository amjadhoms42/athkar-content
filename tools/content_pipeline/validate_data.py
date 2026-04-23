"""
validate_data.py
Validates the generated JSON files in data/ against required fields.
Exits with code 1 if any errors are found (blocks the CI workflow).

Usage:
  python validate_data.py
"""

import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

# Required fields per file type
REQUIRED = {
    "items.json": ["id", "title", "text", "type", "sectionMain", "status", "interaction"],
    "readings.json": ["id", "title", "type", "section"],
    "segments.json": ["id", "readingId", "segmentNumber", "text"],
    "hijri_content.json": ["id", "hijriMonth", "hijriDay", "entryType", "title"],
}


def validate_file(filename: str, required_fields: list[str]) -> list[str]:
    path = DATA_DIR / filename
    if not path.exists():
        return [f"{filename}: file not found"]

    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{filename}: invalid JSON — {e}"]

    if not isinstance(records, list):
        return [f"{filename}: root must be a JSON array"]

    errors = []
    seen_ids: set[str] = set()

    for i, record in enumerate(records):
        row = i + 1
        for field in required_fields:
            if field not in record or record[field] == "":
                errors.append(f"{filename} row {row}: missing required field '{field}'")

        record_id = record.get("id", "")
        if record_id:
            if record_id in seen_ids:
                errors.append(f"{filename} row {row}: duplicate id '{record_id}'")
            seen_ids.add(record_id)

    return errors


def main():
    all_errors: list[str] = []

    for filename, fields in REQUIRED.items():
        errs = validate_file(filename, fields)
        all_errors.extend(errs)

    if all_errors:
        print("VALIDATION FAILED:")
        for e in all_errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        total = sum(
            len(json.loads((DATA_DIR / f).read_text()))
            for f in REQUIRED
            if (DATA_DIR / f).exists()
        )
        print(f"Validation passed — {total} total records across {len(REQUIRED)} files.")


if __name__ == "__main__":
    main()
