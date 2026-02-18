# MQTT Integration Guide

## Purpose

This guide provides comprehensive MQTT setup, broker configuration, publish/subscribe patterns, QoS levels, and n8n MQTT node usage with practical examples.

## Overview

MQTT (Message Queuing Telemetry Transport) is a lightweight, low-bandwidth protocol perfect for IoT and real-time data streaming. It uses a publish-subscribe model where clients connect to a broker and exchange messages on topics.

## MQTT Concepts

### Publish-Subscribe Model

- **Publisher** — Sends messages to a topic
- **Subscriber** — Listens to topics
- **Broker** — Central hub that routes messages (Mosquitto, EMQX, AWS IoT Core)
- **Topic** — Hierarchical string like "devices/dev-123/telemetry"

### Topic Wildcards

- `+` — Single level (e.g., `sensors/+/data` matches `sensors/temp/data`)
- `#` — Multiple levels (e.g., `sensors/#` matches all subtopics)

## n8n MQTT Configuration

### Creating MQTT Credentials

Settings → Credentials → New → MQTT

```javascript
{
  "protocol": "mqtt or mqtts",
  "hostname": "broker.example.com",
  "port": 1883,                  // 8883 for MQTTS
  "username": "your-username",
  "password": "your-password",
  "clientId": "n8n-client-123"
}
```

### MQTT Trigger Node

Subscribe to MQTT topics and trigger workflows:

```javascript
{
  "topics": [
    "devices/+/telemetry",
    "alerts/system/#"
  ],
  "qos": 1,
  "credentials": "mqtt-production"
}
```

### MQTT Publish Node

Publish messages to MQTT topics:

```javascript
{
  "topic": "notifications/alert",
  "message": JSON.stringify({
    alert_type: "temperature_high",
    value: 45.2
  }),
  "qos": 1,
  "retain": false
}
```

## QoS (Quality of Service) Levels

| QoS | Delivery | Use Case | Overhead |
|-----|----------|----------|----------|
| 0 | At Most Once | Non-critical sensors | Low |
| 1 | At Least Once | Standard IoT | Medium |
| 2 | Exactly Once | Critical data | High |

## Workflow Patterns

### Pattern 1: Sensor Ingestion
```
[MQTT Trigger] → [Parse JSON] → [Validate] → [Store to DB]
```

### Pattern 2: Topic-Based Routing
```
[MQTT Trigger on alerts/#, data/#]
  ↓
[Route by topic prefix]
  → alert handler / data processor / config updater
```

### Pattern 3: Request-Response
```
[Request Topic] → [n8n processes] → [Publish response]
```

## Broker Setup

### Mosquitto (Docker)

```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto:latest
```

### Authentication

```bash
mosquitto_passwd /etc/mosquitto/passwd username
# Update config with: password_file /etc/mosquitto/passwd
```

### TLS/SSL

```bash
# Generate certificates
openssl req -new -x509 -days 365 -nodes \
  -out broker.crt -keyout broker.key

# Configure Mosquitto with TLS enabled
```

## Best Practices

- Use QoS 1 for reliability unless duplicates acceptable (QoS 0 for non-critical)
- Keep messages small with compact JSON keys
- Use topic hierarchy: `org/{id}/device/{id}/telemetry`
- Implement error handling with dead-letter queues
- Prefer TLS for all connections
- Rotate credentials regularly
- Never embed secrets in workflow JSON

## Performance Tips

- Compress large payloads before publishing
- Batch multiple readings into single message
- Monitor broker message queue depth
- Implement message sampling for high-frequency sensors
- Use broker clustering for scale

## Example Workflow

```
1. mqtt-subscriber receives from devices/+/telemetry
2. parse-json extracts metrics
3. validate-schema checks required fields
4. db-insert stores in TimescaleDB
5. Error path sends failures to error queue
```

Example payload:
```json
{ "deviceId": "dev-1234", "ts": 1670000000, "temp": 22.5 }
```

## References

- [IoT Integration Guide](../by-industry/iot-guide.md) — IoT patterns
- [Security Best Practices](../security-best-practices.md) — MQTT security
- [Deployment Guide](../deployment-guide.md) — Production setup
- [Workflow Style Guide](../workflow-style-guide.md) — Documentation conventions
