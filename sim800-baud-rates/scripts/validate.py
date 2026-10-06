#!/usr/bin/env python3
"""Validate data/baud-rates.yaml against data/schema/baud-rates.schema.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema is required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "baud-rates.yaml"
SCHEMA_FILE = ROOT / "data" / "schema" / "baud-rates.schema.json"


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found: {DATA_FILE}", file=sys.stderr)
        return 1
    if not SCHEMA_FILE.exists():
        print(f"ERROR: schema file not found: {SCHEMA_FILE}", file=sys.stderr)
        return 1

    with DATA_FILE.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    with SCHEMA_FILE.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)

    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as exc:
        print(f"VALIDATION FAILED: {exc.message}", file=sys.stderr)
        print(f"  at: {'/'.join(str(p) for p in exc.absolute_path)}", file=sys.stderr)
        return 1

    uart = data["uart"]
    if uart["default_baud_rate"] not in uart["supported_baud_rates"]:
        print("VALIDATION FAILED: default_baud_rate not in supported_baud_rates", file=sys.stderr)
        return 1

    ab = uart["autobauding"]
    if ab["supported"] and ab["min_baud"] > ab["max_baud"]:
        print("VALIDATION FAILED: autobauding min_baud > max_baud", file=sys.stderr)
        return 1

    for name, model in data["models"].items():
        if model["default_baud_rate"] not in uart["supported_baud_rates"]:
            print(
                f"VALIDATION FAILED: {name}.default_baud_rate "
                f"({model['default_baud_rate']}) not in supported_baud_rates",
                file=sys.stderr,
            )
            return 1

    print(f"OK: {DATA_FILE.name} is valid ({len(data['models'])} models, "
          f"{len(uart['supported_baud_rates'])} baud rates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
