#!/usr/bin/env python3
"""Export data/baud-rates.yaml to a C++ header."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "baud-rates.yaml"


def render(data: dict) -> str:
    uart = data["uart"]
    ab = uart["autobauding"]
    rates = uart["supported_baud_rates"]

    lines = []
    lines.append("// Auto-generated from data/baud-rates.yaml. Do not edit manually.")
    lines.append("#pragma once")
    lines.append("#include <cstdint>")
    lines.append("#include <array>")
    lines.append("")
    lines.append("namespace sim800::baud_rates {")
    lines.append("")
    lines.append(f"constexpr std::uint32_t kDefaultBaudRate = {uart['default_baud_rate']}U;")
    lines.append(f"constexpr bool kAutobaudingSupported = {'true' if ab['supported'] else 'false'};")
    lines.append(f"constexpr std::uint32_t kAutobaudMin = {ab['min_baud']}U;")
    lines.append(f"constexpr std::uint32_t kAutobaudMax = {ab['max_baud']}U;")
    lines.append("")
    lines.append(f"constexpr std::array<std::uint32_t, {len(rates)}> kSupportedBaudRates = {{")
    for r in rates:
        lines.append(f"    {r}U,")
    lines.append("};")
    lines.append("")
    lines.append("// Per-model default baud rates")
    for name, model in sorted(data["models"].items()):
        ident = name.replace("-", "_")
        lines.append(f"constexpr std::uint32_t k{ident}DefaultBaud = {model['default_baud_rate']}U;")
    lines.append("")
    lines.append("} // namespace sim800::baud_rates")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", required=True, help="Output .hpp path")
    args = parser.parse_args()

    if not DATA_FILE.exists():
        print(f"ERROR: data file not found: {DATA_FILE}", file=sys.stderr)
        return 1

    with DATA_FILE.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(data), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
