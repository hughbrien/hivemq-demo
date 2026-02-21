#!/usr/bin/env python3
"""Entry point for the airport security agent."""

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

from src.mqtt_client import MQTTClient
from src.agent import create_default_agent

try:
    client = MQTTClient()
except KeyError as e:
    sys.exit(f"Missing required environment variable: {e}")

agent = create_default_agent(client)
agent.run(interval=5.0)
