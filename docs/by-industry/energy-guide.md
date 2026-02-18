# Energy and Smart Grid Integration Guide

## Purpose

This guide covers integrating renewable energy systems, smart grid infrastructure, power consumption monitoring, and demand response systems with n8n workflows.

## Overview

Modern energy systems generate massive amounts of real-time data from smart meters, solar panels, wind turbines, and batteries. n8n provides the integration layer for collecting, analyzing, and responding to energy data across distributed systems.

## Renewable Energy Integration

### Solar Panel Systems

Monitor distributed solar installations for power output optimization:

```javascript
// Solar inverter data structure
{
  "site_id": "solar-farm-01",
  "inverter_id": "inv-001",
  "power_output_kw": 12.5,
  "voltage": 480,
  "frequency": 60,
  "efficiency": 96.2,
  "temperature": 45.2,
  "cumulative_output_kwh": 15230.5
}
```

Collect data from solar inverters via Modbus, MQTT, or HTTP APIs. Store in time-series database and calculate daily yield, efficiency metrics, and anomaly detection.

### Wind Turbine Monitoring

```
[Wind Turbine SCADA System]
  Real-time metrics: Power, RPM, Blade angle, Wind speed
  ↓
[n8n Collector Workflow]
  ├→ Modbus TCP from turbine controller
  ├→ Parse binary data
  └→ Validate readings
  ↓
[Calculate Performance]
  ├→ Actual vs expected power curve
  ├→ Capacity factor
  └→ Energy yield
  ↓
[Alert if Maintenance Needed]
  Abnormal vibrations, temperature, pitch errors
  ↓
[Store Time-Series Data]
  ├→ InfluxDB/TimescaleDB
  └→ Dashboard updates
```

## Smart Meter Integration

### Residential Smart Meters

Typical smart meter sends data via Zigbee, LoRaWAN, or cellular networks:

```javascript
// Smart meter reading data
{
  "meter_id": "MTR-123456",
  "customer_id": "CUST-789",
  "active_energy_kwh": 1234.56,    // Total consumption
  "reactive_energy_kvarh": 123.45,
  "power_factor": 0.95,
  "voltage_l1_l2_l3": [240, 241, 239],
  "current_l1_l2_l3": [15.2, 14.8, 16.1],
  "frequency": 60,
  "timestamp": "2026-02-18T10:30:00Z"
}
```

Process meter readings to calculate hourly consumption, daily peaks, trend analysis, and update billing systems.

### Advanced Metering Infrastructure (AMI)

```
[Meter Data Management System]
  ↓
[n8n Aggregation Workflow]
  ├→ Collect 1000s of meters every hour
  ├→ Validate data quality
  ├→ Detect anomalies
  └→ Aggregate by district/area
  ↓
[Demand Forecasting]
  ├→ Machine learning model
  ├→ Historical consumption patterns
  ├→ Weather correlation
  └→ Predict next 24 hours
  ↓
[Peak Load Management]
  ├→ Identify high consumption periods
  ├→ Alert demand response capable devices
  └→ Trigger load shifting programs
```

## Consumption Monitoring

### Real-Time Energy Dashboard

Calculate consumption metrics from current vs previous meter readings:
- Hourly consumption in kWh
- Estimated monthly usage projection
- Cost estimates based on rate structure
- Daily peak power demand
- Usage trends (stable, increasing, decreasing)

### Commercial Building Energy Management

```
[Multiple Meters - Facility]
  Lighting, HVAC, Equipment, EV Charging
  ↓
[n8n Aggregation]
  ├→ Sum by circuit/floor/building
  ├→ Calculate baseline
  └→ Identify efficiency opportunities
  ↓
[Energy Benchmarking]
  ├→ Compare to similar buildings
  ├→ Calculate kWh per square foot
  └→ Identify anomalies
  ↓
[Optimization Recommendations]
  ├→ HVAC scheduling
  ├→ Lighting efficiency
  ├→ Equipment upgrades
  └→ Demand response enrollment
```

## Battery Management

### Residential Battery Storage

Monitor home battery during solar generation and grid discharge:

```
[Solar Generation + Grid State]
  ↓
[Battery Decision Logic]
  if (solar_output > consumption) {
    // Charge battery
  } else if (peak_hour && battery_soc > 30%) {
    // Discharge during peak (high rates)
  } else {
    // Buy from grid
  }
  ↓
[Optimize for Cost]
  ├→ Avoid peak pricing periods
  ├→ Maximize self-consumption
  └→ Provide grid services revenue
```

### Large-scale Battery Storage

Manage utility-scale energy storage systems for grid services:

```
[Grid Operator Request]
  Frequency regulation, peak shaving, arbitrage
  ↓
[n8n Battery Control Workflow]
  ├→ Check current SOC (State of Charge)
  ├→ Verify available capacity
  ├→ Calculate revenue opportunity
  └→ Execute charge/discharge command
  ↓
[Real-time Monitoring]
  ├→ Monitor battery health
  ├→ Track cycle count
  └→ Alert on degradation
  ↓
[Financial Settlement]
  ├→ Calculate revenues earned
  ├→ Log for utility billing
  └→ Report to ISO/RTO
```

Battery data structure:

```javascript
{
  "battery_id": "BESS-001",
  "capacity_kwh": 250,
  "current_charge_kwh": 150,
  "state_of_charge_percent": 60,
  "max_charge_rate_kw": 50,
  "max_discharge_rate_kw": 50,
  "round_trip_efficiency": 0.90,
  "temperature": 25.3,
  "health_score": 98,
  "estimated_cycles_remaining": 3500
}
```

## Demand Response Systems

### Automated Demand Response (ADR)

Utilities can automatically reduce loads during peak periods:

```
[Grid Operator Alert]
  Peak demand expected at 4-6 PM
  ↓
[n8n Demand Response Trigger]
  ├→ Send signal to smart thermostats
  ├→ Reduce HVAC to 76°F
  ├→ Delay water heater activation
  ├→ Pause EV charging
  └→ Adjust smart loads
  ↓
[Customer Notification]
  ├→ Mobile app alert
  ├→ Estimated bill savings
  └→ Estimated duration
  ↓
[Monitoring]
  ├→ Track actual load reduction
  ├→ Verify response
  └→ Calculate incentive payment
```

### Time-of-Use (ToU) Pricing Response

Implement smart charging decisions based on electricity pricing:

```
[Check Current Time and Price]
  ↓
[If Peak Hour + High Price]
  Pause/delay charging, defer loads
  ↓
[If Off-Peak Hour + Low Price]
  Charge batteries, run water heater
```

## Integration Patterns

### Pattern 1: Real-Time Energy Trading

```
[Wholesale Market Signal]
  Electricity price spike detected
  ↓
[n8n Decision Engine]
  ├→ Check battery SOC
  ├→ Check customer comfort constraints
  └→ Evaluate revenue opportunity
  ↓
[Execute Trade]
  ├→ Discharge battery for price arbitrage
  ├→ Reduce load to sell capacity
  └→ Provide ancillary services
  ↓
[Settlement]
  Record transaction for grid operator billing
```

### Pattern 2: Distributed Energy Resource Aggregation

```
[Virtual Power Plant]
  Aggregate 1000s of small resources:
  - Solar panels
  - Batteries
  - Smart thermostats
  - EV chargers
  ↓
[n8n Orchestration]
  ├→ Collect status from all resources
  ├→ Calculate available capacity
  ├→ Respond to grid operator requests
  └→ Optimize for highest revenue
  ↓
[Transparent Marketplace]
  ├→ Bid available capacity to ISO
  ├→ Execute if cleared
  └→ Settle payments
```

### Pattern 3: Microgrid Control

```
[Islanded Microgrid]
  Can operate connected to grid or independently
  ↓
[n8n Microgrid Controller]
  ├→ Monitor island condition
  ├→ Balance supply and demand
  ├→ Manage battery discharge/charge
  ├→ Shed non-critical loads if needed
  └→ Coordinate renewable generation
  ↓
[Grid Reconnection]
  ├→ Synchronize frequency
  ├→ Match voltage
  └→ Smooth reconnection
```

## Data Analytics and Reporting

### Energy Efficiency Analysis

Find inefficiencies in consumption patterns and recommend improvements:
- Analyze baseline load patterns
- Identify peak consumption periods
- Compare to industry benchmarks
- Suggest equipment upgrades or scheduling changes

### Sustainability Reporting

Calculate carbon footprint reduction from renewable energy:
- kg CO2 per kWh varies by grid composition
- Solar: 0.04 kg CO2/kWh
- Wind: 0.01 kg CO2/kWh
- Grid average: 0.42 kg CO2/kWh

## Best Practices

### 1. Data Quality

- Validate meter readings for physical impossibilities
- Detect and flag sensor failures
- Implement checksums for critical data
- Monitor data freshness and detect stale readings

### 2. Cybersecurity

- Encrypt all communications (TLS)
- Authenticate all devices
- Implement rate limiting on API access
- Monitor for anomalous consumption patterns

### 3. Reliability

- Implement message queuing for buffering
- Use exponential backoff for retries
- Maintain local caches for offline operation
- Have manual fallback procedures

### 4. Interoperability

- Support multiple smart meter standards
- Use standardized data formats (IEC 61850)
- Document API contracts
- Version APIs properly

## Related Documentation

- [IoT Integration Guide](./iot-guide.md) — Sensor data collection
- [MQTT Integration](../by-technology/mqtt-integration.md) — Device communication
- [Security Best Practices](../security-best-practices.md) — Energy system security
- [Deployment Guide](../deployment-guide.md) — Production energy workflows
