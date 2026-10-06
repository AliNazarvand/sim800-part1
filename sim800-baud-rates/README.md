# SIM800 Baud Rates

Data-driven reference for UART baud-rate configuration across the SIM800
family. Extracted from the official SIMCom Hardware Design Manuals.

## Purpose

Store UART baud-rate information (supported rates, autobauding range, and
per-model default) as machine-readable YAML so drivers, probes, and modem
descriptors can consume it without hard-coding constants.

## Structure

- `data/baud-rates.yaml` - source of truth.
- `data/schema/baud-rates.schema.json` - JSON Schema for validation.
- `scripts/validate.py` - validates the YAML against the schema and runs
  semantic checks.
- `scripts/export_cpp.py` - exports the YAML to a C++ header.
- `provenance.md` - per-field source tracking.
- `conflict.md` - recorded conflicts and their resolutions.

## Usage

```bash
pip install -r requirements.txt
python scripts/validate.py
python scripts/export_cpp.py --output baud_rates.hpp
```

## Design Notes

- The YAML file is the single source of truth. Do not hard-code baud-rate
  constants anywhere else.
- The `baud` field of a `ModemDescriptor` should be populated from
  `models.<MODEL>.default_baud_rate`.
- Autobauding is reported as a range, not a single value, because the modem
  negotiates the actual rate with the host.
