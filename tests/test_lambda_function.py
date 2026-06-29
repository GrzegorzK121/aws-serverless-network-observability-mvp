import json

from app.lambda_function import lambda_handler


def test_lambda_handler_accepts_valid_metric(monkeypatch):
    saved = {}

    def fake_save_metric_to_dynamodb(metric, anomalies):
        saved["metric"] = metric
        saved["anomalies"] = anomalies

    monkeypatch.setattr(
        "app.lambda_function.save_metric_to_dynamodb",
        fake_save_metric_to_dynamodb,
    )

    event = {
        "body": json.dumps({
            "device_id": "ap-001",
            "timestamp": "2026-06-29T22:10:00Z",
            "latency_ms": 35,
            "packet_loss": 0.1,
            "rssi": -55,
        })
    }

    response = lambda_handler(event, context=None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["message"] == "metric accepted"
    assert body["is_anomaly"] is False
    assert saved["metric"]["device_id"] == "ap-001"


def test_lambda_handler_rejects_invalid_rssi():
    event = {
        "body": json.dumps({
            "device_id": "ap-007",
            "timestamp": "2026-06-29T22:30:00Z",
            "latency_ms": 45,
            "packet_loss": 0.2,
            "rssi": -265,
        })
    }

    response = lambda_handler(event, context=None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["message"] == "rssi must be between -120 and 0"