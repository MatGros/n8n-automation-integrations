# Healthcare Integration Guide

## Purpose

This guide covers healthcare system integrations with n8n, including HL7/FHIR standards, medical device connectivity, patient data workflows, and HIPAA compliance considerations.

## Overview

Healthcare workflows require careful handling of Protected Health Information (PHI) while maintaining interoperability between different medical systems. n8n can safely integrate EHRs, medical devices, labs, and imaging systems while respecting HIPAA requirements.

## HL7 Protocol Integration

### Understanding HL7

HL7 (Health Level 7) is the standard protocol for healthcare data exchange:

- **HL7 v2** — Legacy format, text-based, still widely used in hospitals
- **HL7 FHIR** — Modern RESTful standard (recommended for new systems)
- **X.12** — Claims and billing format
- **eCQMs** — Electronic Clinical Quality Measures

### HL7 v2 Format

HL7 v2 uses pipe-delimited text format. Each message contains segments (MSH, PID, OBX, etc.) with specific fields.

### HL7 FHIR Integration (Recommended)

FHIR uses RESTful JSON/XML format and is easier to work with than HL7 v2. Most modern EHRs (Epic, Cerner, Athenahealth) expose FHIR APIs.

Example: Fetch patient appointments from FHIR server

```javascript
// n8n HTTP Request: FHIR Patient lookup
{
  "url": "https://fhir-server.example.com/Appointment",
  "method": "GET",
  "params": {
    "patient": "patient-id-123",
    "status": "proposed,pending,booked",
    "_format": "json"
  },
  "headers": {
    "Authorization": "Bearer ${{ $credentials.fhir_api_token }}"
  }
}
```

## Medical Device Integration

### Device Connectivity Patterns

```
[Medical Device - Monitor/Sensor]
  ↓ (HL7, MQTT, or serial)
[n8n Gateway/Middleware]
  ├→ Parse device-specific format
  ├→ Validate measurements
  └→ Handle transmission errors
  ↓
[Transform to FHIR/EHR format]
  ├→ Observation resource
  ├→ Patient linkage
  └→ Timestamp synchronization
  ↓
[Store in EHR/Data Lake]
```

Example: Vital signs from bedside monitor transformed to FHIR Observation resource.

## Patient Data Workflows

### Workflow 1: Patient Registration

```
[New Patient Arrives at Registration]
  ↓
[Capture Demographics via Form]
  ↓
[n8n Workflow]
  ├→ Validate email/phone format
  ├→ Check for duplicates in EHR
  ├→ Generate MRN if needed
  └→ Create FHIR Patient resource
  ↓
[Store in EHR System]
  ├→ Create patient record
  ├→ Set up insurance links
  └→ Configure access controls
  ↓
[Notify Systems]
  ├→ Update lab system
  ├→ Update pharmacy
  └→ Sync to billing
```

### Workflow 2: Test Results Processing

```
[Lab System Sends Results]
  via HL7 ORM/ORU message
  ↓
[n8n Receives Results]
  ├→ Parse HL7 message
  ├→ Validate values in range
  └→ Check critical values
  ↓
[Create FHIR Observation]
  ├→ Link to patient
  ├→ Reference test order
  └→ Add interpretation
  ↓
[Store Results]
  ├→ EHR database
  ├→ Data warehouse
  └→ Patient portal
  ↓
[Alert If Critical]
  ├→ Page physician
  ├→ Record alert in chart
  └→ Notify nursing station
```

### Workflow 3: Prescription Management

```
[Provider Orders Medication]
  in EHR system
  ↓
[n8n Receives Order]
  Parse MedicationRequest FHIR resource
  ↓
[Send to Pharmacy]
  ├→ Check patient allergies
  ├→ Check drug interactions
  ├→ Verify insurance coverage
  └→ Send via HL7 RXO
  ↓
[Track Dispensing]
  ├→ Receive fill confirmation
  ├→ Update EHR status
  └→ Alert patient
  ↓
[Billing]
  ├→ Capture NDC code
  ├→ Calculate co-pay
  └→ Send claim
```

## HIPAA Compliance Considerations

### 1. Data Encryption

All PHI must be encrypted:
- In transit: Use HTTPS/TLS for all communications
- At rest: Encrypt database columns containing PHI

### 2. Access Logging

Every access to PHI must be logged with:
- User ID who accessed the data
- Which patient record was accessed
- What action was performed (view, modify, delete)
- Exact timestamp

### 3. Minimal Necessary Access

Only transmit PHI that is needed for the specific operation. Do not include full medical histories, insurance info, or complete patient records when only test results are needed.

### 4. Data Retention

Implement data retention policies:
- Keep detailed records for 7 years (HIPAA requirement)
- Archive older records to secure cold storage
- Securely delete data beyond retention period using cryptographic erasure

### 5. Business Associate Agreement (BAA)

Ensure all systems and vendors have:
- Valid Business Associate Agreements
- HIPAA compliance certification
- Regular security audits

## Clinical Decision Support

Implement drug interaction checking before dispensing medications:

```
[Medication Order Received]
  ↓
[Check Current Medications]
  ↓
[Query Interaction Database]
  for each medication pair
  ↓
[Assess Severity]
  Low, Moderate, Severe
  ↓
[Alert Pharmacist if Severe]
  Block dispensing, require override
```

## Data Anonymization

For research and analytics, remove PHI using HIPAA Safe Harbor method:

- Remove exact dates (use age ranges instead)
- Remove names and contact information
- Keep only ICD-10 diagnosis codes
- Keep only procedure codes
- Retain lab values without identifiers

Example: Age 45-50 instead of "born 1980-01-15"

## Best Practices

### 1. Error Handling

Always use generic error messages that don't leak PHI:
- Correct: "Failed to process prescription - contact support"
- Wrong: "Failed to fill prescription for John Doe (MRN: 123456)"

### 2. Validation

Validate all medical data:
- Lab values within physiologically possible ranges
- ICD-10 codes match standard format
- Dates are within reasonable bounds
- Required clinical fields are present

### 3. Testing

Use completely de-identified test data:
- Test patient: "TEST00001"
- Synthetic values that are realistic but clearly fake
- Never use production data for testing

### 4. Audit Trail

Maintain comprehensive audit logs:
- All data access attempts
- All modifications to patient records
- All authentication events
- All system errors

## Related Documentation

- [Security Best Practices](../security-best-practices.md) — PHI security protocols
- [FHIR Resources](https://hl7.org/fhir/resourcelist.html) — FHIR specification
- [Deployment Guide](../deployment-guide.md) — Healthcare production deployment
- [Contributing Guide](../contributing.md) — Healthcare workflow standards
