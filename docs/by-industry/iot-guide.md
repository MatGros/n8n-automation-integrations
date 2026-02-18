# IoT Integration Guide

## Purpose

This guide covers integrating IoT devices and sensors with n8n workflows, including MQTT protocols, CoAP, LoRaWAN, sensor data collection patterns, and best practices for edge processing and cloud synchronization.

## Overview

IoT integration requires handling high-volume, low-latency sensor data while ensuring reliable communication between edge devices and cloud systems. n8n provides flexible options for ingesting, processing, and responding to IoT data streams.

## MQTT Integration

### What is MQTT?

MQTT (Message Queuing Telemetry Transport) is a lightweight publish-subscribe protocol ideal for IoT. It uses minimal bandwidth, supports QoS levels for reliability, and is widely supported by IoT platforms globally.

### Setting Up MQTT in n8n

1. Configure MQTT Broker (Mosquitto, Azure IoT Hub, AWS IoT Core)
2. Create MQTT Credentials in n8n Settings
3. Set up MQTT Trigger with topic subscriptions
4. Parse incoming MQTT messages using Code nodes

Example Mosquitto setup (Docker):

```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto

# Test connection
mosquitto_pub -h localhost -t "devices/dev-123/telemetry" -m '{"ts":1670000000,"temp":22.5}'
mosquitto_sub -h localhost -t "devices/+"
```

### MQTT QoS Levels

| QoS | Level | Use Case | Guarantee |
|-----|-------|----------|-----------|
| 0 | At Most Once | Non-critical sensors | No guarantee |
| 1 | At Least Once | Standard sensors | Delivered at least once |
| 2 | Exactly Once | Critical data | Exactly one delivery |

## CoAP Integration

CoAP (Constrained Application Protocol) is ideal for very resource-constrained devices. Use HTTP Request nodes to interact with CoAP gateways that translate between CoAP and HTTP protocols.

## LoRaWAN Integration

LoRaWAN provides long-range, low-power connectivity for distributed sensor networks. Configure webhook endpoints in LoRaWAN Network Servers (The Things Network, ChirpStack) to send uplink messages directly to n8n workflows.

## Common Sensor Data Patterns

### Pattern 1: Telemetry Ingestion
Workflow: MQTT Trigger → Parse Payload → Validate Data → Store to Time-Series DB

### Pattern 2: Event-Driven Rules
Edge devices filter data locally and forward important events to cloud for processing

### Pattern 3: Device Provisioning
HTTP onboarding flow for registering new IoT devices with authentication

## Design Recommendations

- Partition topics by tenant/org to simplify multi-tenancy
- Use schema validation for payloads (jsonschema node or custom validation)
- Implement DLQ (dead-letter) queue for malformed payloads
- Add rate-limiting and sampling for high-frequency sensors
- Keep transient filtering and aggregation at edge; persist raw telemetry in cloud
- Use batching for database writes to reduce load

## Monitoring & Reliability

- Add heartbeat messages from devices and alerts on missed heartbeats
- Monitor message backlog and queue lengths
- Implement retry logic with exponential backoff
- Log all failed message processing
- Set up alerts for sensor anomalies

## Best Practices

### 1. Data Validation
- Check value ranges appropriate to sensor type
- Verify required fields are present
- Validate timestamps are recent (within last hour)
- Check for duplicate messages

### 2. Error Handling
Comprehensive error handling with proper logging and retry mechanisms

### 3. Performance Optimization
- Use batch processing for high-volume data
- Implement data sampling for non-critical metrics
- Cache device metadata locally
- Use message compression for large payloads

### 4. Security
- Use TLS/SSL for all connections (mqtts://)
- Rotate API keys and credentials regularly
- Validate device certificates
- Implement rate limiting per device
- Encrypt sensitive sensor data at rest

## Common IoT Use Cases

1. **Temperature Monitoring** — HVAC, cold storage, greenhouses
2. **Predictive Maintenance** — Vibration, temperature, pressure sensors
3. **Smart Metering** — Energy, water consumption tracking
4. **Occupancy Detection** — Motion sensors, people counting
5. **Environmental Monitoring** — Air quality, humidity, noise levels
6. **Asset Tracking** — Location, movement patterns

## References

- [MQTT Integration Guide](../by-technology/mqtt-integration.md) — Detailed MQTT setup
- [Edge Computing Guide](../by-technology/edge-computing.md) — Edge processing patterns
- [Security Best Practices](../security-best-practices.md) — IoT security
- [Workflow Style Guide](../workflow-style-guide.md) — Node naming conventions
