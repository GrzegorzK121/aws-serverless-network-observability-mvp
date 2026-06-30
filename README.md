# AWS Serverless Network Observability MVP

Small AWS serverless Python project for collecting network device telemetry, validating metrics and detecting simple connectivity anomalies.

The project is inspired by network observability systems used for device telemetry, metrics collection and troubleshooting.

## Architecture

Postman / HTTP Client  
→ API Gateway  
→ AWS Lambda  
→ validation + anomaly detection  
→ DynamoDB `NetworkMetrics`

## AWS services used

- AWS Lambda
- API Gateway
- DynamoDB
- IAM execution role
- CloudWatch Logs

## Metrics

The Lambda function processes JSON telemetry events with:

- `device_id`
- `timestamp`
- `latency_ms`
- `packet_loss`
- `rssi`

## Anomaly detection rules

- `latency_ms > 150` → `HIGH_LATENCY`
- `packet_loss > 2.0` → `PACKET_LOSS`
- `rssi < -85` → `LOW_RSSI`

Invalid telemetry values are rejected before saving to DynamoDB.

## Example payload

```json
{
  "device_id": "router-001",
  "timestamp": "2026-06-29T22:25:00Z",
  "latency_ms": 190,
  "packet_loss": 3.1,
  "rssi": -90
}
```

## Screenshots

### Successful metric ingestion
![Normal metric](docs/screenshots/postman-normal-metric.png)

### Anomaly detection
![Anomaly metric](docs/screenshots/postman-anomaly-metric.png)

### Validation error
![Validation error](docs/screenshots/postman-validation-error.png)

### DynamoDB stored observations
![DynamoDB items](docs/screenshots/dynamodb-networkmetrics-items.png)

## Randomized telemetry load test

As another small building block of this project, I added a randomized telemetry load-style test.

The test sends multiple JSON events to the API Gateway endpoint using PowerShell. Each event represents a network device telemetry sample with values such as latency, packet loss and RSSI. The script mixes normal metrics, anomaly scenarios and invalid payloads to check how the system behaves with different kinds of input.

The goal was to make the project closer to a real network observability ingestion pipeline, not just a single manually tested Lambda function.

The test verifies the full flow:

* API Gateway receives telemetry events
* AWS Lambda validates the payload
* anomaly detection classifies problematic metrics
* valid observations are stored in DynamoDB
* invalid telemetry is rejected before persistence
* CloudWatch custom metrics show accepted, rejected and anomalous events

Tested scenarios include:

* normal telemetry events
* high latency events
* packet loss events
* low RSSI events
* combined anomaly events
* invalid RSSI values
* negative latency values
* missing required fields

### PowerShell randomized load test

![PowerShell load test 1](docs/screenshots/powershell-load-test1.png)

![PowerShell load test 5](docs/screenshots/powershell-load-test5.png)

### CloudWatch custom metrics after the test

![CloudWatch custom metrics load test](docs/screenshots/cloudwatch-custom-metrics-load-test.png)

### DynamoDB stored telemetry observations

![DynamoDB load test items](docs/screenshots/dynamodb-load-test-items.png)

### Validation error example from Postman

![Postman validation error](docs/screenshots/postman-validation-error.png)
