# CLAUDE.md — AI Assistant Guide for hivemq-demo

This file provides context, conventions, and guidance for AI assistants (Claude Code and others) working in this repository.

---

## Project Overview

**hivemq-demo** is a Python-based agentic system that simulates and manages IoT devices for an airport security scenario. The agent monitors a fleet of virtual devices and publishes security events to a HiveMQ MQTT broker.

### Domain Model

| Device Type       | Count | Sub-types                              |
|-------------------|-------|----------------------------------------|
| Gates             | 10    | 5 Pedestrian Gates, 5 Vehicle Gates    |
| Motion Detectors  | 10    | N/A                                    |

The agent's responsibilities:
- Simulate device state (open/closed, triggered/idle, etc.)
- Monitor all devices continuously
- Generate and publish **security events** to HiveMQ via MQTT

---

## Tech Stack

| Layer             | Technology                        |
|-------------------|-----------------------------------|
| Language          | Python 3                          |
| MQTT Client       | `paho-mqtt`                       |
| Message Broker    | HiveMQ (MQTT protocol)            |
| Testing           | pytest (expected)                 |
| Linting           | Ruff (expected, per .gitignore)   |
| Type Checking     | mypy (expected, per .gitignore)   |

---

## Repository Structure

The project is in its initial phase. The expected layout once source code is added:

```
hivemq-demo/
├── CLAUDE.md               # This file
├── README.md               # Project overview
├── .gitignore              # Python-standard gitignore
├── requirements.txt        # Python dependencies (to be created)
├── src/                    # Main source package (to be created)
│   ├── agent.py            # Core agentic controller
│   ├── devices/            # Device simulators
│   │   ├── gate.py         # Pedestrian and vehicle gate classes
│   │   └── motion_detector.py
│   └── mqtt_client.py      # HiveMQ/paho-mqtt wrapper
└── tests/                  # Test suite (to be created)
    ├── test_devices.py
    └── test_agent.py
```

> This structure is a recommendation, not yet implemented. Adjust this section as the codebase evolves.

---

## Development Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install paho-mqtt
# Or, once requirements.txt exists:
pip install -r requirements.txt
```

### 3. Configure HiveMQ connection

HiveMQ connection settings (broker host, port, credentials) should be provided via environment variables or a config file — **never hardcoded**. Use a `.env` file locally (already in `.gitignore`):

```
HIVEMQ_HOST=<your-broker-host>
HIVEMQ_PORT=8883
HIVEMQ_USERNAME=<username>
HIVEMQ_PASSWORD=<password>
```

---

## Key Conventions

### Python Style
- Use **Python 3.10+** features where appropriate (match statements, structural pattern matching).
- Follow **PEP 8** formatting. Ruff is the preferred linter/formatter.
- Add **type hints** to all public functions and class methods; mypy should pass without errors.

### MQTT / HiveMQ
- Use **MQTT v5** where the broker supports it (paho-mqtt supports it).
- Default port for TLS connections is **8883**; plain text is **1883** (avoid in production).
- MQTT topic naming convention: `airport/security/<device_type>/<device_id>/events`
  - Example: `airport/security/gate/pedestrian_01/events`
  - Example: `airport/security/motion_detector/md_05/events`
- Use **QoS 1** (at least once) for security events to guarantee delivery.
- Each published message should be a **JSON-encoded payload** with at minimum:
  ```json
  {
    "device_id": "pedestrian_gate_01",
    "device_type": "pedestrian_gate",
    "event_type": "access_granted",
    "timestamp": "2026-02-20T12:00:00Z",
    "payload": {}
  }
  ```

### Device Simulation
- Each device should be an independent class with a clear interface.
- Devices should support a `simulate_event()` method that returns a structured event dict.
- The agent should be able to register and deregister devices at runtime.

### Security Events
Suggested event types (expand as needed):

| Device Type      | Event Types                                      |
|------------------|--------------------------------------------------|
| Pedestrian Gate  | `access_granted`, `access_denied`, `forced_open`, `alarm` |
| Vehicle Gate     | `vehicle_entered`, `vehicle_exited`, `tailgate_detected`, `alarm` |
| Motion Detector  | `motion_detected`, `motion_cleared`, `tamper_alert` |

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Type check
mypy src/
```

- Tests live in the `tests/` directory.
- Mirror the `src/` structure in `tests/` (e.g., `tests/devices/test_gate.py`).
- Mock the MQTT client in unit tests — do not require a live HiveMQ connection for tests to pass.

---

## Git Workflow

- `master` is the primary branch.
- Feature and AI-assistant branches follow the pattern: `claude/<description>-<session-id>`
- Write clear, imperative commit messages: `Add pedestrian gate simulator`, `Fix MQTT reconnect logic`.
- Do not commit `.env` files or any secrets.

---

## Important Reminders for AI Assistants

- **No hardcoded credentials.** Broker host, port, username, and password must come from environment variables.
- **Do not create a live MQTT connection during tests.** Mock `paho.mqtt.client.Client`.
- **Keep device simulators deterministic or controllably random** (accept a seed) so tests are reproducible.
- **Update this file** whenever the project structure, dependencies, or conventions change significantly.
- When adding a new dependency, also add it to `requirements.txt` (or `pyproject.toml` if adopted).
