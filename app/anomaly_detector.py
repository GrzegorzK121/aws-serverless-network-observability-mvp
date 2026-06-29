def detect_anomalies(metric: dict) -> list[str]:
    anomalies = []

    if metric["latency_ms"] > 150:
        anomalies.append("HIGH_LATENCY")

    if metric["packet_loss"] > 2.0:
        anomalies.append("PACKET_LOSS")

    if metric["rssi"] < -85:
        anomalies.append("LOW_RSSI")

    return anomalies