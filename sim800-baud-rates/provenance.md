# Provenance

Mapping of each field in `data/baud-rates.yaml` to its source document.

| Field | Source | Notes |
| :--- | :--- | :--- |
| `metadata.source_documents` | Per-model Hardware Design Manuals | All ten manuals listed |
| `uart.frame_format` | SIM800 Hardware Design Manuals | Uniformly 8N1 across the family |
| `uart.data_bits` | SIM800 Hardware Design Manuals | 8 |
| `uart.parity` | SIM800 Hardware Design Manuals | none |
| `uart.stop_bits` | SIM800 Hardware Design Manuals | 1 |
| `uart.flow_control_default` | SIM800 Hardware Design Manuals | none |
| `uart.flow_control_optional` | SIM800 Hardware Design Manuals | RTS/CTS available |
| `uart.supported_baud_rates` | SIM800 Hardware Design Manuals | Range 1200 - 460800 |
| `uart.autobauding.supported` | SIM800 Hardware Design Manuals | Yes on main UART |
| `uart.autobauding.min_baud` | SIM800 Hardware Design Manuals | 1200 |
| `uart.autobauding.max_baud` | SIM800 Hardware Design Manuals | 115200 |
| `uart.autobauding.enabled_by_default` | SIM800 Hardware Design Manuals | Disabled by default |
| `uart.default_baud_rate` | SIM800 Hardware Design Manuals | 115200 |
| `models.*.default_baud_rate` | Per-model Hardware Design Manual | 115200 for every model |
| `models.*.autobauding_range` | Per-model Hardware Design Manual | 1200 - 115200 |
| `models.*.notes` | Derived from capability matrix | Cross-reference to `sim800-capabilities` |
