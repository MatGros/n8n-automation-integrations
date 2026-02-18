# Industry 4.0 and Manufacturing Guide

## Purpose

This guide covers integrating manufacturing systems, PLCs, SCADA networks, and supply chain management with n8n. Includes OEE metrics, ERP integration patterns, and automated manufacturing workflows.

## Overview

Industry 4.0 combines IoT sensors, automation, data analytics, and system integration to create smart factories. n8n provides the connectivity layer between manufacturing equipment, ERP systems, and business intelligence platforms.

## PLC and SCADA Integration

### Understanding PLC and SCADA

- **PLC** (Programmable Logic Controller) — Industrial computer controlling machines
- **SCADA** (Supervisory Control and Data Acquisition) — System monitoring and controlling industrial processes
- **OPC UA** (OLE for Process Control) — Standard protocol for PLC-to-IT communication

### Connecting n8n to PLCs

#### Method 1: Modbus TCP (Recommended)

Modbus is a simple, widely-supported industrial protocol. Create HTTP gateway to bridge Modbus and n8n:

```bash
# Modbus TCP gateway exposes REST API
curl -X POST http://modbus-gateway:502/api/read \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "machine_001",
    "address": 0,
    "quantity": 10
  }'
```

#### Method 2: OPC UA

For more advanced manufacturing systems using OPC UA, bridge via HTTP gateway service that translates OPC UA to REST API.

#### Method 3: MQTT from PLC

Modern PLCs often publish to MQTT brokers. Subscribe to manufacturing topics:

```javascript
// n8n MQTT Trigger configuration
{
  "topics": [
    "factory/machines/+/status",
    "factory/machines/+/metrics"
  ],
  "qos": 1
}
```

### Typical PLC Data Points

```javascript
{
  "machine_id": "CNC-001",
  "line_id": "assembly-line-1",
  "status": "running",        // running, idle, maintenance, error
  "speed": 1200,              // RPM or units/hour
  "temperature": 45.2,        // Celsius
  "pressure": 8.5,            // Bar
  "cycle_time": 45,           // Seconds
  "parts_produced": 1250,     // Today's count
  "parts_rejected": 3,        // Defects
  "uptime_percentage": 94.5,
  "last_maintenance": "2026-02-10T10:30:00Z"
}
```

## OEE Metrics Calculation

OEE (Overall Equipment Effectiveness) = Availability × Performance × Quality

Calculate these components:
- **Availability** = Run time / Total time
- **Performance** = Actual output / Ideal output
- **Quality** = Good parts / Total parts

Store OEE metrics in database and alert if below target (85% is standard).

## ERP Integration Patterns

### Pattern 1: Real-Time Production Orders to Manufacturing

```
[ERP System - New Production Order]
  ↓
[n8n Webhook receives order]
  ├→ Extract order details
  ├→ Validate materials available
  └→ Format for PLC
  ↓
[Send to PLC/Machine]
  ├→ Set machine parameters
  ├→ Queue production job
  └→ Confirm receipt
  ↓
[Notify ERP] — Update order status: Started
```

### Pattern 2: Production Completion to ERP

```
[Machine Completes Batch]
  ↓ (via Modbus/MQTT)
[n8n Receives Production Data]
  ├→ Parts produced
  ├→ Defect rate
  ├→ Time taken
  └→ Quality metrics
  ↓
[Calculate Performance]
  ├→ Yield percentage
  ├→ Cost per unit
  └→ Actual vs planned time
  ↓
[Update ERP System]
  ├→ Record production completion
  ├→ Update inventory
  ├→ Trigger QC workflow
  └→ Generate documents
```

### Pattern 3: Supply Chain Integration

```
[ERP Inventory Alert] — Materials running low
  ↓
[n8n Workflow]
  ├→ Check reorder point
  ├→ Verify supplier availability
  └→ Check budget
  ↓
[Create Purchase Order]
  ├→ Via supplier API
  ├→ Via email
  └→ Via EDI gateway
  ↓
[Update ERP] — Create purchase record
  ↓
[Track Shipment]
  ├→ Monitor delivery date
  ├→ Update receiving schedule
  └→ Notify warehouse
```

## Supply Chain Automation

### Supplier Integration

Query supplier APIs to check material availability and pricing before creating purchase orders.

### Logistics Tracking

Monitor carrier APIs (FedEx, UPS, DHL) to track shipment location, estimate delivery dates, and trigger receiving workflows upon arrival.

## Preventive Maintenance Workflows

### Pattern: Predictive Maintenance

```
[Collect Machine Metrics]
  Temperature, vibration, pressure, runtime
  ↓
[Anomaly Detection]
  ├→ Compare to historical baseline
  ├→ Identify trend changes
  └→ Calculate failure probability
  ↓
[Score Risk Level] — Low, Medium, High
  ↓
[Take Action]
  ├→ Green (Low): Continue monitoring
  ├→ Yellow (Medium): Schedule maintenance
  └→ Red (High): Alert, stop production
  ↓
[Update Maintenance Schedule]
  ├→ Notify maintenance team
  ├→ Reserve parts
  └→ Plan downtime
```

## Quality Control Integration

### Automated Defect Detection

```
[Production Line Camera/Sensors]
  Visual inspection, dimensional check
  ↓
[AI Model - Defect Detection]
  Classify: Good, Minor defect, Major defect
  ↓
[Trigger Action]
  ├→ Good: Continue to next station
  ├→ Minor: Flag for secondary inspection
  └→ Major: Reject, trigger rework
  ↓
[Log Quality Data]
  ├→ Store defect image
  ├→ Record defect type
  ├→ Update machine quality metrics
  └→ Alert if defect rate > threshold
```

## Manufacturing Dashboard Integration

Push production metrics to BI platforms (Power BI, Tableau, Grafana) for real-time dashboard updates. Use API integrations to refresh datasets hourly.

## Best Practices

### 1. Reliability

- Implement retry logic for critical PLC communications
- Use message queuing for buffering between systems
- Monitor connection health continuously
- Have fallback to manual procedures

### 2. Security

- Encrypt all PLC/SCADA communications
- Separate manufacturing network from business network
- Use VPN for remote access
- Audit all system changes
- Implement role-based access control

### 3. Performance

- Cache machine metadata locally
- Batch updates to ERP systems
- Use efficient protocols (Modbus, MQTT)
- Monitor n8n CPU/memory under high volume

### 4. Data Integrity

- Validate all manufacturing data before storage
- Implement checksums for critical messages
- Log all state changes for audit trail
- Cross-check between PLC and ERP periodically

## Related Documentation

- [IoT Integration Guide](./iot-guide.md) — Sensor data patterns
- [MQTT Integration](../by-technology/mqtt-integration.md) — Manufacturing device communication
- [Security Best Practices](../security-best-practices.md) — Industrial security
- [Deployment Guide](../deployment-guide.md) — Production manufacturing workflows
