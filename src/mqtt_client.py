"""HiveMQ MQTT client wrapper using paho-mqtt."""

import json
import os
import ssl
from typing import Any

import paho.mqtt.client as mqtt


class MQTTClient:
    """Thin wrapper around paho-mqtt that reads connection settings from env vars."""

    def __init__(self) -> None:
        self._host: str = os.environ["HIVEMQ_HOST"]
        self._port: int = int(os.environ.get("HIVEMQ_PORT", "8883"))
        self._username: str | None = os.environ.get("HIVEMQ_USERNAME")
        self._password: str | None = os.environ.get("HIVEMQ_PASSWORD")

        self._client = mqtt.Client(protocol=mqtt.MQTTv5)
        if self._username:
            self._client.username_pw_set(self._username, self._password)
        self._client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)

    def connect(self) -> None:
        """Connect to the HiveMQ broker and start the network loop."""
        self._client.connect(self._host, self._port)
        self._client.loop_start()

    def disconnect(self) -> None:
        """Stop the network loop and disconnect from the broker."""
        self._client.loop_stop()
        self._client.disconnect()

    def publish(self, topic: str, payload: dict[str, Any], qos: int = 1) -> None:
        """Publish a JSON-encoded payload to the given topic at the given QoS."""
        message = json.dumps(payload)
        self._client.publish(topic, message, qos=qos)
