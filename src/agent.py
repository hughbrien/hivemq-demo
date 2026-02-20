"""Core agentic controller for the airport security IoT system."""

import logging
import time
from typing import Any, Protocol

from src.devices.gate import PedestrianGate, VehicleGate
from src.devices.motion_detector import MotionDetector
from src.mqtt_client import MQTTClient

logger = logging.getLogger(__name__)

TOPIC_TEMPLATE = "airport/security/{device_type}/{device_id}/events"


class Device(Protocol):
    """Interface that all device simulators must satisfy."""

    device_id: str
    device_type: str

    def simulate_event(self) -> dict[str, Any]: ...


class SecurityAgent:
    """Monitors a fleet of IoT devices and publishes security events to HiveMQ."""

    def __init__(self, mqtt_client: MQTTClient) -> None:
        self._mqtt = mqtt_client
        self._devices: list[Any] = []

    def register_device(self, device: Any) -> None:
        """Register a device to be monitored by this agent."""
        self._devices.append(device)

    def deregister_device(self, device: Any) -> None:
        """Remove a previously registered device."""
        self._devices.remove(device)

    def _get_topic(self, device_type: str, device_id: str) -> str:
        return TOPIC_TEMPLATE.format(device_type=device_type, device_id=device_id)

    def monitor_once(self) -> None:
        """Simulate one event per device and publish all results."""
        for device in self._devices:
            event = device.simulate_event()
            topic = self._get_topic(event["device_type"], event["device_id"])
            self._mqtt.publish(topic, event)
            logger.info("Published %s -> %s", event["event_type"], topic)

    def run(self, interval: float = 5.0) -> None:
        """Connect and continuously monitor all devices until interrupted."""
        logger.info("Security agent starting with %d devices.", len(self._devices))
        self._mqtt.connect()
        try:
            while True:
                self.monitor_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Agent stopped by user.")
        finally:
            self._mqtt.disconnect()


def create_default_agent(mqtt_client: MQTTClient) -> SecurityAgent:
    """Build a SecurityAgent pre-loaded with the full airport device fleet.

    Fleet:
      - 5 pedestrian gates  (pedestrian_gate_01 … 05)
      - 5 vehicle gates     (vehicle_gate_01 … 05)
      - 10 motion detectors (motion_detector_01 … 10)
    """
    agent = SecurityAgent(mqtt_client)

    for i in range(1, 6):
        agent.register_device(PedestrianGate(f"pedestrian_gate_{i:02d}"))

    for i in range(1, 6):
        agent.register_device(VehicleGate(f"vehicle_gate_{i:02d}"))

    for i in range(1, 11):
        agent.register_device(MotionDetector(f"motion_detector_{i:02d}"))

    return agent
