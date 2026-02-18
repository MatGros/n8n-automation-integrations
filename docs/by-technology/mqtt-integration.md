# MQTT integration — guide rapide

This guide explains common MQTT integration patterns for n8n workflows.

## Use cases
- IoT sensors → ingest telemetry into DB or analytics
- Edge devices → forward events to cloud services
- Command & control → send commands to devices via MQTT publish

## Quick start
1. Create an MQTT Broker (Mosquitto / EMQX / AWS IoT Core).
2. In n8n, create `MQTT` credentials (host, port, username/password or TLS).
3. Import `workflows/05-iot/mqtt-subscriber/workflow.json` (example).

## Pattern: Subscriber → Transformer → Store
- `MQTT Trigger` (topic=`devices/+/telemetry`)
- `JSON Parse` (parse payload)
- `Function` / `Set` (normalize fields)
- `HTTP Request` / `Database` (persist)

## Example `Process` (short)
1. `mqtt-subscriber` receives messages from `devices/+/telemetry` topic.
2. `parse-json` extracts metrics and timestamps.
3. `validate-schema` ensures required fields exist.
4. `db-insert` stores metrics in TimescaleDB.

## Best practices
- Use QoS 1 for telemetry (at-least-once) unless duplicates are harmful.
- Keep messages small and use compact JSON keys for sensors.
- Use topic hierarchy: `org/{orgId}/device/{deviceId}/telemetry`.
- Add an error path: on parsing failure, push the event to a dead-letter topic or save in `errors/` table.

## Security
- Prefer TLS and authenticated clients.
- Rotate credentials regularly and avoid embedding secrets in workflow JSON.

## Example payload
```json
{ "deviceId": "dev-1234", "ts": 1670000000, "temp": 22.5 }
```

## References & templates
- Example workflow: `workflows/05-iot/mqtt-subscriber/workflow.json`
- See `docs/workflow-style-guide.md` for documentation conventions.
