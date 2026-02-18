# IoT Guide — patterns & best practices

Scope: patterns for ingesting sensor data, edge processing, and reliability concerns.

## Common patterns
- Telemetry ingestion (MQTT → validates → time-series DB)
- Event-driven rules (edge filters → forward important events)
- Device provisioning (HTTP onboarding flow)

## Quick start (example)
1. Deploy an MQTT broker or use cloud provider.
2. Create `MQTT` credentials in n8n.
3. Import `workflows/05-iot/mqtt-subscriber/workflow.json` and test with `mosquitto_pub`.

## Design recommendations
- Partition topics by tenant/org to simplify multi-tenancy.
- Use schema validation for payloads (`jsonschema` node or custom function).
- Implement DLQ (dead-letter) for malformed payloads.
- Add rate-limiting / sampling for high-frequency sensors.

## Edge vs Cloud
- Keep transient filtering & aggregation at the edge; persist raw telemetry in the cloud.
- Use batching for DB writes to reduce load.

## Monitoring & reliability
- Add heartbeat messages from devices and alerts on missed heartbeats.
- Monitor message backlog and queue lengths.

## Example `mosquitto_pub` command
```bash
mosquitto_pub -h broker.local -t "devices/dev-123/telemetry" -m '{"ts":1670000000,"temp":22.5}'
```

## References
- `docs/by-technology/mqtt-integration.md`
- `docs/workflow-style-guide.md`
