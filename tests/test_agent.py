"""Unit tests for the SecurityAgent controller."""

from unittest.mock import MagicMock

import pytest

from src.agent import SecurityAgent, create_default_agent
from src.devices.gate import PedestrianGate, VehicleGate
from src.devices.motion_detector import MotionDetector


class TestSecurityAgent:
    def setup_method(self) -> None:
        self.mock_mqtt = MagicMock()
        self.agent = SecurityAgent(self.mock_mqtt)

    def test_register_device(self) -> None:
        gate = PedestrianGate("gate_01", seed=42)
        self.agent.register_device(gate)
        assert gate in self.agent._devices

    def test_deregister_device(self) -> None:
        gate = PedestrianGate("gate_01", seed=42)
        self.agent.register_device(gate)
        self.agent.deregister_device(gate)
        assert gate not in self.agent._devices

    def test_monitor_once_publishes_events(self) -> None:
        gate = PedestrianGate("pedestrian_gate_01", seed=42)
        self.agent.register_device(gate)
        self.agent.monitor_once()
        assert self.mock_mqtt.publish.called

    def test_monitor_once_uses_correct_topic(self) -> None:
        gate = PedestrianGate("pedestrian_gate_01", seed=42)
        self.agent.register_device(gate)
        self.agent.monitor_once()
        topic = self.mock_mqtt.publish.call_args[0][0]
        assert topic == "airport/security/pedestrian_gate/pedestrian_gate_01/events"

    def test_monitor_once_publishes_all_devices(self) -> None:
        for i in range(3):
            self.agent.register_device(PedestrianGate(f"gate_{i:02d}", seed=i))
        self.agent.monitor_once()
        assert self.mock_mqtt.publish.call_count == 3

    def test_monitor_once_vehicle_gate_topic(self) -> None:
        gate = VehicleGate("vehicle_gate_01", seed=42)
        self.agent.register_device(gate)
        self.agent.monitor_once()
        topic = self.mock_mqtt.publish.call_args[0][0]
        assert topic == "airport/security/vehicle_gate/vehicle_gate_01/events"

    def test_monitor_once_motion_detector_topic(self) -> None:
        md = MotionDetector("motion_detector_01", seed=42)
        self.agent.register_device(md)
        self.agent.monitor_once()
        topic = self.mock_mqtt.publish.call_args[0][0]
        assert topic == "airport/security/motion_detector/motion_detector_01/events"

    def test_event_payload_is_dict(self) -> None:
        gate = PedestrianGate("pedestrian_gate_01", seed=42)
        self.agent.register_device(gate)
        self.agent.monitor_once()
        payload = self.mock_mqtt.publish.call_args[0][1]
        assert isinstance(payload, dict)
        assert "device_id" in payload
        assert "event_type" in payload
        assert "timestamp" in payload


class TestCreateDefaultAgent:
    def test_creates_20_devices(self) -> None:
        mock_mqtt = MagicMock()
        agent = create_default_agent(mock_mqtt)
        assert len(agent._devices) == 20

    def test_has_5_pedestrian_gates(self) -> None:
        mock_mqtt = MagicMock()
        agent = create_default_agent(mock_mqtt)
        pedestrian_gates = [d for d in agent._devices if isinstance(d, PedestrianGate)]
        assert len(pedestrian_gates) == 5

    def test_has_5_vehicle_gates(self) -> None:
        mock_mqtt = MagicMock()
        agent = create_default_agent(mock_mqtt)
        vehicle_gates = [d for d in agent._devices if isinstance(d, VehicleGate)]
        assert len(vehicle_gates) == 5

    def test_has_10_motion_detectors(self) -> None:
        mock_mqtt = MagicMock()
        agent = create_default_agent(mock_mqtt)
        motion_detectors = [d for d in agent._devices if isinstance(d, MotionDetector)]
        assert len(motion_detectors) == 10

    def test_pedestrian_gate_ids_are_correct(self) -> None:
        mock_mqtt = MagicMock()
        agent = create_default_agent(mock_mqtt)
        ids = {d.device_id for d in agent._devices if isinstance(d, PedestrianGate)}
        expected = {f"pedestrian_gate_{i:02d}" for i in range(1, 6)}
        assert ids == expected

    def test_vehicle_gate_ids_are_correct(self) -> None:
        mock_mqtt = MagicMock()
        agent = create_default_agent(mock_mqtt)
        ids = {d.device_id for d in agent._devices if isinstance(d, VehicleGate)}
        expected = {f"vehicle_gate_{i:02d}" for i in range(1, 6)}
        assert ids == expected

    def test_motion_detector_ids_are_correct(self) -> None:
        mock_mqtt = MagicMock()
        agent = create_default_agent(mock_mqtt)
        ids = {d.device_id for d in agent._devices if isinstance(d, MotionDetector)}
        expected = {f"motion_detector_{i:02d}" for i in range(1, 11)}
        assert ids == expected
