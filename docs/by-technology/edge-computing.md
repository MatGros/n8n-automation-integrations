# Edge Computing Guide

## Purpose

This guide covers edge computing deployment patterns with n8n, including local AI/ML inference, edge data processing, and synchronization between edge devices and cloud systems.

## Overview

Edge computing moves processing closer to data sources for low-latency, offline-capable operations. n8n can run on edge devices to process data locally while syncing with cloud systems for long-term storage and analysis.

## Edge Computing Architecture

### Edge vs Cloud

```
Traditional Cloud:
Data → Internet → Cloud Processing → Storage → Analytics

Edge Computing:
Data → Edge Device (n8n) → Local Processing + Local Storage
         ↓ (sync periodically)
      Cloud System → Long-term Storage, ML, Reporting
```

### Benefits

1. **Low Latency** — Process data locally, instant response
2. **Offline Capability** — Continue operating without internet
3. **Reduced Bandwidth** — Pre-process, send only summaries
4. **Privacy** — Sensitive data never leaves location
5. **Cost** — Reduce cloud bandwidth and processing costs

## Edge Hardware

### Suitable Platforms

| Platform | CPU | RAM | Use Case |
|----------|-----|-----|----------|
| **Raspberry Pi** | 1.5-2.4 GHz | 2-8 GB | Home automation, small sensors |
| **NVIDIA Jetson** | 8-core | 4-16 GB | AI inference, video processing |
| **Intel NUC** | Multi-core | 8-64 GB | Complex processing, many sensors |
| **AWS Greengrass** | Varies | Varies | AWS ecosystem, cloud-connected |
| **Docker Container** | Varies | Varies | Generic, any OS |

## Running n8n on Edge Devices

### Installation on Raspberry Pi

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install n8n globally
sudo npm install -g n8n

# Start n8n
n8n start
# Accessible at http://localhost:5678
```

### Docker on Edge

```bash
# Pull n8n Docker image
docker pull n8nio/n8n:latest

# Run with persistent storage
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e NODE_ENV=production \
  n8nio/n8n:latest
```

### Kubernetes on Edge (K3s)

For multiple edge devices or complex deployments:

```bash
# Install K3s (lightweight Kubernetes)
curl -sfL https://get.k3s.io | sh -

# Deploy n8n on K3s
kubectl create deployment n8n --image=n8nio/n8n:latest
kubectl expose deployment n8n --port=5678 --target-port=5678
```

## Edge Data Processing Patterns

### Pattern 1: Local Aggregation

```
[IoT Sensors - High Frequency]
  10 readings per second
  ↓
[Edge n8n]
  Buffer 600 readings (60 seconds)
  ↓
[Aggregate]
  Calculate average, min, max, std dev
  ↓
[Send to Cloud]
  1 summary every 60 seconds
  (vs 600 raw readings)
```

Benefits:
- 600x bandwidth reduction
- Faster processing
- Local alerts within 1 second

Implementation:

```javascript
// Aggregate sensor data locally
const buffer = [];
const BUFFER_SIZE = 600;
const INTERVAL_MS = 100;

// n8n triggered every 100ms from sensor
buffer.push({
  timestamp: Date.now(),
  temperature: items[0].json.temperature
});

// When buffer full, process
if (buffer.length >= BUFFER_SIZE) {
  const temps = buffer.map(b => b.temperature);
  const summary = {
    count: temps.length,
    avg: temps.reduce((a,b) => a+b) / temps.length,
    min: Math.min(...temps),
    max: Math.max(...temps),
    timestamp: new Date().toISOString()
  };

  // Send summary to cloud
  await sendToCloud(summary);
  buffer.length = 0;  // Reset buffer
}
```

### Pattern 2: Conditional Forwarding

```
[Stream data through edge]
  ↓
[Check against threshold]
  if temperature > 40°C: critical
  if humidity < 20%: critical
  ↓
[Local action]
  Trigger alarm immediately
  ↓
[Conditional cloud sync]
  Always send critical events
  Send non-critical every 1 hour
```

### Pattern 3: Local Anomaly Detection

```
[Sensor data arrives]
  ↓
[Compare to baseline]
  Expected: 22°C, actual: 45°C
  ↓
[Calculate deviation]
  5 standard deviations above normal
  ↓
[Immediate action]
  Alert locally
  Stop process
  ↓
[Async cloud sync]
  Send data for investigation
```

## Local AI/ML Inference

### Lightweight ML Models

Models suitable for edge:

- **TensorFlow Lite** — Mobile/embedded inference
- **ONNX Runtime** — Multiple framework support
- **PyTorch Mobile** — Smaller model files
- **MediaPipe** — Pre-built ML solutions

### Deploying Models on Edge

```javascript
// n8n Code node - Run ML inference locally
const tf = require('@tensorflow/tfjs');
const tflite = require('@tensorflow/tfjs-tflite');

// Load model from local storage
const model = await tflite.loadTFLiteModel('file:///models/sensor-classifier.tflite');

// Inference
const input = tf.tensor2d([[22.5, 45.2, 1013.25]]);  // temp, humidity, pressure
const output = model.predict(input);

// Get prediction
const prediction = output.dataSync()[0];
return {
  prediction: prediction > 0.5 ? 'normal' : 'anomaly',
  confidence: Math.round(prediction * 100)
};
```

### Common Edge ML Use Cases

1. **Predictive Maintenance** — Vibration analysis for equipment failure prediction
2. **Quality Control** — Vision inspection on manufacturing line
3. **Anomaly Detection** — Identify unusual patterns in sensor data
4. **Sound Classification** — Detect equipment problems from sound signatures
5. **Image Recognition** — Local object detection without cloud

## Offline-First Architecture

### Local Data Persistence

```
[Data arrives at edge]
  ↓
[Store locally in SQLite]
  ├→ Create local database
  ├→ Store all events
  └→ Index for fast queries
  ↓
[Process locally]
  Aggregation, ML inference, alerts
  ↓
[Sync when online]
  Check internet connection
  Upload queued data
  ↓
[Resolve conflicts]
  Cloud has newer data
  Merge or choose winner
```

### Sync Strategy

```javascript
// Queue data for cloud sync
async function syncWithCloud() {
  // Check connectivity
  if (!await isConnected()) {
    console.log('Offline, will retry later');
    return;
  }

  // Get unsynced records
  const unsynced = await db.query(`
    SELECT * FROM sensor_data WHERE synced = false
  `);

  // Batch upload
  const batches = chunk(unsynced, 1000);
  for (const batch of batches) {
    try {
      await fetch('https://cloud.example.com/api/data', {
        method: 'POST',
        body: JSON.stringify(batch)
      });

      // Mark as synced
      await db.query(`
        UPDATE sensor_data SET synced = true WHERE id IN (?)
      `, [batch.map(b => b.id)]);
    } catch (error) {
      console.error('Sync failed:', error);
      // Retry next time
      break;
    }
  }
}

// Schedule sync every 5 minutes
setInterval(syncWithCloud, 5 * 60 * 1000);
```

## Network Synchronization

### Edge-to-Cloud Sync

```
[Edge Device]
  Local n8n instance
  SQLite database
  ↓
[Scheduled Sync Workflow]
  Every 30 minutes or when online
  ↓
[Upload batch data]
  1000 records per request
  ↓
[Verify on cloud]
  Checksum validation
  ↓
[Delete from local cache]
  Free local storage
```

### Cloud-to-Edge Configuration

```
[Cloud System]
  Configuration changes
  ↓
[Push to edge devices]
  Updated sensor thresholds
  New ML models
  Workflow changes
  ↓
[Edge updates locally]
  Apply configuration
  Restart if needed
  ↓
[Verify application]
  Health check
```

## Local Gateway Patterns

### Multi-Device Gateway

```
[Multiple IoT Devices]
  Thermometer, humidity sensor, pressure sensor
  ↓ (via Zigbee/LoRa/BLE)
[Edge Gateway - n8n]
  Collect from all devices
  Local aggregation
  ↓
[Cloud Upload]
  One connection to internet
  Centralized aggregation
```

### Industrial Edge (PLC Integration)

```
[Manufacturing Equipment]
  CNC machine, sensors, PLC
  ↓ (Modbus, OPC UA)
[Edge Controller - n8n]
  Real-time monitoring
  Emergency stop capability
  Local alerting
  ↓
[Cloud ERP]
  Production metrics
  Maintenance scheduling
  Analytics
```

## Resource Constraints

### CPU Optimization

```javascript
// Optimize for low CPU edge devices
// Avoid: Complex regex, recursive functions, heavy processing

// DO: Use simple loops, batch processing

// ❌ Inefficient
const data = hugeArray.filter(x => x.match(/complex_regex/));

// ✅ Efficient
const threshold = 22;
const data = hugeArray.filter(x => x > threshold);
```

### Memory Management

```javascript
// Stream processing instead of loading all data
// ❌ Loads entire file into memory
const allData = await fs.readFile('data.json', 'utf8');
const records = JSON.parse(allData);

// ✅ Stream processing
const lines = fs.createReadStream('data.jsonl')
  .split('\n')
  .map(line => JSON.parse(line))
  .each(record => processRecord(record));
```

### Storage Optimization

```bash
# SQLite with compression
sqlite> PRAGMA page_size = 4096;
sqlite> PRAGMA journal_mode = WAL;
sqlite> PRAGMA synchronous = NORMAL;

# Reduce database size
sqlite> VACUUM;
sqlite> ANALYZE;
```

## Security on Edge

### Secure Boot

```bash
# Raspberry Pi secure boot
# Enable UEFI secure boot in UEFI firmware settings
# Sign n8n binary with secure key
```

### Data Encryption

```javascript
// Encrypt sensitive data before sync
const crypto = require('crypto');

function encryptForTransit(data, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

  let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
  encrypted += cipher.final('hex');

  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: cipher.getAuthTag().toString('hex')
  };
}
```

### Network Security

- Use VPN for edge-to-cloud communication
- Implement mTLS (mutual TLS)
- Authenticate all API calls
- Firewall rules to restrict network access

## Workflow Example: Smart Thermostat

```
[Temperature sensor every 30 seconds]
  ↓
[Local n8n on RPi]
  ├→ Buffer 120 readings (1 hour)
  ├→ Detect temperature trend
  └→ Control heater locally
  ↓
[If temperature out of range]
  Alert homeowner (local)
  ↓
[Hourly cloud sync]
  Send aggregate data
  Receive updated setpoints
  ↓
[Cloud Dashboard]
  History, analytics, remote control
```

## Best Practices

### 1. Redundancy

- Multiple edge devices for critical operations
- Heartbeat monitoring between devices
- Failover to cloud if edge unavailable

### 2. Updates

- Test updates on staging edge device first
- Gradual rollout to other edge devices
- Keep rollback capability for 2 weeks

### 3. Monitoring

- Log all events locally
- Periodically upload logs for analysis
- Alert on edge device health issues
- Track uptime and performance metrics

### 4. Compliance

- Audit local data access
- Encrypt PII locally
- Maintain compliance logs
- Data retention policies

## Related Documentation

- [IoT Integration Guide](../by-industry/iot-guide.md) — Edge IoT patterns
- [Security Best Practices](../security-best-practices.md) — Edge security
- [Kubernetes Automation](./kubernetes-automation.md) — K3s on edge
- [Deployment Guide](../deployment-guide.md) — Edge deployment
