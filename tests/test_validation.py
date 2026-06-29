import pytest

from app.validation import ValidationError, validate_metric


def test_valid_metric_passes_validation():
    payload = {
        "device_id": "ap-001",
        "timestamp": "2026-06-29T22:10:00Z",
        "latency_ms": 35,
        "packet_loss": 0.1,
        "rssi": -55,
    }

    metric = validate_metric(payload)

    assert metric["device_id"] == "ap-001"
    assert metric["latency_ms"] == 35.0
    assert metric["packet_loss"] == 0.1
    assert metric["rssi"] == -55.0


def test_missing_field_raises_validation_error():
    payload = {
        "timestamp": "2026-06-29T22:10:00Z",
        "latency_ms": 35,
        "packet_loss": 0.1,
        "rssi": -55,
    }

    with pytest.raises(ValidationError, match="Missing field: device_id"):
        validate_metric(payload)


def test_invalid_rssi_is_rejected():
    payload = {
        "device_id": "ap-007",
        "timestamp": "2026-06-29T22:30:00Z",
        "latency_ms": 45,
        "packet_loss": 0.2,
        "rssi": -265,
    }

    with pytest.raises(ValidationError, match="rssi must be between -120 and 0"):
        validate_metric(payload)


def test_negative_latency_is_rejected():
    payload = {
        "device_id": "ap-008",
        "timestamp": "2026-06-29T22:30:00Z",
        "latency_ms": -10,
        "packet_loss": 0.2,
        "rssi": -65,
    }

    with pytest.raises(ValidationError, match="latency_ms cannot be negative"):
        validate_metric(payload)