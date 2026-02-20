"""Gate device simulators for airport security scenario."""

import random
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class GateEventType(str, Enum):
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    FORCED_OPEN = "forced_open"
    ALARM = "alarm"


class VehicleGateEventType(str, Enum):
    VEHICLE_ENTERED = "vehicle_entered"
    VEHICLE_EXITED = "vehicle_exited"
    TAILGATE_DETECTED = "tailgate_detected"
    ALARM = "alarm"


class PedestrianGate:
    """Simulates a pedestrian gate at an airport entry point."""

    def __init__(self, device_id: str, seed: int | None = None) -> None:
        self.device_id = device_id
        self.device_type = "pedestrian_gate"
        self._rng = random.Random(seed)
        self.is_open: bool = False

    def simulate_event(self) -> dict[str, Any]:
        """Generate a random pedestrian gate security event."""
        event_type: GateEventType = self._rng.choice(list(GateEventType))
        if event_type in (GateEventType.ACCESS_GRANTED, GateEventType.FORCED_OPEN):
            self.is_open = True
        else:
            self.is_open = False

        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "event_type": event_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {"is_open": self.is_open},
        }


class VehicleGate:
    """Simulates a vehicle gate at an airport entry point."""

    def __init__(self, device_id: str, seed: int | None = None) -> None:
        self.device_id = device_id
        self.device_type = "vehicle_gate"
        self._rng = random.Random(seed)
        self.is_open: bool = False

    def simulate_event(self) -> dict[str, Any]:
        """Generate a random vehicle gate security event."""
        event_type: VehicleGateEventType = self._rng.choice(list(VehicleGateEventType))
        if event_type == VehicleGateEventType.VEHICLE_ENTERED:
            self.is_open = True
        elif event_type == VehicleGateEventType.VEHICLE_EXITED:
            self.is_open = False

        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "event_type": event_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {"is_open": self.is_open},
        }
