"""Motion detector device simulator for airport security scenario."""

import random
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class MotionEventType(str, Enum):
    MOTION_DETECTED = "motion_detected"
    MOTION_CLEARED = "motion_cleared"
    TAMPER_ALERT = "tamper_alert"


class MotionDetector:
    """Simulates a motion detector unit in the airport."""

    def __init__(self, device_id: str, seed: int | None = None) -> None:
        self.device_id = device_id
        self.device_type = "motion_detector"
        self._rng = random.Random(seed)
        self.is_triggered: bool = False

    def simulate_event(self) -> dict[str, Any]:
        """Generate a random motion detector security event."""
        event_type: MotionEventType = self._rng.choice(list(MotionEventType))
        self.is_triggered = event_type == MotionEventType.MOTION_DETECTED

        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "event_type": event_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {"is_triggered": self.is_triggered},
        }
