from app.anomaly_detector import detect_anomalies


def test_normal_metric_has_no_anomalies():
    metric = {
        "device_id": "ap-001",
        "timestamp": "2026-06-29T22:10:00Z",
        "latency_ms": 35,
        "packet_loss": 0.1,
        "rssi": -55,
    }

    anomalies = detect_anomalies(metric)

    assert anomalies == []


def test_detects_high_latency():
    metric = {
        "device_id": "router-001",
        "timestamp": "2026-06-29T22:25:00Z",
        "latency_ms": 190,
        "packet_loss": 0.1,
        "rssi": -55,
    }

    anomalies = detect_anomalies(metric)

    assert "HIGH_LATENCY" in anomalies


def test_detects_multiple_anomalies():
    metric = {
        "device_id": "router-002",
        "timestamp": "2026-06-29T22:25:00Z",
        "latency_ms": 190,
        "packet_loss": 3.1,
        "rssi": -90,
    }

    anomalies = detect_anomalies(metric)

    assert anomalies == ["HIGH_LATENCY", "PACKET_LOSS", "LOW_RSSI"]