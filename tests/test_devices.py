"""Unit tests for device simulators."""

import pytest

from src.devices.gate import GateEventType, PedestrianGate, VehicleGate, VehicleGateEventType
from src.devices.motion_detector import MotionDetector, MotionEventType


class TestPedestrianGate:
    def test_simulate_event_structure(self) -> None:
        gate = PedestrianGate("pedestrian_gate_01", seed=42)
        event = gate.simulate_event()
        assert event["device_id"] == "pedestrian_gate_01"
        assert event["device_type"] == "pedestrian_gate"
        assert event["event_type"] in [e.value for e in GateEventType]
        assert "timestamp" in event
        assert "payload" in event
        assert "is_open" in event["payload"]

    def test_simulate_event_deterministic(self) -> None:
        gate1 = PedestrianGate("gate_01", seed=100)
        gate2 = PedestrianGate("gate_01", seed=100)
        assert gate1.simulate_event()["event_type"] == gate2.simulate_event()["event_type"]

    def test_access_granted_opens_gate(self) -> None:
        found = False
        for seed in range(200):
            gate = PedestrianGate("gate_01", seed=seed)
            event = gate.simulate_event()
            if event["event_type"] == GateEventType.ACCESS_GRANTED.value:
                assert gate.is_open is True
                found = True
                break
        assert found, "No seed in range produced ACCESS_GRANTED"

    def test_access_denied_closes_gate(self) -> None:
        found = False
        for seed in range(200):
            gate = PedestrianGate("gate_01", seed=seed)
            event = gate.simulate_event()
            if event["event_type"] == GateEventType.ACCESS_DENIED.value:
                assert gate.is_open is False
                found = True
                break
        assert found, "No seed in range produced ACCESS_DENIED"

    def test_forced_open_opens_gate(self) -> None:
        found = False
        for seed in range(200):
            gate = PedestrianGate("gate_01", seed=seed)
            event = gate.simulate_event()
            if event["event_type"] == GateEventType.FORCED_OPEN.value:
                assert gate.is_open is True
                found = True
                break
        assert found, "No seed in range produced FORCED_OPEN"


class TestVehicleGate:
    def test_simulate_event_structure(self) -> None:
        gate = VehicleGate("vehicle_gate_01", seed=42)
        event = gate.simulate_event()
        assert event["device_id"] == "vehicle_gate_01"
        assert event["device_type"] == "vehicle_gate"
        assert event["event_type"] in [e.value for e in VehicleGateEventType]
        assert "timestamp" in event
        assert "payload" in event
        assert "is_open" in event["payload"]

    def test_simulate_event_deterministic(self) -> None:
        gate1 = VehicleGate("gate_01", seed=200)
        gate2 = VehicleGate("gate_01", seed=200)
        assert gate1.simulate_event()["event_type"] == gate2.simulate_event()["event_type"]

    def test_vehicle_entered_opens_gate(self) -> None:
        found = False
        for seed in range(200):
            gate = VehicleGate("gate_01", seed=seed)
            event = gate.simulate_event()
            if event["event_type"] == VehicleGateEventType.VEHICLE_ENTERED.value:
                assert gate.is_open is True
                found = True
                break
        assert found, "No seed in range produced VEHICLE_ENTERED"

    def test_vehicle_exited_closes_gate(self) -> None:
        found = False
        for seed in range(200):
            gate = VehicleGate("gate_01", seed=seed)
            event = gate.simulate_event()
            if event["event_type"] == VehicleGateEventType.VEHICLE_EXITED.value:
                assert gate.is_open is False
                found = True
                break
        assert found, "No seed in range produced VEHICLE_EXITED"


class TestMotionDetector:
    def test_simulate_event_structure(self) -> None:
        md = MotionDetector("motion_detector_01", seed=42)
        event = md.simulate_event()
        assert event["device_id"] == "motion_detector_01"
        assert event["device_type"] == "motion_detector"
        assert event["event_type"] in [e.value for e in MotionEventType]
        assert "timestamp" in event
        assert "payload" in event
        assert "is_triggered" in event["payload"]

    def test_simulate_event_deterministic(self) -> None:
        md1 = MotionDetector("md_01", seed=300)
        md2 = MotionDetector("md_01", seed=300)
        assert md1.simulate_event()["event_type"] == md2.simulate_event()["event_type"]

    def test_motion_detected_sets_triggered(self) -> None:
        found = False
        for seed in range(200):
            md = MotionDetector("md_01", seed=seed)
            event = md.simulate_event()
            if event["event_type"] == MotionEventType.MOTION_DETECTED.value:
                assert md.is_triggered is True
                found = True
                break
        assert found, "No seed in range produced MOTION_DETECTED"

    def test_motion_cleared_unsets_triggered(self) -> None:
        found = False
        for seed in range(200):
            md = MotionDetector("md_01", seed=seed)
            event = md.simulate_event()
            if event["event_type"] == MotionEventType.MOTION_CLEARED.value:
                assert md.is_triggered is False
                found = True
                break
        assert found, "No seed in range produced MOTION_CLEARED"
